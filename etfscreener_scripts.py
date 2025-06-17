import yfinance as yf
import numpy as np

#####BASIC INFORMATION
# Create ticker object
ticker = yf.Ticker("IWM")

# Get the full name
name = ticker.info['longName']

# Get current stock price
hist = ticker.history(period="1d")
current_price = hist['Close'].iloc[-1]

# Get 1-day change in nominal amount and percentage
previous_close = ticker.info['previousClose']
change_nominal = current_price - previous_close
change_percent = (change_nominal / previous_close) * 100

# Get asset class type
asset_class = ticker.info.get('quoteType', 'Unknown')

# Get Market Cap
market_cap = ticker.info.get('marketCap', 'N/A')

# Get Average Volume (90D)
avg_volume = ticker.info.get('averageVolume', 'N/A')

#####BETA CORRELATION CHECK
# Get historical data for correlation analysis (5Y monthly)
hist_extended = ticker.history(period="5y", interval="1mo")
spy_hist = yf.Ticker("SPY").history(period="5y", interval="1mo")

# Calculate 5-year beta and correlation with SPY using monthly data
def calculate_5y_beta_correlation(ticker_data, spy_data):
    # Calculate monthly returns
    ticker_returns = ticker_data['Close'].pct_change().dropna()
    spy_returns = spy_data['Close'].pct_change().dropna()
    
    # Align the data to ensure same dates
    aligned_returns = ticker_returns.align(spy_returns, join='inner')
    ticker_aligned = aligned_returns[0]
    spy_aligned = aligned_returns[1]
    
    # Calculate correlation
    correlation = ticker_aligned.corr(spy_aligned)
    
    # Calculate beta (covariance / variance)
    covariance = ticker_aligned.cov(spy_aligned)
    spy_variance = spy_aligned.var()
    beta = covariance / spy_variance if spy_variance != 0 else 0
    
    return beta, correlation

# Calculate idiosyncratic risk ratio (Residual SD / Total SD)
def calculate_idiosyncratic_risk_ratio(ticker_data, spy_data):
    """
    Calculate the ratio of residual standard deviation to total standard deviation
    This quantifies idiosyncratic risk relative to total risk
    """
    # Calculate monthly returns
    ticker_returns = ticker_data['Close'].pct_change().dropna()
    spy_returns = spy_data['Close'].pct_change().dropna()
    
    # Align the data to ensure same dates
    aligned_returns = ticker_returns.align(spy_returns, join='inner')
    ticker_aligned = aligned_returns[0]
    spy_aligned = aligned_returns[1]
    
    if len(ticker_aligned) < 12:  # Need at least 12 months of data
        return 0
    
    # Calculate beta
    covariance = ticker_aligned.cov(spy_aligned)
    spy_variance = spy_aligned.var()
    beta = covariance / spy_variance if spy_variance != 0 else 0
    
    # Calculate predicted returns based on CAPM
    predicted_returns = beta * spy_aligned
    
    # Calculate residuals
    residuals = ticker_aligned - predicted_returns
    
    # Calculate residual standard deviation
    residual_sd = residuals.std()
    
    # Calculate total standard deviation
    total_sd = ticker_aligned.std()
    
    # Calculate ratio
    rsd_tsd_ratio = residual_sd / total_sd if total_sd != 0 else 0
    
    return rsd_tsd_ratio

# Calculate beta and correlation
beta, correlation = calculate_5y_beta_correlation(hist_extended, spy_hist)

# Check if relative valuation should be performed
perform_relative_valuation = not (0.975 <= abs(correlation) <= 1.025)

# Get daily data for relative valuation analysis
hist_extended = ticker.history(period="2y")
spy_hist = yf.Ticker("SPY").history(period="2y")

#####VALUATION VS. BENCHMARK (200D) - CONDITIONAL
if perform_relative_valuation:
    # Align the dates between the ticker and SPY
    # Use inner join to only keep dates where both have data
    aligned_data = hist_extended.join(spy_hist, how='inner', rsuffix='_spy')

    # Calculate the relative performance ratio (ticker / SPY)
    relative_ratio = aligned_data['Close'] / aligned_data['Close_spy']

    # Bollinger Bands parameters for relative performance
    bb_length_rel = 200
    bb_stdev_rel = 1
    bb_offset_rel = 0

    # Calculate SMA (Simple Moving Average) for relative ratio - this is the basis
    sma_basis_rel = relative_ratio.rolling(window=bb_length_rel).mean()

    # Calculate standard deviation for relative ratio
    rolling_std_rel = relative_ratio.rolling(window=bb_length_rel).std()

    # Calculate Bollinger Bands for relative performance
    bb_upper_rel = sma_basis_rel + (bb_stdev_rel * rolling_std_rel)
    bb_lower_rel = sma_basis_rel - (bb_stdev_rel * rolling_std_rel)

    # Apply offset (shift the bands forward by offset periods)
    bb_upper_offset_rel = bb_upper_rel.shift(bb_offset_rel)
    bb_lower_offset_rel = bb_lower_rel.shift(bb_offset_rel)
    bb_basis_offset_rel = sma_basis_rel.shift(bb_offset_rel)

    # Get the most recent values (latest trading day)
    latest_upper_rel = bb_upper_offset_rel.iloc[-1]
    latest_basis_rel = bb_basis_offset_rel.iloc[-1]
    latest_lower_rel = bb_lower_offset_rel.iloc[-1]
    current_ratio = relative_ratio.iloc[-1]

    # Calculate additional Bollinger Band levels for valuation ranges (relative performance)
    bb_upper_2_0_rel = sma_basis_rel + (2.0 * rolling_std_rel)
    bb_upper_2_5_rel = sma_basis_rel + (2.5 * rolling_std_rel)
    bb_lower_2_0_rel = sma_basis_rel - (2.0 * rolling_std_rel)
    bb_lower_2_5_rel = sma_basis_rel - (2.5 * rolling_std_rel)

    # Apply offset to all levels
    bb_upper_2_0_offset_rel = bb_upper_2_0_rel.shift(bb_offset_rel)
    bb_upper_2_5_offset_rel = bb_upper_2_5_rel.shift(bb_offset_rel)
    bb_lower_2_0_offset_rel = bb_lower_2_0_rel.shift(bb_offset_rel)
    bb_lower_2_5_offset_rel = bb_lower_2_5_rel.shift(bb_offset_rel)

    # Get the most recent values for all levels
    latest_upper_2_0_rel = bb_upper_2_0_offset_rel.iloc[-1]
    latest_upper_2_5_rel = bb_upper_2_5_offset_rel.iloc[-1]
    latest_lower_2_0_rel = bb_lower_2_0_offset_rel.iloc[-1]
    latest_lower_2_5_rel = bb_lower_2_5_offset_rel.iloc[-1]

    # Define valuation function for relative performance (same ranges as self-valuation)
    def determine_relative_valuation(ratio, basis, upper_1_0, upper_2_0, upper_2_5, lower_1_0, lower_2_0, lower_2_5):
        if ratio > upper_2_5:
            return "STRONG OUTPERFORM"
        elif ratio > upper_2_0:
            return "OUTPERFORM"
        elif ratio > upper_1_0:
            return "SLIGHT OUTPERFORM"
        elif ratio > lower_1_0:
            return "NEUTRAL"
        elif ratio > lower_2_0:
            return "SLIGHT UNDERPERFORM"
        elif ratio > lower_2_5:
            return "UNDERPERFORM"
        else:
            return "STRONG UNDERPERFORM"

    # Get current relative valuation
    current_relative_valuation = determine_relative_valuation(
        current_ratio,
        latest_basis_rel,
        latest_upper_rel,      # +1.0σ
        latest_upper_2_0_rel,  # +2.0σ
        latest_upper_2_5_rel,  # +2.5σ
        latest_lower_rel,      # -1.0σ
        latest_lower_2_0_rel,  # -2.0σ
        latest_lower_2_5_rel   # -2.5σ
    )

    # Calculate how many standard deviations away from basis (relative)
    ratio_deviation = (current_ratio - latest_basis_rel) / rolling_std_rel.iloc[-1]

    # Additional context: show percentage over/underperformance vs long-term average
    relative_performance_pct = ((current_ratio / latest_basis_rel) - 1) * 100

else:
    # Set NA values for relative valuation
    ratio_deviation = None

#####VALUATION VS. BENCHMARK (500D) - CONDITIONAL
if perform_relative_valuation:
    # Align the dates between the ticker and SPY (reuse aligned_data from above)
    # Calculate the relative performance ratio (ticker / SPY) - same as above
    relative_ratio_500D = aligned_data['Close'] / aligned_data['Close_spy']

    # Bollinger Bands parameters for relative performance (500D)
    bb_length_rel_500D = 500
    bb_stdev_rel_500D = 1
    bb_offset_rel_500D = 0

    # Calculate SMA (Simple Moving Average) for relative ratio - this is the basis
    sma_basis_rel_500D = relative_ratio_500D.rolling(window=bb_length_rel_500D).mean()

    # Calculate standard deviation for relative ratio
    rolling_std_rel_500D = relative_ratio_500D.rolling(window=bb_length_rel_500D).std()

    # Calculate Bollinger Bands for relative performance
    bb_upper_rel_500D = sma_basis_rel_500D + (bb_stdev_rel_500D * rolling_std_rel_500D)
    bb_lower_rel_500D = sma_basis_rel_500D - (bb_stdev_rel_500D * rolling_std_rel_500D)

    # Apply offset (shift the bands forward by offset periods)
    bb_upper_offset_rel_500D = bb_upper_rel_500D.shift(bb_offset_rel_500D)
    bb_lower_offset_rel_500D = bb_lower_rel_500D.shift(bb_offset_rel_500D)
    bb_basis_offset_rel_500D = sma_basis_rel_500D.shift(bb_offset_rel_500D)

    # Get the most recent values (latest trading day)
    latest_upper_rel_500D = bb_upper_offset_rel_500D.iloc[-1]
    latest_basis_rel_500D = bb_basis_offset_rel_500D.iloc[-1]
    latest_lower_rel_500D = bb_lower_offset_rel_500D.iloc[-1]
    current_ratio_500D = relative_ratio_500D.iloc[-1]

    # Calculate additional Bollinger Band levels for valuation ranges (relative performance 500D)
    bb_upper_2_0_rel_500D = sma_basis_rel_500D + (2.0 * rolling_std_rel_500D)
    bb_upper_2_5_rel_500D = sma_basis_rel_500D + (2.5 * rolling_std_rel_500D)
    bb_lower_2_0_rel_500D = sma_basis_rel_500D - (2.0 * rolling_std_rel_500D)
    bb_lower_2_5_rel_500D = sma_basis_rel_500D - (2.5 * rolling_std_rel_500D)

    # Apply offset to all levels
    bb_upper_2_0_offset_rel_500D = bb_upper_2_0_rel_500D.shift(bb_offset_rel_500D)
    bb_upper_2_5_offset_rel_500D = bb_upper_2_5_rel_500D.shift(bb_offset_rel_500D)
    bb_lower_2_0_offset_rel_500D = bb_lower_2_0_rel_500D.shift(bb_offset_rel_500D)
    bb_lower_2_5_offset_rel_500D = bb_lower_2_5_rel_500D.shift(bb_offset_rel_500D)

    # Get the most recent values for all levels
    latest_upper_2_0_rel_500D = bb_upper_2_0_offset_rel_500D.iloc[-1]
    latest_upper_2_5_rel_500D = bb_upper_2_5_offset_rel_500D.iloc[-1]
    latest_lower_2_0_rel_500D = bb_lower_2_0_offset_rel_500D.iloc[-1]
    latest_lower_2_5_rel_500D = bb_lower_2_5_offset_rel_500D.iloc[-1]

    # Define valuation function for relative performance (500D - same logic as 200D)
    def determine_relative_valuation_500D(ratio, basis, upper_1_0, upper_2_0, upper_2_5, lower_1_0, lower_2_0, lower_2_5):
        if ratio > upper_2_5:
            return "STRONG OUTPERFORM"
        elif ratio > upper_2_0:
            return "OUTPERFORM"
        elif ratio > upper_1_0:
            return "SLIGHT OUTPERFORM"
        elif ratio > lower_1_0:
            return "NEUTRAL"
        elif ratio > lower_2_0:
            return "SLIGHT UNDERPERFORM"
        elif ratio > lower_2_5:
            return "UNDERPERFORM"
        else:
            return "STRONG UNDERPERFORM"

    # Get current relative valuation (500D)
    current_relative_valuation_500D = determine_relative_valuation_500D(
        current_ratio_500D,
        latest_basis_rel_500D,
        latest_upper_rel_500D,      # +1.0σ
        latest_upper_2_0_rel_500D,  # +2.0σ
        latest_upper_2_5_rel_500D,  # +2.5σ
        latest_lower_rel_500D,      # -1.0σ
        latest_lower_2_0_rel_500D,  # -2.0σ
        latest_lower_2_5_rel_500D   # -2.5σ
    )

    # Calculate how many standard deviations away from basis (relative 500D)
    ratio_deviation_500D = (current_ratio_500D - latest_basis_rel_500D) / rolling_std_rel_500D.iloc[-1]

    # Additional context: show percentage over/underperformance vs long-term average (500D)
    relative_performance_pct_500D = ((current_ratio_500D / latest_basis_rel_500D) - 1) * 100

else:
    # Set NA values for relative valuation (500D)
    ratio_deviation_500D = None

#####COMPOSITE PERFORMANCE RATING
if perform_relative_valuation:
    # Calculate average z-score from 200D and 500D
    average_z_score = (ratio_deviation + ratio_deviation_500D) / 2
    
    # Determine composite performance rating based on average z-score
    def determine_composite_performance(avg_z_score):
        if avg_z_score > 2.5:
            return "STRONG OUTPERFORM"
        elif avg_z_score >= 2.0:
            return "OUTPERFORM"
        elif avg_z_score >= 1.0:
            return "SLIGHT OUTPERFORM"
        elif avg_z_score >= -1.0:
            return "NEUTRAL"
        elif avg_z_score >= -2.0:
            return "SLIGHT UNDERPERFORM"
        elif avg_z_score >= -2.5:
            return "UNDERPERFORM"
        else:
            return "STRONG UNDERPERFORM"
    
    composite_performance = determine_composite_performance(average_z_score)

#####MULTIPLE STOCK ANALYSIS FUNCTION
def analyze_multiple_stocks(ticker_list):
    """
    Analyze multiple stocks and present results in a table format
    
    Parameters:
    ticker_list (list): List of stock ticker symbols to analyze
    """
    import pandas as pd
    
    # Initialize results list
    results = []
    
    print(f"\nAnalyzing {len(ticker_list)} stocks...")
    print("="*120)
    
    for i, symbol in enumerate(ticker_list, 1):
        print(f"Processing {symbol} ({i}/{len(ticker_list)})...")
        
        try:
            # Create ticker object
            stock_ticker = yf.Ticker(symbol)
            
            # Get basic information
            stock_name = stock_ticker.info.get('longName', 'N/A')
            
            # Get current price and 1-day change
            stock_hist = stock_ticker.history(period="1d")
            if not stock_hist.empty:
                stock_current_price = stock_hist['Close'].iloc[-1]
                stock_previous_close = stock_ticker.info.get('previousClose', stock_current_price)
                stock_change_1d = stock_current_price - stock_previous_close
                stock_change_1d_pct = (stock_change_1d / stock_previous_close) * 100
            else:
                stock_current_price = stock_change_1d = stock_change_1d_pct = 0
            
            # Get Market Cap, Average Volume
            stock_market_cap = stock_ticker.info.get('marketCap', None)
            stock_avg_volume = stock_ticker.info.get('averageVolume', None)
            
            # Calculate 5Y Beta and Correlation
            stock_hist_5y = stock_ticker.history(period="5y", interval="1mo")
            spy_hist_5y = yf.Ticker("SPY").history(period="5y", interval="1mo")
            
            if len(stock_hist_5y) >= 12 and len(spy_hist_5y) >= 12:
                stock_beta, stock_correlation = calculate_5y_beta_correlation(stock_hist_5y, spy_hist_5y)
                stock_rsd_tsd_ratio = calculate_idiosyncratic_risk_ratio(stock_hist_5y, spy_hist_5y)
                stock_perform_rel_val = not (0.975 <= abs(stock_correlation) <= 1.025)
            else:
                stock_beta = stock_correlation = stock_rsd_tsd_ratio = 0
                stock_perform_rel_val = False
            
            # Initialize relative valuation variables
            stock_z_score_200d = stock_rating_200d = stock_z_score_500d = stock_rating_500d = "N/A"
            stock_z_score_avg = stock_rating_avg = "N/A"
            
            if stock_perform_rel_val:
                # Get daily data for relative valuation
                stock_hist_daily = stock_ticker.history(period="2y")
                spy_hist_daily = yf.Ticker("SPY").history(period="2y")
                
                if len(stock_hist_daily) >= 200 and len(spy_hist_daily) >= 200:
                    # Align daily data
                    stock_aligned_data = stock_hist_daily.join(spy_hist_daily, how='inner', rsuffix='_spy')
                    stock_relative_ratio = stock_aligned_data['Close'] / stock_aligned_data['Close_spy']
                    
                    # 200D Analysis
                    if len(stock_relative_ratio) >= 200:
                        stock_sma_200d = stock_relative_ratio.rolling(window=200).mean()
                        stock_std_200d = stock_relative_ratio.rolling(window=200).std()
                        stock_current_ratio_200d = stock_relative_ratio.iloc[-1]
                        stock_basis_200d = stock_sma_200d.iloc[-1]
                        stock_z_score_200d = (stock_current_ratio_200d - stock_basis_200d) / stock_std_200d.iloc[-1]
                        
                        # Determine 200D rating
                        if stock_z_score_200d > 2.5:
                            stock_rating_200d = "STRONG OUTPERFORM"
                        elif stock_z_score_200d >= 2.0:
                            stock_rating_200d = "OUTPERFORM"
                        elif stock_z_score_200d >= 1.0:
                            stock_rating_200d = "SLIGHT OUTPERFORM"
                        elif stock_z_score_200d >= -1.0:
                            stock_rating_200d = "NEUTRAL"
                        elif stock_z_score_200d >= -2.0:
                            stock_rating_200d = "SLIGHT UNDERPERFORM"
                        elif stock_z_score_200d >= -2.5:
                            stock_rating_200d = "UNDERPERFORM"
                        else:
                            stock_rating_200d = "STRONG UNDERPERFORM"
                    
                    # 500D Analysis
                    if len(stock_relative_ratio) >= 500:
                        stock_sma_500d = stock_relative_ratio.rolling(window=500).mean()
                        stock_std_500d = stock_relative_ratio.rolling(window=500).std()
                        stock_current_ratio_500d = stock_relative_ratio.iloc[-1]
                        stock_basis_500d = stock_sma_500d.iloc[-1]
                        stock_z_score_500d = (stock_current_ratio_500d - stock_basis_500d) / stock_std_500d.iloc[-1]
                        
                        # Determine 500D rating
                        if stock_z_score_500d > 2.5:
                            stock_rating_500d = "STRONG OUTPERFORM"
                        elif stock_z_score_500d >= 2.0:
                            stock_rating_500d = "OUTPERFORM"
                        elif stock_z_score_500d >= 1.0:
                            stock_rating_500d = "SLIGHT OUTPERFORM"
                        elif stock_z_score_500d >= -1.0:
                            stock_rating_500d = "NEUTRAL"
                        elif stock_z_score_500d >= -2.0:
                            stock_rating_500d = "SLIGHT UNDERPERFORM"
                        elif stock_z_score_500d >= -2.5:
                            stock_rating_500d = "UNDERPERFORM"
                        else:
                            stock_rating_500d = "STRONG UNDERPERFORM"
                        
                        # Calculate Average Z-Score and Rating
                        if stock_z_score_200d != "N/A" and stock_z_score_500d != "N/A":
                            stock_z_score_avg = (stock_z_score_200d + stock_z_score_500d) / 2
                            
                            # Determine average rating
                            if stock_z_score_avg > 2.5:
                                stock_rating_avg = "STRONG OUTPERFORM"
                            elif stock_z_score_avg >= 2.0:
                                stock_rating_avg = "OUTPERFORM"
                            elif stock_z_score_avg >= 1.0:
                                stock_rating_avg = "SLIGHT OUTPERFORM"
                            elif stock_z_score_avg >= -1.0:
                                stock_rating_avg = "NEUTRAL"
                            elif stock_z_score_avg >= -2.0:
                                stock_rating_avg = "SLIGHT UNDERPERFORM"
                            elif stock_z_score_avg >= -2.5:
                                stock_rating_avg = "UNDERPERFORM"
                            else:
                                stock_rating_avg = "STRONG UNDERPERFORM"
            
            # Append results - CORRECT STOCK COLUMNS
            results.append({
                'SYMBOL': symbol,
                'NAME': stock_name,
                'CURRENT_PRICE': f"${stock_current_price:.2f}" if stock_current_price > 0 else "N/A",
                'CHANGE_1D': f"{stock_change_1d_pct:+.2f}%" if stock_current_price > 0 else "N/A",
                'MARKET_CAP': f"${stock_market_cap/1e9:.1f}B" if stock_market_cap and stock_market_cap >= 1e9 else f"${stock_market_cap/1e6:.0f}M" if stock_market_cap and stock_market_cap >= 1e6 else "N/A",
                'BETA_5Y': f"{stock_beta:.3f}" if stock_beta != 0 else "N/A",
                'CORRELATION': f"{stock_correlation:.3f}" if stock_correlation != 0 else "N/A",
                'RSD/TSD': f"{stock_rsd_tsd_ratio:.3f}" if stock_rsd_tsd_ratio != 0 else "N/A",
                'Z_SCORE_200D': f"{stock_z_score_200d:.2f}" if stock_z_score_200d != "N/A" else "N/A",
                'RATING_200D': stock_rating_200d,
                'Z_SCORE_500D': f"{stock_z_score_500d:.2f}" if stock_z_score_500d != "N/A" else "N/A",
                'RATING_500D': stock_rating_500d,
                'Z_SCORE_AVG': f"{stock_z_score_avg:.2f}" if stock_z_score_avg != "N/A" else "N/A",
                'RATING_AVG': stock_rating_avg,
                'AVG_VOLUME_90D': f"{stock_avg_volume/1e6:.1f}M" if stock_avg_volume and stock_avg_volume >= 1e6 else f"{stock_avg_volume/1e3:.0f}K" if stock_avg_volume and stock_avg_volume >= 1e3 else str(stock_avg_volume) if stock_avg_volume else "N/A"
            })
            
        except Exception as e:
            results.append({
                'SYMBOL': symbol,
                'NAME': 'ERROR',
                'CURRENT_PRICE': 'N/A',
                'CHANGE_1D': 'N/A',
                'MARKET_CAP': 'N/A',
                'BETA_5Y': 'N/A',
                'CORRELATION': 'N/A',
                'RSD/TSD': 'N/A',
                'Z_SCORE_200D': 'N/A',
                'RATING_200D': 'N/A',
                'Z_SCORE_500D': 'N/A',
                'RATING_500D': 'N/A',
                'Z_SCORE_AVG': 'N/A',
                'RATING_AVG': 'N/A',
                'AVG_VOLUME_90D': 'N/A'
            })
    
    # Create DataFrame and display
    df = pd.DataFrame(results)
    
    # Save to CSV file
    csv_filename = 'sp500_analysis.csv'
    df.to_csv(csv_filename, index=False)
    
    print("\n" + "="*180)
    print(f"{'MULTIPLE STOCK ANALYSIS RESULTS':^180}")
    print("="*180)
    print(f"Results saved to: {csv_filename}")
    print(f"Total stocks analyzed: {len(df)}")
    print("="*180)
    
    return df

# Example usage (commented out - user can uncomment and modify)
stock_list = ["MSFT", "NVDA", "AAPL", "AMZN", "GOOGL", "GOOG", "META", "AVGO", "BRK.B", "TSLA", "LLY", "WMT", "JPM", "V", "ORCL", "MA", "NFLX", "XOM", "COST", "PG", "JNJ", "HD", "ABBV", "BAC", "PLTR", "KO", "UNH", "PM", "IBM", "TMUS", "CSCO", "GE", "CRM", "CVX", "WFC", "ABT", "LIN", "MCD", "INTU", "DIS", "MS", "AXP", "NOW", "MRK", "T", "ACN", "AMD", "GS", "RTX", "ISRG", "VZ", "PEP", "TXN", "UBER", "BKNG", "ADBE", "QCOM", "BX", "CAT", "SCHW", "AMGN", "PGR", "TMO", "SPGI", "BA", "BLK", "NEE", "DHR", "C", "BSX", "SYK", "HON", "PFE", "AMAT", "DE", "GILD", "TJX", "UNP", "GEV", "PANW", "CMCSA", "MU", "ETN", "COF", "ADP", "LOW", "ANET", "CRWD", "COP", "VRTX", "LRCX", "CB", "KLAC", "ADI", "APH", "MDT", "KKR", "LMT", "CHTR", "MMC", "SBUX", "BMY", "PLD", "ICE", "AMT", "MO", "WELL", "SO", "CME", "WM", "TT", "CEG", "FI", "NKE", "DASH", "MCK", "DUK", "INTC", "CTAS", "HCA", "SHW", "MDLZ", "EQIX", "ELV", "ABNB", "MCO", "VTR", "UPS", "PH", "CI", "CDNS", "CVS", "AJG", "TDG", "APO", "RSG", "MMM", "ORLY", "FTNT", "DELL", "AON", "ECL", "SNPS", "CL", "ZTS", "GD", "WMB", "PYPL", "RCL", "MAR", "ITW", "NOC", "EMR", "PNC", "HWM", "MSI", "USB", "CMG", "JCI", "WDAY", "EOG", "BK", "ADSK", "APD", "NEM", "CARR", "MNST", "AZO", "ROP", "KMI", "COIN", "CSX", "AXON", "TRV", "HLT", "DLR", "FCX", "VST", "COR", "NSC", "REGN", "AFL", "PAYX", "AEP", "NXPI", "FDX", "PWR", "ALL", "MET", "O", "TFC", "PSA", "GWW", "SPG", "OKE", "MPC", "BDX", "NDAQ", "SRE", "PSX", "CTVA", "AIG", "TEL", "FAST", "PCAR", "AMP", "SLB", "CPRT", "D", "GM", "LHX", "URI", "TGT", "KDP", "CMI", "EW", "KMB", "EXC", "OXY", "VRSK", "ROST", "HES", "FANG", "CCI", "GLW", "FICO", "KR", "MSCI", "FIS", "IDXX", "KVUE", "F", "VLO", "TTWO", "AME", "PEG", "CBRE", "GRMN", "YUM", "XEL", "CTSH", "DHI", "CAH", "BKR", "OTIS", "EA", "ED", "PRU", "RMD", "TRGP", "ROK", "MCHP", "SYY", "ETR", "HIG", "EBAY", "VMC", "WAB", "HSY", "BRO", "CSGP", "ACGL", "VICI", "MPWR", "ODFL", "WEC", "A", "GEHC", "EFX", "MLM", "IR", "EQT", "LYV", "DXCM", "TKO", "EXR", "DAL", "IT", "PCG", "KHC", "XYL", "LULU", "CCL", "IRM", "ANSS", "STZ", "RJF", "GIS", "WTW", "AVB", "LVS", "MTB", "NRG", "LEN", "DD", "HUM", "DTE", "BR", "WRB", "KEYS", "STT", "K", "ROL", "AWK", "CNC", "IQV", "TSCO", "EXE", "NUE", "AEE", "STX", "EQR", "VRSN", "FITB", "SMCI", "DRI", "PPG", "PPL", "TYL", "GDDY", "UAL", "TPL", "EL", "WBD", "IP", "MTD", "CPAY", "DG", "ATO", "DOV", "SBAC", "VLTO", "CHD", "ES", "FTV", "ADM", "STE", "HPE", "CNP", "CBOE", "FE", "SYF", "HBAN", "HPQ", "TDY", "FOX", "FOXA", "CINF", "CDW", "SW", "ON", "DVN", "LH", "EXPE", "NVR", "PODD", "DOW", "AMCR", "NTRS", "CMS", "PHM", "HUBB", "TROW", "WAT", "ULTA", "INVH", "NTAP", "PTC", "MKC", "DLTR", "IFF", "DGX", "CTRA", "RF", "WY", "STLD", "LII", "WDC", "TSN", "BIIB", "EIX", "LYB", "JBL", "GPN", "LDOS", "WSM", "HAL", "NI", "GEN", "L", "ESS", "LUV", "ZBH", "FSLR", "CFG", "MAA", "KEY", "PKG", "PFG", "TRMB", "HRL", "TPR", "GPC", "CPT", "FFIV", "ERIE", "SNA", "NWS", "NWSA", "PNR", "WST", "RL", "FDS", "DECK", "BAX", "MOH", "LNT", "EXPD", "CLX", "EVRG", "DPZ", "BBY", "J", "BALL", "CF", "APTV", "ZBRA", "HOLX", "PAYC", "EG", "KIM", "COO", "TXT", "AVY", "JBHT", "UDR", "OMC", "IEX", "TER", "MAS", "INCY", "ALGN", "JKHY", "REG", "BF.B", "SOLV", "BLDR", "ARE", "DOC", "NDSN", "JNPR", "ALLE", "BEN", "BXP", "AKAM", "RVTY", "CHRW", "UHS", "POOL", "MOS", "HST", "PNW", "SWKS", "VTRS", "CAG", "MRNA", "TAP", "SWK", "DVA", "SJM", "BG", "AIZ", "LKQ", "KMX", "GL", "EPAM", "CPB", "WBA", "HAS", "DAY", "AOS", "EMN", "WYNN", "MGM", "HII", "IPG", "HSIC", "MKTX", "PARA", "FRT", "NCLH", "AES", "TECH", "LW", "GNRC", "MTCH", "CRL", "ALB", "APA", "IVZ", "MHK", "ENPH", "CZR"]
results_df = analyze_multiple_stocks(stock_list)