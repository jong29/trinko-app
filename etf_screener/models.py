from django.db import models

# Create your models here.
class Assets(models.Model):
    ticker = models.CharField(max_length=10, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    focus = models.CharField(max_length=255)
    index_tracked = models.CharField(max_length=255)
    aum = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        help_text="Assets Under Management in Billions USD"
    )

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    def __str__(self):
        return f"{self.ticker} - {self.name}"
    

class AssetPriceData(models.Model):
    asset = models.ForeignKey(Assets, on_delete=models.CASCADE, related_name="price_data")
    date = models.DateField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = "Asset Price Data"
        verbose_name_plural = "Asset Price Data"
        indexes = [models.Index(fields=['asset', 'date'])]

    def __str__(self):
        return f"{self.asset.ticker} - {self.date}"

class AssetPerformanceData(models.Model):
    asset = models.OneToOneField(Assets, on_delete=models.CASCADE, related_name="performance_data")
    last_updated = models.DateTimeField(auto_now=True)

    # Performance data
    change_1d = models.DecimalField(max_digits=10, decimal_places=2, help_text="1-day percentage change")
    perf_1w = models.DecimalField(max_digits=10, decimal_places=2, help_text="1-week percentage change")
    perf_1m = models.DecimalField(max_digits=10, decimal_places=2, help_text="1-month percentage change")
    perf_3m = models.DecimalField(max_digits=10, decimal_places=2, help_text="3-month percentage change")
    perf_6m = models.DecimalField(max_digits=10, decimal_places=2, help_text="6-month percentage change")
    perf_ytd = models.DecimalField(max_digits=10, decimal_places=2, help_text="Year-to-date percentage change")
    perf_1y = models.DecimalField(max_digits=10, decimal_places=2, help_text="1-year percentage change")
    perf_5y = models.DecimalField(max_digits=10, decimal_places=2, help_text="5-year percentage change")
    perf_10y = models.DecimalField(max_digits=10, decimal_places=2, help_text="10-year percentage change")

    # Price highs
    high_52w = models.DecimalField(max_digits=15, decimal_places=2, help_text="52-week high price")

    def __str__(self):
        return f"{self.asset.ticker} Performance Metrics"

    @property
    def recovery_upside(self):
        # TODO: check if correct with yonghee formula
        current_price = AssetPriceData.objects.filter(asset=self.asset).order_by('-date').first().price
        if current_price < self.high_52w:
            return round((self.high_52w / current_price - 1) * 100, 2)
        return None
        
class AssetZScore(models.Model):
    asset = models.OneToOneField(Assets, on_delete=models.CASCADE, related_name="zscore")
    last_updated = models.DateTimeField(auto_now=True)
    
    zscore_20d = models.DecimalField(max_digits=10, decimal_places=2)
    zscore_100d = models.DecimalField(max_digits=10, decimal_places=2)
    zscore_365d = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.asset.ticker} Z-Scores"

    @property
    def has_trinko_choice(self):
        # Check if the asset meets the Trinko choice criteria
        # Typically this would be when the z-score is below a certain threshold
        # indicating the asset is oversold
        return self.zscore_20d < -2.0 or self.zscore_100d < -2.0