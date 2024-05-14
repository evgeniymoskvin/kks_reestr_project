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

from .models import KksCodeModel, KksObjectModel, KksStageObjectModel, KksOrganizationCodeObjectModel, \
    KksTypeBuildingModel, KksBuildingModel, KksHighMarkModel, KksSector5Model

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
    objects = KksObjectModel.objects.get_queryset().filter(kks_object_show=True).order_by('kks_object_abr')
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
        objects = KksStageObjectModel.objects.get_queryset().filter(kks_object_id=kks_object_number).order_by(
            'kks_stage__kks_stage_letter')
        content = {'objects': objects}
        resp = render(request, 'kks_reestr_app/ajax/sector_2.html', content)
        # Устанавливаем cookies
        resp.set_cookie(key='kks_sector1_text', value=obj)  # cookies: текст сектора 1
        resp.set_cookie(key='kks_sector1_id', value=kks_object_number)  # cookies: id сектора 1
        return resp


class GetSector3View(View):
    """Сектор 3"""

    def post(self, request):
        print('sector3')
        print(request.POST)
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
    """Сектор 4"""

    def post(self, request):
        print('sector4')
        print(request.POST)
        kks_org_number_id = request.POST.get('kks_org_number')
        kks_object_id = request.COOKIES['kks_sector1_id']  # id сектора 1
        obj = KksOrganizationCodeObjectModel.objects.get(id=kks_org_number_id).kks_organization_code.kks_org_code
        objects = KksTypeBuildingModel.objects.get_queryset().filter(kks_object_id=kks_object_id).order_by(
            'kks_type_building_code')
        content = {'objects': objects}
        print(objects)
        resp = render(request, 'kks_reestr_app/ajax/sector_4.html', content)
        resp.set_cookie(key='kks_sector3_text', value=obj)
        resp.set_cookie(key='kks_sector3_id', value=kks_org_number_id)
        return resp


class GetTypeDocView(View):
    def post(self, request):
        print('type_doc')
        print(request.POST)
        kks_type_building_number_id = request.POST.get('kks_type_building_number')
        kks_object_id = request.COOKIES['kks_sector1_id']  # id сектора 1
        obj = KksTypeBuildingModel.objects.get(id=kks_type_building_number_id).kks_type_building_code
        # objects = KksTypeBuildingModel.objects.get_queryset().filter(kks_object_id=kks_object_id)
        # content = {'objects': objects}
        content = {}
        resp = render(request, 'kks_reestr_app/ajax/get_type_doc.html', content)
        resp.set_cookie(key='kks_sector4_text', value=obj)
        resp.set_cookie(key='kks_sector4_id', value=kks_type_building_number_id)
        return resp


class GetSector5View(View):
    """Сектор 4"""

    def post(self, request):
        print('sector5')
        print(request.POST)
        kks_type_doc_id = int(request.POST.get('kks_type_doc'))
        if kks_type_doc_id == 4 or kks_type_doc_id == 5 or kks_type_doc_id == 6:
            kks_object_id = request.COOKIES['kks_sector1_id']  # id сектора 1
            kks_sector4_id = request.COOKIES['kks_sector4_id']  # id сектора 1
            objects = KksBuildingModel.objects.get_queryset().filter(kks_building_visible=True).filter(
                kks_object_id=kks_object_id).filter(
                kks_type_building_id=kks_sector4_id).order_by('kks_building_abr')
            high_marks = KksHighMarkModel.objects.get_queryset().order_by('kks_high_mark')
            print(objects)
            content = {'objects': objects,
                       'high_marks': high_marks}
            resp = render(request, 'kks_reestr_app/ajax/sector_5.2.html', content)
        else:
            content = {}
            resp = render(request, 'kks_reestr_app/ajax/sector_5.1.html', content)
        # content = {'objects': objects}
        content = {}
        # print(objects)

        resp.set_cookie(key='kks_type_doc', value=kks_type_doc_id)
        return resp


class GetSector6View(View):
    """Сектор 6"""

    def post(self, request):
        print('sector6')
        print(f'REQUEST: {request.POST}')
        print(f'COOKIES: {request.COOKIES}')
        kks_type_doc_id = int(request.COOKIES['kks_type_doc'])
        if kks_type_doc_id == 4 or kks_type_doc_id == 5 or kks_type_doc_id == 6:
            kks_building_id = request.POST.get('kks_building')
            kks_high_id = request.POST.get('kks_high')
            kks_building_text = KksBuildingModel.objects.get(id=kks_building_id).kks_building_abr
            kks_high_text = KksHighMarkModel.objects.get(id=kks_high_id).kks_high_mark
            result = f'{kks_building_text}{kks_high_text}'
            sector_5_id, created = KksSector5Model.objects.get_or_create(kks_sector5_value=f'{result}')
            print(sector_5_id.id)
            print(sector_5_id)

        content = {'result': result}
        resp = render(request, 'kks_reestr_app/ajax/sector_5.2.html', content)
        resp.set_cookie(key='kks_sector5_text', value=result)
        resp.set_cookie(key='kks_sector5_id', value=sector_5_id.id)
        return resp
