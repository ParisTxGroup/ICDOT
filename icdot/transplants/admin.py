# coding: utf-8

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from nonrelated_inlines.admin import NonrelatedStackedInline

from icdot.transplants import fieldsets, forms, models, resources

admin.site.site_title = "ICDOT"
admin.site.site_header = "ICDOT"


@admin.register(models.Transplant)
class TransplantAdmin(ImportExportModelAdmin):
    resource_class = resources.TransplantResource
    fieldsets = fieldsets.transplant.DEFAULT


@admin.register(models.Biopsy)
class BiopsyAdmin(ImportExportModelAdmin):
    resource_class = resources.BiopsyResource
    fieldsets = fieldsets.biopsy.DEFAULT


@admin.register(models.Histology)
class HistologyAdmin(ImportExportModelAdmin):
    resource_class = resources.HistologyResource
    fieldsets = fieldsets.histology.DEFAULT


@admin.register(models.FileUpload)
class FileUploadAdmin(ImportExportModelAdmin):
    pass


class FileUploadInline(admin.TabularInline):
    model = models.FileUpload
    max_num = 0


@admin.register(models.FileUploadBatch)
class FileUploadBatchAdmin(admin.ModelAdmin):
    form = forms.FileUploadBatchAdminForm
    inlines = [FileUploadInline]

    def save_related(self, request, form, formsets, change):
        # From https://web.archive.org/web/20220107040356/
        # https://xn--w5d.cc/2019/09/18/minimalistic-multiupload-in-django-admin.html
        # ModelAdmin handles saving the object separately and only
        # calls form’s save() method with commit=False.
        # We must call the save_files method manually.
        super().save_related(request, form, formsets, change)
        form.save_files(form.instance)


class StackedFileUploadInline(NonrelatedStackedInline):
    model = models.FileUpload
    exclude = ("batch", "file_ref")
    max_num = 1
    formset = forms.FileUploadInlineFormSet

    def get_form_queryset(self, obj):
        # We want this to act like a "quick upload form".
        # We do not attempt to manage the referenced file (eg: editing.)
        # That is why we always return an empty queryset.
        return self.model.objects.none()

    def save_new_instance(self, parent, instance):
        instance.file_ref = parent.file_ref


@admin.register(models.SequencingData)
class SequencingDataAdmin(ImportExportModelAdmin):
    resource_class = resources.SequencingDataResource
    readonly_fields = ("file_path",)
    inlines = [StackedFileUploadInline]
