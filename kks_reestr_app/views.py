import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .models import KksCodeModel, KksObjectModel, KksStageObjectModel

from .forms import KksCodeForm


class IndexView(View):
    def get(self, request):
        # kks_form = KksCodeForm()
        objects = KksObjectModel.objects.get_queryset().filter(kks_object_show=True)
        content = {'objects': objects}
        # content = {'kks_form': kks_form}
        resp = render(request, 'kks_reestr_app/index.html', content)

        return resp


def get_objects(request):
    """Функция получения списка объектов"""
    objects = KksObjectModel.objects.get_queryset().filter(kks_object_show=True)
    content = {'objects': objects}
    # content = {'kks_form': kks_form}
    resp = render(request, 'kks_reestr_app/ajax/sector_1.html', content)
    return resp


class GetSector2View(View):
    def post(self, request):
        print('sector2')
        print(request.POST)
        kks_object_number = request.POST.get('kks_object_number')
        print(kks_object_number)
        obj = KksObjectModel.objects.get(id=kks_object_number).kks_object_abr
        objects = KksStageObjectModel.objects.get_queryset().filter(kks_object_id=kks_object_number)
        content = {'objects': objects}
        resp = render(request, 'kks_reestr_app/ajax/sector_2.html', content)
        resp.set_cookie(key='kks_object', value=obj)
        return resp
