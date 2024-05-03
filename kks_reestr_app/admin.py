from django.contrib import admin
from kks_reestr_app.models import EmployeeModel, MoreDetailsEmployeeModel, KksCodeModel, KksSector6Model, \
    KksTechnicalSpecialtyModel, KksOrganizationCodeObjectModel, KksTypeBuildingModel, KksTypeDocument, KksSector5Model, \
    KksStageObjectModel, KksCodeSystemModel, KksObjectModel, KksOrganizationCodeModel, KksStageModel, KksBuildingModel, \
    KksHighMarkModel, KksChangesHistoryModel, KksTypeConstructionModel, KksExecutionConstructionModel, \
    KksCodeSystemOrganizationModel


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

# admin.site.register(EmployeeModel, EmployeeAdmin)
# admin.site.register(EmployeeModel)
# admin.site.register(MoreDetailsEmployeeModel, MoreDetailsEmployeeAdmin)
admin.site.register(KksCodeSystemOrganizationModel)
admin.site.register(KksExecutionConstructionModel)
admin.site.register(KksCodeModel)
admin.site.register(KksSector5Model)
admin.site.register(KksSector6Model)
admin.site.register(KksTechnicalSpecialtyModel)
admin.site.register(KksOrganizationCodeModel)
admin.site.register(KksOrganizationCodeObjectModel)
admin.site.register(KksTypeBuildingModel)
admin.site.register(KksTypeDocument)
admin.site.register(KksStageObjectModel)
admin.site.register(KksCodeSystemModel)
admin.site.register(KksObjectModel)
admin.site.register(KksStageModel)
admin.site.register(KksBuildingModel)
admin.site.register(KksHighMarkModel, KksHighMarkAdmin)
admin.site.register(KksChangesHistoryModel)
admin.site.register(KksTypeConstructionModel)



# admin.site.register(MoreDetailsEmployeeModel)
# admin.site.register(GroupDepartmentModel, GroupDepartmentAdmin)
# admin.site.register(GroupDepartmentModel)
# admin.site.register(CityDepModel)
# admin.site.register(CommandNumberModel, CommandNumberAdmin)
# admin.site.register(CommandNumberModel)
# admin.site.register(JobTitleModel, JobTitleAdmin)
# admin.site.register(JobTitleModel)


# Register your models here.
