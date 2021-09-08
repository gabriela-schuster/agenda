from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Categoria(models.Model):
	nome = models.CharField(max_length=255)

	def __str__(self):
		return self.nome


class Contato(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	nome = models.CharField(max_length=225)
	sobrenome = models.CharField(max_length=225, blank=True)
	telefone = models.CharField(max_length=225)
	email = models.CharField(max_length=225, blank=True)
	data_criacao = models.DateField(default=timezone.now)
	descricao = models.TextField(blank=True)
	categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
	mostrar = models.BooleanField(default=True)
	foto = models.ImageField(blank=True, upload_to='fotos/%Y/%m/')

	def __str__(self):
		return self.nome
