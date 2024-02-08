import time

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def setup_useragent_on_request_middleware(get_response):
    print('Инициализация кода')

    def middleware(request: HttpRequest):
        print('До получения ответа')
        request.user_agent = request.META['HTTP_USER_AGENT']
        print(request.META.get('REMOTE_ADDR'), time.time())
        response = get_response(request)
        print('После получения ответа')
        return response

    return middleware


class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.response_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.request_count += 1
        print('Количество запросов', self.request_count)
        response = self.get_response(request)
        self.response_count += 1
        print('Количество ответов', self.response_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print(f'За все время получено {self.exceptions_count} ошибок')


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_user_attempts = {}

    def __call__(self, request: HttpRequest) -> HttpResponse:
        timeout = 0
        if not self.request_user_attempts:
            print('Доступ пользователя разрешен')
        else:
            if (time.time() - self.request_user_attempts['user_time']) < timeout and \
                    self.request_user_attempts['user_ip'] == request.META['REMOTE_ADDR']:
                print('Ошибка доступа')
                return render(request, 'my_shop/user_request_error.html')
            else:
                print('Доступ пользователя разрешен')

        self.request_user_attempts = {'user_ip': request.META['REMOTE_ADDR'], 'user_time': time.time()}

        response = self.get_response(request)
        return response
