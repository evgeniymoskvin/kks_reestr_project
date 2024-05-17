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
    KksTypeBuildingModel, KksBuildingModel, KksHighMarkModel, KksSector5Model, KksCodeSystemModel, \
    KKSThematicDirectionModel, KksTypeConstructionModel, KksExecutionConstructionModel, KksSector6Model, \
    KksTechnicalSpecialtyModel, KksTypeDocument, EmployeeModel


class IndexView(View):
    """
    Главная страница проекта
    """

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        content = {
        }
        resp = render(request, 'kks_reestr_app/index.html', content)
        return resp


def get_objects(request):
    """Функция получения списка объектов"""
    print('Sector1')
    objects = KksObjectModel.objects.get_queryset().filter(kks_object_show=True).order_by('kks_object_abr')
    content = {'objects': objects}
    print(objects)
    # content = {'kks_form': kks_form}
    resp = render(request, 'kks_reestr_app/ajax/sector_1.html', content)
    return resp


class GetSector2View(View):
    """Сектор 2"""

    def post(self, request):
        """
        :param request: Получение данных по сектору 1, установка значений в cookies
        :return: Страница для сектора 2
        """
        print('Sector_2')
        print(f'REQUEST: {request.POST}')
        print(f'COOKIES: {request.COOKIES}')
        kks_object_number = request.POST.get('kks_object_number')  # id сектора 1
        print(kks_object_number)
        obj = KksObjectModel.objects.get(id=kks_object_number).kks_object_abr
        # Получение этапов относящихся к объекту и фильтрация по алфавиту
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
        print(f'REQUEST: {request.POST}')
        print(f'COOKIES: {request.COOKIES}')
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
        print(f'REQUEST: {request.POST}')
        print(f'COOKIES: {request.COOKIES}')
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
        print(f'REQUEST: {request.POST}')
        print(f'COOKIES: {request.COOKIES}')
        kks_type_building_number_id = request.POST.get('kks_type_building_number')
        obj = KksTypeBuildingModel.objects.get(id=kks_type_building_number_id).kks_type_building_code
        content = {}
        resp = render(request, 'kks_reestr_app/ajax/get_type_doc.html', content)
        resp.set_cookie(key='kks_sector4_text', value=obj)
        resp.set_cookie(key='kks_sector4_id', value=kks_type_building_number_id)
        return resp


class GetSector5View(View):
    """Сектор 4"""

    def post(self, request):
        print('sector5')
        print(f'REQUEST: {request.POST}')
        print(f'COOKIES: {request.COOKIES}')
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
        # Устанавливаем cookies с типом документации
        resp.set_cookie(key='kks_type_doc', value=kks_type_doc_id)
        return resp


class GetSector6View(View):
    """Сектор 6"""

    def post(self, request):
        print('Sector6')
        print(f'REQUEST: {request.POST}')
        print(f'COOKIES: {request.COOKIES}')
        kks_type_doc_id = int(request.COOKIES['kks_type_doc'])
        if kks_type_doc_id == 4 or kks_type_doc_id == 5 or kks_type_doc_id == 6:
            kks_building_id = request.POST.get('kks_building')  # Получаем id кода здания
            kks_high_id = request.POST.get('kks_high')  # Получаем id кода высотной отметки
            kks_building_text = KksBuildingModel.objects.get(id=kks_building_id).kks_building_abr  # Сокращение здания
            kks_high_text = KksHighMarkModel.objects.get(id=kks_high_id).kks_high_mark  # Код высотной отметки
            result = f'{kks_building_text}{kks_high_text}'  # Итоговое значение для сектора 5
            sector_5_id, created = KksSector5Model.objects.get_or_create(kks_sector5_value=f'{result}')
            print(f'Sector 5: value = {sector_5_id}, id = {sector_5_id.id}')
        else:
            kks_number_chapter = request.POST.get('input_sector5_txt1')  # Раздел
            kks_number_part = request.POST.get('input_sector5_txt2')  # Часть
            kks_number_subsection = request.POST.get('input_sector5_txt3')  # Подраздел
            result = f'{kks_number_chapter}{kks_number_part}{kks_number_subsection}'
            sector_5_id, created = KksSector5Model.objects.get_or_create(kks_sector5_value=f'{result}')
            print(f'Sector 5: value = {sector_5_id}, id = {sector_5_id.id}')

        # Определение полей для сектора 6
        if kks_type_doc_id == 0 or kks_type_doc_id == 1 or kks_type_doc_id == 2 or kks_type_doc_id == 3:
            # В Случае если ОБИН, ПООБ, ПД
            link = f'kks_reestr_app/ajax/sector_6.1.html'
            content = {'result': result,
                       'kks_type_doc_id': kks_type_doc_id}
        elif kks_type_doc_id == 7:
            # В случае если НИР и ОКР
            objects = KKSThematicDirectionModel.objects.get_queryset().filter(
                kks_thematic_direction_visible=True).order_by('kks_thematic_direction_abr')
            link = f'kks_reestr_app/ajax/sector_6.3.1.html'
            content = {'result': result,
                       'objects': objects,
                       'kks_type_doc_id': kks_type_doc_id}

        elif kks_type_doc_id == 5:
            # в случае рабочей документации с вопросом про строительную конструкцию
            link = f'kks_reestr_app/ajax/sector_6.2_question.html'
            content = {'result': result,
                       'kks_type_doc_id': kks_type_doc_id}

        else:
            # в остальных случаях
            objects = KksCodeSystemModel.objects.get_queryset().filter(kks_system_visible=True).order_by(
                'kks_system_abr')
            content = {'result': result,
                       'objects': objects,
                       'kks_type_doc_id': kks_type_doc_id}
            link = 'kks_reestr_app/ajax/sector_6.3.2.html'

        resp = render(request, link, content)
        resp.set_cookie(key='kks_sector5_text', value=result)
        resp.set_cookie(key='kks_sector5_id', value=sector_5_id.id)
        return resp


class GetSector61View(View):
    """Для рабочей документации в секторе 6"""

    def post(self, request):
        print('Sector6.1')
        print(f'REQUEST: {request.POST}')
        print(f'COOKIES: {request.COOKIES}')
        kks_building_construction = int(
            request.POST.get('kks_building_construction'))  # Проверка на строительную конструкцию
        if kks_building_construction == 0:
            # Если конструкция не строительная
            objects = KksCodeSystemModel.objects.get_queryset().filter(kks_system_visible=True).order_by(
                'kks_system_abr')  # KKS коды систем
            content = {'objects': objects}
            resp = render(request, 'kks_reestr_app/ajax/sector_6.3.2.html', content)
        else:
            # Если конструкция строительная
            types_construction = KksTypeConstructionModel.objects.get_queryset().order_by(
                'kks_type_construction')  # KKS коды типов конструкций
            execution_construction = KksExecutionConstructionModel.objects.get_queryset().order_by(
                'kks_exec_construction')  # KKS коды типов разрабатываемых чертежей
            content = {'types_construction': types_construction,
                       'execution_construction': execution_construction}
            resp = render(request, 'kks_reestr_app/ajax/sector_6.3.3_building_constr.html', content)
        resp.set_cookie(key='kks_building_construction', value=kks_building_construction)
        return resp


class GetSector7View(View):
    """Сектор 7"""

    def post(self, request):
        print('Sector7')
        print(f'REQUEST: {request.POST}')
        print(f'COOKIES: {request.COOKIES}')
        kks_type_doc_id = int(request.COOKIES['kks_type_doc'])
        kks_building_construction = int(request.COOKIES['kks_building_construction'])
        if kks_type_doc_id == 0 or kks_type_doc_id == 1 or kks_type_doc_id == 2 or kks_type_doc_id == 3:
            # Если ОБИН, ПООБ, Предпроектная документация или Том проектной документации
            input_sector6_txt1 = request.POST.get('input_sector6_txt1')
            input_sector6_txt2 = request.POST.get('input_sector6_txt2')
            input_sector6_txt3 = request.POST.get('input_sector6_txt3')
            if input_sector6_txt3 is None:
                input_sector6_txt3 = '&'
            result = f'{input_sector6_txt1}{input_sector6_txt2}{input_sector6_txt3}'
        elif kks_type_doc_id == 7:
            # Если НИР и ОКР
            kks_thematic_direction_id = int(request.POST.get('kks_thematic_direction_id'))
            kks_thematic_direction_text = KKSThematicDirectionModel.objects.get(
                id=kks_thematic_direction_id).kks_thematic_direction_abr
            result = f'{kks_thematic_direction_text}&&'
        else:
            # В остальных случаях: Структурная единица проектной документации, РД, Конструкторская документация
            if kks_building_construction == 1:  # Если конструкция строительная
                kks_types_construction_id = request.POST.get('kks_types_construction_id')  # id типа конструкции
                kks_execution_construction_id = request.POST.get(
                    'kks_execution_construction_id')  # id типа разрабатываемого чертежа
                kks_types_construction_text = KksTypeConstructionModel.objects.get(
                    id=kks_types_construction_id).kks_type_construction
                kks_execution_construction_text = KksExecutionConstructionModel.objects.get(
                    id=kks_execution_construction_id).kks_exec_construction
                result = f'&&&{kks_types_construction_text}{kks_execution_construction_text}'
            else:
                kks_code_system_id = int(request.POST.get('kks_code_system_id'))  # id кода системы
                input_sector6_txt1 = request.POST.get(
                    'input_sector6_txt1')  # системная нумерация функционального кода KKS
                kks_code_system_text = KksCodeSystemModel.objects.get(id=kks_code_system_id).kks_system_abr
                result = f'{kks_code_system_text}{input_sector6_txt1}'
        sector_6_id, created = KksSector6Model.objects.get_or_create(
            kks_sector6_value=f'{result}')  # Создаем запись в таблице секторов 6
        print(f'Sector 6: value = {sector_6_id}, id = {sector_6_id.id}')
        objects = KksTechnicalSpecialtyModel.objects.get_queryset().filter(kks_tech_speciality_show=True).order_by(
            'kks_tech_speciality')
        content = {'objects': objects}
        resp = render(request, 'kks_reestr_app/ajax/sector_7.html', content)
        resp.set_cookie(key='kks_sector6_id', value=sector_6_id.id)
        resp.set_cookie(key='kks_sector6_text', value=result)
        return resp


class GetSector8View(View):
    """Сектор 8"""

    def post(self, request):
        print('Sector8')
        print(f'REQUEST: {request.POST}')
        print(f'COOKIES: {request.COOKIES}')
        kks_tech_speciality_id = int(request.POST.get('kks_tech_speciality_id'))
        kks_tech_speciality_text = KksTechnicalSpecialtyModel.objects.get(id=kks_tech_speciality_id).kks_tech_speciality
        objects = KksTypeDocument.objects.get_queryset().order_by('kks_type_doc')
        content = {'objects': objects}
        resp = render(request, 'kks_reestr_app/ajax/sector_8.html', content)
        resp.set_cookie(key='kks_sector7_id', value=kks_tech_speciality_id)
        resp.set_cookie(key='kks_sector7_text', value=kks_tech_speciality_text)
        return resp


class GetSector9View(View):
    """Сектор 9"""

    def post(self, request):
        print('Sector9')
        print(f'REQUEST: {request.POST}')
        print(f'COOKIES: {request.COOKIES}')
        kks_type_document_id = int(request.POST.get('kks_type_document_id'))
        kks_type_document_text = KksTypeDocument.objects.get(id=kks_type_document_id).kks_type_doc
        # Получение id каждого сектора из cookies
        kks_sector1_id = int(request.COOKIES['kks_sector1_id'])
        kks_sector2_id = int(request.COOKIES['kks_sector2_id'])
        kks_sector3_id = int(request.COOKIES['kks_sector3_id'])
        kks_sector4_id = int(request.COOKIES['kks_sector4_id'])
        kks_sector5_id = int(request.COOKIES['kks_sector5_id'])
        kks_sector6_id = int(request.COOKIES['kks_sector6_id'])
        kks_sector7_id = int(request.COOKIES['kks_sector7_id'])
        kks_sector8_id = kks_type_document_id
        # Фильтруем из таблицы кодов по id
        kks_code_queryset = KksCodeModel.objects.get_queryset().filter(object_id=kks_sector1_id).filter(
            stage_id=kks_sector2_id).filter(organization_id=kks_sector3_id).filter(
            type_building_id=kks_sector4_id).filter(sector5_id=kks_sector5_id).filter(sector6_id=kks_sector6_id).filter(
            tech_speciality_id=kks_sector7_id).filter(type_doc_id=kks_sector8_id)
        # Присваиваем порядковый номер
        if len(kks_code_queryset) == 0:
            index_number = 1
        else:
            index_number = len(kks_code_queryset) + 1
        # Текстовая строка для сектора 9
        index_number_str = str(index_number).rjust(4, '0')

        content = {'kks_sector1_text': request.COOKIES['kks_sector1_text'],
                   'kks_sector2_text': request.COOKIES['kks_sector2_text'],
                   'kks_sector3_text': request.COOKIES['kks_sector3_text'],
                   'kks_sector4_text': request.COOKIES['kks_sector4_text'],
                   'kks_sector5_text': request.COOKIES['kks_sector5_text'],
                   'kks_sector6_text': request.COOKIES['kks_sector6_text'],
                   'kks_sector7_text': request.COOKIES['kks_sector7_text'],
                   'kks_sector8_text': kks_type_document_text,
                   'kks_sector9_text': index_number_str}
        resp = render(request, 'kks_reestr_app/ajax/sector_9.html', content)
        resp.set_cookie(key='kks_sector8_id', value=kks_type_document_id)
        resp.set_cookie(key='kks_sector8_text', value=kks_type_document_text)
        resp.set_cookie(key='kks_sector9_text', value=index_number_str)
        return resp


class ApproveSaveCodeView(View):
    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        print('Sector9')
        print(f'REQUEST: {request.POST}')
        print(f'COOKIES: {request.COOKIES}')
        # Получение всех данных из cookies
        kks_sector1_id = int(request.COOKIES['kks_sector1_id'])
        kks_sector1_text = request.COOKIES['kks_sector1_text']
        kks_sector2_id = int(request.COOKIES['kks_sector2_id'])
        kks_sector2_text = request.COOKIES['kks_sector2_text']
        kks_sector3_id = int(request.COOKIES['kks_sector3_id'])
        kks_sector3_text = request.COOKIES['kks_sector3_text']
        kks_sector4_id = int(request.COOKIES['kks_sector4_id'])
        kks_sector4_text = request.COOKIES['kks_sector4_text']
        kks_sector5_id = int(request.COOKIES['kks_sector5_id'])
        kks_sector5_text = request.COOKIES['kks_sector5_text']
        kks_sector6_id = int(request.COOKIES['kks_sector6_id'])
        kks_sector6_text = request.COOKIES['kks_sector6_text']
        kks_sector7_id = int(request.COOKIES['kks_sector7_id'])
        kks_sector7_text = request.COOKIES['kks_sector7_text']
        kks_sector8_id = int(request.COOKIES['kks_sector8_id'])
        kks_sector8_text = request.COOKIES['kks_sector8_text']
        # Фильтруем из таблицы кодов по id
        kks_code_queryset = KksCodeModel.objects.get_queryset().filter(object_id=kks_sector1_id).filter(
            stage_id=kks_sector2_id).filter(organization_id=kks_sector3_id).filter(
            type_building_id=kks_sector4_id).filter(sector5_id=kks_sector5_id).filter(sector6_id=kks_sector6_id).filter(
            tech_speciality_id=kks_sector7_id).filter(type_doc_id=kks_sector8_id)
        # Присваиваем порядковый номер
        if len(kks_code_queryset) == 0:
            index_number = 1
        else:
            index_number = len(kks_code_queryset) + 1
        # Текстовая строка для сектора 9
        kks_sector9_text = str(index_number).rjust(4, '0')
        # Текстовая строка кода целиком
        text_kks_code = f'{kks_sector1_text}.{kks_sector2_text}.{kks_sector3_text}.{kks_sector4_text}.{kks_sector5_text}.{kks_sector6_text}.{kks_sector7_text}.{kks_sector8_text}.{kks_sector9_text}'
        # Создаем новую запись с кодом
        new_kks_code = KksCodeModel(
            object_id=kks_sector1_id,
            stage_id=kks_sector2_id,
            organization_id=kks_sector3_id,
            type_building_id=kks_sector4_id,
            sector5_id=kks_sector5_id,
            sector6_id=kks_sector6_id,
            tech_speciality_id=kks_sector7_id,
            type_doc_id=kks_sector8_id,
            index_number=index_number,
            author_id=EmployeeModel.objects.get(user=request.user).id,
            text=text_kks_code,
        )
        new_kks_code.save()
        print(new_kks_code)
        user = EmployeeModel.objects.get(user=request.user)
        objects = KksCodeModel.objects.get_queryset().filter(author_id=user.id).order_by('-id')
        content = {"objects": objects}
        resp = render(request, 'kks_reestr_app/my-kks-codes.html', content)  # Страница переадресации
        # Чистим cookies
        cookies_list = ['kks_sector1_text', 'kks_sector2_text', 'kks_sector3_text', 'kks_sector4_text',
                        'kks_sector5_text', 'kks_sector6_text', 'kks_sector7_text', 'kks_sector8_text',
                        'kks_sector9_text',
                        'kks_sector1_id', 'kks_sector2_id', 'kks_sector3_id', 'kks_sector4_id', 'kks_sector5_id',
                        'kks_sector6_id', 'kks_sector7_id', 'kks_sector8_id',
                        'kks_building_construction',
                        'kks_type_doc']
        for i in cookies_list:
            resp.delete_cookie(i)
        return resp


class GetAllKksCodeView(View):
    def get(self, request):
        objects = KksCodeModel.objects.get_queryset().order_by('-id')
        content = {"objects": objects}
        return render(request, 'kks_reestr_app/all-kks-codes.html', content)


class GetMyKksCodeView(View):
    def get(self, request):
        user = EmployeeModel.objects.get(user=request.user)
        objects = KksCodeModel.objects.get_queryset().filter(author_id=user.id).order_by('-id')
        content = {"objects": objects}
        return render(request, 'kks_reestr_app/my-kks-codes.html', content)
