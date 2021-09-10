from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('edit/<int:contato_id>', views.edit, name='edit'),
	# path('delete/', views.index, name='index'),
	path('busca/', views.busca, name='busca'),
	path('<int:contato_id>', views.ver_contato, name='ver_contato'),
]