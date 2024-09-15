from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Country, Company, Person, Document, Entry, Dastur, DPL, Branch, Account, Vehicle
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
import datetime as dt


#####################################################
# sessions
####################################################

@login_required(login_url="login_index")
def control_index(request):
    if request.user.last_name not in ["100", "400"]: return redirect('login_index')
    active_sessions = Entry.objects.filter(date_finish__isnull=True)
    today = timezone.now().date()
    history_sessions = Entry.objects.filter(date_finish__isnull=False, date_start__date=today)
    data = {"active_sessions":active_sessions, "history_sessions":history_sessions}
    
    return render(request, "control/index.html", context=data)

#####################################################
# Country 
####################################################

@login_required(login_url="login_index")
def control_country(request):
    if request.user.last_name not in ["100", "400"]: return redirect('login_index')
    countries = Country.objects.all()
    data = {"countries":countries}
    
    return render(request, "control/country.html", context=data)

@login_required(login_url="login_index")
def control_country_create(request):
    if request.user.last_name not in ["100", "400"]: return redirect('login_index')
    if request.method == "POST":
        Country.objects.create(
            priority = request.POST["priority"],
            title = request.POST["title"],
            code = request.POST["code"]
        )

        return redirect("control_country")

@login_required(login_url="login_index")
def control_country_delete(request):
    if request.user.last_name not in ["100", "400"]: return redirect('login_index')
    if request.method == "POST":
        c = Country.objects.get(id=request.POST["id"])
        c.delete()

        return redirect("control_country")

@login_required(login_url="login_index")
def control_country_edit(request):
    if request.user.last_name not in ["100", "400"]: return redirect('login_index')
    if request.method == "POST":
        c = Country.objects.get(id=request.POST["id"])
        c.title = request.POST["title"]
        c.priority = request.POST["priority"]
        c.code = request.POST["code"]
        c.save()

        return redirect("control_country")

#####################################################
# Company 
####################################################

@login_required(login_url="login_index")
def control_company(request):
    if request.user.last_name not in ["100", "400"]: return redirect('login_index')
    companies = Company.objects.filter(available=True)
    data = {"companies":companies}
    
    return render(request, "control/company.html", context=data)


@login_required(login_url="login_index")
def control_company_create(request):
    if request.user.last_name not in ["100", "400"]: return redirect('login_index')
    if request.method == "POST":
        Company.objects.create(
            title = request.POST["title"]
        )

        return redirect("control_company")
    

@login_required(login_url="login_index")
def control_company_delete(request):
    if request.user.last_name not in ["100", "400"]: return redirect('login_index')
    if request.method == "POST":
        c = Company.objects.get(id=request.POST["id"])
        c.available = False
        c.save()
        return redirect("control_company")
    

@login_required(login_url="login_index")
def control_company_edit(request):
    if request.user.last_name not in ["100", "400"]: return redirect('login_index')
    if request.method == "POST":
        c = Company.objects.get(id=request.POST["id"])
        c.title = request.POST["title"]
        c.save()
    
    return redirect("control_company")


#####################################################
# Personallar
####################################################
from django.core.paginator import Paginator

@login_required(login_url="login_index")
def control_personal(request):
    if request.user.last_name not in ["100", "400"]: return redirect('login_index')
    if request.GET.get("search"):
         persons = Person.objects.filter((Q(title__icontains = request.GET.get("search")) | 
         Q(company__title__icontains = request.GET.get("search")) | 
         Q(passport__icontains = request.GET.get("search")) & Q(available=True)))
    else:
        persons = Person.objects.filter(available=True)
    persons_length = persons.count()
    countries = Country.objects.all()
    companies = Company.objects.filter(available=True)
    try: code = request.build_absolute_uri().split('?')[1]
    except: code = None
    paginator = Paginator(persons, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {"page_obj":page_obj, "countries":countries, "companies":companies, "code":code, "persons_length":persons_length}
    return render(request, "control/personal.html", context=data)

@login_required(login_url="login_index")
def control_personal_create(request):
    if request.method == "POST":
        if request.user.last_name not in ["100", "400"]: return redirect('login_index')
        country = Country.objects.get(id=request.POST["country"])
        c = Company.objects.get(id=request.POST["company"])
        if Person.objects.filter(passport = request.POST["passport"]).exists():
            return redirect("/personal/?exists")
        Person.objects.create(
            title = request.POST["title"],
            tools = request.POST["tools"],
            passport = request.POST["passport"],
            country = country,
            company = c,
            created_by = request.user.first_name,
            room = request.POST["room"]
        )

        return redirect("control_personal")
    

@login_required(login_url="login_index")
def control_personal_delete(request):
    if request.user.last_name not in ["100", "400"]: return redirect('login_index')
    if request.method == "POST":
        p = Person.objects.get(id=request.POST["id"])
        p.available = False
        p.save()
        return redirect("control_personal")
    

@login_required(login_url="login_index")
def control_personal_edit(request):
    if request.user.last_name not in ["100", "400"]: return redirect('login_index')
    if request.method == "POST":
        country = Country.objects.get(id=request.POST["country"])
        company = Company.objects.get(id=request.POST["company"])
        p = Person.objects.get(id=request.POST["id"])
        p.title = request.POST["title"]
        p.company = company
        p.country = country
        p.passport = request.POST["passport"]
        p.tools = request.POST["tools"]
        p.room = request.POST["room"]
        p.save()
        return redirect("control_personal")
    
#######################################################
### Document
#######################################################

@login_required(login_url="login_index")
def control_document_create(request):
    if request.user.last_name != '100': return redirect('login_index')
    if request.method == "POST":
        person = Person.objects.get(id=request.POST["id"])
        d = Document.objects.create(
            person = person,
            date_start = request.POST["date_start"],
            date_finish = request.POST["date_finish"],
            time_start = request.POST["time_start"],
            time_end = request.POST["time_end"],
            title = request.POST["title"],
            responsible = request.POST["responsible"]
        )
        try:
            d.file = request.FILES["file"]
            d.save()
        except:
            pass
 
        return redirect("control_personal")
    
@login_required(login_url="login_index")
def control_document_delete(request, id):
    if request.user.last_name != '100': return redirect('login_index')
    d = Document.objects.get(id=id)
    d.available = False
    d.save()
    return redirect("control_personal")

##################################################
### Users
#################################################

@login_required(login_url="login_index")
def control_user(request):
    if request.user.last_name != '100': return redirect('login_index')
    users = User.objects.filter(is_active = 1)
    branches = Branch.objects.all()
    data = {"users":users, "branches":branches}
    
    return render(request, "control/user.html", context=data)

@login_required(login_url="login_index")
def control_user_create(request):
    if request.user.last_name != '100': return redirect('login_index')
    if request.method == "POST":
        branch = Branch.objects.get(id=request.POST["branch"])
        user = User.objects.create_user(
            username = request.POST["username"].lower(),
            first_name = request.POST["first_name"],
            last_name = request.POST["role"],
            password = request.POST["password"]
        )
        Account.objects.create(
            user = user,
            branch = branch
        )

        return redirect("control_user")

@login_required(login_url="login_index")
def control_user_delete(request):
    if request.user.last_name != '100': return redirect('login_index')
    if request.method == "POST":
        u = User.objects.get(id=request.POST["id"])
        u.is_active = 0
        u.save()

        return redirect("control_user")

@login_required(login_url="login_index")
def control_user_edit(request):
    if request.user.last_name != '100': return redirect('login_index')
    if request.method == "POST":
        c = User.objects.get(id=request.POST["id"])
        c.username = request.POST["username"].lower()
        c.first_name = request.POST["first_name"]
        c.last_name = request.POST["role"]
        c.save()
        branch = Branch.objects.get(id=request.POST["branch"])
        c.account.branch = branch
        c.account.save()
        return redirect("control_user")
    
@login_required(login_url="login_index")
def control_user_edit_pwd(request):
    if request.user.last_name != '100': return redirect('login_index')
    if request.method == "POST":
        c = User.objects.get(id=request.POST["id"])
        c.set_password(request.POST["password"])
        c.save()

        return redirect("control_user")

@login_required(login_url="login_index")
def control_search(request):
    persons = Person.objects.all()
    data = {"persons":persons} # 1-person: jinja uchun, 2-person: viewsdan 256 qator 
    return render(request, "control/search.html", context=data)

##########################################################
# Izlash
#########################################################

@login_required(login_url="login_index")
def control_search_go(request):
    persons = Person.objects.all()
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    print(type(to_date))
    
    guest = request.GET.get("guest")
    sessions = []
    if len(guest):
        if from_date and to_date:
            sessions = Entry.objects.filter(person__id=guest.split(" ")[0], date_start__gte = from_date, date_finish__lte = to_date)
    else:
        if from_date and to_date:
            sessions = Entry.objects.filter(date_start__gte=from_date, date_finish__lte = to_date) 
    data = {"persons":persons, "sessions":sessions} # 1-person: jinja uchun, 2-person: viewsdan 256 qator 
    
    return render(request, "control/search.html", context=data)
    

from openpyxl import Workbook
from openpyxl.styles import Alignment
from django.http import HttpResponse

@login_required(login_url="login_index")
def control_to_excel(request):
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    if len(from_date)==0 and len(to_date)==0:
        return HttpResponse("")
    sessions = Entry.objects.filter(date_start__gte=from_date, date_finish__lte = to_date)
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "arxiv"
    worksheet.column_dimensions["C"].width=10
    worksheet.column_dimensions["H"].width=60
    worksheet.column_dimensions["D"].width=35
    worksheet.column_dimensions["E"].width=15
    worksheet.column_dimensions["F"].width=100
    worksheet.column_dimensions["G"].width=10
    worksheet.column_dimensions["K"].width=12
    worksheet.column_dimensions["L"].width=15
    worksheet.column_dimensions["M"].width=15
    worksheet.column_dimensions["N"].width=20
    worksheet.column_dimensions["O"].width=20
    worksheet.column_dimensions["P"].width=200
    
    columns = ["T/r", "ID", "Filial", "F.I.Sh", "Pasport/ID raqami", "Rasm", "Fuqaroligi", "Shirkat", 
               "Dastur", "Holati","Eslatma", "Kirgan sanasi", "Chiqqan sanasi", "Resepshnchi", "Ruxsat beruvchi", "Anjomlari"]
    worksheet.append(columns)
    c = 1
    for i in sessions:
        if i.guest:
            worksheet.append([c,0, str(i.branch),i.info.title, i.info.passport, "https://10.200.203.6:8030"+i.photo.url, i.info.citizenship.title, i.info.company, "mehmon", "Aktiv",i.info.room, str(i.date_start_current()), str(i.date_finish_current()), i.user.first_name, i.info.permited_by,i.info.tools])
        else:    
            worksheet.append([c,i.person.id, str(i.branch) ,i.person.title, i.person.passport, "https://10.200.203.6:8030"+i.photo.url, i.person.country.title, i.person.company.title, str(i.dastur), "Eskirgan" if i.dastur.is_date_expired() else "Aktiv","joyi", str(i.date_start_current()), str(i.date_finish_current()), i.user.first_name, "Dastur asosida",i.person.tools])
        c = c + 1
    
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = "attachment; filename=myfile.xlsx"
    workbook.save(response)
    return response

#######################################################

@login_required(login_url="login_index")
def control_dastur(request):
    dasturs = Dastur.objects.all()
    companies = Company.objects.filter(available=True)
    branches = Branch.objects.all()
    data = {'dasturs':dasturs, 'companies':companies, "branches":branches}
    return render(request, "control/dastur.html", context=data)


@login_required(login_url="login_index")
def control_dastur_detail(request, id):
    dastur = Dastur.objects.get(id=id)
    persons = Person.objects.filter(available=True, company=dastur.company)
    companies=Company.objects.filter(available=True)
    branches = Branch.objects.all()
    current_users = []
    for i in DPL.objects.filter(dastur=dastur):
        current_users.append(i.person.id)
    data = {'dastur':dastur, 'persons':persons, 'companies':companies, 'current_users':current_users, "branches":branches}
    return render(request, "control/dastur_detail.html", context=data)


@login_required(login_url="login_index")
def control_dastur_create(request):
    if request.user.last_name != '100': return redirect('login_index')
    if request.method == "POST":
    
        d = Dastur.objects.create(
            company = Company.objects.get(id=request.POST["shirkat_id"]),
            date_start = request.POST["date_start"],
            date_end = request.POST["date_end"],
            title = request.POST["title"],
            tools = request.POST["tools"],
        )
        d.branch.set(request.POST.getlist("branch"))
        try:
            d.file = request.FILES["file"]
            d.save()
        except:
            pass
 
    return redirect("control_dastur")

############

@login_required(login_url="login_index")
def control_dastur_add_person(request):
    if request.method == "POST":
        DPL.objects.create(
            dastur_id = request.POST["did"],
            person_id = request.POST["pid"],
        )

        return redirect(f"/dastur/{request.POST['did']}")
    

@login_required(login_url="login_index")
def control_dastur_remove_person(request):
    if request.method == "POST":
        DPL.objects.get(id=request.POST["pid"]).delete()

        return redirect(f"/dastur/{request.POST['did']}")
    

@login_required(login_url="login_index")
def control_dastur_edit(request):
    if request.user.last_name != '100': return redirect('login_index')
    if request.method == "POST":
        dastur = Dastur.objects.get(id=request.POST['did'])
        dastur.company = Company.objects.get(id=request.POST["shirkat_id"])
        dastur.date_start = request.POST["date_start"]
        dastur.date_end = request.POST["date_end"]
        dastur.title = request.POST["title"]
        dastur.tools = request.POST["tools"]
        dastur.branch.set(request.POST.getlist("branch"))
        try:
            dastur.file = request.FILES["file"]
            dastur.save()
        except:
            pass

        dastur.save()
 
    return redirect(f'/dastur/{dastur.id}')


@login_required(login_url="login_index")
def control_dastur_delete(request):
    if request.user.last_name != '100': return redirect('login_index')
    if request.method == "POST":
        dastur = Dastur.objects.get(id=request.POST['did'])
        dastur.delete()
 
    return redirect('/dastur/')

####################################
# Vehicles
####################################

@login_required(login_url="login_index")
def control_vehicle(request):
    vehicles = Vehicle.objects.all()
    
    data = {"vehicles":vehicles}
    return render(request, "control/vehicle.html", context=data)