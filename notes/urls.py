from django.urls import path, include
from .views import *

urlpatterns = [
    path('upload_note/', upload_note_view, name='upload_note'),
    path('history/', history_view, name='history'),
    path('note/<int:note_id>/', note_view, name='note_view'),
    path('ask_doubt/<int:note_id>/', ask_doubt_view, name='ask_doubt'),
    path('delete_note/<int:note_id>/', delete_note_view, name='delete_note'),
]
