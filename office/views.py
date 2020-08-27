from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
from office import models
from django.shortcuts import get_object_or_404

# Create your views here.


def index(request):
    """
    index页面
    :param request:
    :return:
    """
    # assets = models.Asset.objects.all()
    return render(request, 'office/index.html', locals())
