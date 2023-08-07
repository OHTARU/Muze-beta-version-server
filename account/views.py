import json
from django.shortcuts import render
import requests

from django.http import JsonResponse
from django.contrib.auth import get_user_model, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from account.serializers import UserSerializer
from .models import UserModel
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()


class UserListView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @method_decorator(csrf_exempt, name="dispatch")
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    @method_decorator(csrf_exempt, name="dispatch")
    def post(self, request):
        profile = request.FILES.get("media/profile")
        data = request.data.copy()
        data["media/profile"] = profile
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                serializer.data, safe=False, status=status.HTTP_201_CREATED
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(csrf_exempt, name="dispatch")
    def put(self, request):
        try:
            user = User.objects.get(id=request.data["id"])
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if "image" in request.FILES:
            # 이미지를 처리하는 추가 로직
            image = request.FILES["media/profile"]
            data = request.data.copy()
            data["media/profile"] = image
            serializer = UserSerializer(user, data=data, partial=True)
        else:
            serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(csrf_exempt, name="dispatch")
    def delete(self, request):
        try:
            user = User.objects.get(id=request.data["id"])
        except User.DoesNotExist:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user.delete()
        return JsonResponse(
            {"message": "User successfully deleted"},
            safe=False,
            status=status.HTTP_204_NO_CONTENT,
        )


class KakaoSignCallbackView(APIView):
    # 카카오 회원 정보를 받아와서 새로운 User 인스턴스를 생성하는 함수
    @staticmethod
    def _create_kakao_user(kakao_response):
        return User.objects.create(
            id=kakao_response["id"],
            name=kakao_response["kakao_account"]["profile"]["nickname"],
            profile=kakao_response["kakao_account"]["profile"]["profile_image_url"],
        )

    # 카카오 액세스 토큰을 통해 사용자 정보를 반환하는 함수
    @staticmethod
    def _get_kakao_user_info(access_token):
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        }
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return json.loads(response.text)

    # 카카오 로그인의 콜백을 처리하는 post 메서드
    @method_decorator(csrf_exempt, name="dispatch")
    def post(self, request):
        # 요청에서 액세스 토큰을 가져옵니다.
        kakao_access_code = request.data.get("accessToken")

        # 액세스 토큰이 제공되지 않았을 경우 에러 메시지와 함께 400 상태 코드를 반환합니다.
        if not kakao_access_code:
            return JsonResponse(
                {"error": "Kakao access token is required."}, status=400
            )
        # 액세스 토큰을 사용하여 카카오 회원 정보를 얻습니다.
        kakao_response = self._get_kakao_user_info(kakao_access_code)

        try:
            # 기존 디비에 있는 사용자 정보를 찾습니다.
            user_info = UserModel.objects.get(id=kakao_response["id"])
            # 기존 사용자는 응답에 ID와 "exist": True를 포함합니다.
            login(request, user_info)  # 로그인 세션 생성
            return JsonResponse({"id": user_info.id, "exist": True})

        except UserModel.DoesNotExist:
            # 사용자 정보를 찾을 수 없는 경우 새 사용자를 생성합니다.
            kakao_user = self._create_kakao_user(kakao_response)
            kakao_user.save()  # 저장
            return JsonResponse({"id": kakao_user.id, "exist": False}, status=201)
            # 새 사용자는 응답에 ID와 "exist": False를 포함합니다.


"""토큰 생성해서 JWT"""
# import json
# import jwt
# import requests

# from django.http import JsonResponse
# from django.contrib.auth import get_user_model
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from rest_framework.views import APIView
# from account.serializers import UserSerializer
# from rest_framework import viewsets
# from config.settings import SECRET_KEY
# from .models import UserModel
# from rest_framework.permissions import IsAuthenticated

# User = get_user_model()


# class UserListView(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]


# class KakaoSignCallbackView(APIView):
#     # JWT 토큰을 생성하는 함수
#     # @staticmethod
#     # def _create_jwt(user_id):
#     #     return jwt.encode({"id": user_id}, SECRET_KEY, algorithm="HS256")

#     # 카카오 회원 정보를 받아와서 새로운 User 인스턴스를 생성하는 함수
#     @staticmethod
#     def _create_kakao_user(kakao_response):
#         return User.objects.create(
#             id=kakao_response["id"],
#             name=kakao_response["kakao_account"]["profile"]["nickname"],
#             profile=kakao_response["kakao_account"]["profile"]["profile_image_url"],
#         )

#     # 카카오 액세스 토큰을 통해 사용자 정보를 반환하는 함수
#     @staticmethod
#     def _get_kakao_user_info(access_token):
#         url = "https://kapi.kakao.com/v2/user/me"
#         headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
#         }
#         response = requests.post(url, headers=headers)
#         response.raise_for_status()
#         return json.loads(response.text)

#     # 카카오 로그인의 콜백을 처리하는 post 메소드
#     @method_decorator(csrf_exempt, name="dispatch")
#     def post(self, request):
#         # 요청에서 액세스 토큰을 가져옵니다.
#         kakao_access_code = request.data.get("accessToken")

#         # 액세스 토큰이 제공되지 않았을 경우 에러 메시지와 함께 400 상태 코드를 반환합니다.
#         if not kakao_access_code:
#             return JsonResponse(
#                 {"error": "Kakao access token is required."}, status=400
#             )
#         print(kakao_access_code)
#         # 액세스 토큰을 사용하여 카카오 회원 정보를 얻습니다.
#         kakao_response = self._get_kakao_user_info(kakao_access_code)

#         try:
#             # 기존 디비에 있는 사용자 정보를 찾습니다.
#             user_info = UserModel.objects.get(id=kakao_response["id"])
#             # 기존 사용자의 경우, JWT 토큰을 생성하고 응답에 포함합니다.
#             # token = self._create_jwt(user_info.id)
#             return JsonResponse({"id": user_info.id, "exist": True})
#             # return JsonResponse({"id": user_info.id, "token": token, "exist": True})

#         except UserModel.DoesNotExist:
#             # 사용자 정보를 찾을 수 없는 경우 새 사용자를 생성합니다.
#             kakao_user = self._create_kakao_user(kakao_response)
#             kakao_user.create()  # create() : 객체 생성과 저장을 동시에함
#             # 새 사용자의 경우, JWT 토큰을 생성하고 응답에 포함합니다.
#             # token = self._create_jwt(kakao_user.id)
#             # print(token)
#             return JsonResponse(
#                 {"id": kakao_user.id, "exist": False},
#                 status=201
#                 # {"id": kakao_user.id, "token": token, "exist": False}, status=201
#             )
