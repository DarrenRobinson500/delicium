import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.db.models import *
from datetime import datetime, date, timedelta, time
from django.db.models.functions import ExtractMonth, ExtractDay
# from ckeditor.fields import RichTextField
from django_ckeditor_5.fields import CKEditor5Field
from collections import namedtuple
from .prob import *


class CustomStorage(FileSystemStorage):
    """Custom storage for django_ckeditor_5 images."""
    location = os.path.join(settings.MEDIA_ROOT, "django_ckeditor_5")
    base_url = urljoin(settings.MEDIA_URL, "django_ckeditor_5/")

class General(Model):
    string_name = "General"
    name = CharField(max_length=30, default="main")
    dog_diary_days = IntegerField(default=200)
    wordles_to_do = IntegerField(default=3)
    def __str__(self): return self.name

class Shop(Model):
    string_name = "Shop"
    name = TextField(null=True, blank=True)
    order = IntegerField(null=True, blank=True)
    def __str__(self): return self.name
    def items(self): return Shopping.objects.filter(shop=self).order_by("order")
    def visible(self):
        if len(self.items()) > 0: return True
        return False

    def max_child_number(self):
        children = Shopping.objects.filter(shop=self).order_by("-order")
        if len(children) == 0: return 0
        if children[0].order: return children[0].order
        return 0
    def next_child_number(self): return self.max_child_number() + 1
    def order_children(self):
        children = Shopping.objects.filter(shop=self).order_by("order")
        correction_made = False
        for count, child in enumerate(children, 1):
            if child.order != count:
                child.order = count
                child.save()
                correction_made = True
        if correction_made:
            children = Note.objects.filter(shop=self).order_by("order")
        return children


class Shopping(Model):
    string_name = "Shopping"
    name = TextField(null=True, blank=True)
    shop = ForeignKey(Shop, null=True, blank=True, on_delete=SET_NULL)
    buy = BooleanField(null=True,)
    order = IntegerField(null=True, blank=True)
    last_edited = DateField(auto_now=True)
    def __str__(self): return self.name
    def age(self): return (date.today() - self.last_edited).days
    def show(self): return self.age() < 45

class Event(Model):
    string_name = "Event"
    description = TextField(null=True, blank=True)
    date = DateField(auto_now=False, null=True)
    def __str__(self): return "[" + str(self.date) + "] " + self.description[0:50]

class Category(Model):
    string_name = "Category"
    name = TextField(null=True, blank=True)
    order = IntegerField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Not named yet"

class Diary(Model):
    string_name = "Diary"
    # text = RichTextField(null=True, blank=True)
    text = CKEditor5Field('Text', null=True, blank=True)
    # text = CKEditor5Field('Text', config_name='extends', null=True)
    date = DateField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Diary Entries"

    def __str__(self): return "[" + str(self.date) + "] " + self.text[0:50]

class Note(Model):
    choices = [("Weekly", "Weekly"), ("Fortnightly", "Fortnightly"), ("Monthly", "Monthly"), ]
    string_name = "Note"
    heading = TextField(null=True, blank=True)
    # text = RichTextField(null=True, blank=True)
    text = CKEditor5Field('Text', null=True, blank=True)
    # text = CKEditor5Field('Text', config_name='extends', null=True)
    category = ForeignKey(Category, null=True, blank=True, on_delete=SET_NULL)
    parent = ForeignKey('self', null=True, blank=True, on_delete=CASCADE)
    create_date = DateField(auto_now_add=True, null=True, blank=True)
    frequency = CharField(null=True, blank=True, choices=choices)
    note_date = DateField(null=True, blank=False)
    order = IntegerField(null=True, blank=True)
    def __str__(self):
        if self.parent:
            chn = self.chain() + " "
        else:
            chn = ""
        return f"{chn}{self.heading}"

    def parent_text(self):
        if self.parent: return f"[{self.parent}]"
        return ""

    def update_date(self):
        print("Update_date:", self, self.frequency)
        if not self.frequency: return
        today = date.today()
        print("Today:", today)
        if self.frequency == "Weekly": freq = timedelta(days=7)
        if self.frequency == "Fortnightly": freq = timedelta(days=14)
        if self.frequency == "Monthly": freq = timedelta(months=1)
        print("Update_date", self, freq, self.note_date, today, self.note_date < today)
        while self.note_date < today:
            self.note_date += freq
            print("Updating date", self, self.note_date)
        self.save()

    def parents(self):
        result = []
        if self.parent:
            result = self.parent.parents()
        result.append(self)
        return result

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

def people():
    people_category = Category.objects.filter(name="People").first()
    return Note.objects.filter(category=people_category)

class Dog(Model):
    string_name = "Dog"
    name = TextField(null=True, blank=True)
    owners = TextField(null=True, blank=True)
    owners_number = TextField(null=True, blank=True)
    # notes = RichTextField(null=True, blank=True)
    notes = CKEditor5Field('Text', null=True, blank=True)
    # notes = CKEditor5Field('Text', config_name='extends', null=True)

    approved = CharField(default="Yes", choices=[("Yes", "Yes"), ("No", "No"), ("Limited", "Limited")])
    image = ImageField(null=True, blank=True, upload_to="images/")
    owners_link = ForeignKey(Note, null=True, on_delete=SET_NULL, blank=True)
    def __str__(self):
        if self.name:
            return self.name
        return f"No name for this dog: {self.id}"

    def bookings(self):
        bookings = Booking.objects.filter(dog=self).order_by('start_date')
        # print(self, bookings)
        return bookings

    def nights(self):
        total = 0
        for booking in self.bookings():
            total += booking.nights_int()
        return total


    def next_booking(self):
        today = date.today()
        bookings = Booking.objects.filter(dog=self).filter(start_date__gte=today).order_by('start_date')
        if bookings: return bookings[0].start_date
        return today + timedelta(days=360)

    def mobile(self):
        if not self.owners_number: return None
        return "+61" + self.owners_number[1:]


class Booking(Model):
    string_name = "Booking"
    dog = ForeignKey(Dog, on_delete=CASCADE, null=True)
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

    def in_future(self):
        return self.end_date >= date.today()

    def nights_int(self):
        return (self.end_date - self.start_date).days

    def nights(self):
        try:
            nights = (self.end_date - self.start_date).days
            nights = f"({nights} nights)"
        except:
            nights = ""
        return nights

class Quote(Model):
    string_name = "Quote"
    quote = TextField(null=True, blank=True)
    category = TextField(null=True, blank=True)
    date = DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.quote

class Birthday(Model):
    string_name = "Birthday"
    person = TextField(null=True, blank=True)
    date = DateField(auto_now=False, null=True)
    reminder_days = IntegerField(null=True, blank=True, default=7)
    tag = CharField(max_length=255, default="Birthday")

    def __str__(self):
        return f"{self.person}({self.id})"

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
        next_age_string = ""
        if self.tag == "Birthday":
            next_age_string = f"{self.person} will turn {next_age} years old in {days} days."
        if self.tag == "Anniversary":
            next_age_string = f"It is the {next_age}th {self.person} anniversary in {days} days."
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
    string_name = "TH"
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
    string_name = "Player"
    name = TextField(null=True, blank=True)
    th = ForeignKey(TH, null=True, blank=True, on_delete=SET_NULL)
    order = IntegerField(null=True, blank=True)
    king = IntegerField(null=True, blank=True)
    queen = IntegerField(null=True, blank=True)
    warden = IntegerField(null=True, blank=True)
    champ = IntegerField(null=True, blank=True)

    def __str__(self): return f"{self.name} (Level {self.th})"
    def total(self): return self.king + self.queen + self.warden + self.champ
    def total_remaining(self): return self.th.total() - (self.king + self.queen + self.warden + self.champ)
    def king_colour(self): return colour(self.king, self.th.king_max)
    def queen_colour(self): return colour(self.queen, self.th.queen_max)
    def warden_colour(self): return colour(self.warden, self.th.warden_max)
    def champ_colour(self): return colour(self.champ, self.th.champ_max)

def colour(value, max):
    if max - value > 5: return "#ffc0cb"
    if max == value: return "#acdf87"
    return "white"

class Timer(Model):
    string_name = "Timer"
    name = TextField(null=True, blank=True)
    def __str__(self): return self.name
    # def elements(self): TimerElement.objects.all()
    def elements(self): return TimerElement.objects.filter(timer=self).order_by('order')
    def visible(self): return True

class TimerElement(Model):
    string_name = "TimerElement"
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
    string_name = "Tide_Date"
    date = DateField(null=True)
    def __str__(self): return f"{self.date}"
    def tides(self): return New_Tide.objects.filter(date=self).filter(type="low").order_by("time")
    def max_temp(self): return MaxTemp.objects.filter(date=self.date).first()
    def notes(self):
        result = Note.objects.filter(note_date=self.date)
        print(result)
        return result
    def weather(self): return Weather.objects.filter(date=self).order_by("time")
    def events(self): return Event.objects.filter(date=self.date)
    def birthdays(self): return Birthday.objects.filter(date__month=self.date.month).filter(date__day=self.date.day)
    def bookings(self): return Booking.objects.filter(start_date__lte=self.date).filter(end_date__gte=self.date).order_by('start_date')

class New_Tide(Model):
    string_name = "New_Tide"
    date = ForeignKey(Tide_Date, on_delete=CASCADE)
#     date = DateField(null=True)
    time = TimeField(null=True)
    height = FloatField()
    type = CharField(max_length=10, null=True)
    def __str__(self): return f"{self.date} {self.time} {self.type}"

class Weather(Model):
    string_name = "Weather"
    date = ForeignKey(Tide_Date, on_delete=CASCADE)
    time = TimeField(null=True)
    precis = CharField(max_length=30, null=True)
    def __str__(self): return f"{self.date} {self.time} {self.precis}"

class MaxTemp(Model):
    string_name = "MaxTemp"
    date = DateField(null=True)
    max = IntegerField(null=True)
    def __str__(self): return f"{self.date}: Max {self.max}"

class Wordle(Model):
    string_name = "Wordle"
    word = CharField(max_length=5, null=True)
    guess_1 = CharField(max_length=5, null=True, blank=True)
    guess_2 = CharField(max_length=5, null=True, blank=True)
    guess_3 = CharField(max_length=5, null=True, blank=True)
    guess_4 = CharField(max_length=5, null=True, blank=True)
    guess_5 = CharField(max_length=5, null=True, blank=True)
    guess_6 = CharField(max_length=5, null=True, blank=True)
    date = DateField(null=True, blank=False)
    last_reviewed = DateField(null=True, blank=False, default=None)
    score = IntegerField(null=True, blank=True)
    attempts = IntegerField(null=True, blank=True)
    def __str__(self):
        if not self.word: return "No word"
        if self.date:
            return f"{self.word} ({self.date})"
        else:
            return self.word
    def upper(self): return self.word.upper()
    def save_guess(self, guess, count):
        if guess is None: return
        guess_str = guess.word[0:5]
        if count == 1:
            self.guess_1 = guess_str
            self.guess_2 = None
            self.guess_3 = None
            self.guess_4 = None
            self.guess_5 = None
            self.guess_6 = None
        if count == 2: self.guess_2 = guess_str
        if count == 3: self.guess_3 = guess_str
        if count == 4: self.guess_4 = guess_str
        if count == 5: self.guess_5 = guess_str
        if count == 6: self.guess_6 = guess_str
        self.save()
    def colour(self):
        todays_word = Wordle.objects.filter(date__isnull=False).order_by('-date')[0]
        # print(todays_word)
        # if todays_word:
        #     print(self.word)
        #     print(todays_word.word)
        #     print(self.guess_1)
        if todays_word.word in [self.guess_1, self.guess_2, self.guess_3, self.guess_4, self.guess_5]:
            return "red"
        else:
            return "blue"

Score_Tuple = namedtuple('Score_Tuple', ["points_A", "points_A_serv", "points_A_rec", "percent_A", "game_prob_A", "points_B", "points_B_serv", "points_B_rec", "percent_B", "game_prob_B"])

class TennisMatch(Model):
    string_name = "TennisMatch"
    # player_A = ForeignKey(TennisPlayer, null=True, blank=True, on_delete=CASCADE, related_name="player_A")
    # player_B = ForeignKey(TennisPlayer, null=True, blank=True, on_delete=CASCADE, related_name="player_B")
    player_A = CharField(max_length=30, null=True)
    player_B = CharField(max_length=30, null=True)
    score_A = IntegerField(null=True, blank=True, default=0)
    score_B = IntegerField(null=True, blank=True, default=0)

    match_date = DateField(auto_now_add=True, null=True, blank=False)
    name = CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.player_A} v {self.player_B} {self.match_date}"

    def play_A(self): return self.player_A[0:3]
    def play_B(self): return self.player_B[0:3]

    def game_score(self):
        if self.score_A == 3 and self.score_B == 3: return "Deuce"
        scores = [0, 15, 30, 40, "Ad"]
        return f"{scores[min(self.score_A, 4)]} - {scores[min(self.score_B, 4)]}"

    # def points(self):
    #     sets = TennisSet.objects.filter(match=self)
    #     points_A, points_B = self.score_A, self.score_B
    #     for set in sets:
    #         a, b = set.points()
    #         points_A += a
    #         points_B += b
    #     return points_A, points_B

    def points(self):
        sets = TennisSet.objects.filter(match=self)
        print("Server:", self.server())
        if self.server() == 1:
            points_A_serv, points_A_rec, points_B_serv, points_B_rec = self.score_A, 0, 0, self.score_B
        else:
            points_A_serv, points_A_rec, points_B_serv, points_B_rec = 0, self.score_A, self.score_B, 0

        for set in sets:
            for game in set.games():
                if game.game_no % 2 == 1:
                    points_A_serv += game.score_A
                    points_B_rec += game.score_B
                else:
                    points_A_rec += game.score_A
                    points_B_serv += game.score_B
        if points_A_serv + points_B_rec > 0: percent_A = round(points_A_serv / (points_A_serv + points_B_rec), 2)
        else: percent_A = 0
        if points_B_serv + points_A_rec > 0: percent_B = round(points_B_serv / (points_B_serv + points_A_rec), 2)
        else: percent_B = 0

        if self.server() == 1:
            game_prob_A = game_prob(self.score_A, self.score_B, percent_A)
            game_prob_B = 0
        else:
            game_prob_A = 0
            game_prob_B = game_prob(self.score_B, self.score_A, percent_B)

        score = Score_Tuple(
            points_A=points_A_serv + points_A_rec,
            points_A_serv=points_A_serv,
            points_A_rec=points_A_rec,
            percent_A=int(percent_A * 100),
            game_prob_A=int(game_prob_A * 100),
            points_B=points_B_serv + points_B_rec,
            points_B_serv=points_B_serv,
            points_B_rec=points_B_rec,
            percent_B=int(percent_B * 100),
            game_prob_B=int(game_prob_B * 100),
        )

        print("Score:", score)
        return score

    def next_game_number(self):
        max_game = 0
        sets = TennisSet.objects.filter(match=self)
        for set in sets:
            for game in TennisGame.objects.filter(set=set):
                if game.game_no > max_game: max_game = game.game_no
        return max_game + 1

    def server(self):
        return self.next_game_number() % 2

    def set_score(self):
        sets = TennisSet.objects.filter(match=self)
        score_string = ""
        for set in sets:
            score_A, score_B = set.score()
            score_string += f"{score_A}-{score_B} "
        return score_string

    def sets(self):
        return TennisSet.objects.filter(match=self)

    def next_set_number(self):
        sets = TennisSet.objects.filter(match=self).order_by('-set_no')
        if len(sets) == 0: return 1
        return sets[0].set_no + 1

    def current_set(self):
        sets = TennisSet.objects.filter(match=self).order_by('-set_no')
        if len(sets) == 0: return None
        return sets[0]

class TennisSet(Model):
    string_name = "TennisSet"
    match = ForeignKey(TennisMatch, null=True, blank=True, on_delete=CASCADE)
    set_no = IntegerField(null=True, blank=True)

    def games(self):
        return TennisGame.objects.filter(set=self)

    def score(self):
        games = TennisGame.objects.filter(set=self)
        games_A, games_B = 0, 0
        for game in games:
            if game.score_A > game.score_B: games_A += 1
            if game.score_B > game.score_A: games_B += 1
        return games_A, games_B

    def points(self):
        games = TennisGame.objects.filter(set=self)
        points_A, points_B = 0, 0
        for game in games:
            points_A += game.score_A
            points_B += game.score_B
        return points_A, points_B

    def is_complete(self):
        games_A, games_B = self.score()
        if games_A == 6 and games_A > games_B + 2: return True
        if games_B == 6 and games_B > games_A + 2: return True
        if games_A == 7 or games_B == 7: return True
        return False

    def score_string(self):
        games_A, games_B = self.score()
        return f"{games_A}:{games_B}"
        # return f"<b>Set {self.set_no}: </b>{games_A} - {games_B}"

    def game_scores(self):
        games = TennisGame.objects.filter(set=self).order_by('game_no')
        games_string = ""
        for game in games:
            games_string += f"(G{game.game_no}) {game.score()}<br>"
        return games_string

    def next_game_number(self):
        games = TennisGame.objects.filter(set=self).order_by('-game_no')
        if len(games) == 0: return 1
        return games[0].game_no + 1

    def delete_last_game(self):
        games = TennisGame.objects.filter(set=self).order_by('-game_no')
        if len(games) > 0: games[0].delete()

class TennisGame(Model):
    string_name = "TennisGame"
    set = ForeignKey(TennisSet, null=True, blank=True, on_delete=CASCADE)
    game_no = IntegerField(null=True, blank=True)
    score_A = IntegerField(null=True, blank=True)
    score_B = IntegerField(null=True, blank=True)

    def __str__(self):
        try:
            return f"{self.set.match} {self.set} {self.game_no}"
        except:
            return "Game Failure"

    def score(self):
        if self.score_A == 3 and self.score_B == 3: return "Deuce"
        scores = [0, 15, 30, 40, "W"]
        return f"{scores[min(self.score_A, 4)]} - {scores[min(self.score_B, 4)]}"

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
        if object.next_age_days() == object.reminder_days:
            text += object.next_age() + ". "
        if object.next_age_days() == 2:
            text += f"It is {object.person}'s birthday tomorrow. "
    return text

all_models = \
    [Category, Diary, Note, Quote, Birthday, Dog, Booking, Event, TH, Player, Shopping, Shop, Timer, TimerElement,
     New_Tide, Tide_Date, Weather, Wordle, TennisMatch, TennisGame, General]

