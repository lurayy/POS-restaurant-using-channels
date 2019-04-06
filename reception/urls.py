from django.urls import path,include
from . import views
urlpatterns = [
    path('staff',views.index , name="reception"),
    path('',views.index, name = "Menu presentation")
]
