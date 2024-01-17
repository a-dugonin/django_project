from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.exceptions import ValidationError


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result
    }
    return render(request, 'my_shop/request_query_params.html', context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, 'my_shop/user_form.html')


def upload_file_oversize(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('user_file'):
        file = request.FILES['user_file']
        if file.size > 1024:
            return render(request, 'my_shop/upload_file_error.html')
        else:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            print('Файл сохранен', filename)
    return render(request, 'my_shop/upload_file.html')