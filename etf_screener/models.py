from django.db import models
from django.contrib.postgres.fields import ArrayField
import json

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


class ColumnCategory(models.Model):
    """Model to categorize columns for the ETF screener"""
    name = models.CharField(max_length=100, unique=True)
    columns = ArrayField(
        models.CharField(max_length=100),
        help_text="List of column names that belong to this category"
    )
    display_order = models.PositiveSmallIntegerField(default=0, help_text="Order in which to display categories")
    
    class Meta:
        verbose_name = "Column Category"
        verbose_name_plural = "Column Categories"
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class Filter(models.Model):
    """Model to store filter configurations"""
    OPERATOR_CHOICES = [
        ('gt', 'Greater than'),
        ('gte', 'Greater than or equal to'),
        ('lt', 'Less than'),
        ('lte', 'Less than or equal to'),
        ('eq', 'Equal to'),
        ('neq', 'Not equal to'),
        ('contains', 'Contains'),
        ('between', 'Between'),
    ]
    
    name = models.CharField(max_length=100)
    field = models.CharField(max_length=100, help_text="Field/column to apply filter on")
    operator = models.CharField(max_length=10, choices=OPERATOR_CHOICES)
    value = models.CharField(max_length=255, help_text="Filter value or JSON for multiple values")
    user_created = models.BooleanField(default=True, help_text="Whether this filter was created by a user")
    
    class Meta:
        verbose_name = "Filter"
        verbose_name_plural = "Filters"
    
    def __str__(self):
        return f"{self.name}: {self.field} {self.operator}"
    
    @property
    def parsed_value(self):
        """Parse the value field if it contains JSON"""
        try:
            return json.loads(self.value)
        except json.JSONDecodeError:
            return self.value


class Preset(models.Model):
    """Model to store combinations of filters as presets"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    filters = models.ManyToManyField(Filter, related_name="presets")
    is_default = models.BooleanField(default=False, help_text="Whether this is a default preset")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Preset"
        verbose_name_plural = "Presets"
        ordering = ['-is_default', 'name']
    
    def __str__(self):
        return self.name