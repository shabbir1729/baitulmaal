from .models import *
from .serializer import *
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
import datetime
from django.utils import timezone
from .permissions import IsPrivateAllowed
from django.db.models import Sum


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):

    queryset                = User.objects.all()
    serializer_class        = UserSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,IsPrivateAllowed)

class MemberViewset(viewsets.ModelViewSet):

    queryset                = Members.objects.all()
    serializer_class        = MemberSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,IsPrivateAllowed)


class LoanViewset(viewsets.ModelViewSet):

    queryset                = Loan.objects.all()
    serializer_class        = LoanSerializer
    authentication_classes  = (JWTAuthentication,)
    permission_classes      = (IsAuthenticated,IsPrivateAllowed)



@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_user_details(request,phone):

    member_obj = Members.objects.get(phone=phone)
    serializer = MemberSerializer(member_obj)

    return Response({"Data":serializer.data})


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_total_actual_balance(request):

    balance = Members.objects.aggregate(Sum('balance'))

    return Response({"Actual Balance": balance})


@api_view(["POST"])
@permission_classes((IsAuthenticated,IsPrivateAllowed))
def apply_loan(request):

    balance = request.data.get('balance')
    loan_amount = request.data.get('loan_amount')
    member_phone = request.data.get('member_phone')

    mem_obj = Members.objects.get(phone=member_phone)
    sum = Members.objects.aggregate(Sum('balance'))

    if int(balance) > mem_obj.balance:
        return Response({"Error": "Member balance is less than the amount entered in the form"})
    if int(balance) + int(loan_amount) > sum['balance__sum']:
        return Response({"Error": "The total transaction amount exceeds the cumaltive balance of all members. Please enter a lesser loan amount"})
    
    loan_obj = Loan(member=mem_obj,balance=balance,loan_amount=loan_amount)
    loan_obj.save()
    
    mem_obj.balance = -int(loan_amount)
    mem_obj.save()

    mem_current_balance = Members.objects.get(phone=member_phone).balance

    response_str = f"Loan was processed with Balance of {balance} and loan amount of {loan_amount}. Current balance is {mem_current_balance}"

    return Response({"Success":response_str})


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def current_member_stat(request):
    
    member_stats = {}
    mem_obj = Members.objects.all()

    for member in mem_obj:
        member_stats[member.get_name()] = member.balance
    
    balance = Members.objects.aggregate(Sum('balance'))
    
    member_stats["Total"] = balance

    return Response(member_stats)