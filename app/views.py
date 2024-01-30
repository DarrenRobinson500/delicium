from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

import pandas as pd
import requests
import socket
import plotly.express as px
from dash import Dash, html

from .forms import *

Event_Tuple = namedtuple('Event_Tuple', ['date', 'description'])
Dog_Diary = namedtuple('Dog_Diary', ['date', 'bookings'])

def home(request):
    if not request.user.is_authenticated: return redirect("login")
    if request.user == "Amanda":
        return redirect("dog_diary")
    return redirect('notes')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("Error logging in."))
            return redirect('login')
    else:
        context = {}
        return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect("login")

def downloadpage(request):
    context = {}
    return render(request, 'down_load.html', context)

def downloadexcel(request):
    if not request.user.is_authenticated: return redirect("login")
    if not socket.gethostname() == "Mum_and_Dads": return redirect("notes")

    writer = pd.ExcelWriter('my_data.xlsx', engine='xlsxwriter')
    for count, model in enumerate(all_models, 1):
        data = model.objects.all()
        df = pd.DataFrame(list(data.values()))
        df.to_excel(writer, sheet_name=f'{model.string_name}', index=False)
    writer.close()

    # Create an HttpResponse object with the Excel file
    response = HttpResponse(open('my_data.xlsx', 'rb').read(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="my_data.xlsx"'

    return response

def shopping(request):
    if not request.user.is_authenticated: return redirect("login")
    if request.method == 'POST':
        form = ShoppingForm(request.POST)
        if form.is_valid(): form.save()
    shops = Shop.objects.order_by('order')

    form = ShoppingForm()
    context = {'form': form, 'shops': shops}
    return render(request, 'shopping.html', context)

def shopping_save(request):
    if not request.user.is_authenticated: return redirect("login")
    objects = Shopping.objects.all()
    if request.method == 'POST':
        for object in objects:
            if f"checkbox{object.id}" in request.POST.keys():
                object.buy = True
            else:
                object.buy = False
            object.save()
    return redirect('shopping')

def shopping_clear(request):
    if not request.user.is_authenticated: return redirect("login")
    objects = Shopping.objects.all()
    for object in objects:
        object.buy = False
        object.save()

    return redirect('shopping')
def shopping_delete(request, id):
    object = Note.objects.filter(id=id).first()
    if object and object.shop: parent = object.shop
    if object: object.delete()
    if parent: return redirect("shopping_edit", f"{parent.id}")
    else: return redirect("shopping")

def shopping_edit(request, id):
    shop = Shop.objects.get(id=id)
    shop.order_children()
    context = {'shop': shop}
    return render(request, "shopping_edit.html", context)

def shopping_up(request, id): return shopping_reorder(request, -1, id)

def shopping_down(request, id): return shopping_reorder(request, 1, id)

def shopping_reorder(request, dir, id):
    object = Shopping.objects.filter(id=id).first()
    if object is None:                                                  pass
    elif dir == 1 and object.order == object.shop.max_child_number():   pass
    elif dir == -1 and object.order == 1:                               pass
    else:
        if object.order:
            other_object = Shopping.objects.filter(shop=object.shop, order=object.order + dir).first()
            if other_object:
                other_object.order = object.order
                other_object.save()
            object.order = object.order + dir
        else:
            object.order = object.shop.next_child_number()
        object.save()

    if object and object.shop:
        return redirect("shopping_edit", str(object.shop.id))
    else:
        return redirect("notes")


def dogs(request):
    if not request.user.is_authenticated: return redirect("login")
    form = DogForm()

    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid(): form.save()
    objects = Dog.objects.all()
    objects = sorted(objects, key=lambda d: d.next_booking())
    options = ["Yes", "No", "Limited"]
    show_images = socket.gethostname() == "Mum_and_Dads"

    count = len(objects)
    context = {'objects': objects, 'title': "Dogs", 'count': count, "form": form, "edit_mode": False, 'people': people(),
               'options':options, 'show_images': show_images}
    return render(request, 'dog.html', context)

def dog_edit(request, id):
    if not request.user.is_authenticated: return redirect("login")
    dog = Dog.objects.get(id=id)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid(): form.save()
        return redirect("dogs")

    form = DogForm(instance=dog)
    objects = Dog.objects.all()
    objects = sorted(objects, key=lambda d: d.next_booking())

    count = len(objects)
    options = ["Yes", "No", "Limited"]
    context = {'objects': objects, 'title': "Dogs", 'count': count, "dog": dog, "edit_mode": True,  'people': people(),
               'options':options, 'form':form}
    return render(request, 'dog.html', context)

def dog_diary(request):
    if not request.user.is_authenticated: return redirect("login")
    general = General.objects.get(name="main")
    today = date.today()

    bookings = Booking.objects.filter(end_date__gte=today).order_by('start_date')
    dog_diary = []
    for x in range(general.dog_diary_days):
        day = today + timedelta(days=x)
        day_bookings = bookings.filter(start_date__lte=day).filter(end_date__gte=day)
        new = Dog_Diary(day, day_bookings)
        dog_diary.append(new)

# Date Chart
    fig = px.line(
        x=[item.date for item in dog_diary],
        y=[len(item.bookings) for item in dog_diary],
        title="No of dogs",
        labels={'x': "", 'y': "Number"}
    )
    fig.update_layout(
        title={"font_size": 22, "xanchor": "center", "x": 0.5}
    )
    chart = fig.to_html()

# Pie Chart
    dogs = Dog.objects.all()
    dogs = sorted(dogs, key=lambda d: d.nights(), reverse=True)
    dogs = dogs[0:8]
    dogs_data = [
        {
            "name": dog.name,
            "nights": dog.nights()
        } for dog in dogs
    ]

    df = pd.DataFrame(dogs_data)

    pie = px.pie(df)

    pie = px.pie(
        names=[dog.name for dog in dogs],
        values=[dog.nights() for dog in dogs],
        hole=0.3,
    )
    chart_pie= pie.to_html()

    general = General.objects.get(name="main")
    durations = [30, 60, 90, 120, 150, 180, 360]

    context = {'dog_diary': dog_diary, "chart": chart, "chart_pie": chart_pie, 'durations': durations, 'general': general}
    return render(request, 'dog_diary.html', context)

def dog_duration(request, dur):
    general = General.objects.get(name="main")
    general.dog_diary_days = dur
    general.save()
    return redirect('dog_diary')

def booking(request, id):
    if not request.user.is_authenticated: return redirect("login")
    dog = Dog.objects.filter(id=id).first()
    if request.method == 'POST':
        form = BookingForm(request.POST or None)
        form.instance.dog = dog
        if form.is_valid():
            new_booking = form.save()
            return redirect("dogs")
        else:
            context = {"dog": dog, "title": f"Booking for {dog.name}", "form": form}
            return render(request, 'booking.html', context)

    context = {"dog": dog, "title": f"Booking for {dog.name}"}
    return render(request, 'booking.html', context)

def diary(request):
    if not request.user.is_authenticated: return redirect("login")
    form = None
    if request.method == 'POST':
        form = DiaryForm(request.POST or None)
        if form.is_valid(): form.save()
    form = DiaryForm()
    objects = Diary.objects.all().order_by("-date")
    count = len(objects)
    context = {'objects': objects, 'title': "Diary", 'count': count, "form": form}
    return render(request, 'diary.html', context)

def quotes(request):
    if not request.user.is_authenticated: return redirect("login")
    if request.method == 'POST':
        form = QuoteForm(request.POST or None)
        if form.is_valid(): form.save()
    objects = Quote.objects.all().order_by('-date')
    context = {'quotes': objects}
    return render(request, 'quotes.html', context)

def notes(request):
    if not request.user.is_authenticated: return redirect("login")
    form = NoteForm()
    if request.method == 'POST':
        form = NoteForm(request.POST or None)
        if form.is_valid(): form.save()
    object = Note.objects.exclude(parent__isnull=False).first()

    return redirect("note", object.id)

def edit_note(request, id):
    if not request.user.is_authenticated: return redirect("login")
    object = Note.objects.get(id=int(id))
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=object)
        if form.is_valid():
            form.save()

            messages.success(request, "Note saved")
            return redirect("note", object.id)
        else:
            for field in form:
                for error in field.errors:
                    print("Error:", field, error)
    form = NoteForm(instance=object)
    categories = Category.objects.all()
    context = {'object': object, 'categories': categories, 'form': form}
    return render(request, 'note_edit.html', context)


def note(request, id):
    if not request.user.is_authenticated: return redirect("login")
    object = Note.objects.get(id=id)
    if request.method == 'POST':
        form = NoteForm(request.POST or None)
        if form.is_valid():
            new_note = form.save()
        else:
            text = form.cleaned_data['text']
            new_note = Note.objects.create(text=text)
        new_note.parent = object
        new_note.save()
    form = NoteForm()
    object.order_children()
    children = Note.objects.filter(parent=object).order_by('category', 'order')
    # add_order_to_children(object)
    count = len(children)
    categories = Category.objects.all()

    for child in children:
        if child.heading == None:
            child.heading = child.text
            child.text = ""
            child.save()
        if child.heading == child.text:
            child.text = ""
            child.save()

    home_pc = socket.gethostname() == "Mum_and_Dads"
    context = {'object': object, 'categories': categories, 'children': children, 'count': count, 'form': form, 'home_pc': home_pc}
    return render(request, 'note.html', context)

def up(request, id):
    return reorder(request, -1, id)

def down(request, id):
    return reorder(request, 1, id)

def reorder(request, dir, id):
    object = Note.objects.filter(id=id).first()
    if object is None:
        pass
    elif dir == 1 and object.order == object.parent.max_child_number():
        pass
    elif dir == -1 and object.order == 1:
        pass
    else:
        if object.order:
            other_object = Note.objects.filter(parent=object.parent, order=object.order + dir).first()
            if other_object:
                other_object.order = object.order
                other_object.save()
            object.order = object.order + dir
        else:
            object.order = object.parent.next_child_number()
        object.save()

    if object and object.parent:
        return redirect("note", str(object.parent.id))
    else:
        return redirect("notes")



def add_order_to_children(object):
    children = Note.objects.filter(parent=object).order_by('category')
    used_numbers = []
    for child in children:
        if child.order is None:
            child.order = object.next_child_number()
            child.save()
        if child.order in used_numbers:
            child.order = object.next_child_number()
            child.save()
        used_numbers.append(child.order)


def delete_note(request, id):
    object = Note.objects.filter(id=id).first()
    if object and object.parent:
        parent = object.parent
    if object:
        object.delete()
    if parent:
        return redirect("note", f"{parent.id}")
    else:
        return redirect("notes")

def delete_diary(request, id):
    object = Diary.objects.filter(id=id).first()
    if object: object.delete()
    return redirect("diary")


def new_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST or None)
        if form.is_valid(): form.save()
    return redirect("notes")

def birthdays(request):
    if request.method == 'POST':
        form = BirthdayForm(request.POST or None)
        if form.is_valid(): form.save()
    objects = Birthday.objects.all().order_by(ExtractMonth('date'), ExtractDay('date'))
    count = len(objects)

    context = {'objects': objects, "count": count, "min_days": min_days_to_birthday(), 'title': "Birthdays"}
    return render(request, 'birthdays.html', context)


def events(request):
    if request.method == 'POST':
        form = EventForm(request.POST or None)
        if form.is_valid(): form.save()

    today = date.today()

    # Weather
    end_date = today + timedelta(days=3)
    weather_check = Tide_Date.objects.filter(date=end_date).first().weather()
    if not weather_check:
        get_weather()

    # Tides
    end_date = today + timedelta(days=30)
    tide_check = Tide_Date.objects.filter(date=end_date).first()
    if tide_check is None or len(tide_check.tides()) == 0: get_tides()

    # Routine
    ongoing_items = Note.objects.filter(frequency__isnull=False)
    for item in ongoing_items: item.update_date()

    tide_dates = Tide_Date.objects.filter(date__lte=end_date).filter(date__gte=today).order_by('date')
    context = {'tide_dates': tide_dates, 'title': "Events"}

    # context = {'objects': events_and_bookings, "count": count}
    return render(request, 'events.html', context)

def clash(request):
    ths = TH.objects.order_by('level')
    players = Player.objects.all().order_by('order')
    total, max, remaining = 0, 0, 0
    for player in players:
        total += player.total()
        max += player.th.total()
    total_string = f"{total} / {max} ({max - total})"
    #     if player.king > player.th.king_max: player.king = player.th.king_max
    #     if player.queen > player.th.queen_max: player.queen = player.th.queen_max
    #     if player.champ > player.th.champ_max: player.champ = player.th.champ_max
    #     player.save()
    context = {'ths': ths, 'players': players, 'total_string': total_string}
    return render(request, 'clash.html', context)

def hero_inc(request, id, hero):
    player = Player.objects.get(id=id)
    if player:
        if hero == "king": player.king += 1
        if hero == "queen": player.queen += 1
        if hero == "warden": player.warden += 1
        if hero == "champ": player.champ += 1
        player.save()

    return redirect('clash')

def timers(request):
    timers = Timer.objects.all()
    context = {'timers': timers}
    return render(request, "timers.html", context)

def timer(request, id):
    timer = Timer.objects.get(id=id)
    context = {'timer': timer}
    return render(request, "timer.html", context)

def get_tides():
    print("Getting tides")
    key = 'ZmY5ZDcxZGQwMzBhNmE3NzY4YTI4Mj'
    location = 3212

    url = f'https://api.willyweather.com.au/v2/{key}/locations/{location}/weather.json'
    params = [("forecasts", ["tides"]), ("days", 31)]
    resp = requests.get(url, params=params, timeout=10).json()

    tidal_data = resp['forecasts']['tides']['days']
    for day in tidal_data:
        for peak in day['entries']:
            date_time_obj = datetime.strptime(peak['dateTime'], '%Y-%m-%d %H:%M:%S')
            date = date_time_obj.date()
            date_object = Tide_Date.objects.filter(date=date).first()
            if date_object is None:
                date_object = Tide_Date(date=date)
                date_object.save()
            existing = New_Tide.objects.filter(date=date_object, time=date_time_obj.time()).first()
            if not existing:
                new_object = New_Tide(date=date_object, time=date_time_obj.time(), height=peak['height'], type=peak['type'])
                new_object.save()

def get_weather():
    print("Getting weather")
    key = 'ZmY5ZDcxZGQwMzBhNmE3NzY4YTI4Mj'
    location = 3212
    url = f'https://api.willyweather.com.au/v2/{key}/locations/{location}/weather.json'
    params = [("forecasts", ["precis"]), ("days", 4)]
    resp = requests.get(url, params=params, timeout=10).json()

    data = resp['forecasts']['precis']['days']
    for day in data:
        for entry in day['entries']:
            date_time_obj = datetime.strptime(entry['dateTime'], '%Y-%m-%d %H:%M:%S')
            date = date_time_obj.date()
            date_object = Tide_Date.objects.filter(date=date).first()
            if date_object is None:
                date_object = Tide_Date(date=date)
                date_object.save()
            existing = Weather.objects.filter(date=date_object).filter(time=date_time_obj.time()).first()
            if not existing:
                if time(8, 0) <= date_time_obj.time() <= time(17, 0):
                    new_object = Weather(date=date_object, time=date_time_obj.time(), precis=entry['precis'])
                    new_object.save()

    params = [("forecasts", ["weather"]), ("days", 4)]
    resp = requests.get(url, params=params, timeout=10).json()
    data = resp['forecasts']['weather']['days']
    for day in data:
        for entry in day['entries']:
            date_time_obj = datetime.strptime(entry['dateTime'], '%Y-%m-%d %H:%M:%S')
            date = date_time_obj.date()
            date_object = Tide_Date.objects.filter(date=date).first()
            if date_object is None:
                date_object = Tide_Date(date=date)
                date_object.save()
            existing = MaxTemp.objects.filter(date=date).first()
            if not existing:
                new_object = MaxTemp(date=date, max=entry['max'])
                new_object.save()


def tides(request):
    today = date.today()

    # Weather
    end_date = today + timedelta(days=4)
    weather_check = Tide_Date.objects.filter(date=end_date).first().weather()
    if not weather_check: get_weather()

    # Tides
    end_date = today + timedelta(days=20)
    tide_check = Tide_Date.objects.filter(date=end_date).first().tides()
    if len(tide_check) == 0: get_tides()

    tide_dates = Tide_Date.objects.filter(date__lte=end_date).filter(date__gte=today).order_by('date')
    context = {'tide_dates': tide_dates}
    return render(request, 'tides.html', context)

def tennis(request):
    form = TennisForm
    matches = TennisMatch.objects.all().order_by('-id')
    context = {"matches": matches, "form": form}
    return render(request, 'tennis.html', context)

def tennis_match_start(request):
    match, set = None, None
    if request.method == 'POST':
        form = TennisForm(request.POST)
        if form.is_valid():
            match = form.save()
            set = TennisSet(match=match, set_no=1)
            set.save()
    context = {"match": match, "set": set}
    return render(request, 'tennis_match.html', context)

def tennis_match(request, id):
    match = TennisMatch.objects.get(id=id)
    set = match.current_set()
    points = match.points()
    context = {"match": match, "set": set, "points": points}
    return render(request, 'tennis_match.html', context)

def save_game(set):
    print("Save game")
    match = set.match
    game = TennisGame(set=set, score_A=match.score_A, score_B=match.score_B, game_no=match.next_game_number())
    game.save()
    match.score_A = 0
    match.score_B = 0
    match.save()
    if set.is_complete():
        set = TennisSet(match=match, set_no=match.next_set_number())
        set.save()
    return set

def tennis_score(request, id, a, b):
    a, b = int(a), int(b)
    set = TennisSet.objects.get(id=id)
    match = set.match
    match.score_A += a
    match.score_B += b
    match.score_A = min(max(match.score_A, 0), 5)
    match.score_B = min(max(match.score_B, 0), 5)
    if match.score_A >= 4 and match.score_A - match.score_B > 1: set = save_game(set)
    if match.score_B >= 4 and match.score_B - match.score_A > 1: set = save_game(set)
    if match.score_A == 4 and match.score_B == 4:
        match.score_A = 3
        match.score_B = 3
    match.save()
    return redirect(f'/tennis_match/{match.id}')

def tennis_delete_game(request, id):
    set = TennisSet.objects.get(id=id)
    match = set.match
    set.delete_last_game()
    context = {"match": match, "set": set}
    return render(request, 'tennis_match.html', context)
