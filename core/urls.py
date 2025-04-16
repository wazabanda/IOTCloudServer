from django.contrib import admin
from django.urls import path, include, reverse_lazy
from .views import HomeView, DeviceData, GPIOPinCreateView, GPIOPinDeleteView, ProfileView, DeleteView
from . import device_views
from .models import ApiKey
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', HomeView.as_view(), name='home-view'),
    path('accounts/profile/', ProfileView.as_view(), name='Profile-view'),
    
    # Device management URLs
    path('devices/', device_views.DeviceListView.as_view(), name='device_list'),
    path('devices/create/', device_views.DeviceCreateView.as_view(), name='device_create'),
    path('devices/<uuid:pk>/', device_views.DeviceDetailView.as_view(), name='device'),
    path('devices/<int:pk>/update/', device_views.DeviceUpdateView.as_view(), name='device_update'),
    path('devices/<int:pk>/delete/', device_views.DeviceDeleteView.as_view(), name='device_delete'),
    
    # GPIO Pin management
    path('gpio/add/', GPIOPinCreateView.as_view(), name='add_gpio_pin'),
    path('gpio/<int:pk>/delete/', GPIOPinDeleteView.as_view(), name='delete_gpio_pin'),
    
    # Profile management URLs
    path('profile/', ProfileView.as_view(), name='profile'),
    path('api-key/delete/<int:pk>/', login_required(DeleteView.as_view(
        model=ApiKey,
        success_url=reverse_lazy('profile'),
        template_name='core/confirm_delete.html'
    )), name='delete_api_key'),
]
