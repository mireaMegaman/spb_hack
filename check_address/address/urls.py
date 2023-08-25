from django.urls import path
from address.views import *
from . import views

urlpatterns = [
    path('', CheckTextView.as_view(), name='text'),
    path('file', CheckFileView.as_view(), name='file'),
    path('vslider', slider, name='project-menu'),
    path('vmegamen', megamen, name='megamen-team-page'),
    path('main', CheckTextView.as_view(), name='main-page'),
]