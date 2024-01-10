from django.db import models
from django.db.models import *
from datetime import datetime, date, timedelta, time
from django.db.models.functions import ExtractMonth, ExtractDay
from ckeditor.fields import RichTextField

class Shop(Model):
    name = TextField(null=True, blank=True)
    order = IntegerField(null=True, blank=True)
    def __str__(self): return self.name
    def items(self): return Shopping.objects.filter(shop=self).order_by("order")
    def visible(self):
        if len(self.items()) > 0: return True
        return False

class Shopping(Model):
    name = TextField(null=True, blank=True)
    shop = ForeignKey(Shop, null=True, blank=True, on_delete=SET_NULL)
    buy = BooleanField(null=True,)
    order = IntegerField(null=True, blank=True)
    def __str__(self): return self.name

class Event(Model):
    description = TextField(null=True, blank=True)
    date = DateField(auto_now=False, null=True)
    def __str__(self): return "[" + str(self.date) + "] " + self.description[0:50]

class Dog(Model):
    name = TextField(null=True, blank=True)
    owners = TextField(null=True, blank=True)
    notes = TextField(null=True, blank=True)
    image = ImageField(null=True, blank=True, upload_to="images/")
    def __str__(self):
        return self.name

    def bookings(self):
        bookings = Booking.objects.filter(dog=self).order_by('start_date')
        # print(self, bookings)
        return bookings

    def next_booking(self):
        today = date.today()
        bookings = Booking.objects.filter(dog=self).filter(start_date__gte=today).order_by('start_date')
        if bookings: return bookings[0].start_date
        return today + timedelta(days=360)


class Booking(Model):
    dog = ForeignKey(Dog, on_delete=CASCADE)
    start_date = DateField(null=True)
    end_date = DateField(null=True)

    def __str__(self):
        try:
            return f"{self.dog}: {self.start_date:%a, %d %b} to {self.end_date:%a, %d %b} {self.nights()}"
        except:
            return f"{self.start_date} to {self.end_date} {self.nights()}"

    def short_name(self):
        return f"{self.start_date:%a, %d %b} to {self.end_date:%a, %d %b} {self.nights()}"

    def description(self):
        return self.dog

    def date(self):
        return self.start_date

    def nights(self):
        try:
            nights = (self.end_date - self.start_date).days
            nights = f"({nights} nights)"
        except:
            nights = ""
        return nights



class Category(Model):
    name = TextField(null=True, blank=True)
    order = IntegerField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

class Diary(Model):
    text = RichTextField(null=True, blank=True)
    date = DateField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Diary Entries"

    def __str__(self): return "[" + str(self.date) + "] " + self.text[0:50]

class Note(Model):
    heading = TextField(null=True, blank=True)
    text = RichTextField(null=True, blank=True)
    category = ForeignKey(Category, null=True, blank=True, on_delete=SET_NULL)
    parent = ForeignKey('self', null=True, blank=True, on_delete=CASCADE)
    date = DateField(auto_now_add=True, null=True)
    order = IntegerField(null=True, blank=True)
    def __str__(self):
        if self.category:
            cat = f" ({self.category})"
        else:
            cat = ""
        if self.parent:
            chn = self.chain() + " "
        else:
            chn = ""

        return f"{chn}{self.heading}"

    def parent_text(self):
        if self.parent: return f"[{self.parent}]"
        return ""

    def chain(self):
        chain = str(self.order) + "."
        parent = self.parent
        while parent:
            if parent.order:
                chain = str(parent.order) + "." + chain
            parent = parent.parent
        return chain

    def next_child_number(self):
        return self.max_child_number() + 1

    def max_child_number(self):
        children = Note.objects.filter(parent=self).order_by("-order")
        if len(children) == 0: return 0
        if children[0].order: return children[0].order
        return 0

    def order_children(self):
        children = Note.objects.filter(parent=self).order_by("order")
        correction_made = False
        for count, child in enumerate(children, 1):
            if child.order != count:
                child.order = count
                child.save()
                correction_made = True
        if correction_made:
            children = Note.objects.filter(parent=self).order_by("order")
        return children

    def children(self):
        return Note.objects.filter(parent=self).order_by("order")

class Quote(Model):
    quote = TextField(null=True, blank=True)
    category = TextField(null=True, blank=True)
    date = DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.quote

class Birthday(Model):
    person = TextField(null=True, blank=True)
    date = DateField(auto_now=False, null=True)
    reminder_days = IntegerField(null=True, blank=True, default=7)
    tag = CharField(max_length=255, default="Birthday")

    def __str__(self):
        return self.person

    def next_age(self):
        today = datetime.today()
        year_adj = 0
        if self.date.month < today.month:
            year_adj = 1
        if self.date.month == today.month and self.date.day < today.day:
            year_adj = 1
        date = datetime(today.year + year_adj, self.date.month, self.date.day)
        days = (date - today).days + 1

        next_age = today.year + year_adj - self.date.year
        next_age_string = f"{self.person} will turn {next_age} years old in {days} days."
        # next_age_string = "XX"

        return next_age_string


    def next_age_days(self):
        today = datetime.today()
        year_adj = 0
        if self.date.month < today.month:
            year_adj = 1
        if self.date.month == today.month and self.date.day < today.day:
            year_adj = 1
        date = datetime(today.year + year_adj, self.date.month, self.date.day)
        days = (date - today).days + 1
        return days

    def next_one(self):
        return self.next_age_days() == min_days_to_birthday()

class TH(Model):
    level = IntegerField(null=True, blank=True)
    king_max = IntegerField(null=True, blank=True)
    queen_max = IntegerField(null=True, blank=True)
    warden_max = IntegerField(null=True, blank=True)
    champ_max = IntegerField(null=True, blank=True)
    def __str__(self):
        return f"TH {self.level}"
    def total(self):
        return self.king_max + self.queen_max + self.warden_max + self.champ_max

class Player(Model):
    name = TextField(null=True, blank=True)
    th = ForeignKey(TH, null=True, blank=True, on_delete=SET_NULL)
    order = IntegerField(null=True, blank=True)
    king = IntegerField(null=True, blank=True)
    queen = IntegerField(null=True, blank=True)
    warden = IntegerField(null=True, blank=True)
    champ = IntegerField(null=True, blank=True)

    def __str__(self): return f"{self.name} (Level {self.th})"
    def total(self): return self.king + self.queen + self.warden + self.champ
    def total_perc(self): return self.th.total() - (self.king + self.queen + self.warden + self.champ)
    def king_highlight(self): return self.th.king_max - self.king > 5
    def queen_highlight(self): return self.th.queen_max - self.queen > 5
    def warden_highlight(self): return self.th.warden_max - self.warden > 5
    def champ_highlight(self): return self.th.champ_max - self.champ > 5

class Timer(Model):
    name = TextField(null=True, blank=True)
    def __str__(self): return self.name
    # def elements(self): TimerElement.objects.all()
    def elements(self): return TimerElement.objects.filter(timer=self).order_by('order')
    def visible(self): return True

class TimerElement(Model):
    timer = ForeignKey(Timer, on_delete=CASCADE)
    name = TextField(null=True, blank=True)
    time = IntegerField(null=True, blank=True)
    order = IntegerField(null=True, blank=True)
    def __str__(self): return f"{self.timer}: {self.name} {self.time}"

    def short_name(self): return f"{self.name}: {self.time}sec"
    def start(self):
        earlier_elements = self.timer.elements().filter(order__lt=self.order)
        delay = 0
        for earlier_element in earlier_elements:
            delay += earlier_element.time
        return delay
    def end(self):
        earlier_elements = self.timer.elements().filter(order__lt=self.order)
        delay = 0
        for earlier_element in earlier_elements:
            delay += earlier_element.time
        return self.start() + self.time

class Tide_Date(Model):
    date = DateField(null=True)
    def __str__(self): return f"{self.date}"
    def tides(self): return New_Tide.objects.filter(date=self).filter(type="low").order_by("time")
    def max_temp(self): return MaxTemp.objects.filter(date=self.date).first()
    def weather(self): return Weather.objects.filter(date=self).order_by("time")
    def events(self): return Event.objects.filter(date=self.date)
    def birthdays(self): return Birthday.objects.filter(date__month=self.date.month).filter(date__day=self.date.day)
    def bookings(self): return Booking.objects.filter(start_date__lte=self.date).filter(end_date__gte=self.date).order_by('start_date')

class New_Tide(Model):
    date = ForeignKey(Tide_Date, on_delete=CASCADE)
#     date = DateField(null=True)
    time = TimeField(null=True)
    height = FloatField()
    type = CharField(max_length=10, null=True)
    def __str__(self): return f"{self.date} {self.time} {self.type}"

class Weather(Model):
    date = ForeignKey(Tide_Date, on_delete=CASCADE)
    time = TimeField(null=True)
    precis = CharField(max_length=30, null=True)
    def __str__(self): return f"{self.date} {self.time} {self.precis}"

class MaxTemp(Model):
    date = DateField(null=True)
    max = IntegerField(null=True)
    def __str__(self): return f"{self.date}: Max {self.max}"

def min_days_to_birthday():
    birthday_objects = Birthday.objects.all()
    minimum = 365
    for birthday in birthday_objects:
        days = birthday.next_age_days()
        if days < minimum:
            minimum = days
    return minimum

def get_birthday_reminders():
    text = ""
    objects = Birthday.objects.all().order_by(ExtractMonth('date'), ExtractDay('date'))
    for object in objects:
        # print(object, object.next_age_days(), object.reminder_days, object.next_age_days() == object.reminder_days)
        if object.next_age_days() == object.reminder_days:
            text += object.next_age() + ". "
        if object.next_age_days() == 0:
            text += f"It is {object.person}'s birthday today. "
    return text

all_models = [Category, Diary, Note, Quote, Birthday, Dog, Booking, Event, TH, Player, Shopping, Shop, Timer, TimerElement, New_Tide, Tide_Date, Weather]
