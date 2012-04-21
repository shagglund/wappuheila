from django.contrib import admin
from wappuheila.wappuheila import models

admin.site.register(models.Wappuheila)
admin.site.register(models.Question)
admin.site.register(models.QuestionOption)
admin.site.register(models.Answer)
admin.site.register(models.Message)