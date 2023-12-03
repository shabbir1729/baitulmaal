from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)



admin.site.site_header = 'Baitulmaal Admin'
admin.site.site_title = 'Baitulmaal Admin'
admin.site.index_title = 'Baitulmaal Administration'
admin.empty_value_display = '**Empty**'



@admin.register(Members)
class MembersAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","created_at")

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ("member","created_at",)

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("member","created_at",)

