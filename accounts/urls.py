from django.urls import path
from .import views
from .views import UpdateProfile



urlpatterns = [
    path('login/',views.login1 , name='login1'),
    # path('sign-up/',views.sign_up , name='signup1'),
    path('logout/' , views.log_out , name='logout1'),
]