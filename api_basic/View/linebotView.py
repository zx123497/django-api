from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
# Create your views here.
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


class LineBot(GenericAPIView):
    @swagger_auto_schema(
        operation_summary='LINEBOT 測試',
        operation_description='line bot testing',
    )
    def post(self, request, symbol, *args, **krgs):
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
        parameters = {
            'symbol': symbol,
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': settings.CURRENCY_API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            return JsonResponse(data, status=200)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return JsonResponse(e, status=400)
