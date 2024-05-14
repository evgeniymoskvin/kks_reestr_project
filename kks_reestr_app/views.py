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

from .models import KksCodeModel, KksObjectModel, KksStageObjectModel, KksOrganizationCodeObjectModel, KksTypeBuildingModel

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
    print('Sector1')
    """Функция получения списка объектов"""
    objects = KksObjectModel.objects.get_queryset().filter(kks_object_show=True)
    content = {'objects': objects}
    print(objects)
    # content = {'kks_form': kks_form}
    resp = render(request, 'kks_reestr_app/ajax/sector_1.html', content)
    return resp


class GetSector2View(View):
    """Сектор 2"""

    def post(self, request):
        print('Sector_2')
        kks_object_number = request.POST.get('kks_object_number')  # id сектора 1
        print(kks_object_number)
        obj = KksObjectModel.objects.get(id=kks_object_number).kks_object_abr
        # Получение этапов относящихся к объекту
        objects = KksStageObjectModel.objects.get_queryset().filter(kks_object_id=kks_object_number)
        content = {'objects': objects}
        resp = render(request, 'kks_reestr_app/ajax/sector_2.html', content)
        # Устанавливаем cookies
        resp.set_cookie(key='kks_sector1_text', value=obj)  # cookies: текст сектора 1
        resp.set_cookie(key='kks_sector1_id', value=kks_object_number)  # cookies: id сектора 1
        return resp


class GetSector3View(View):
    def post(self, request):
        print('sector3')
        print(request.POST)
        print(request.COOKIES['kks_sector1_id'])
        kks_object_id = request.COOKIES['kks_sector1_id']  # id сектора 1
        kks_stage_number = request.POST.get('kks_stage_number')  # id сектора 2
        print(kks_stage_number)
        obj = KksStageObjectModel.objects.get(id=kks_stage_number).kks_stage.kks_stage_letter
        objects = KksOrganizationCodeObjectModel.objects.get_queryset().filter(kks_object_id=kks_object_id)
        content = {'objects': objects}
        resp = render(request, 'kks_reestr_app/ajax/sector_3.html', content)
        resp.set_cookie(key='kks_sector2_text', value=obj)
        resp.set_cookie(key='kks_sector2_id', value=kks_stage_number)
        return resp

class GetSector4View(View):
    def post(self, request):
        print('sector4')
        print(request.POST)
        print(request.COOKIES['kks_sector1_id'])
        kks_org_number_id = request.POST.get('kks_org_number')
        kks_object_id = request.COOKIES['kks_sector1_id']  # id сектора 1
        obj = KksOrganizationCodeObjectModel.objects.get(id=kks_org_number_id).kks_organization_code.kks_org_code
        objects = KksTypeBuildingModel.objects.get_queryset().filter(kks_object_id=kks_object_id)
        content = {'objects': objects}
        print(objects)
        resp = render(request, 'kks_reestr_app/ajax/sector_4.html', content)
        resp.set_cookie(key='kks_sector3_text', value=obj)
        resp.set_cookie(key='kks_sector3_id', value=kks_org_number_id)
        return resp
