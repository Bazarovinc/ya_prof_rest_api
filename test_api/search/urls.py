from django.urls import path
from .views import NotesView

app_name = "search"

urlpatterns = [
    path('notes/', NotesView.as_view(), name='get_all_users'),
    path('notes/<int:pk>', NotesView.as_view(), name='get_id_user'),
]
