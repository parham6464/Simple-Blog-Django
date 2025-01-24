from django.urls import path
from .import views
from .views import  showhome , showdetail1 , addlike , filtercat , searchresult


urlpatterns = [
    path('home/' , showhome , name='home'),
    path('home/<int:id>/' , showdetail1 , name='showdetail'),
    path('home/like/<int:id>/' , addlike , name='addlike'),
    path('home/<slug:category>/' , filtercat , name='filtercat'),
    path('home/search/result' , searchresult , name='searchresult'),
]
