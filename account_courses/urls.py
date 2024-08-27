from django.urls import path
from .views import *

app_name = 'account_courses'

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='search'),
]
