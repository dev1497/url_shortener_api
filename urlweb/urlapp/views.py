import random
import string
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from .models import urlShortener
from .serializers import urlShortenerSerializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# Create your views here.
@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def shorten_url(request):
    meta_data = request.META['HTTP_USER_AGENT']
    print("meta data",meta_data)

    if request.method == 'POST':
        data = request.data
        print('data url', data)
        #invalid URL check
        if valid_url(data['long_url']):
            short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            print('generated url :', short_url)

            url_record = urlShortener.objects.create(long_url=data['long_url'], short_url=short_url)
            short_url = "http://127.0.0.1:8000/" + short_url
            return Response({"status": "success", "short_url": short_url, "click_count": url_record.click_count,
                             "meta_data": meta_data}, status=status.HTTP_200_OK,
                            template_name='short_url.html')
        else:
            return Response({"status": "error", "message": "URL not found"},
                            status=status.HTTP_400_BAD_REQUEST, template_name='short_url.html')
    return render(request, 'short_url.html')


def get_url(request, short_url):
    try:
        result = urlShortener.objects.get(short_url=short_url)
        print('result:', result.click_count)
        result.click_count = result.click_count + 1
        result.save()
        print('result after update:', result.click_count)
        return redirect(result.long_url)

    except urlShortener.DoesNotExist:
        result = None
        raise Http404("Short url does not exist") # invalid short url check


def valid_url(to_validate):
    validator = URLValidator()
    try:
        validator(to_validate)
        return True
    except ValidationError as exception:
        print(exception)
        return False