
from django.urls import path, re_path
from .views import article_list, article_detail, PttView, PttDetail
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Leo's Website API",
        default_version='v1',
        description="這是我的網站使用的API，練習使用django架設服務",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="leo000111444@gmail.com"),
        license=openapi.License(name="Leo License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
    path('article/', article_list),
    path('article/<int:pk>/', article_detail),
    path('ptt/', PttView.as_view()),
    path('ptt/<int:pk>/', PttDetail.as_view())
]
