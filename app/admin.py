from django.contrib import admin
from django.db.models.functions import Lower
from .models import *

admin_models = all_models
admin_models.remove(Wordle)
admin_models.remove(Dog)
admin_models.remove(Note)

admin.site.register(admin_models)

class NoteAdmin(admin.ModelAdmin):
    ordering = ['heading',]
    search_fields = ['heading',]

class WordleAdmin(admin.ModelAdmin):
    list_filter = ('date', )
    ordering = ['-date',]
    search_fields = ['word',]

class DogAdmin(admin.ModelAdmin):
    ordering = ['name',]

admin.site.register(Wordle, WordleAdmin)
admin.site.register(Dog, DogAdmin)
admin.site.register(Note, NoteAdmin)


