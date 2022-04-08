# from turtle import st
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
        operation_summary='取得ptt紀錄',
        operation_description='拿到所有儲存的ptt紀錄',
    )
    def get(self, request, *args, **krgs):
        users = self.get_queryset()
        serializer = self.serializer_class(users, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    @swagger_auto_schema(
        operation_summary='儲存ptt內容',
        operation_description='儲存傳入url的ptt內容',
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
        operation_summary='加密貨幣列表',
        operation_description='得到加密貨幣列表',
    )
    def get(self, request, *args, **krgs):
        url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': '5000',
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c',
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            JsonResponse(data, status=200)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            JsonResponse(e, status=400)


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
