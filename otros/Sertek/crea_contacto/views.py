from django.shortcuts import render
from django.template import Template
from django.http import HttpRequest as request
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



# @login_required(redirect_field_name="")
def crea_contacto(request):
        # username = request.user.username
        return render(request, 'pages/crea_contacto.html')
        # return redirect("/home")