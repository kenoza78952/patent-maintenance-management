from django.contrib import admin
from .models import GptResult, CalculationResult

def delete_files(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()  

delete_files.short_description = "Delete selected files"

class GptResultAdmin(admin.ModelAdmin):
    list_display = ('filename', 'model_used', 'created_at')
    search_fields = ('filename', 'model_used', 'prompt')
    list_filter = ('model_used', 'created_at') 
    actions = [delete_files] 

class CalculationResultAdmin(admin.ModelAdmin):
    list_display = ('filename', 'created_at')
    search_fields = ('filename',)
    actions = [delete_files]  

admin.site.register(GptResult, GptResultAdmin)
admin.site.register(CalculationResult, CalculationResultAdmin)
