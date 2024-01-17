from django.contrib import admin
from .models import *

admin_models = all_models
admin_models.remove(Wordle)
admin_models.remove(Dog)

admin.site.register(admin_models)

class WordleAdmin(admin.ModelAdmin):
    list_filter = ('date', )
    ordering = ['-date',]
    search_fields = ['word',]

class DogAdmin(admin.ModelAdmin):
    ordering = ['name',]

admin.site.register(Wordle, WordleAdmin)
admin.site.register(Dog, DogAdmin)


