from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *


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
            messages.success(request, ("You are now logged in."))
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

def dogs(request):
    if not request.user.is_authenticated: return redirect("login")
    form = None
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid(): form.save()
    objects = Dog.objects.all()
    count = len(objects)
    context = {'objects': objects, 'title': "Dogs", 'count': count, "form": form}
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
    objects = Diary.objects.all().order_by("-date")
    count = len(objects)
    context = {'objects': objects, 'title': "Diary", 'count': count, "form": form}
    return render(request, 'diary.html', context)

def quotes(request):
    if not request.user.is_authenticated: return redirect("login")
    if request.method == 'POST':
        form = QuoteForm(request.POST or None)
        if form.is_valid(): form.save()
    objects = Quote.objects.all
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

def note(request, id):
    if not request.user.is_authenticated: return redirect("login")
    object = Note.objects.get(id=int(id))
    if request.method == 'POST':
        form = NoteForm(request.POST or None)
        if form.is_valid():
            new_note = form.save()
        else:
            text = form.cleaned_data['text']
            new_note = Note.objects.create(text=text)
        new_note.parent = object
        new_note.save()
    children = Note.objects.filter(parent=object).order_by('category', 'order')
    add_order_to_children(object)
    count = len(children)
    categories = Category.objects.all()

    context = {'object': object, 'categories': categories, 'children': children, 'count': count}
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
