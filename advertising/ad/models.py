from django.db import models
from django.utils import timezone


# Create your models here.
class BaseModel(models.Model): 
    created = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField()

    class Meta:
        abstract = True


class AdvertiserModel(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)

    def get_clicks(self):
        count = 0
        for ad in self.ads.all():
            count += ad.clicks.count()
        return count

    get_clicks.short_description = "Total clicks"

    def get_views(self):
        count = 0
        for ad in self.ads.all():
            count += ad.views.count()
        return count

    get_views.short_description = "Total views"

    def approved_ads(self):
        ads = self.ads.filter(approved=True)
        return ads

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Advertiser"

class AdModel(models.Model):

    advertiser = models.ForeignKey(to=AdvertiserModel, on_delete=models.CASCADE, related_name="ads")
    title = models.CharField(max_length=255, null=False, blank=False)
    image_url = models.CharField(max_length=255, null=False, blank=False, default='https://martialartsplusinc.com/wp-content/uploads/2017/04/default-image.jpg')
    link = models.CharField(max_length=255, null=True, blank=True)
    approved = models.BooleanField(default=False)

    def display_advertiser(self):
        return self.advertiser.name

    display_advertiser.short_description = "Advertiser"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ad"


class ClickModel(BaseModel):
    delay = models.DurationField(null=True)
    ad = models.ForeignKey(to=AdModel, on_delete=models.CASCADE, related_name="clicks")

    def display_ad(self):
        return self.ad.title 

    display_ad.short_description = "Ad Title"

    @staticmethod
    def create_click(ad, ip):
        ClickModel.objects.create(ad=ad, ip=ip, 
                                delay=timezone.now() - ad.views.filter(ip=ip).order_by('-created').first().created)

    def __str__(self):
        return self.ad.title
    
    class Meta:
        verbose_name = "Click"

class ViewModel(BaseModel):
    ad = models.ForeignKey(to=AdModel, on_delete=models.CASCADE, related_name="views")

    def display_view(self):
        return self.ad.title 
    def display_advertiser(self):
        return self.ad.advertiser
    display_view.short_description = "Title"
    display_advertiser.short_description = "Advertiser"

    @staticmethod
    def create_view(ad, ip):
        ViewModel.objects.create(ad=ad, ip=ip)

    def __str__(self):
        return self.ad.title

    class Meta:
        verbose_name = "View"
    
    
