from django.db import models
from django.db.models import *
from datetime import datetime
from django.db.models.functions import ExtractMonth, ExtractDay


class Category(Model):
    name = TextField(null=True, blank=True)
    def __str__(self):
        return self.name

class Diary(Model):
    text = TextField(null=True, blank=True)
    date = DateField(auto_now_add=True, null=True)
    def __str__(self): return str(self.date)

class Note(Model):
    text = TextField(null=True, blank=True)
    category = ForeignKey(Category, null=True, blank=True, on_delete=SET_NULL)
    parent = ForeignKey('self', null=True, blank=True, on_delete=CASCADE)
    date = DateField(auto_now_add=True, null=True)
    order = IntegerField(null=True, blank=True)
    def __str__(self):
        if self.category:
            cat = f"({self.category})"
        else:
            cat = "(No category)"
        if self.parent:
            chn = self.chain()
        else:
            chn = ""

        return f"{chn} {self.text} {cat}"

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



class Quote(Model):
    quote = TextField(null=True, blank=True)
    category = TextField(null=True, blank=True)

    def __str__(self):
        return self.quote

class Birthday(Model):
    person = TextField(null=True, blank=True)
    date = DateField(auto_now=False, null=True)
    reminder_days = IntegerField(null=True, blank=True, default=7)

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


all_models = [Category, Diary, Note, Quote, Birthday]


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

