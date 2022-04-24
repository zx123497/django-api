# from turtle import st
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article, PTTArticle
from .serializers import ArticleSerializer, PTTArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .functions import getPTTJson
# Create your views here.
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


class PttView(GenericAPIView):
    queryset = PTTArticle.objects.all()
    serializer_class = PTTArticleSerializer

    @swagger_auto_schema(
        operation_summary='取得有趣pttの紀錄列表',
        operation_description='拿到所有儲存的有趣pttの紀錄',
    )
    def get(self, request, *args, **krgs):
        users = self.get_queryset()
        serializer = self.serializer_class(users, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    @swagger_auto_schema(
        operation_summary='儲存有趣ptt',
        operation_description='儲存傳入url　有趣pttの紀錄內容 \n可以把看到有趣的PTT文章上傳上去和大家分享 成為生活小樂趣',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'url': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='ptt url'
                )
            }
        )
    )
    def post(self, request, *args, **krgs):
        data = request.data
        res = getPTTJson(data["url"])
        try:
            serializer = self.serializer_class(data=res)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = serializer.data
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data)


class PttDetail(GenericAPIView):
    queryset = PTTArticle.objects.all()
    serializer_class = PTTArticleSerializer

    def get_object(self, pk):
        try:
            return PTTArticle.objects.get(pk=pk)
        except PTTArticle.DoesNotExist:
            raise JsonResponse(status=404)

    @swagger_auto_schema(
        operation_summary='取得單筆ptt紀錄',
        operation_description='拿到一筆ptt紀錄',
    )
    def get(self, request, pk, format=None):
        ptt = self.get_object(pk)
        serializer = self.serializer_class(ptt)
        data = serializer.data
        return JsonResponse(data, safe=False)

    @swagger_auto_schema(
        operation_summary='修改單筆ptt紀錄',
        operation_description='修改單筆ptt紀錄',
    )
    def put(self, request, pk, format=None):
        ptt = self.get_object(pk)
        data = JSONParser().parse(request)
        serializer = PTTArticleSerializer(ptt, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary='刪除單筆ptt紀錄',
        operation_description='刪除單筆ptt紀錄',
    )
    def delete(self, request, pk, format=None):
        ptt = self.get_object(pk)
        ptt.delete()
        return JsonResponse(status=204)


class CurrencyList(GenericAPIView):
    @swagger_auto_schema(
        operation_summary='加密貨幣列表Cryptocurrency list on CoinMarketCap',
        operation_description='得到加密貨幣列表(ID 前200)',
    )
    def get(self, request, *args, **krgs):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': '200',
            'convert': 'USD'
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


class CurrencyDetail(GenericAPIView):
    @swagger_auto_schema(
        operation_summary='一項加密貨幣市價 a type of crypto market quote',
        operation_description='一項加密貨幣市價 a type of crypto market quote \nsymbol 是指 BTC ETH SOL AVAX 等等',
    )
    def get(self, request, symbol, *args, **krgs):
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
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


class CurrencyStory(GenericAPIView):
    @swagger_auto_schema(
        operation_summary='一項加密貨幣的簡介 LOGO 相關社群媒體 官網 技術文件白皮書等',
        operation_description='Returns all static metadata available for one or more cryptocurrencies. This information includes details like logo, description, official website URL, social links, and links to a cryptocurrencys technical documentation.',
    )
    def get(self, request, symbol, *args, **krgs):
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


@csrf_exempt
def article_list(request):

    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return JsonResponse(status=404)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        article.delete()
        return JsonResponse(status=200)
