import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class CalculationResult(models.Model):
    filename = models.CharField(max_length=255)
    custom_name = models.CharField(max_length=255, blank=True, null=True) 
    file_path = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 

    def delete_file(self):
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
            print(f"Deleted file: {self.file_path}")

    def delete(self, *args, **kwargs):
        self.delete_file() 
        super().delete(*args, **kwargs)


class GptResult(models.Model):
    filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=1024)
    prompt = models.TextField()
    model_used = models.CharField(max_length=255, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    
    def __str__(self):
        return self.filename

    def delete_file(self):
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
            print(f"Deleted file: {self.file_path}")

    def delete(self, *args, **kwargs):
        self.delete_file() 
        super().delete(*args, **kwargs)
