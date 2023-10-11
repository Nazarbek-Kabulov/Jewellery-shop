from django.http import HttpResponseForbidden


class IPRestrictedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        client_ip = request.META.get('REMOTE_ADDR')

        ip_addresses = [
            '127.0.0.1',
            '192.168.107.133'
        ]

        if client_ip not in ip_addresses and request.path.find('/admin/') != -1:
            return HttpResponseForbidden('Permission denied')

        response = self.get_response(request)
        return response
