from django.urls import path, include
from ad.views.views import AdDetailView, GenericAdAPIView, AdvertisersView,AdRedirectView
from ad.views.logs import AdViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('logs', AdViewSet)

urlpatterns = [
    #path('', ApiOverview.as_view()),
    path('ads/', GenericAdAPIView.as_view()),
    path('ads/<int:id>', AdDetailView.as_view()),
    path('advertisers/', AdvertisersView.as_view()),
    path('advertisers/ads/<int:id>/', AdRedirectView.as_view()),
    path('', include(router.urls))
]