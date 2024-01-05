from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from collections import namedtuple

from .forms import *

Event_Tuple = namedtuple('Event_Tuple', ['date', 'description'])


def home(request):
    if not request.user.is_authenticated: return redirect("login")
    return redirect("diary")

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
        print("Keys:", request.POST.keys())
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


def dogs(request):
    if not request.user.is_authenticated: return redirect("login")
    form = None
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid(): form.save()
    objects = Dog.objects.all()
    objects = sorted(objects, key=lambda d: d.next_booking())

    count = len(objects)
    context = {'objects': objects, 'title': "Dogs", 'count': count, "form": form, "edit_mode": False}
    return render(request, 'dog.html', context)

def dog_edit(request, id):
    if not request.user.is_authenticated: return redirect("login")
    dog = Dog.objects.get(id=id)
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid(): form.save()
        return redirect("dogs")

    objects = Dog.objects.all()
    objects = sorted(objects, key=lambda d: d.next_booking())

    count = len(objects)
    context = {'objects': objects, 'title': "Dogs", 'count': count, "dog": dog, "edit_mode": True}
    return render(request, 'dog.html', context)

def booking(request, id):
    if not request.user.is_authenticated: return redirect("login")
    dog = Dog.objects.filter(id=id).first()
    if request.method == 'POST':
        form = BookingForm(request.POST or None)
        form.instance.dog = dog
        print(form.instance)
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
    # all_notes = Note.objects.all()
    # categories = Category.objects.all()
    # count = len(objects)
    # context = {'objects': objects, 'all_notes': all_notes, 'categories': categories, 'count': count, 'form': form, 'title': "Notes"}
    # return render(request, 'notes.html', context)
    # id = objects.id
    return redirect("note", object.id)

def edit_note(request, id):
    if not request.user.is_authenticated: return redirect("login")
    object = Note.objects.get(id=int(id))
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            # print("Note saved")
            # for field in form:
            #     print("Note saved:", field.name, field.value())

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
    add_order_to_children(object)
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

    context = {'object': object, 'categories': categories, 'children': children, 'count': count, 'form': form}
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
            other_object = Note.objects.filter(category=object.category, order=object.order + dir).first()
            if other_object:
                other_object.order = object.order
                other_object.save()
            object.order = object.order + dir
        else:
            object.order = object.next_child_number()
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

Event_Tuple = namedtuple('Event_Tuple', ['date', 'description'])

def events(request):
    if request.method == 'POST':
        form = EventForm(request.POST or None)
        if form.is_valid(): form.save()

    today = date.today()
    events = Event.objects.filter(date__gte=today).order_by(ExtractMonth('date'), ExtractDay('date'))
    bookings = Booking.objects.filter(start_date__gte=today).order_by(ExtractMonth('start_date'), ExtractDay('start_date'))

    events_and_bookings = []

    for event in events:
        new = Event_Tuple(event.date, event.description)
        events_and_bookings.append(new)

    for booking in bookings:
        new = Event_Tuple(booking.start_date, "Dog Booking: " + booking.dog.name)
        events_and_bookings.append(new)

    events_and_bookings = sorted(events_and_bookings, key=lambda e: e.date)

    for item in events_and_bookings:
        print(item)

    count = len(events_and_bookings)

    context = {'objects': events_and_bookings, "count": count, 'title': "Events"}
    return render(request, 'events.html', context)

def clash(request):
    ths = TH.objects.order_by('level')
    players = Player.objects.all().order_by('order')
    context = {'ths': ths, 'players': players}
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