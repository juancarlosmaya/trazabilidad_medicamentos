from django.shortcuts import render
from django.contrib.auth import alogin, alogout
from django.shortcuts import redirect
from  django.http import HttpRequest as request
from  django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from config import models as config
IP_Orion=config.config.ip_orion[0]
Port_Orion=config.config.port_orion[0]

# @login_required(redirect_field_name="/home")
async def logout(request):
        await alogout(request)
        user = request.user
        # await alogout(request)
        return redirect("/login")
        # return HttpResponse("<h1>Page was found</h1>")
        # return render(request, 'pages/home.html')

