# from turtle import st
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article, PTTArticle
from .serializers import ArticleSerializer, PTTArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from .functions import getPTTJson
# Create your views here.

@csrf_exempt
def article_list(request):

    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many = True )
        return JsonResponse( serializer.data, safe = False )

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse( serializer.data, status = 201)
        return JsonResponse( serializer.errors, status = 400)

@csrf_exempt
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return JsonResponse(status = 404)

    if request.method == 'GET':
        serializer = ArticleSerializer (article)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer (article, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse( serializer.data, status = 201)
        return JsonResponse( serializer.errors, status = 400)

    elif request.method == 'DELETE':
        article.delete()
        return JsonResponse(status = 204)


@csrf_exempt
def ptt_article_list(request):
    if request.method == 'GET':
        articles = PTTArticle.objects.all()
        serializer = PTTArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        res = getPTTJson(data["url"])
        serializer = PTTArticleSerializer(data = res)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def ptt_article_detail(request, pk):
    try:
        article = PTTArticle.objects.get(pk=pk)

    except PTTArticle.DoesNotExist:
        return JsonResponse(status=404)

    if request.method == 'GET':
        serializer = PTTArticleSerializer(article)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PTTArticleSerializer(article, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        article.delete()
        return JsonResponse(status=204)
