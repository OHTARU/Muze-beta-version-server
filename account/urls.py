from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("", views.UserListView.as_view()),  # 유저 리스트 읽기
    path("kakaologin/", views.KakaoSignCallbackView.as_view()),  # 카카오 로그인 주소
    path(
        "userchange/",
        views.UserListView.as_view(),
    ),
    # 받아온 유저 정보 변경주소
    ##임시로 만든 url (토큰 생성)
    # path("token/", TokenObtainPairView.as_view()),
    # path("token/refresh/", TokenRefreshView.as_view()),
]
