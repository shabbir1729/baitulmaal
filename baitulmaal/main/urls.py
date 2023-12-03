from django.urls import path,include
from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

apiRouter = routers.DefaultRouter()

apiRouter.register(r'user', UserViewSet, basename="users")
apiRouter.register(r'members', MemberViewset, basename='members')



urlpatterns = [
    path('api/', include(apiRouter.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/member/<int:phone>/details', get_user_details,name='get-user-details'),
    path('api/get-actual-balance',get_total_actual_balance,name='get-actual-balance'),
    path('api/apply-loan/',apply_loan,name='apply-loan'),
    path('api/member-stat',current_member_stat,name='member-stat'),


]