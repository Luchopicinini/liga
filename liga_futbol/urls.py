from django.contrib import admin
from django.urls import path
from torneos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('torneo/', views.ver_torneo, name='ver_torneo'),
    path('tabla/<int:division_id>/', views.tabla_division, name='tabla_division'),
    path('goleadores/', views.goleadores, name='goleadores'),  # NUEVO.
    path('partidos/', views.partidos, name='partidos'),

]
