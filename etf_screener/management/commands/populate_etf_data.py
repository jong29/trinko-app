import yfinance as yf
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from etf_screener.models import Assets, AssetPriceData, AssetPerformanceData, AssetZScore

class Command(BaseCommand):
    help = 'Populate ETF data from Yahoo Finance'

    def add_arguments(self, parser):
        parser.add_argument(
            '--etfs',
            nargs='+',
            type=str,
            help='List of ETF tickers to populate (e.g., SPY QQQ IWM)',
            default=None
        )
        parser.add_argument(
            '--days',
            type=int,
            help='Number of days of historical data to fetch',
            default=365*2  # Default to 2 years
        )

    def clean_ticker(self, ticker):
        """Remove exchange prefixes from ticker symbols"""
        # Remove exchange prefixes like AMEX:, NASDAQ:, etc.
        cleaned = re.sub(r'^[A-Z]+:', '', ticker.strip())
        # Remove any trailing dots that might be present
        cleaned = cleaned.rstrip('.')
        return cleaned
        
    def handle(self, *args, **options):
        # Default ETFs if none provided
        default_etfs_str = "AMEX:XOP,CBOE:ITB,AMEX:ZROZ,NASDAQ:SOXX,AMEX:XHB,AMEX:EDV,CBOE:TLTW,AMEX:VDE,AMEX:XSD,AMEX:XLE,AMEX:FENY,AMEX:XBI,AMEX:IYE,AMEX:XMHQ,NASDAQ:IBB,AMEX:IYH,AMEX:XLV,AMEX:VHT,AMEX:FHLC,NASDAQ:TLT,AMEX:PFFD,AMEX:SLYV,AMEX:PZA,NASDAQ:PFF,AMEX:VIOV,NASDAQ:VGLT,AMEX:IJS,AMEX:VAW,AMEX:SPTL,AMEX:XLB,AMEX:BLV,AMEX:PFXF,AMEX:XME,AMEX:IJR,NASDAQ:VCLT,CBOE:HYD,AMEX:HYMB,AMEX:SPSM,AMEX:SPLB,CBOE:COWZ,AMEX:IGLB,AMEX:VIOO,AMEX:IWN,AMEX:TLH,AMEX:TFI,AMEX:SCMB,AMEX:MUB,AMEX:DES,AMEX:VTEB,AMEX:CMF,AMEX:SLYG,NASDAQ:IJT,AMEX:KLMN,CBOE:NUSC,AMEX:FNDA,AMEX:IVOG,AMEX:MDYG,CBOE:ITM,AMEX:IJK,CBOE:FLOT,AMEX:FLRN,AMEX:RWJ,AMEX:FLTR,AMEX:HYGV,AMEX:SMBS,AMEX:CLIP,AMEX:TFLO,AMEX:BIL,NASDAQ:SHV,AMEX:SPGP,NASDAQ:TBIL,AMEX:SGOV,AMEX:BILS,AMEX:GBIL,AMEX:SPBO,AMEX:XHLF,AMEX:USFR,AMEX:TBLL,NASDAQ:UNIY,AMEX:LQD,CBOE:HYDB,NASDAQ:VTWO,NASDAQ:FALN,NASDAQ:IBTF,NASDAQ:ANGL,OTC:INITF,AMEX:IWM,NASDAQ:VBIL,NASDAQ:VTC,NASDAQ:PRFZ,AMEX:QLTA,AMEX:BKAG,AMEX:SJNK,NASDAQ:SUSC,AMEX:VTES,AMEX:CORP,AMEX:SPHY,CBOE:IGEB,AMEX:BBAG,NASDAQ:USIG,AMEX:SCHZ,AMEX:SHYG,AMEX:SCHO,AMEX:EAGG,AMEX:SPSB,AMEX:SCHA,AMEX:SPAB,NASDAQ:VGSH,NASDAQ:IBTG,NASDAQ:IUSB,AMEX:SCYB,AMEX:SPTS,CBOE:GOVT,AMEX:IBDQ,NASDAQ:SHY,AMEX:AGG,AMEX:IBDX,AMEX:VBR,NASDAQ:BND,NASDAQ:MBB,NASDAQ:BSCP,NASDAQ:BSJQ,AMEX:MDY,AMEX:SHM,AMEX:IVOO,AMEX:SPMD,NASDAQ:VMBS,AMEX:IJH,AMEX:SPMB,AMEX:JNK,NASDAQ:IEF,AMEX:SUB,AMEX:IBDR,AMEX:SCHI,AMEX:RSSL,AMEX:SCHP,CBOE:ESML,NASDAQ:BSCQ,NASDAQ:IBTH,CBOE:USHY,AMEX:IBDS,AMEX:SCHD,AMEX:TIP,AMEX:SPIB,AMEX:TDTT,AMEX:SCHR,NASDAQ:SLQD,AMEX:VRP,NASDAQ:ISTB,AMEX:SPTI,NASDAQ:VGIT,AMEX:IBDT,NASDAQ:IGSB,NASDAQ:IBTI,AMEX:IBDU,NASDAQ:VCSH,AMEX:BSV,AMEX:BIV,NASDAQ:VCIT,CBOE:GVI,AMEX:IBDW,NASDAQ:BSCR,NASDAQ:IGIB,CBOE:SMMD,NASDAQ:BSCS,AMEX:DON,AMEX:HYLB,AMEX:IBDV,AMEX:TIPX,NASDAQ:BSCT,NASDAQ:IEI,NASDAQ:BSCU,AMEX:STIP,AMEX:HYG,AMEX:SCHM,AMEX:IWO,AMEX:VB,AMEX:IJJ,AMEX:MDYV,CBOE:FLQM,NASDAQ:VTIP,CBOE:NOBL,AMEX:VOOV,AMEX:IVE,CBOE:MOAT,CBOE:VLUE,AMEX:SPYV,NASDAQ:IUSV,AMEX:SMLF,AMEX:IWS,AMEX:SDY,CBOE:OMFL,AMEX:VBK,AMEX:BBMC,AMEX:SPYD,AMEX:FSMD,AMEX:VOE,AMEX:JHMM,AMEX:SDOG,AMEX:XSMO,AMEX:MLPA,NASDAQ:DVY,AMEX:SPHD,AMEX:RSPT,AMEX:RPV,CBOE:NULV,NASDAQ:DGRW,CBOE:PAVE,AMEX:ILCV,CBOE:QUAL,AMEX:RSP,AMEX:FNDX,AMEX:VTV,AMEX:HDV,CBOE:REGL,AMEX:IWD,NASDAQ:VONV,AMEX:VXF,AMEX:RWR,AMEX:PRF,NASDAQ:QQQE,AMEX:VNQ,AMEX:XMMO,AMEX:IYK,AMEX:XLP,AMEX:SCHV,AMEX:MGV,AMEX:QDF,AMEX:EFIV,AMEX:SNPE,CBOE:IFRA,CBOE:TILT,AMEX:FREL,AMEX:EUSA,AMEX:SCHH,AMEX:IWR,AMEX:VYM,AMEX:DGRO,NASDAQ:VFLO,AMEX:IMCB,AMEX:QUS,OTC:BZSPF.AMEX:IWX,AMEX:SPUS,AMEX:FDL,AMEX:IYR,NASDAQ:RDVY,AMEX:RWL,AMEX:XLK,AMEX:DSI,AMEX:USRT,AMEX:VDC,AMEX:CWB,AMEX:DIA,AMEX:FDLO,AMEX:FSTA,AMEX:IHI,AMEX:VIG,CBOE:ICVT,AMEX:XLRE,AMEX:VO,AMEX:DTD,CBOE:GSEW,AMEX:EPS,CBOE:ICF,AMEX:SPTM,AMEX:DHS,AMEX:VTI,AMEX:ITOT,AMEX:SCHB,AMEX:IWV,NASDAQ:VTHR,AMEX:DLN,NASDAQ:ESGU,CBOE:ESGV,AMEX:SUSA,AMEX:IYY,AMEX:GUSA,AMEX:QVML,AMEX:RECS,AMEX:GSLC,AMEX:FIDU,AMEX:SCHK,AMEX:SPLG,AMEX:IW,AMEX:SPY,AMEX:VOO,AMEX:IWB,AMEX:USCA,AMEX:VIS,NASDAQ:USCL,NASDAQ:VONE,AMEX:SCHX,AMEX:USPX,NASDAQ:USXF,CBOE:BBUS,CBOE:PBUS,AMEX:SPYX,CBOE:FLQL,AMEX:LRGF,AMEX:VGT,AMEX:WV,NASDAQ:PABU,AMEX:FTEC,CBOE:GSUS,AMEX:BKLC,AMEX:MGC,AMEX:VPU,AMEX:IWL,AMEX:SPLV,CBOE:1YJ,AMEX:IMCG,AMEX:FUTY,AMEX:EQWL,CBOE:USMV,AMEX:XLU,AMEX:IYW,NASDAQ:ONEQ,AMEX:XLG,AMEX:FQAL,AMEX:SPHQ,AMEX:JQUA,AMEX:KBE,AMEX:OEF,AMEX:LGLV,AMEX:IDU,CBOE:NULG,NASDAQ:QQQ,NASDAQ:QQQM,AMEX:KRE,AMEX:XLI,AMEX:IWY,AMEX:SCHG,OTC:INQQF,AMEX:FDIS,AMEX:IWF,AMEX:VCR,NASDAQ:VONG,AMEX:QGRW,AMEX:VOT,AMEX:IGM,AMEX:JMOM,AMEX:VUG,AMEX:MGK,NASDAQ:IUSG,AMEX:XNTK,AMEX:ILCG,AMEX:EWC,CBOE:BBCA,AMEX:SPYG,AMEX:IVW,AMEX:VOOG,AMEX:VOX,AMEX:FCOM,AMEX:RPG,CBOE:TMFC,AMEX:XLY,AMEX:IWP,NASDAQ:KBWB,AMEX:VFH,AMEX:IYC,OTC:HRZSF,AMEX:IYF,AMEX:FNCL,AMEX:XLC,AMEX:XLF,CBOE:MTUM,AMEX:MLPX,AMEX:IYG,AMEX:QGRO,AMEX:FDN,AMEX:SPMO,AMEX:IAI,CBOE:ITA,CBOE:IGV,NASDAQ:COWG,AMEX:XAR,AMEX:BAR,AMEX:PPLT,OTC:PHYMF,OTC:CGBLF,OTC:EFMSF,CBOE:AAAU,AMEX:GLD,AMEX:SLV,AMEX:SIVR,AMEX:GLDM,AMEX:OUNZ,AMEX:IAUM,AMEX:IAU,AMEX:SGOL,OTC:ZKBHF,AMEX:GLTR,OTC:IPHSF,CBOE:HODL,AMEX:BITB,AMEX:ETH,OTC:CXBTF,AMEX:BITU,AMEX:ETHE,NASDAQ:ETHA,NASDAQ:IBIT,AMEX:BTC,CBOE:BITX,CBOE:FETH,CBOE:ARKB,CBOE:FBTC,AMEX:GBTC"
        
        # Clean up the default ETFs string
        default_etfs = []
        if options['etfs']:
            # Use provided ETFs
            etfs = options['etfs']
        else:
            # Use default ETFs from the string
            # Split by comma and clean each ticker
            for ticker in default_etfs_str.split(','):
                clean_ticker = self.clean_ticker(ticker)
                if clean_ticker:  # Only add non-empty tickers
                    default_etfs.append(clean_ticker)
            etfs = default_etfs
        
        days = options['days']
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        self.stdout.write(self.style.SUCCESS(f'Fetching data for {len(etfs)} ETFs from {start_date.date()} to {end_date.date()}'))
        
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
            'zscore_100d': 100,
            'zscore_365d': 365
        }
        
        zscore_data = {}
        
        for field, days in periods.items():
            if len(history) >= days:
                period_data = history['Close'].iloc[-days:]
                mean = period_data.mean()
                std = period_data.std()
                
                if std > 0:  # Avoid division by zero
                    latest_price = history['Close'].iloc[-1]
                    zscore_data[field] = (latest_price - mean) / std
                else:
                    zscore_data[field] = 0
            else:
                zscore_data[field] = 0
        
        # Create or update Z-score data
        AssetZScore.objects.update_or_create(
            asset=asset,
            defaults=zscore_data
        )
