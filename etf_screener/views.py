from django.shortcuts import render
from django.http import JsonResponse
from .models import Assets, AssetPriceData, AssetPerformanceData, AssetZScore
from django.db.models import Prefetch
import json

# Create your views here.
def etf_screener(request):
    """
    View for the ETF screener page.
    Fetches ETF data from the models and passes it to the template.
    """
    # Fetch all assets with their related performance data and z-scores
    assets = Assets.objects.all().prefetch_related(
        Prefetch('performance_data'),
        Prefetch('zscore')
    )
    
    # Prepare ETF data for the template
    etf_data = []
    for asset in assets:
        # Get the latest price data
        latest_price = AssetPriceData.objects.filter(asset=asset).order_by('-date').first()
        price = latest_price.price if latest_price else 0
        
        # Get performance data
        perf = asset.performance_data if hasattr(asset, 'performance_data') else None
        zscore = asset.zscore if hasattr(asset, 'zscore') else None
        
        # Calculate Trinko Choice rating
        trinko_choice = False
        if perf and zscore:
            recovery_upside = perf.recovery_upside if perf.recovery_upside else 0
            # An ETF is a Trinko Choice if it has recovery upside > 5% and zscore_20d < -1
            if recovery_upside > 5 and zscore.zscore_20d < -1:
                trinko_choice = True
        
        # Create ETF data object
        etf = {
            'ticker': asset.ticker,
            'name': asset.name,
            'focus': asset.focus,
            'index_tracked': asset.index_tracked,
            'aum': float(asset.aum),
            'price': float(price),
            'trinko_choice': trinko_choice,
        }
        
        # Add performance data if available
        if perf:
            etf.update({
                'change_1d': float(perf.change_1d),
                'perf_1w': float(perf.perf_1w),
                'perf_1m': float(perf.perf_1m),
                'perf_3m': float(perf.perf_3m),
                'perf_6m': float(perf.perf_6m),
                'perf_ytd': float(perf.perf_ytd),
                'perf_1y': float(perf.perf_1y),
                'perf_5y': float(perf.perf_5y),
                'perf_10y': float(perf.perf_10y),
                'high_52w': float(perf.high_52w),
                'recovery_upside': float(perf.recovery_upside) if perf.recovery_upside else 0,
            })
        
        # Add z-score data if available
        if zscore:
            etf.update({
                'zscore_20d': float(zscore.zscore_20d),
                'zscore_100d': float(zscore.zscore_100d),
                'zscore_365d': float(zscore.zscore_365d),
            })
        
        etf_data.append(etf)
    
    # Pass data to the template
    context = {
        'title': 'ETF Screening Tool',
        'etf_data_json': json.dumps(etf_data),
    }
    
    return render(request, 'etf_screener/etf_screener.html', context)
