from django.forms import *
from .models import *
# from ckeditor.widgets import CKEditorWidget
from django_ckeditor_5.widgets import CKEditor5Widget

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
        fields = ['name', 'owners', 'owners_link', "owners_number", 'notes', 'image', "approved"]
        widgets = {
            'owners_link': Select(attrs={'class': 'form-control'}),
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="comment"
            ),
            'name': TextInput(attrs={'class':'form-control', 'placeholder': "Name"}),
            'owners': TextInput(attrs={'class':'form-control', 'placeholder': "Owners"}),
            'owners_number': TextInput(attrs={'class':'form-control', 'placeholder': "Mobile"}),
            'approved': Select(attrs={'class': 'form-control'}),
            "image": FileInput(attrs={"class": "form-control", "placeholder": ""}),
        }

class TennisForm(ModelForm):
    class Meta:
        model = TennisMatch
        fields = ['player_A', 'player_B']
        widgets = {
            'player_A': TextInput(attrs={'class': 'form-control', 'placeholder': "Name"}),
            'player_B': TextInput(attrs={'class': 'form-control', 'placeholder': "Name"}),
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
        fields = ['heading', 'text', 'category', 'note_date', 'frequency']
        labels = {
            'heading': "",
            'text': "",
            'category': "",
            'frequency': "",
        }
        widgets = {
            'heading': TextInput(attrs={'class':'form-control', 'placeholder': "Heading"}),
            'category': Select(attrs={'class': 'form-control'}),
            'note_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'frequency': Select(attrs={'class': 'form-control'}),
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

