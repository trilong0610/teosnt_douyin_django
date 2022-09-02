from django.contrib import admin
from django.db import models


class CodeModel(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True)
    time_out = models.DateTimeField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.code)


admin.site.register(CodeModel)