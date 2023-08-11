import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .models import Resume
from .serializers import ResumeSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response


# 들어오는 요청을 처리하는 메서드를 담고 있는 클래스입니다.
class ResumeList(APIView):
    parser_classes = (MultiPartParser, FormParser)

    # GET 요청에 대한 응답을 처리하는 메서드입니다.
    def get(self, request):
        # 데이터베이스에서 모든 Resume 객체를 가져옵니다.
        queryset = Resume.objects.all()
        # 가져온 객체들을 ResumeSerializer를 사용하여 JSON 형태로 변환하여 반환합니다.
        serializer = ResumeSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    # POST 요청에 대한 응답을 처리하는 메서드입니다.
    def post(self, request):
        profile = request.FILES.get("profile")

        data = request.data.copy()
        data["profile"] = profile
        serializer = ResumeSerializer(data=data)
        # 유효성 검증이 완료된 데이터를 저장합니다.
        if serializer.is_valid():
            serializer.save()
            # 저장된 데이터를 JSON 형태로 변환하여 반환합니다.
            return JsonResponse(
                serializer.data, status=status.HTTP_201_CREATED, safe=False
            )
        # 유효성 검증이 실패한 경우 에러 메시지를 JSON 형태로 변환하여 반환합니다.
        return JsonResponse(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
        )


# 들어오는 요청을 처리하는 메서드를 담고 있는 클래스입니다.
class ResumeDetail(APIView):
    # Primary Key로 객체를 가져올 때 사용하는 메서드입니다.
    def get_object(self, pk):
        try:
            # 주어진 Primary Key를 사용하여 데이터베이스에서 객체를 가져옵니다.
            return Resume.objects.get(pk=pk)
        except Resume.DoesNotExist:
            return None

    # GET 요청에 대한 응답을 처리하는 메서드입니다.
    def get(self, request, pk):
        # Primary Key를 사용하여 객체를 가져옵니다.
        Resume_user = self.get_object(pk)
        # 객체를 찾지 못한 경우 에러 메시지를 반환합니다.
        if not Resume_user:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, safe=False)
        # 가져온 객체를 ResumeSerializer를 사용하여 JSON 형태로 변환하여 반환합니다.
        serializer = ResumeSerializer(Resume_user)
        return JsonResponse(serializer.data, safe=False)

    # POST 요청에 대한 응답을 처리하는 메서드입니다.
    def post(self, request):
        post_image = request.FILES.get("profile")

        data = request.data.copy()
        data["profile"] = post_image
        # 들어온 데이터를 ResumeSerializer를 사용하여 검증합니다.
        serializer = ResumeSerializer(data=data)
        # 유효성 검증이 완료된 데이터를 저장합니다.
        if serializer.is_valid():
            serializer.save()
            # 저장된 데이터를 JSON 형태로 변환하여 반환합니다.
            return JsonResponse(
                serializer.data, status=status.HTTP_201_CREATED, safe=False
            )
        # 유효성 검증이 실패한 경우 에러 메시지를 JSON 형태로 변환하여 반환합니다.
        return JsonResponse(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
        )

    # PUT 요청에 대한 응답을 처리하는 메서드입니다.
    def put(self, request, pk):
        post_user = self.get_object(pk)
        if not post_user:
            # 해당 게시물이 존재하지 않을 경우 404 에러 반환
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        if 'profile' in request.FILES:
            data['profile'] = request.FILES['profile']

        # 이전에 조회한 PerformancePost객체와 수정하고자 하는 데이터(request.data)를 이용해 PostSerializer 생성
        serializer = PostSerializer(post_user, data=data, partial=True)
        if serializer.is_valid():
            # serializer가 유효하다면 PerformancePost 객체를 업데이트하고 성공 상태 코드 반환
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        # serializer가 유효하지 않다면 오류 메시지와 함께 실패 상태 코드 반환
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # DELETE 요청에 대한 응답을 처리하는 메서드입니다.
    def delete(self, request, pk):
        # Primary Key를 사용하여 객체를 가져옵니다.
        Resume_obj = self.get_object(pk)
        # 객체를 찾지 못한 경우 에러 메시지를 반환합니다.
        if not Resume_obj:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND, safe=False)
        # 객체를 삭제하고 반환합니다.
        Resume_obj.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT, safe=False)
