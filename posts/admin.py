from django.contrib import admin
from .models import Post


# admin.site.register(Post)


class MyAdmin(admin.ModelAdmin):
    readonly_fields = ['autoconsumption', 'autoconsumption_percentage', 'consumption', 'consumption_average', 'energy_surplus', 'energy_surplus_cash']

admin.site.register(Post, MyAdmin)