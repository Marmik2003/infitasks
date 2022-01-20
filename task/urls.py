from django.urls import path
from .views import ListView, DeleteItem, AddItem, CompleteItem, StartOver

urlpatterns = [
    path('', ListView.as_view()),
    path('delete/<int:id>', DeleteItem.as_view()),
    path('add', AddItem.as_view()),
    path('complete/<int:id>', CompleteItem.as_view()),
    path('start_over', StartOver.as_view())
]