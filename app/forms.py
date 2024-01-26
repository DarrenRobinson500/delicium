from django.forms import *
from .models import *
from ckeditor.widgets import CKEditorWidget

class ShoppingForm(ModelForm):
    class Meta:
        model = Shopping
        fields = ['name', "shop", ]
        widgets = {
            'name': TextInput(attrs={'class':'form-control', 'placeholder': "Item"}),
            'shop': Select(attrs={'class': 'form-control'}),
        }

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['description', 'date',]

class DogForm(ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'owners', 'owners_link', 'notes', 'image', "approved"]
        widgets = {
            'owners_link': Select(attrs={'class': 'form-control'}),
            'approved': Select(attrs={'class': 'form-control'}),
        }

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', ]

class DiaryForm(ModelForm):
    class Meta:
        model = Diary
        fields = ['text', ]
        labels = {'text': "",}

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['heading', 'text', 'category', 'note_date']
        labels = {
            'heading': "",
            'text': "",
            'category': "",
        }
        widgets = {
            'heading': TextInput(attrs={'class':'form-control', 'placeholder': "Heading"}),
            'category': Select(attrs={'class': 'form-control'}),
            'note_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['note_date'].required = False

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'category', ]

class BirthdayForm(ModelForm):
    class Meta:
        model = Birthday
        fields = ['person', 'date', ]

