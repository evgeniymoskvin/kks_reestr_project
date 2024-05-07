from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator

from django.core.files.storage import FileSystemStorage
from os import path
import datetime


# Create your models here.

class JobTitleModel(models.Model):
    """ Таблица должностей """

    job_title = models.CharField("Должность", max_length=200)

    class Meta:
        verbose_name = _("должность")
        verbose_name_plural = _("должности")
        managed = False
        db_table = 'ToDo_tasks_jobtitlemodel'

    def __str__(self):
        return f'{self.job_title}'


class CityDepModel(models.Model):
    city = models.CharField(verbose_name="Город", max_length=100)
    name_dep = models.CharField(verbose_name="Наименование организации", max_length=350)

    class Meta:
        managed = False
        verbose_name = _("город/организация")
        verbose_name_plural = _("города/организации")
        db_table = 'admin_panel_app_citydepmodel'

    def __str__(self):
        return f'{self.city} - {self.name_dep}'


class GroupDepartmentModel(models.Model):
    """Список управлений"""
    group_dep_abr = models.CharField("Сокращенное название управления", max_length=10)
    group_dep_name = models.CharField("Полное название управления", max_length=250)
    city_dep = models.ForeignKey(CityDepModel, verbose_name="Город", on_delete=models.SET_NULL, null=True, blank=True)
    show = models.BooleanField("Отображать отдел", default=True)

    def __str__(self):
        return f'{self.group_dep_abr}, {self.group_dep_name}'

    class Meta:
        verbose_name = _("управление")
        verbose_name_plural = _("управления")
        managed = False
        db_table = 'ToDo_tasks_groupdepartmentmodel'


class CommandNumberModel(models.Model):
    """Номера отделов"""
    command_number = models.IntegerField("Номер отдела/Сокращение")
    command_name = models.CharField("Наименование отдела", max_length=150)
    department = models.ForeignKey(GroupDepartmentModel, verbose_name="Управление", on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    show = models.BooleanField("Отображать отдел", default=True)

    def __str__(self):
        return f'{self.command_number}, {self.command_name}'

    class Meta:
        verbose_name = _("номер отдела")
        verbose_name_plural = _("номера отделов")
        managed = False
        db_table = 'ToDo_tasks_commandnumbermodel'


class EmployeeModel(models.Model):
    """Таблица сотрудников"""
    user = models.OneToOneField(User, models.PROTECT, verbose_name="Пользователь", related_name='phonebook_emp_user')
    last_name = models.CharField("Фамилия", max_length=150)
    first_name = models.CharField("Имя", max_length=150)
    middle_name = models.CharField("Отчество", max_length=150)
    personnel_number = models.CharField("Табельный номер", max_length=20, null=True, default=None)
    job_title = models.ForeignKey(JobTitleModel, on_delete=models.PROTECT, null=True, verbose_name="Должность")
    department = models.ForeignKey(CommandNumberModel, on_delete=models.PROTECT, null=True, verbose_name="№ отдела")
    user_phone = models.IntegerField("№ телефона внутренний", null=True, default=None, blank=True)
    department_group = models.ForeignKey(GroupDepartmentModel, on_delete=models.SET_NULL, default=None, null=True,
                                         verbose_name="Управление")
    right_to_sign = models.BooleanField(verbose_name="Право подписывать задания", default=False)
    check_edit = models.BooleanField("Возможность редактирования задания", default=True)
    can_make_task = models.BooleanField("Возможность выдавать задания", default=True)
    cpe_flag = models.BooleanField("Флаг ГИП (техническая метка)", default=False)
    mailing_list_check = models.BooleanField("Получать рассылку", default=True)
    work_status = models.BooleanField("Сотрудник работает", default=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    class Meta:
        managed = False
        verbose_name = _("сотрудник")
        verbose_name_plural = _("сотрудники")
        db_table = 'ToDo_tasks_employee'


def upload_to(instance, filename):
    name_to_path = str(instance.emp.id)
    new_path = path.join('files',
                         # "media", filename)
                         name_to_path,
                         filename)
    print(new_path)
    return new_path


class MoreDetailsEmployeeModel(models.Model):
    emp = models.OneToOneField(EmployeeModel, models.CASCADE, verbose_name="Пользователь")
    photo = models.ImageField(verbose_name="Файл", null=True, blank=True,
                              upload_to=upload_to)
    outside_email = models.EmailField(verbose_name="Внешняя почта", null=True, blank=True)
    mobile_phone = models.CharField(verbose_name="Мобильный телефон", null=True, blank=True, max_length=30)
    date_birthday = models.DateField(verbose_name="День рождения", null=True, blank=True)
    room = models.CharField(verbose_name="Номер комнаты", null=True, blank=True, max_length=30)
    date_birthday_show = models.BooleanField(verbose_name="Отображать день рождения", default=False, null=True)
    city_dep = models.ForeignKey(CityDepModel, on_delete=models.PROTECT, null=True, verbose_name="Город/Подразделение",
                                 blank=True)

    class Meta:
        managed = False
        verbose_name = _("дополнительная информация по сотруднику")
        verbose_name_plural = _("дополнительная информация по сотрудникам")
        db_table = 'admin_panel_app_moredetailsemployeemodel'

    def __str__(self):
        return f'{self.emp}'


# Таблицы проекта

class KksObjectModel(models.Model):
    """
    KKS объекта (1 сектор)
    """

    kks_object_abr = models.CharField(verbose_name="KKS код объекта сокращенно", max_length=4,
                                      validators=[MinLengthValidator(4)],
                                      help_text="Сектор 1")
    kks_object_full_name = models.CharField(verbose_name="KKS код объекта полностью", max_length=100)
    kks_object_show = models.BooleanField("Видимость в списках", default=True,
                                          help_text="Отображение в списках выбора, при генерации нового kks кода")

    class Meta:
        verbose_name = _("kks объекта")
        verbose_name_plural = _("kks объектов")

    def __str__(self):
        return f'{self.kks_object_abr} - {self.kks_object_full_name}'


class KksStageModel(models.Model):
    """
    KKS код этапа (стадии)
    """
    kks_stage_letter = models.CharField(verbose_name="Буквенное обозначение этапа (стадии)",
                                        help_text="Код этапа (стадии) жизненного цикла в соответствии с таблицаей А.1 приложения А (сектор 2)",
                                        max_length=1)
    kks_stage_description = models.CharField(verbose_name="Описание кода этапа (стадии)",
                                             max_length=35)

    class Meta:
        verbose_name = _("kks код этапа")
        verbose_name_plural = _("kks коды этапов")

    def __str__(self):
        return f'{self.kks_stage_letter} - {self.kks_stage_description}'


class KksStageObjectModel(models.Model):
    """
    KKS код этапа (стадии) (2 сектор)
    """
    kks_object = models.ForeignKey(KksObjectModel, on_delete=models.PROTECT, verbose_name='Объект', null=False,
                                   default=None)
    kks_stage = models.ForeignKey(KksStageModel, on_delete=models.PROTECT, verbose_name='Стадия', null=False,
                                  default=None)
    kks_stage_object_visible = models.BooleanField(verbose_name="Видимость", default=True)

    class Meta:
        verbose_name = _("этап у объекта")
        verbose_name_plural = _("этапы у объектов")

    def __str__(self):
        return f'{self.kks_object.kks_object_abr} | {self.kks_stage}'


class KksOrganizationCodeModel(models.Model):
    """
    KKS код организации (3 сектор)
    """
    kks_org_code = models.CharField(verbose_name="Код организации", max_length=3,
                                    validators=[MinLengthValidator(3)],
                                    help_text='3 символа')
    kks_org_description = models.CharField(verbose_name="Наименование организации", max_length=150)
    kks_org_visible = models.BooleanField(default=True, verbose_name='Видимость')

    class Meta:
        verbose_name = _("Kks код организации")
        verbose_name_plural = _("Kks коды организаций")

    def __str__(self):
        return f'{self.kks_org_code} - {self.kks_org_description}'


class KksOrganizationCodeObjectModel(models.Model):
    kks_object = models.ForeignKey(KksObjectModel, verbose_name="Объект", on_delete=models.PROTECT, null=False,
                                   default=None)
    kks_organization_code = models.ForeignKey(KksOrganizationCodeModel, verbose_name='Организация',
                                              on_delete=models.PROTECT, null=False, default=None)
    kks_organization_code_object_visible = models.BooleanField(default=True, verbose_name='Видимость')

    class Meta:
        verbose_name = _("организация относящаяся к объекту")
        verbose_name_plural = _("организации относящиеся к объектам")

    def __str__(self):
        return f'{self.kks_object} - {self.kks_organization_code}'


class KksTypeBuildingModel(models.Model):
    """
    KKS код типа здания (4 сектор)
    """
    kks_object = models.ForeignKey(KksObjectModel, verbose_name='Объект', on_delete=models.PROTECT, default=None,
                                   null=True)
    kks_type_building_code = models.CharField(verbose_name="Код KKS типа здания (сектора 4)",
                                              max_length=1)
    kks_type_building_description = models.CharField(verbose_name="Описание", max_length=150)

    class Meta:
        verbose_name = _("kks код типа здания")
        verbose_name_plural = _("kks коды типов зданий")

    def __str__(self):
        return f'{self.kks_object.kks_object_abr} | {self.kks_type_building_code}: {self.kks_type_building_description}'


class KksSector5Model(models.Model):
    """
    KKS код сектора 5
    """
    kks_sector5_value = models.CharField(verbose_name="Значение сектора 5", max_length=6,
                                         validators=[MinLengthValidator(6)],
                                         help_text="6 символов")

    class Meta:
        verbose_name = _("значение сектора 5")
        verbose_name_plural = _("значения сектора 5")

    def __str__(self):
        return f'{self.kks_sector5_value}'


class KksSector6Model(models.Model):
    """
    KKS код сектора 6
    """
    kks_sector6_value = models.CharField(verbose_name="Значение сектора 5", max_length=5,
                                         validators=[MinLengthValidator(5)],
                                         help_text="Максимум 5 символов")

    class Meta:
        verbose_name = _("значение сектора 6")
        verbose_name_plural = _("значения сектора 6")

    def __str__(self):
        return f'{self.kks_sector6_value}'


class KksTechnicalSpecialtyModel(models.Model):
    """
    KKS код сектор 7
    """
    kks_tech_speciality = models.CharField(verbose_name="Код технической специальности", max_length=3,
                                           validators=[MinLengthValidator(3)],
                                           help_text="3 цифр, согласно таблице В.1 приложения В, "
                                                     "за исключением конструкторской документации")
    kks_tech_speciality_description = models.CharField(verbose_name="Описание", max_length=250)
    kks_tech_speciality_show = models.BooleanField(verbose_name='Видимость', default=True)
    kks_tech_speciality_construction = models.BooleanField(verbose_name='Конструкторская документация', default=False)

    class Meta:
        verbose_name = _("kks код технической специальности")
        verbose_name_plural = _("kks коды технических специальностей (сектор 7)")

    def __str__(self):
        return f'{self.kks_tech_speciality} - {self.kks_tech_speciality_description}'


class KksTypeDocument(models.Model):
    """
    KKS код сектор 8
    """
    kks_type_doc = models.CharField(verbose_name="Код вида документа", max_length=2,
                                    validators=[MinLengthValidator(2)],
                                    help_text="2 буквы, согласно таблице Г.1 приложения Г")
    kks_type_doc_description = models.CharField(verbose_name="Описание", max_length=100)

    class Meta:
        verbose_name = _("kks код вида документа")
        verbose_name_plural = _("kks коды видов документов")

    def __str__(self):
        return f'{self.kks_type_doc} - {self.kks_type_doc_description}'


class KksBuildingModel(models.Model):
    """
    Здания, сектор 5.1
    """
    kks_object = models.ForeignKey(KksObjectModel, verbose_name="Объект", on_delete=models.PROTECT, default=None,
                                   null=False)
    kks_type_building = models.ForeignKey(KksTypeBuildingModel, verbose_name='Тип здания (сектор 4)',
                                          on_delete=models.PROTECT,
                                          default=None, null=True)
    kks_building_abr = models.CharField(verbose_name="Kks код здания", max_length=4, validators=[MinLengthValidator(4)])
    kks_building_description = models.CharField(verbose_name="Описание здания", max_length=150)
    kks_building_visible = models.BooleanField(verbose_name='Видимость', default=True)

    class Meta:
        verbose_name = _("kks код здания")
        verbose_name_plural = _("kks коды зданий")

    def __str__(self):
        return f'{self.kks_type_building.kks_object.kks_object_abr} | {self.kks_type_building.kks_type_building_code}.{self.kks_building_abr} | {self.kks_building_description}'


class KksHighMarkModel(models.Model):
    """
    Kks коды высотных отметок, сектор 5.2
    """
    kks_high_mark = models.CharField(verbose_name="Код высотной отметки", max_length=2,
                                     validators=[MinLengthValidator(2)],
                                     help_text='Код высотной отметки по таблице 4.12')
    kks_high_mark_description = models.CharField(verbose_name="Область высотны отметок", max_length=100)

    class Meta:
        verbose_name = _("kks код высотной отметки")
        verbose_name_plural = _("kks коды высотных отметок")

    def __str__(self):
        return f'{self.kks_high_mark}: {self.kks_high_mark_description}'


class KksCodeSystemModel(models.Model):
    """
    KKS код системы (сектор 6.1, рд)
    """
    kks_system_abr = models.CharField(verbose_name="Код системы",
                                      max_length=3,
                                      validators=[MinLengthValidator(3)],
                                      help_text='Обязательно 3 символа')
    kks_system_description = models.CharField(verbose_name="Описание", max_length=150)
    kks_system_visible = models.BooleanField(default=True, verbose_name="Видимость")

    class Meta:
        verbose_name = _("kks код системы")
        verbose_name_plural = _("kks коды систем")

    def __str__(self):
        return f'{self.kks_system_abr} - {self.kks_system_description}'


class KksCodeSystemOrganizationModel(models.Model):
    """
    Коды систем по объектам
    """
    kks_system = models.ForeignKey(KksCodeSystemModel, verbose_name="Код системы", on_delete=models.PROTECT,
                                   default=None,
                                   null=False)
    kks_object = models.ForeignKey(KksObjectModel, verbose_name="Объект", on_delete=models.PROTECT, null=False)
    kks_system_organization_visible = models.BooleanField(default=True, verbose_name="Видимость")

    class Meta:
        verbose_name = _('код системы у объекта')
        verbose_name_plural = _("коды систем у объектов")

    def __str__(self):
        return f'{self.kks_object} - {self.kks_system}'


class KksTypeConstructionModel(models.Model):
    """
    Kks коды типов конструкций (сектор 6.2)
    """
    kks_type_construction = models.IntegerField(verbose_name='Код типа конструкции',
                                                help_text="0-8",
                                                validators=[MaxValueValidator(8), MinValueValidator(0)])
    kks_type_construction_description = models.CharField(verbose_name='Описание типа конструкции', max_length=100)

    class Meta:
        verbose_name = _('kks код типа конструкции')
        verbose_name_plural = _("kks коды типов конструкций")

    def __str__(self):
        return f'{self.kks_type_construction} - {self.kks_type_construction_description}'


class KksExecutionConstructionModel(models.Model):
    """
    Kks коды исполнения конструкции (сектор 6.3)
    """
    kks_exec_construction = models.IntegerField(verbose_name='Код типа конструкции',
                                                help_text="0-5",
                                                validators=[MaxValueValidator(5), MinValueValidator(0)])
    kks_exec_construction_description = models.CharField(verbose_name='Описание типа конструкции', max_length=100)

    class Meta:
        verbose_name = _('kks код исполнения конструкции')
        verbose_name_plural = _("kks коды исполнения конструкций")

    def __str__(self):
        return f'{self.kks_exec_construction} - {self.kks_exec_construction_description}'


class KksCodeModel(models.Model):
    """
    Kks коды
    """

    class StatusKksChoice(models.IntegerChoices):
        """Статус кода Kks"""
        CANCELED = 0, _('Аннулирован')
        ACTUAL = 1, _('Актуален')

    object = models.ForeignKey(KksObjectModel, verbose_name='Объект', on_delete=models.PROTECT, null=False,
                               default=None)
    stage = models.ForeignKey(KksStageObjectModel, verbose_name='Стадия', on_delete=models.PROTECT, null=False,
                              default=None)
    organization = models.ForeignKey(KksOrganizationCodeObjectModel, verbose_name='Организация',
                                     on_delete=models.PROTECT, null=False, default=None)
    type_building = models.ForeignKey(KksTypeBuildingModel, verbose_name='Тип здания', on_delete=models.PROTECT,
                                      null=False, default=None)
    sector5 = models.ForeignKey(KksSector5Model, verbose_name='Сектор 5', on_delete=models.PROTECT, null=False,
                                default=None)
    sector6 = models.ForeignKey(KksSector6Model, verbose_name='Сектор 6', on_delete=models.PROTECT, null=False,
                                default=None)
    tech_speciality = models.ForeignKey(KksTechnicalSpecialtyModel, verbose_name='Код технической специальности',
                                        on_delete=models.PROTECT, null=False, default=None)
    type_doc = models.ForeignKey(KksTypeDocument, verbose_name='Код вида документа', on_delete=models.PROTECT,
                                 null=False, default=None)
    index_number = models.IntegerField(verbose_name="Порядковый номер")
    author = models.ForeignKey(EmployeeModel, verbose_name='Кто взял номер', on_delete=models.PROTECT, default=None,
                               null=True)
    status = models.IntegerField(verbose_name="Статус номера", choices=StatusKksChoice.choices, default=1)
    text = models.CharField(verbose_name='Kks код', max_length=37)
    add_date = models.DateTimeField('Дата создания', auto_now_add=True, null=True)

    class Meta:
        verbose_name = _('kks код')
        verbose_name_plural = _("kks коды")

    def __str__(self):
        return f'{self.text} ({self.add_date})'


class KksChangesHistoryModel(models.Model):
    """Лог изменений kks кодов"""
    kks_code = models.ForeignKey(KksCodeModel, verbose_name='Kks код', on_delete=models.CASCADE, null=True,
                                 default=None)
    change_date = models.DateTimeField(verbose_name='Дата изменения', auto_now_add=True, null=True)
    author_of_change = models.ForeignKey(EmployeeModel, verbose_name='Автор изменения', on_delete=models.CASCADE,
                                         null=True, default=None)
    previous_value = models.CharField(verbose_name='Старое значение', max_length=37)
    new_value = models.CharField(verbose_name='Старое значение', max_length=37)

    class Meta:
        verbose_name = _('история изменения')
        verbose_name_plural = _('история изменений')

    def __str__(self):
        return f'{self.previous_value} -> {self.new_value} ({self.change_date})'
