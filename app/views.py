"""
Definition of views.
"""
import six
import requests
import logging
from rest_framework import viewsets, permissions, generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.models import User, Group
from stockmarketservice.serializers import SignupSerializer, UserSerializer, DailyPricesSerializer

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Stock Market Service API endpoint',
            'year':datetime.now().year
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Stock Market Service API endpoint by Andrés Distéfano.',
            'year':datetime.now().year,
        }
    )

class SignUpViewSet(viewsets.ModelViewSet):
    """ Viewset for user signup """
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'User created successfully',
        })

class DailyPricesView(ListAPIView):
    """ Viewset for Alpha Vantage's Daily timeseries API """
    serializer_class = DailyPricesSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """ Main GET method for AlphaVantage API """

        url = settings.AVAPI_URL
        params = {'function'  : settings.AVAPI_QUERY,
                  'symbol'    : request.query_params.get("symbol"),
                  'outputsize': request.query_params.get("outputsize"),
                  'apikey'    : settings.AVAPI_KEY}
        r = requests.get(url, params=params)

        try:
            timeSeries = r.json()['Time Series (Daily)']
            tsWithVariation = self.calculateVariation(timeSeries)

            return Response({'TimeSeries': tsWithVariation})
        except KeyError as e:
            return Response(r.json())

    def calculateVariation(self, timeseries):
        """ Calculate price variation between the last two close prices """

        prices  = {}
        prevKey = None

        for k, v in six.iteritems(timeseries):
            # Check if we have a previous key in order to add the price variation (or not)
            if prevKey:
                variation = float(v['4. close']) - float(prevClose)
                prices[prevKey]['closeVariation'] = str(round(variation,4))

            prevKey = k
            prevClose = v['4. close']
            prices[k] = {
                         'openPrice':   v['1. open'],
                         'higherPrice': v['2. high'],
                         'lowerPrice':  v['3. low']
                        }

        return prices