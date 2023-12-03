from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save,sender=Contribution)
def update_balance(sender,instance,**kwargs):
    
    mem_obj = Members.objects.get(id=instance.member.id)
    mem_obj.balance += instance.amount
    mem_obj.save()

