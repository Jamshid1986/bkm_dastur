from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from control.models import *
import base64
from django.core.files.base import ContentFile
import datetime
from django.db.models import Q
import requests
from django.conf import settings

@login_required(login_url="login_index")
def reception_index(request):
    entries = Entry.objects.filter(date_finish__isnull=True, guest=False, branch = request.user.account.branch).distinct()
    guests = Entry.objects.filter(date_finish__isnull=True, guest=True, info__branch = request.user.account.branch).distinct()
    persons = Person.objects.filter(available=True)
    aktivlar = []
    for i in entries:
        aktivlar.append(i.person.id)
    odamlar = []
    if request.GET.get("search"):
        odamlar = Person.objects.filter((Q(title__icontains = request.GET.get("search")) | 
         Q(company__title__icontains = request.GET.get("search")) | 
         Q(passport__icontains = request.GET.get("search"))), dpl__dastur__branch = request.user.account.branch).distinct()
    elif request.GET.get("dastur"):
        try:
            dastur = Dastur.objects.get(title=request.GET.get("dastur"))
            odamlar = Person.objects.filter(dpl__dastur=dastur, dpl__dastur__branch = request.user.account.branch).distinct() 
        except:
            pass

    data = {"persons":persons, "entries": entries | guests, "odamlar":odamlar, "aktivlar": aktivlar}

    return render(request, "reception/index.html", context=data)


def reception_detail(request):
    
    if request.method == "POST":
        pid = request.POST["pid"]
        try:
            person = Person.objects.get(id=pid)
        except:
            return redirect("reception_index")
        data = {"person":person}
        return render(request, "reception/detail.html", context=data)
    return redirect("reception_index")

def reception_guest(request):
    countries = Country.objects.all()
    data = {"countries":countries}
    return render(request, "reception/guest.html", context=data)
    


def reception_create_session(request):
    if request.method == "POST":
        person = Person.objects.get(id = request.POST["id"])
        file = request.POST["image"]
        format, imgstr = file.split(";base64,")
        ext = format.split("/")[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f"{person.title}_session." + ext)
        dastur = Dastur.objects.get(id = request.POST["dastur"])
        branch = Branch.objects.get(id=request.user.account.branch.id)
        g=Entry.objects.create(
            person = person,
            date_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            photo = data,
            user = request.user,
            dastur = dastur,
            branch = branch
        )
        
        if person.country.title != "Uzbekistan":
            text = f"""
Hello Dear Admin!
Bot detected new foreigner's sign in at {g.branch}:
Name: {person.title}
Company: {person.company}
Branch: {g.branch}
Citizenship: {person.country.title}
Sign in date: {g.date_start}
"""
            requests.get(f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage?chat_id={-1002079629028}&text={text}")
        return redirect("reception_index")


def reception_create_guest(request):
    if request.method == "POST":
        
        file = request.POST["image"]
        format, imgstr = file.split(";base64,")
        ext = format.split("/")[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f"session." + ext)
        entry = Entry.objects.create(
            date_start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            photo = data,
            user = request.user,
            guest = True
        )
        country = Country.objects.get(id = request.POST["citizenship"])
        branch = Branch.objects.get(id=request.user.account.branch.id)
        g=Guest.objects.create(
            info = entry,
            title = request.POST["title"],
            citizenship = country,
            company = request.POST["company"],
            tools = request.POST["tools"],
            accompanied_by = request.POST["accompanied_by"],
            room = request.POST["room"],
            passport = request.POST["passport"],
            permited_by = request.POST["permited_by"],
            branch = branch
        )
        
        if g.citizenship.title != "Uzbekistan":
            text = f"""
TEST!
New Foreign Guest sign in detected at {g.branch}
Name: {g.title}
Company: {g.company}
Branch: {g.branch}
Permited by: {g.permited_by}
Citizenship: {g.citizenship}
Sign in date: {entry.date_start}
"""
            requests.get(f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage?chat_id={-1002079629028}&text={text}")
        return redirect("reception_index")
    

def reception_delete_session(request):
    if request.method == "POST":
        entry = Entry.objects.get(id = request.POST["id"])
        entry.date_finish = datetime.datetime.now()
        entry.save()
        return redirect("reception_index")