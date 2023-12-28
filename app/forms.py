from django.forms import *
from .models import *

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', ]

class DiaryForm(ModelForm):
    class Meta:
        model = Diary
        fields = ['text', ]

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['text', 'parent', 'category']

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'category', ]

class BirthdayForm(ModelForm):
    class Meta:
        model = Birthday
        fields = ['person', 'date', ]

