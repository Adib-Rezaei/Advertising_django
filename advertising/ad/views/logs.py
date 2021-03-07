from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from rest_framework.viewsets import ViewSet
from ad.models import AdModel
from ad.serializers import AdSerializer

from django.db.models import Count, FloatField, Avg
from django.db.models.functions import Cast


class AdViewSet(ViewSet):
    queryset = AdModel.objects.all()
    serializer_class = AdSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        serializer = AdSerializer(self.queryset.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def annotate_logs(self, request, query):
        query = query.annotate(click_delay_avg=Avg('clicks__delay'))
        query = query.annotate(total_views_count=Count('views', distinct=True),
                                total_clicks_count=Count('clicks', distinct=True))
        query = query.exclude(total_views_count=0) \
            .annotate(rate_total=Cast('total_clicks_count', FloatField()) / Cast('total_views_count', FloatField()))
        
        fields = ['id','title', 'advertiser__name', 'click_delay_avg', 'rate_total','total_views_count', 'total_clicks_count']
        return query.values(*fields)

    @action(detail=False, url_path='log', url_name='log')
    def logs(self, request):
        return Response(data=self.annotate_logs(request, self.queryset))