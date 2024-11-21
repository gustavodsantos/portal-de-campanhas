from django.urls import path

from mysite.base import views

app_name = 'base'

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('desafios/', views.listar_desafios, name='listar_desafios'),
    path('desafios/<int:id>/', views.detalhes_desafio, name='detalhes_desafio'),
    path('desafios/<int:id>/aceitar/', views.aceitar_desafio, name='aceitar_desafio'),
    path('desafios/atribuidos/', views.visualizar_desafios_atribuidos, name='visualizar_desafios_atribuidos'),
    path('logged_out/', views.logged_out, name='logged_out'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
]
