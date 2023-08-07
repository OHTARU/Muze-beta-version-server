from rest_framework.views import APIView
from .models import PerformancePost  # PerformancePost 모델 import
from .serializers import PostSerializer  # PostSerializer import
from rest_framework import status
from django.http import JsonResponse  # JSON response import
from rest_framework.response import Response


# Create your views here.
class PostList(APIView):
    # GET 요청 처리 메소드
    def get(self, request):
        # queryset으로 모든 PerformancePost 객체 조회
        queryset = PerformancePost.objects.all()
        # 조회한 queryset을 PostSerializer를 이용해 직렬화
        serializer = PostSerializer(queryset, many=True)
        # JsonResponse를 이용하여 JSON response 반환
        return JsonResponse(serializer.data, safe=False)

    # POST 요청 처리 메소드
    def post(self, request):
        # 전달받은 request.data를 이용하여 PostSerializer 객체 생성
        serializer = PostSerializer(data=request.data)
        # serializer가 유효하다면 DB에 저장 후 성공 상태 코드 반환
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # serializer가 유효하지 않다면 오류 메시지와 함께 실패 상태 코드 반환
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    # 게시물 조회 메소드
    def get_object(self, pk):
        try:
            return PerformancePost.objects.get(pk=pk)
        except PerformancePost.DoesNotExist:
            return None

    def get(self, request, pk):
        # pk 값을 이용하여 게시물 조회
        post_user = self.get_object(pk)
        if not post_user:
            # 해당 게시물이 존재하지 않을 경우 404 에러 반환
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
        # PostSerializer를 이용해 조회한 PerformancePost 객체를 직렬화하여 JSON response 반환
        serializer = PostSerializer(post_user)
        return JsonResponse(serializer.data, safe=False)

    # 게시물 수정 메소드
    def put(self, request, pk):
        # pk 값을 이용하여 게시물 조회
        post_user = self.get_object(pk)
        if not post_user:
            # 해당 게시물이 존재하지 않을 경우 404 에러 반환
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
        # 이전에 조회한 PerformancePost객체와 수정하고자 하는 데이터(request.data)를 이용해 PostSerializer 생성
        serializer = PostSerializer(post_user, data=request.data)
        if serializer.is_valid():
            # serializer가 유효하다면 PerformancePost 객체를 업데이트하고 성공 상태 코드 반환
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        # serializer가 유효하지 않다면 오류 메시지와 함께 실패 상태 코드 반환
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시물 삭제 메소드
    def delete(self, request, pk):
        # pk 값을 이용하여 게시물 조회
        post_user = self.get_object(pk)
        if not post_user:
            # 해당 게시물이 존재하지 않을 경우 404 에러 반환
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        # PerformancePost 객체를 삭제하고 성공 상태 코드 반환
        post_user.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
