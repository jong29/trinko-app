import yfinance as yf
import numpy as np

#####BASIC INFORMATION
# Create ticker object
ticker = yf.Ticker("XOP")

# Get the full name
name = ticker.info['longName']
print(name)

# Get current stock price
hist = ticker.history(period="1d")
current_price = hist['Close'].iloc[-1]
print(f"Current price: ${current_price:.2f}")

# Get 1-day change in nominal amount and percentage
previous_close = ticker.info['previousClose']
change_nominal = current_price - previous_close
change_percent = (change_nominal / previous_close) * 100
print(f"1-day change: ${change_nominal:.2f} ({change_percent:.2f}%)")

# Get asset class type
asset_class = ticker.info.get('quoteType', 'Unknown')
print(f"Asset class: {asset_class}")

# Get ETF focus/category
etf_focus = ticker.info.get('category', ticker.info.get('fundFamily', 'Unknown'))
print(f"ETF focus: {etf_focus}")

# Get AUM of ETF
aum = ticker.info.get('totalAssets', 'N/A')
print(f"AUM: ${aum:,}" if aum != 'N/A' else "AUM: N/A")

# Get Expense Ratio of ETF (try multiple field names)
expense_ratio = ticker.info.get('netExpenseRatio')
print(f"Expense Ratio: {expense_ratio:.2f}%" if expense_ratio else "Expense Ratio: N/A")

# Get Average Volume (90D)
avg_volume = ticker.info.get('averageVolume', 'N/A')
print(f"Average Volume (90D): {avg_volume:,}" if avg_volume != 'N/A' else "Average Volume (90D): N/A")

#####VALUATION VS. SELF (52WK)
# Get historical data for Bollinger Bands calculation (need more than 365 days)
hist_extended = ticker.history(period="2y")  # Get 2 years of data to ensure we have enough

# Bollinger Bands parameters
bb_length = 365
bb_stdev = 1
bb_offset = 0

# Calculate SMA (Simple Moving Average) - this is the basis
sma_basis = hist_extended['Close'].rolling(window=bb_length).mean()

# Calculate standard deviation
rolling_std = hist_extended['Close'].rolling(window=bb_length).std()

# Calculate Bollinger Bands
bb_upper = sma_basis + (bb_stdev * rolling_std)
bb_lower = sma_basis - (bb_stdev * rolling_std)

# Apply offset (shift the bands forward by offset periods)
bb_upper_offset = bb_upper.shift(bb_offset)
bb_lower_offset = bb_lower.shift(bb_offset)
bb_basis_offset = sma_basis.shift(bb_offset)

# Get the most recent values (latest trading day)
latest_upper = bb_upper_offset.iloc[-1]
latest_basis = bb_basis_offset.iloc[-1]
latest_lower = bb_lower_offset.iloc[-1]

print(f"\nBollinger Bands (Length: {bb_length}, StdDev: {bb_stdev}, Offset: {bb_offset}):")
print(f"Upper Band: ${latest_upper:.2f}")
print(f"Basis (SMA): ${latest_basis:.2f}")
print(f"Lower Band: ${latest_lower:.2f}")

# Calculate additional Bollinger Band levels for valuation ranges
bb_upper_1_5 = sma_basis + (1.5 * rolling_std)
bb_upper_2_0 = sma_basis + (2.0 * rolling_std)
bb_upper_2_5 = sma_basis + (2.5 * rolling_std)
bb_lower_2_0 = sma_basis - (2.0 * rolling_std)

# Apply offset to all levels
bb_upper_1_5_offset = bb_upper_1_5.shift(bb_offset)
bb_upper_2_0_offset = bb_upper_2_0.shift(bb_offset)
bb_upper_2_5_offset = bb_upper_2_5.shift(bb_offset)
bb_lower_2_0_offset = bb_lower_2_0.shift(bb_offset)

# Get the most recent values for all levels
latest_upper_1_5 = bb_upper_1_5_offset.iloc[-1]
latest_upper_2_0 = bb_upper_2_0_offset.iloc[-1]
latest_upper_2_5 = bb_upper_2_5_offset.iloc[-1]
latest_lower_2_0 = bb_lower_2_0_offset.iloc[-1]

# Print all trading range levels
print(f"\nTrading Range Levels (52wk):")
print(f"Significantly Overvalued (>+2.5σ): Above ${latest_upper_2_5:.2f}")
print(f"Overvalued (+2.0σ to +2.5σ): ${latest_upper_2_0:.2f} - ${latest_upper_2_5:.2f}")
print(f"Slightly Overvalued (+1.5σ to +2.0σ): ${latest_upper_1_5:.2f} - ${latest_upper_2_0:.2f}")
print(f"Fairly Valued (Basis to +1.5σ): ${latest_basis:.2f} - ${latest_upper_1_5:.2f}")
print(f"Slightly Undervalued (Basis to -1.0σ): ${latest_lower:.2f} - ${latest_basis:.2f}")
print(f"Undervalued (-1.0σ to -2.0σ): ${latest_lower_2_0:.2f} - ${latest_lower:.2f}")
print(f"Significantly Undervalued (<-2.0σ): Below ${latest_lower_2_0:.2f}")

# Determine current valuation based on price position
def determine_valuation(price, basis, upper_1_5, upper_2_0, upper_2_5, lower_1_0, lower_2_0):
    if price > upper_2_5:
        return "Significantly Overvalued"
    elif price > upper_2_0:
        return "Overvalued"
    elif price > upper_1_5:
        return "Slightly Overvalued"
    elif price > basis:
        return "Fairly Valued"
    elif price > lower_1_0:
        return "Slightly Undervalued"
    elif price > lower_2_0:
        return "Undervalued"
    else:
        return "Significantly Undervalued"

# Get current valuation
current_valuation = determine_valuation(
    current_price, 
    latest_basis, 
    latest_upper_1_5, 
    latest_upper_2_0, 
    latest_upper_2_5, 
    latest_lower, 
    latest_lower_2_0
)

print(f"\nCurrent Valuation Assessment (52wk):")
print(f"Current Price: ${current_price:.2f}")
print(f"Valuation: {current_valuation}")

# Calculate how many standard deviations away from basis
price_deviation = (current_price - latest_basis) / rolling_std.iloc[-1]
print(f"Standard Deviations from Basis: {price_deviation:.2f}σ")

#####BETA CORRELATION CHECK
# Get SPY data for correlation analysis
spy_ticker = yf.Ticker("SPY")
spy_hist = spy_ticker.history(period="2y")

# Calculate 1-year beta correlation with SPY
def calculate_beta_correlation(ticker_data, spy_data, period_days=252):
    # Get the last 252 trading days (approximately 1 year)
    ticker_returns = ticker_data['Close'].pct_change().dropna().tail(period_days)
    spy_returns = spy_data['Close'].pct_change().dropna().tail(period_days)
    
    # Align the data to ensure same dates
    aligned_returns = ticker_returns.align(spy_returns, join='inner')
    ticker_aligned = aligned_returns[0]
    spy_aligned = aligned_returns[1]
    
    # Calculate correlation (which equals beta when SPY variance = 1)
    correlation = ticker_aligned.corr(spy_aligned)
    
    # Calculate beta more precisely
    covariance = ticker_aligned.cov(spy_aligned)
    spy_variance = spy_aligned.var()
    beta = covariance / spy_variance if spy_variance != 0 else 0
    
    return correlation, beta

# Check if relative valuation should be performed
correlation, beta = calculate_beta_correlation(hist_extended, spy_hist)
perform_relative_valuation = not (0.975 <= abs(correlation) <= 1.025)

print(f"\nBeta/Correlation Analysis:")
print(f"1-Year Correlation with SPY: {correlation:.4f}")
print(f"1-Year Beta: {beta:.4f}")
print(f"Perform Relative Valuation: {'Yes' if perform_relative_valuation else 'No (too correlated with SPY)'}")

#####VALUATION VS. BENCHMARK (52wk) - CONDITIONAL
if perform_relative_valuation:
    # Align the dates between the ticker and SPY
    # Use inner join to only keep dates where both have data
    aligned_data = hist_extended.join(spy_hist, how='inner', rsuffix='_spy')

    # Calculate the relative performance ratio (ticker / SPY)
    relative_ratio = aligned_data['Close'] / aligned_data['Close_spy']

    # Bollinger Bands parameters for relative performance
    bb_length_rel = 365
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

    print(f"\nRelative Performance Bollinger Bands vs SPY (Length: {bb_length_rel}, StdDev: {bb_stdev_rel}, Offset: {bb_offset_rel}):")
    print(f"Upper Band: {latest_upper_rel:.4f}")
    print(f"Basis (SMA): {latest_basis_rel:.4f}")
    print(f"Lower Band: {latest_lower_rel:.4f}")
    print(f"Current Ratio: {current_ratio:.4f}")

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

    # Print all trading range levels (relative performance)
    print(f"\nRelative Valuation Range Levels vs SPY (52wk):")
    print(f"Significantly Overvalued (>+2.5σ): Above {latest_upper_2_5_rel:.4f}")
    print(f"Overvalued (+2.0σ to +2.5σ): {latest_upper_2_0_rel:.4f} - {latest_upper_2_5_rel:.4f}")
    print(f"Slightly Overvalued (+1.0σ to +2.0σ): {latest_upper_rel:.4f} - {latest_upper_2_0_rel:.4f}")
    print(f"Fairly Valued (-1.0σ to +1.0σ): {latest_lower_rel:.4f} - {latest_upper_rel:.4f}")
    print(f"Slightly Undervalued (-1.0σ to -2.0σ): {latest_lower_2_0_rel:.4f} - {latest_lower_rel:.4f}")
    print(f"Undervalued (-2.0σ to -2.5σ): {latest_lower_2_5_rel:.4f} - {latest_lower_2_0_rel:.4f}")
    print(f"Significantly Undervalued (<-2.5σ): Below {latest_lower_2_5_rel:.4f}")

    # Define valuation function for relative performance (different ranges)
    def determine_relative_valuation(ratio, basis, upper_1_0, upper_2_0, upper_2_5, lower_1_0, lower_2_0, lower_2_5):
        if ratio > upper_2_5:
            return "Significantly Overvalued"
        elif ratio > upper_2_0:
            return "Overvalued"
        elif ratio > upper_1_0:
            return "Slightly Overvalued"
        elif ratio > lower_1_0:
            return "Fairly Valued"
        elif ratio > lower_2_0:
            return "Slightly Undervalued"
        elif ratio > lower_2_5:
            return "Undervalued"
        else:
            return "Significantly Undervalued"

    # Get current relative valuation
    current_relative_valuation = determine_relative_valuation(
        current_ratio,
        latest_basis_rel,
        latest_upper_rel,
        latest_upper_2_0_rel,
        latest_upper_2_5_rel,
        latest_lower_rel,
        latest_lower_2_0_rel,
        latest_lower_2_5_rel
    )

    print(f"\nCurrent Relative Valuation Assessment vs SPY (52wk):")
    print(f"Current Ratio (Ticker/SPY): {current_ratio:.4f}")
    print(f"Relative Valuation: {current_relative_valuation}")

    # Calculate how many standard deviations away from basis (relative)
    ratio_deviation = (current_ratio - latest_basis_rel) / rolling_std_rel.iloc[-1]
    print(f"Standard Deviations from Basis: {ratio_deviation:.2f}σ")

    # Additional context: show percentage over/underperformance vs long-term average
    relative_performance_pct = ((current_ratio / latest_basis_rel) - 1) * 100
    print(f"Performance vs Long-term Average: {relative_performance_pct:+.2f}%")

else:
    # Set NA values for relative valuation
    print(f"\nRelative Performance vs SPY: N/A (ETF too correlated with benchmark)")
    print(f"Current Relative Valuation: N/A")
    print(f"Relative Z-Score: N/A")
    
    # Set ratio_deviation to None so we can handle it in overall valuation
    ratio_deviation = None

#####SMA TREND ANALYSIS
# Calculate Simple Moving Averages
sma_20 = hist_extended['Close'].rolling(window=20).mean()
sma_50 = hist_extended['Close'].rolling(window=50).mean()
sma_200 = hist_extended['Close'].rolling(window=200).mean()

# Get the most recent values
latest_sma_20 = sma_20.iloc[-1]
latest_sma_50 = sma_50.iloc[-1]
latest_sma_200 = sma_200.iloc[-1]

# Check 20D SMA vs 200D SMA
def check_20d_vs_200d_sma(sma_20, sma_200):
    if sma_20 > sma_200:
        return "Above"
    else:
        return "Below"

# Check 50D SMA vs 200D SMA
def check_50d_vs_200d_sma(sma_50, sma_200):
    if sma_50 > sma_200:
        return "Above"
    else:
        return "Below"

# Determine momentum based on SMA relationships
def determine_momentum(sma_20, sma_50, sma_200):
    sma_20_vs_200 = "ABOVE" if sma_20 > sma_200 else "BELOW"
    sma_50_vs_200 = "ABOVE" if sma_50 > sma_200 else "BELOW"
    
    if sma_20_vs_200 == "ABOVE" and sma_50_vs_200 == "ABOVE":
        return "Very Strong"
    elif sma_20_vs_200 == "ABOVE" and sma_50_vs_200 == "BELOW":
        return "Strong"
    elif sma_20_vs_200 == "BELOW" and sma_50_vs_200 == "ABOVE":
        return "Weak"
    else:  # Both BELOW
        return "Very Weak"

# Get momentum assessment
momentum = determine_momentum(latest_sma_20, latest_sma_50, latest_sma_200)

# Print the results
print(f"\nSMA Trend Analysis:")
print(f"20D SMA (${latest_sma_20:.2f}) vs 200D SMA (${latest_sma_200:.2f}): {check_20d_vs_200d_sma(latest_sma_20, latest_sma_200)}")
print(f"50D SMA (${latest_sma_50:.2f}) vs 200D SMA (${latest_sma_200:.2f}): {check_50d_vs_200d_sma(latest_sma_50, latest_sma_200)}")
print(f"Momentum: {momentum}")

#####OVERALL VALUATION ASSESSMENT - ENHANCED
# Calculate average z-score from both self valuation and benchmark valuation
def calculate_overall_valuation_enhanced(self_zscore, benchmark_zscore=None, self_valuation_text=None):
    if benchmark_zscore is None:
        # Use the exact self-valuation text when relative valuation is not available
        if self_valuation_text:
            # Convert self-valuation text to the standardized format
            valuation_mapping = {
                "Significantly Overvalued": "SIG OVERVALUE",
                "Overvalued": "OVERVALUE", 
                "Slightly Overvalued": "SLI OVERVALUE",
                "Fairly Valued": "FAIR VALUE",
                "Slightly Undervalued": "SLI UNDERVALUE",
                "Undervalued": "UNDERVALUE",
                "Significantly Undervalued": "SIG UNDERVALUE"
            }
            mapped_valuation = valuation_mapping.get(self_valuation_text, "FAIR VALUE")
            note = " (Self-valuation only - ETF too correlated with SPY)"
            return mapped_valuation, self_zscore, note
        else:
            # Fallback to z-score method if no self-valuation text provided
            average_zscore = self_zscore
            note = " (Self-valuation only - ETF too correlated with SPY)"
    else:
        # Use average z-score when both are available
        average_zscore = (self_zscore + benchmark_zscore) / 2
        note = ""
    
    # Determine overall valuation based on average z-score ranges
    if average_zscore > 2.5:
        return "SIG OVERVALUE", average_zscore, note
    elif average_zscore >= 2.0:
        return "OVERVALUE", average_zscore, note
    elif average_zscore >= 1.25:
        return "SLI OVERVALUE", average_zscore, note
    elif average_zscore >= -0.5:
        return "FAIR VALUE", average_zscore, note
    elif average_zscore >= -1.5:
        return "SLI UNDERVALUE", average_zscore, note
    elif average_zscore >= -2.25:
        return "UNDERVALUE", average_zscore, note
    else:
        return "SIG UNDERVALUE", average_zscore, note

# Get z-scores from previous calculations
self_valuation_zscore = price_deviation

# Calculate overall valuation with conditional logic
overall_valuation, avg_zscore, valuation_note = calculate_overall_valuation_enhanced(
    self_valuation_zscore, 
    ratio_deviation if perform_relative_valuation else None,
    current_valuation if not perform_relative_valuation else None
)

print(f"\nOverall Valuation Assessment:")
print(f"52wk Self Valuation Z-Score: {self_valuation_zscore:.2f}")
if perform_relative_valuation:
    print(f"52wk Benchmark Valuation Z-Score: {ratio_deviation:.2f}")
    print(f"Average Z-Score: {avg_zscore:.2f}")
else:
    print(f"52wk Benchmark Valuation Z-Score: N/A")
    print(f"Z-Score (Self-valuation only): {avg_zscore:.2f}")
print(f"Overall Valuation: {overall_valuation}{valuation_note}")

#####INVESTMENT RATING
def determine_investment_rating(momentum, overall_valuation):
    # Create the rating matrix based on momentum and valuation
    rating_matrix = {
        ("Very Weak", "SIG OVERVALUE"): "STRONG SELL",
        ("Very Weak", "OVERVALUE"): "SELL",
        ("Very Weak", "SLI OVERVALUE"): "SELL",
        ("Very Weak", "FAIR VALUE"): "SELL",
        ("Very Weak", "SLI UNDERVALUE"): "HOLD",
        ("Very Weak", "UNDERVALUE"): "HOLD",
        ("Very Weak", "SIG UNDERVALUE"): "BUY",
        
        ("Weak", "SIG OVERVALUE"): "STRONG SELL", 
        ("Weak", "OVERVALUE"): "SELL",
        ("Weak", "SLI OVERVALUE"): "HOLD",
        ("Weak", "FAIR VALUE"): "HOLD",
        ("Weak", "SLI UNDERVALUE"): "HOLD",
        ("Weak", "UNDERVALUE"): "HOLD",
        ("Weak", "SIG UNDERVALUE"): "BUY",
        
        ("Strong", "SIG OVERVALUE"): "SELL",
        ("Strong", "OVERVALUE"): "HOLD",
        ("Strong", "SLI OVERVALUE"): "HOLD",
        ("Strong", "FAIR VALUE"): "HOLD",
        ("Strong", "SLI UNDERVALUE"): "BUY",
        ("Strong", "UNDERVALUE"): "BUY",
        ("Strong", "SIG UNDERVALUE"): "STRONG BUY",
        
        ("Very Strong", "SIG OVERVALUE"): "SELL",
        ("Very Strong", "OVERVALUE"): "HOLD",
        ("Very Strong", "SLI OVERVALUE"): "HOLD",
        ("Very Strong", "FAIR VALUE"): "BUY",
        ("Very Strong", "SLI UNDERVALUE"): "BUY",
        ("Very Strong", "UNDERVALUE"): "STRONG BUY",
        ("Very Strong", "SIG UNDERVALUE"): "STRONG BUY"
    }
    
    return rating_matrix.get((momentum, overall_valuation), "UNKNOWN")

# Calculate investment rating
investment_rating = determine_investment_rating(momentum, overall_valuation)

print(f"\nInvestment Rating:")
print(f"Momentum: {momentum}")
print(f"Overall Valuation: {overall_valuation}")
print(f"INVESTMENT RATING: {investment_rating}")

#####COMPREHENSIVE SUMMARY TABLE
#####JONG THIS SECTION IS JUST FOR REFERENCE WILL NOT APPEAR LIKE THIS IN THE ACTUAL UI
def display_summary_table():
    print("\n" + "="*80)
    print(f"{'ETF ANALYSIS SUMMARY':^80}")
    print("="*80)
    
    # Basic Information Section
    print(f"{'BASIC INFORMATION':^80}")
    print("-"*80)
    print(f"{'ETF Name:':<25} {name}")
    print(f"{'Current Price:':<25} ${current_price:.2f}")
    print(f"{'1-Day Change:':<25} ${change_nominal:.2f} ({change_percent:+.2f}%)")
    print(f"{'Asset Class:':<25} {asset_class}")
    print(f"{'ETF Focus:':<25} {etf_focus}")
    if aum != 'N/A':
        print(f"{'AUM:':<25} ${aum:,}")
    else:
        print(f"{'AUM:':<25} N/A")
    if expense_ratio:
        print(f"{'Expense Ratio:':<25} {expense_ratio:.2f}%")
    else:
        print(f"{'Expense Ratio:':<25} N/A")
    if avg_volume != 'N/A':
        print(f"{'Avg Volume (90D):':<25} {avg_volume:,}")
    else:
        print(f"{'Avg Volume (90D):':<25} N/A")
    
    print()
    
    # Valuation Analysis Section
    print(f"{'VALUATION ANALYSIS':^80}")
    print("-"*80)
    print(f"{'52wk Self Valuation:':<25} {current_valuation}")
    print(f"{'Self Z-Score:':<25} {self_valuation_zscore:.2f}σ")
    
    if perform_relative_valuation:
        print(f"{'52wk Relative Valuation:':<25} {current_relative_valuation}")
        print(f"{'Relative Z-Score:':<25} {ratio_deviation:.2f}σ")
        print(f"{'Average Z-Score:':<25} {avg_zscore:.2f}")
    else:
        print(f"{'52wk Relative Valuation:':<25} N/A (Too correlated with SPY)")
        print(f"{'Relative Z-Score:':<25} N/A")
        print(f"{'Z-Score (Self only):':<25} {avg_zscore:.2f}")
    
    print(f"{'Overall Valuation:':<25} {overall_valuation}")
    
    print()
    
    # Technical Analysis Section
    print(f"{'TECHNICAL ANALYSIS':^80}")
    print("-"*80)
    print(f"{'Beta vs SPY (1Y):':<25} {beta:.4f}")
    print(f"{'Correlation vs SPY (1Y):':<25} {correlation:.4f}")
    print(f"{'20D SMA vs 200D SMA:':<25} {check_20d_vs_200d_sma(latest_sma_20, latest_sma_200)}")
    print(f"{'50D SMA vs 200D SMA:':<25} {check_50d_vs_200d_sma(latest_sma_50, latest_sma_200)}")
    print(f"{'Momentum:':<25} {momentum}")
    
    print()
    
    # Investment Decision Section
    print(f"{'INVESTMENT DECISION':^80}")
    print("-"*80)
    print(f"{'Momentum Assessment:':<25} {momentum}")
    print(f"{'Valuation Assessment:':<25} {overall_valuation}")
    print(f"{'FINAL RATING:':<25} {investment_rating}")
    
    print()
    
    # Key Price Levels Section
    print(f"{'KEY PRICE LEVELS (52WK)':^80}")
    print("-"*80)
    print(f"{'Current Price:':<25} ${current_price:.2f}")
    print(f"{'365D SMA (Basis):':<25} ${latest_basis:.2f}")
    print(f"{'20D SMA:':<25} ${latest_sma_20:.2f}")
    print(f"{'50D SMA:':<25} ${latest_sma_50:.2f}")
    print(f"{'200D SMA:':<25} ${latest_sma_200:.2f}")
    print(f"{'Upper BB (+1σ):':<25} ${latest_upper:.2f}")
    print(f"{'Lower BB (-1σ):':<25} ${latest_lower:.2f}")
    print(f"{'Strong Resistance (+2σ):':<25} ${latest_upper_2_0:.2f}")
    print(f"{'Strong Support (-2σ):':<25} ${latest_lower_2_0:.2f}")
    
    if perform_relative_valuation:
        print()
        print(f"{'RELATIVE PERFORMANCE vs SPY':^80}")
        print("-"*80)
        print(f"{'Current Ratio:':<25} {current_ratio:.4f}")
        print(f"{'Long-term Avg Ratio:':<25} {latest_basis_rel:.4f}")
        print(f"{'Relative Performance:':<25} {relative_performance_pct:+.2f}%")
    
    print("="*80)
    
    # Investment Rating Color/Symbol
    rating_symbols = {
        "STRONG BUY": "🚀 STRONG BUY 🚀",
        "BUY": "📈 BUY",
        "HOLD": "⚖️ HOLD",
        "SELL": "📉 SELL", 
        "STRONG SELL": "🔴 STRONG SELL 🔴"
    }
    
    symbol = rating_symbols.get(investment_rating, investment_rating)
    print(f"{symbol:^80}")
    print("="*80)

# Display the comprehensive summary
display_summary_table()