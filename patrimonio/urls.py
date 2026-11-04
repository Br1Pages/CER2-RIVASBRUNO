from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from catalogo import views

urlpatterns = [
    # Páginas públicas
    path("", views.inicio, name="inicio"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("categoria/<int:categoria_id>/", views.por_categoria, name="por_categoria"),
    path("lugar/<int:lugar_id>/", views.detalle, name="detalle"),
    # Inicio y cierre de sesión, ya hechos por Django
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Área de gestión
    path("gestion/", views.gestion, name="gestion"),
    path("gestion/agregar/", views.agregar, name="agregar"),
    path("gestion/editar/<int:lugar_id>/", views.editar, name="editar"),
    # Panel de administración de Django
    path("admin/", admin.site.urls),
]
