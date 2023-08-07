from django.urls import path
from .views import ResumeDetail, ResumeList
from django.urls import include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("", ResumeList.as_view(), name="Resume_list"),
    path("<int:pk>/", ResumeDetail.as_view(), name="Resume_detail"),
    path("delete/<int:pk>/", ResumeDetail.as_view(), name="Resume_delete"),
]
