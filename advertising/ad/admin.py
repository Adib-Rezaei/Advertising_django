from django.contrib import admin
from .models import AdvertiserModel, AdModel, ClickModel, ViewModel
# Register your models here.

class ClickAdmin(admin.ModelAdmin):
    fields = ['ad', 'ip', 'created']
    list_display = ('id', 'display_ad', 'ip', 'created','delay')

class ViewAdmin(admin.ModelAdmin):
    fields = ['ad', 'ip', 'created']
    list_display = ('id', 'display_view', 'display_advertiser', 'ip', 'created',)
        

class AdAdmin(admin.ModelAdmin):
    fields = ['advertiser', 'title', 'image_url', 'link', 'approved']
    list_display = ['title', 'display_advertiser','image_url', 'link', 'approved']
    list_filter = ['approved']
    search_fields = ['title']

class AdvertiserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Advertiser information', {'fields': ['name']}),
        ('Advertiser Stats', {'fields': ['get_clicks', 'get_views']})
    ]
    list_display = ['name', 'get_clicks', 'get_views']
    readonly_fields = ('get_clicks','get_views')

class AdInline(admin.TabularInline):
    model = AdModel
    extra = 1

admin.site.register(AdvertiserModel, AdvertiserAdmin)
admin.site.register(AdModel, AdAdmin)
admin.site.register(ClickModel, ClickAdmin)
admin.site.register(ViewModel, ViewAdmin)