import yfinance as yf
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from etf_scanner.models import Assets, AssetPriceData, AssetPerformanceData, AssetZScore

class Command(BaseCommand):
    help = 'Populate a small sample of ETF data from Yahoo Finance'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            help='Number of days of historical data to fetch',
            default=30  # Default to 30 days for testing
        )
        parser.add_argument(
            '--batch',
            type=str,
            choices=['stocks', 'bonds', 'commodities', 'crypto', 'mixed'],
            help='Which batch of ETFs to populate',
            default='mixed'
        )

    def clean_ticker(self, ticker):
        """Remove exchange prefixes from ticker symbols"""
        # Remove exchange prefixes like AMEX:, NASDAQ:, etc.
        cleaned = re.sub(r'^[A-Z]+:', '', ticker.strip())
        # Remove any trailing dots that might be present
        cleaned = cleaned.rstrip('.')
        return cleaned
        
    def handle(self, *args, **options):
        # Sample ETF batches for different asset classes
        etf_batches = {
            'stocks': ['SPY', 'QQQ', 'IWM', 'VTI', 'VOO'],
            'bonds': ['AGG', 'BND', 'TLT', 'LQD', 'VCSH'],
            'commodities': ['GLD', 'SLV', 'IAU', 'PPLT', 'GLTR'],
            'crypto': ['GBTC', 'ETHE', 'BITB', 'BITU', 'ETH'],
            'mixed': ['SPY', 'BND', 'GLD', 'VNQ', 'TLT']
        }
        
        batch = options['batch']
        etfs = etf_batches[batch]
        
        days = options['days']
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        self.stdout.write(self.style.SUCCESS(f'Fetching data for {len(etfs)} ETFs in the {batch} batch from {start_date.date()} to {end_date.date()}'))
        
        for ticker in etfs:
            try:
                self.populate_etf(ticker, start_date, end_date)
                self.stdout.write(self.style.SUCCESS(f'Successfully populated data for {ticker}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error populating data for {ticker}: {str(e)}'))
    
    @transaction.atomic
    def populate_etf(self, ticker, start_date, end_date):
        """Populate all data for a single ETF"""
        # Clean the ticker symbol and fetch ETF info and historical data
        clean_ticker = self.clean_ticker(ticker)
        etf = yf.Ticker(clean_ticker)
        info = etf.info
        history = etf.history(start=start_date, end=end_date)
        
        # Create or update Assets record
        asset, created = Assets.objects.update_or_create(
            ticker=ticker,
            defaults={
                'name': info.get('shortName', info.get('longName', ticker)),
                'focus': info.get('category', ''),
                'index_tracked': info.get('index', ''),
                'aum': info.get('totalAssets', 0) / 1_000_000_000  # Convert to billions
            }
        )
        
        # Populate price data
        self._populate_price_data(asset, history)
        
        # Populate performance data
        self._populate_performance_data(asset, history)
        
        # Calculate and populate Z-scores
        self._populate_zscores(asset, history)
    
    def _populate_price_data(self, asset, history):
        """Populate historical price data for an asset"""
        # Delete existing price data for this asset
        AssetPriceData.objects.filter(asset=asset).delete()
        
        # Create new price data entries
        price_data_objects = []
        for date, row in history.iterrows():
            price_data_objects.append(
                AssetPriceData(
                    asset=asset,
                    date=date.date(),
                    price=row['Close']
                )
            )
        
        # Bulk create price data
        AssetPriceData.objects.bulk_create(price_data_objects)
    
    def _populate_performance_data(self, asset, history):
        """Calculate and populate performance metrics"""
        if len(history) == 0:
            # Create empty performance data with zeros if no history available
            perf_data = {
                'change_1d': 0,
                'perf_1w': 0, 'perf_1m': 0, 'perf_3m': 0, 'perf_6m': 0,
                'perf_ytd': 0, 'perf_1y': 0, 'perf_5y': 0, 'perf_10y': 0,
                'high_52w': 0
            }
            AssetPerformanceData.objects.update_or_create(
                asset=asset,
                defaults=perf_data
            )
            return
        
        # Get the latest price
        latest_price = history['Close'].iloc[-1]
        
        # Calculate performance metrics
        perf_data = {}
        
        # 1-day change
        if len(history) >= 2:
            perf_data['change_1d'] = (history['Close'].iloc[-1] / history['Close'].iloc[-2] - 1) * 100
        else:
            perf_data['change_1d'] = 0
        
        # Other time periods
        time_periods = {
            'perf_1w': 7,
            'perf_1m': 30,
            'perf_3m': 90,
            'perf_6m': 180,
            'perf_1y': 365,
            'perf_5y': 365 * 5,
            'perf_10y': 365 * 10
        }
        
        for field, days in time_periods.items():
            if len(history) >= days:
                perf_data[field] = (latest_price / history['Close'].iloc[-min(days, len(history))] - 1) * 100
            else:
                # If we don't have enough data, use the oldest available price
                perf_data[field] = (latest_price / history['Close'].iloc[0] - 1) * 100
        
        # YTD performance - handle differently to avoid timezone issues
        current_year = datetime.now().year
        # Filter by year using string comparison which is safer with timezones
        ytd_data = history[history.index.strftime('%Y').astype(int) >= current_year] if not history.empty else pd.DataFrame()
        if len(ytd_data) > 0:
            perf_data['perf_ytd'] = (latest_price / ytd_data['Close'].iloc[0] - 1) * 100
        else:
            perf_data['perf_ytd'] = 0
        
        # 52-week high
        year_data = history.iloc[-min(365, len(history)):]
        perf_data['high_52w'] = year_data['High'].max()
        
        # Create or update performance data
        AssetPerformanceData.objects.update_or_create(
            asset=asset,
            defaults=perf_data
        )
    
    def _populate_zscores(self, asset, history):
        """Calculate and populate Z-scores"""
        if len(history) < 20:
            # Create default Z-scores with zeros if not enough history
            zscore_data = {
                'zscore_20d': 0,
                'zscore_100d': 0,
                'zscore_365d': 0
            }
            AssetZScore.objects.update_or_create(
                asset=asset,
                defaults=zscore_data
            )
            return
        
        # Calculate Z-scores for different time periods
        periods = {
            'zscore_20d': 20,
            'zscore_100d': min(100, len(history)),
            'zscore_365d': min(365, len(history))
        }
        
        zscore_data = {}
        
        for field, days in periods.items():
            period_data = history['Close'].iloc[-days:]
            mean = period_data.mean()
            std = period_data.std()
            
            if std > 0:  # Avoid division by zero
                latest_price = history['Close'].iloc[-1]
                zscore_data[field] = (latest_price - mean) / std
            else:
                zscore_data[field] = 0
        
        # Create or update Z-score data
        AssetZScore.objects.update_or_create(
            asset=asset,
            defaults=zscore_data
        )
