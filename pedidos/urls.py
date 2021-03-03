from django.urls import path
from .views import *

urlpatterns = [
    path('', IntroPage),
    path('LongList', LongList),
    
    
]