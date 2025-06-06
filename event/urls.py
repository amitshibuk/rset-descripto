from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/new/', views.create_event, name='create_event'),
    path('event/<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:pk>/delete/', views.delete_post, name='delete_event'),
    path('event/<int:pk>/approve/', views.approve_event, name='approve_event'),
    path('event/<int:pk>/reject/', views.reject_event, name='reject_event'),
    path('event/<int:pk>/update/', views.update_event, name='update_event'),
    path('event/<int:pk>/send-files/', views.send_event_files, name='send_event_files'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)