from django.contrib import admin
from kks_reestr_app.models import EmployeeModel, MoreDetailsEmployeeModel, KksCodeModel, KksSector6Model, \
    KksTechnicalSpecialtyModel, KksOrganizationCodeObjectModel, KksTypeBuildingModel, KksTypeDocument, KksSector5Model, \
    KksStageObjectModel, KksCodeSystemModel, KksObjectModel, KksOrganizationCodeModel, KksStageModel, KksBuildingModel, \
    KksHighMarkModel, KksChangesHistoryModel, KksTypeConstructionModel, KksExecutionConstructionModel, \
    KksCodeSystemOrganizationModel, KKSThematicDirectionModel


class EmployeeAdmin(admin.ModelAdmin):
    # list_display = ("author", "text_task")
    ordering = ["last_name", "first_name", "middle_name"]
    search_fields = ["last_name", "first_name", "middle_name", "personnel_number", "user_phone"]
    list_filter = ("department_group__city_dep__city", "department_group__group_dep_abr", "department__command_number")


class MoreDetailsEmployeeAdmin(admin.ModelAdmin):
    ordering = ["emp__last_name", "emp__first_name", "emp__middle_name"]
    search_fields = ["emp__last_name", "emp__first_name", "emp__middle_name"]
    list_filter = (
        "emp__department_group__city_dep__city", "emp__department_group__group_dep_abr",
        "emp__department__command_number")


class KksHighMarkAdmin(admin.ModelAdmin):
    ordering = ['kks_high_mark']
    search_fields = ['kks_high_mark', 'kks_high_mark_description']


class KksTypeDocumentAdmin(admin.ModelAdmin):
    ordering = ['kks_type_doc']
    search_fields = ['kks_type_doc', 'kks_type_doc_description']


class KksBuildingAdmin(admin.ModelAdmin):
    ordering = ['kks_object__kks_object_abr', 'kks_building_abr']
    search_fields = ['kks_object__kks_object_abr', 'kks_building_abr', 'kks_building_description']
    list_filter = ('kks_object__kks_object_abr', 'kks_type_building__kks_type_building_code')


class KksExecutionConstructionAdmin(admin.ModelAdmin):
    ordering = ['kks_exec_construction']


class KksOrganizationCodeAdmin(admin.ModelAdmin):
    ordering = ['kks_org_code']
    search_fields = ['kks_org_code', 'kks_org_description']


class KksCodeSystemOrganizationAdmin(admin.ModelAdmin):
    ordering = ['kks_object__kks_object_abr']
    search_fields = ['kks_object__kks_object_abr', 'kks_system__kks_system_abr']
    list_filter = ('kks_object__kks_object_abr',)


class KksTechnicalSpecialtyAdmin(admin.ModelAdmin):
    ordering = ['kks_tech_speciality']
    search_fields = ['kks_tech_speciality', 'kks_tech_speciality_description']


class KksTypeBuildingAdmin(admin.ModelAdmin):
    ordering = ['kks_object__kks_object_abr', 'kks_type_building_code']
    list_filter = ('kks_object__kks_object_abr',)


class KksOrganizationCodeObjectAdmin(admin.ModelAdmin):
    ordering = ['kks_object__kks_object_abr', 'kks_organization_code__kks_org_code']
    search_fields = ['kks_object__kks_object_abr', 'kks_organization_code__kks_org_code']
    list_filter = ('kks_object__kks_object_abr',)


class KksSector5Admin(admin.ModelAdmin):
    search_fields = ['kks_sector5_value']


class KksSector6Admin(admin.ModelAdmin):
    search_fields = ['kks_sector6_value']


class KksStageAdmin(admin.ModelAdmin):
    ordering = ['kks_stage_letter']


class KksStageObjectAdmin(admin.ModelAdmin):
    ordering = ['kks_object__kks_object_abr', 'kks_stage__kks_stage_letter']
    search_fields = ['kks_object__kks_object_abr', 'kks_stage__kks_stage_letter']
    list_filter = ('kks_object__kks_object_abr',)


class KksCodeSystemAdmin(admin.ModelAdmin):
    ordering = ['kks_system_abr', 'kks_system_description']
    search_fields = ['kks_system_abr', 'kks_system_description']


class KksTypeConstructionAdmin(admin.ModelAdmin):
    ordering = ['kks_type_construction']
    search_fields = ['kks_type_construction', 'kks_type_construction_description']


class KksChangesHistoryAdmin(admin.ModelAdmin):
    search_fields = ['kks_code__text', 'previous_value', 'author_of_change__user__username', 'author_of_change__lastname',
                     'author_of_change__first_name', 'author_of_change__middle_name']
    list_filter = ('kks_code__object__kks_object_abr', )


class KksCodeAdmin(admin.ModelAdmin):
    search_fields = ['object__kks_object_abr', 'object__kks_object_kks_object_full_name',
                     ]
    list_filter = ('object__kks_object_abr', 'organization__kks_organization_code__kks_org_code')

class KKSThematicDirectionAdmin(admin.ModelAdmin):
    search_fields = ['kks_thematic_direction_abr', 'kks_thematic_direction_description']
    ordering = ['kks_thematic_direction_abr']



# admin.site.register(EmployeeModel, EmployeeAdmin)
# admin.site.register(EmployeeModel)
# admin.site.register(MoreDetailsEmployeeModel, MoreDetailsEmployeeAdmin)
# admin.site.register(KksCodeSystemOrganizationModel, KksCodeSystemOrganizationAdmin)
admin.site.register(KksExecutionConstructionModel, KksExecutionConstructionAdmin)
admin.site.register(KksCodeModel, KksCodeAdmin)
admin.site.register(KksSector5Model, KksSector5Admin)
admin.site.register(KksSector6Model, KksSector6Admin)
admin.site.register(KksTechnicalSpecialtyModel, KksTechnicalSpecialtyAdmin)
admin.site.register(KksOrganizationCodeModel, KksOrganizationCodeAdmin)
admin.site.register(KksOrganizationCodeObjectModel, KksOrganizationCodeObjectAdmin)
admin.site.register(KksTypeBuildingModel, KksTypeBuildingAdmin)
admin.site.register(KksTypeDocument, KksTypeDocumentAdmin)
admin.site.register(KksStageObjectModel, KksStageObjectAdmin)
admin.site.register(KksCodeSystemModel, KksCodeSystemAdmin)
admin.site.register(KksObjectModel)
admin.site.register(KksStageModel, KksStageAdmin)
admin.site.register(KksBuildingModel, KksBuildingAdmin)
admin.site.register(KksHighMarkModel, KksHighMarkAdmin)
admin.site.register(KksChangesHistoryModel, KksChangesHistoryAdmin)
admin.site.register(KksTypeConstructionModel, KksTypeConstructionAdmin)
admin.site.register(KKSThematicDirectionModel, KKSThematicDirectionAdmin)
admin.site.register(EmployeeModel, EmployeeAdmin)

# admin.site.register(MoreDetailsEmployeeModel)
# admin.site.register(GroupDepartmentModel, GroupDepartmentAdmin)
# admin.site.register(GroupDepartmentModel)
# admin.site.register(CityDepModel)
# admin.site.register(CommandNumberModel, CommandNumberAdmin)
# admin.site.register(CommandNumberModel)
# admin.site.register(JobTitleModel, JobTitleAdmin)
# admin.site.register(JobTitleModel)


# Register your models here.
