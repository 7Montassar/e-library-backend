from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    ## Token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
