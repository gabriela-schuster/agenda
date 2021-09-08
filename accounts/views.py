from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def logout(req):
	auth.logout(req)
	return redirect('index')


def login(req):
	if req.method != 'POST':
		return render(req, 'accounts/login.html')

	usuario = req.POST.get('usuario')
	senha = req.POST.get('senha')

	user = auth.authenticate(req, username=usuario, password=senha)
	if not user:
		messages.error(req, 'Usuário ou senha inválidos')
	else:
		auth.login(req, user)
		messages.success(req, 'Login efetuado com sucesso')
		return redirect('index')


def cadastro(req):
	if req.method != 'POST':
		return render(req, 'accounts/cadastro.html')

	nome = req.POST.get('nome')
	sobrenome = req.POST.get('sobrenome')
	usuario = req.POST.get('usuario')
	email = req.POST.get('email')
	senha = req.POST.get('senha')
	senha2 = req.POST.get('senha2')

	try:
		validate_email(email)
	except:
		messages.error(req, 'Email inválido')
		return render(req, 'accounts/cadastro.html')

	messages_list = handle_cadastro(usuario=usuario, email=email, senha=senha, senha2=senha2, nome=nome, sobrenome=sobrenome)
	if len(messages_list) != 0:
		for message in messages_list:
			messages.error(req, message)
		return render(req, 'accounts/cadastro.html')

	messages.success(req, 'Registro efetuado com sucesso')
	user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
	user.save()
	user_login = auth.authenticate(req, username=usuario, password=senha)
	auth.login(req, user_login)
	return redirect('index')


@login_required(redirect_field_name='login')
def dashboard(req):
	return render(req, 'accounts/dashboard.html')


#? ---------------- not views: 


def handle_cadastro(usuario, email, senha, senha2, nome, sobrenome):
	messages_list = []

	if not nome or not sobrenome or not usuario or not email or not senha or not senha2:
		messages_list.append('Por favor, preencha todos os campos')

	if len(senha) < 6 or len(senha) > 50:
		messages_list.append('Senha precisa ter entre 6 e 50 caracteres')
	if len(usuario) < 6:
		messages_list.append('Usuário precisa ser maior que 6 caracteres')
	if senha != senha2:
		messages_list.append('As senhas precisam ser iguais')

	if User.objects.filter(username=usuario).exists():
		messages_list.append('Usuário já cadastrado')
	if User.objects.filter(email=email).exists():
		messages_list.append('Email já cadastrado')

	return messages_list
