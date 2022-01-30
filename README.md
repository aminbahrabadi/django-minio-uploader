# Simple Django Uploader using MinIO / API
## How to run
1. Clone the project
2. Create postgresql db
3. Install MinIo and run server (command: ./minio server /minio_config --console-address ":9001")
4. Open terminal and create a virtual environment:
<br />```virtualenv venv```
3. Activate virtual environment:
<br />```source venv/bin/activate```
4. Install packages:
<br />```pip install -r requirements.txt```
5. Migrate and create database:
<br />```python manage.py migrate```
6. Run server:
<br />```python manage.py runserver```
7. You can run tests:
<br />```python manage.py test```
8. Open the browser and browse this URL and user Swagger (attention: for the Authentication, user the token with a 'Bearer' word before the token):
<br />```127.0.0.1:8000```
## Api
API links are as follow:
### Token (POST request):
<br />Before using each end-point, you should get a token by using this URL.
<br />URL: ```/api/token/```
### Upload file (POST request):
<br />URL: ```/api/upload/```
### List of Uploaded files (GET request):
<br />URL: ```/api/upload/```
### Delete Uploaded file (DELETE request):
<br />URL: ```upload/<int:file_id>/```
