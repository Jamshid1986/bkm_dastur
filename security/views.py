from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from control.models import *
import base64
from django.core.files.base import ContentFile
import datetime
from django.db.models import Q

@login_required(login_url="login_index")
def security_index(request):
    entries = Entry.objects.filter(date_finish__isnull=True, guest = False, branch = request.user.account.branch).distinct()
    guests = Entry.objects.filter(date_finish__isnull=True, guest=True, info__branch = request.user.account.branch).distinct()
    
    data = {"entries": entries | guests}

    return render(request, "security/index.html", context=data)

def security_create_image_tool(request):
    if request.method == "POST":
        entry = Entry.objects.get(id = request.POST["id"])
        file = request.POST["image"]
        format, imgstr = file.split(";base64,")
        ext = format.split("/")[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f"tools." + ext)
        ToolsImage.objects.create(
            entry = entry,
            image = data,
        )
        return redirect("security_index")