from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .serializers import CreateUploadSerializer
from .models import UploadedFile


class ApiUpload(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateUploadSerializer(data=request.data)

        if serializer.is_valid():
            user = self.request.user
            file = serializer.validated_data.get('file')

            uploaded_file = UploadedFile.objects.create(
                user=user,
                file=file
            )

            file_dict = {
                'id': uploaded_file.id,
                'file_url': uploaded_file.file.url,
                'type': uploaded_file.file_extension,
                'size': uploaded_file.file_size
            }

            return Response(file_dict, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = self.request.user
        uploads = UploadedFile.objects.filter(user=user)
        uploads_dict = {}
        for upload in uploads:
            uploads_dict[upload.id] = {}
            uploads_dict[upload.id]['id'] = upload.id
            uploads_dict[upload.id]['url'] = upload.file.url
            uploads_dict[upload.id]['type'] = upload.file_extension
            uploads_dict[upload.id]['size'] = upload.file_size

        return Response(uploads_dict, status=status.HTTP_200_OK)


class ApiUploadDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        file_id = self.kwargs.get('file_id')
        file = get_object_or_404(UploadedFile, id=file_id)
        file.delete()
        return Response('file is deleted!', status=status.HTTP_200_OK)
