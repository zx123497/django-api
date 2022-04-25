from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
# Create your views here.
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


class LineBot(GenericAPIView):
    @swagger_auto_schema(
        operation_summary='LINEBOT ECHO',
        operation_description='line bot testing echo',
    )
    def post(self, request, *args, **krgs):
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )
        return HttpResponse()
