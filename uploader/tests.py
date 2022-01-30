from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files import File

from rest_framework.test import APITestCase

from uploader.models import UploadedFile

from uploader.functions import minioClient

User = get_user_model()


class TestApi(APITestCase):
    def setUp(self) -> None:
        super(TestApi, self).setUp()

        user = User.objects.create_user(
            username='api_test_user'
        )
        user.set_password('@api_pass!')
        user.save()

        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.user = user

    def get_token(self):
        token_url = reverse('api:token_obtain_pair')
        response = self.client.post(token_url, {
            'username': 'api_test_user',
            'password': '@api_pass!'
        })

        return response.data.get('access')

    def upload_file(self):
        create_upload_url = reverse('api:upload_create_list')
        f = File(open('test_file.txt', 'r'))

        response = self.client.post(create_upload_url, data={
            'file': f
        }, format='multipart')

        return response

    def test_get_token(self):
        token_url = reverse('api:token_obtain_pair')
        response = self.client.post(token_url, {
            'username': 'api_test_user',
            'password': '@api_pass!'
        })

        self.assertTrue(response.data.get('access'))

    def test_create_upload(self):
        response = self.upload_file()

        upload_item = UploadedFile.objects.get(id=response.data.get('id'))

        minio_file = minioClient.get_object(bucket_name=settings.MINIO_STORAGE_MEDIA_BUCKET_NAME,
                                            object_name=upload_item.file.name)
        self.assertEqual(response.data.get('id'), 1)
        self.assertTrue(response.data.get('id'), upload_item.id)
        self.assertEqual(response.data.get('type'), 'txt')
        self.assertTrue(response.data.get('file_url'))
        self.assertTrue(minio_file)

    def test_list_upload(self):
        list_url = reverse('api:upload_create_list')
        self.upload_file()

        response = self.client.get(list_url)

        uploads = UploadedFile.objects.all()

        self.assertEqual(len(response.data), uploads.count())
        self.assertTrue(uploads[0].id in [item['id'] for _, item in response.data.items()])

    def test_delete_upload(self):
        self.upload_file()
        uploaded_file = UploadedFile.objects.all()[0]
        delete_url = reverse('api:upload_delete', kwargs={'file_id': uploaded_file.id})

        response = self.client.delete(delete_url, format='json')

        self.assertEqual(response.data, 'file is deleted!')

        uploaded_files = UploadedFile.objects.all()
        self.assertFalse(uploaded_files)

        try:
            minioClient.get_object(bucket_name=settings.MINIO_STORAGE_MEDIA_BUCKET_NAME,
                                   object_name=uploaded_file.file.name)
        except Exception as e:
            error = e.message

        self.assertTrue('specified key does not exist' in error)

    def test_integration(self):
        minio_url = settings.MINIO_STORAGE_ENDPOINT
        response = self.client.get('http://{}/'.format(minio_url))
        self.assertEqual(response.status_code, 200)
