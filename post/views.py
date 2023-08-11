from rest_framework.views import APIView
from .models import PerformancePost
from .serializers import PostSerializer
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


class PostList(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        queryset = PerformancePost.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    # POST 요청 처리 메소드에서 이미지 처리 수정
    def post(self, request):
        profile = request.FILES.get("profile")

        data = request.data.copy()
        data["profile"] = profile
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return PerformancePost.objects.get(pk=pk)
        except PerformancePost.DoesNotExist:
            return None

    def get(self, request, pk):
        post_user = self.get_object(pk)
        if not post_user:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post_user)
        return JsonResponse(serializer.data, safe=False)

    # PUT 요청 처리 메소드에서 이미지 처리 수정
    def put(self, request, pk):
        post_user = self.get_object(pk)
        if not post_user:
            return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()

        if 'profile' in request.FILES:
            data['profile'] = request.FILES['profile']

        serializer = PostSerializer(post_user, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post_user = self.get_object(pk)
        if not post_user:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        post_user.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
