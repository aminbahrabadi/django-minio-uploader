from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


app_name = 'api'


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('upload/', views.ApiUpload.as_view(), name='upload_create_list'),
    path('upload/<int:file_id>/', views.ApiUploadDelete.as_view(), name='upload_delete'),
]
