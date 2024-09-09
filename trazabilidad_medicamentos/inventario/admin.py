from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import medicamento


# Register your models here.

admin.site.register(medicamento, SimpleHistoryAdmin)

