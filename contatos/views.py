from accounts.forms import ContatoForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.contrib import messages
from django.db.models.functions import Concat

def index(req):
	user = req.user
	if str(user) != 'AnonymousUser':
		contatos = Contato.objects.all().order_by('-id').filter(mostrar = True, owner = user)
		paginator = Paginator(contatos, 5)
		page_number = req.GET.get('page')
		contatos = paginator.get_page(page_number)
		context = {
			'contatos': contatos
		}
		return render(req, 'contatos/index.html', context)
	else:
		return render(req, 'contatos/index.html')

def ver_contato(req, contato_id):
	# contato = Contato.objects.get(id=contato_id)
	contato = get_object_or_404(Contato, id=contato_id)

	if not contato.mostrar:
		raise Http404()

	context = {
		'contato': contato
	}
	return render(req, 'contatos/ver_contato.html', context)


def busca(req):
	termo = req.GET.get('termo')
	if termo is None or not termo:
		messages.add_message(req, messages.WARNING, 'Este campo não pode ficar vaio!')
		return redirect('index')

	campos = Concat('nome', Value(' '), 'sobrenome')
	contatos = Contato.objects.annotate(nome_completo=campos).filter(
		Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
	)
	#? search nome OR sobrenome (Q does that); __icontains is for searching 
	#? like values, like 'ia' in 'maria'

	paginator = Paginator(contatos, 5)
	page_number = req.GET.get('page')
	contatos = paginator.get_page(page_number)

	context = {'contatos': contatos}
	return render(req, 'contatos/busca.html', context)


def edit(req, contato_id):
	contato = Contato.objects.get(id=contato_id)
	form = ContatoForm(instance=contato)

	context = {
		'contato': contato,
		'form': form
	}
	if req.method != 'POST':
		return render(req, 'contatos/edit.html', context)
	form = ContatoForm(req.POST, instance=contato)

	if not form.is_valid:
		messages.error(req, 'formulário inválido')
		return render(req, 'contatos/edit.html')

	form.save()
	messages.success(req, f'contato de {req.POST.get("nome")} atualizado com sucesso')
	return render(req, 'contatos/edit.html', context)