from django.shortcuts import render
from ad.serializers import AdvertiserSerializer, AdSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.renderers import TemplateHTMLRenderer
from ad.models import ViewModel
from django.views.generic import RedirectView
from rest_framework.generics import get_object_or_404
from ad.models import *



class GenericAdAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = AdSerializer
    queryset = AdModel.objects.all()

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

class AdDetailView(APIView):
    def get_object(self, id):
        try:
            return AdModel.objects.get(id=id)
        except AdModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        ad = self.get_object(id)
        serilizer = AdSerializer(ad)
        return Response(serilizer.data)

    def put(self, request, id):
        id = request.data.get('id')
        ad = self.get_object(id)
        serializer = AdSerializer(ad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        ad = self.get_object(id)
        ad.delete()
        return Response({"status": "OK"}, status=status.HTTP_200_OK)


class AdvertisersView(APIView):
    queryset = AdvertiserModel.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'ads.html'

    def get(self, request, *args, **kwargs):
        for advertiser in self.queryset.all():
            for ad in advertiser.approved_ads():
                ViewModel.create_view(ad=ad, ip=kwargs['ip'])
        context = {
            'advertisers': self.queryset.all(),
        }
        return Response(context, template_name=self.template_name)


class AdRedirectView(RedirectView):
    is_permanent = False

    def get_redirect_url(self, *args, **kwargs):
        print(args, kwargs)
        ad = get_object_or_404(AdModel, id=kwargs.get('id'))
        ClickModel.create_click(ad=ad, ip=kwargs['ip'])
        return ad.link


