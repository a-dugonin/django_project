from django.urls import path
from .views import process_get_view, user_form, upload_file_oversize

app_name = 'my_shop'
urlpatterns = [
    path('get/', process_get_view, name='get_view'),
    path('bio/', user_form, name='user_form'),
    path('upload/', upload_file_oversize, name='upload_file'),
]
