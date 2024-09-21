from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import medicamento,Location,Continent,Country,Via_administracion,Forma_farmaceutica
# Register your models here.

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(Location)

# Register your models here.
admin.site.register(Via_administracion)
admin.site.register(Forma_farmaceutica)
admin.site.register(medicamento, SimpleHistoryAdmin)

