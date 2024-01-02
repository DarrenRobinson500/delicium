from django.forms import *
from .models import *

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['description', 'date',]

class DogForm(ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'owners', 'notes', 'image']

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

