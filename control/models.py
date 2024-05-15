from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date

class Branch(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.first_name

class Country(models.Model):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=2)
    priority = models.IntegerField()

    def __str__(self):
        return self.title
    
    def person_count(self):
        return self.person_set.all().count()
    
    class Meta:
        ordering = ("priority",)

class Company(models.Model):
    title = models.CharField(max_length=255)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def person_count(self):
        return self.person_set.all().count()
    
    class Meta:
        ordering = ("-id",)
    
class Person(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    passport = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    tools = models.TextField()
    available = models.BooleanField(default=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    room = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ("-id",)
    
class Document(models.Model):
    file = models.FileField(upload_to="docs/", null=True, blank=True)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    available = models.BooleanField(default=True)
    date_start = models.DateField()
    date_finish = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    title = models.CharField(max_length=255)
    responsible = models.CharField(max_length=255)

    def __str__(self):
        return self.person.title
    
    
class Entry(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT, null=True, blank=True)
    date_start = models.DateTimeField()
    date_finish = models.DateTimeField(null=True, blank=True)
    photo = models.ImageField(upload_to="entries/")
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    guest = models.BooleanField(default=False)
    dastur = models.ForeignKey("Dastur", on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, blank=True)

    def date_start_current(self):
        return (self.date_start + timedelta(hours=int(5))).strftime('%d-%m-%Y %H:%M')
    
    def date_finish_current(self):
        return (self.date_finish + timedelta(hours=int(5))).strftime('%d-%m-%Y %H:%M')
    
    class Meta:
        ordering = ("-id",)
    
class ToolsImage(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tools_images/")
    
    class Meta:
        ordering = ("-id",)
    
class Guest(models.Model):
    info = models.OneToOneField(Entry, on_delete=models.CASCADE, related_name="info")
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    passport = models.CharField(max_length=255)
    citizenship = models.ForeignKey(Country, on_delete=models.PROTECT)
    permited_by = models.CharField(max_length=255)
    tools = models.TextField()
    accompanied_by = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.title

class Dastur(models.Model):
    title = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    tools = models.TextField()
    file = models.FileField(null=True, blank=True)
    date_start = models.DateField()
    date_end = models.DateField()
    branch = models.ManyToManyField(Branch)
    def get_correct_date_start(self):
        return self.date_start.strftime("%Y-%m-%d")
    def get_correct_date_end(self):
        return self.date_end.strftime("%Y-%m-%d")
    def get_count_person(self):
        return self.dpl_set.all().count()
    def is_date_expired(self):
        return date.today() > self.date_end
    
    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return str(self.title)

class DPL(models.Model):
    dastur = models.ForeignKey(Dastur, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class Vehicle(models.Model):
    title = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    numberplate = models.CharField(max_length=255, unique=True)
    dastur = models.ForeignKey(Dastur, on_delete=models.PROTECT)
    driver = models.ForeignKey(Person, on_delete=models.PROTECT)

######### Role #########

#### 100 #### superadmin

### 200 ### reception

### 300 ### security

### 400 ### watcher






