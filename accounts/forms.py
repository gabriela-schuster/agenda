from django.forms import fields
from contatos.models import Contato
from django import forms


class ContatoForm(forms.ModelForm):
	class Meta:
		model = Contato
		# fields = ['owner', 'nome', 'sobrenome', 'telefone', 'email','descricao', 'categoria', 'mostrar', 'foto']
		exclude = ('owner', 'data_criacao')

	def __init__(self, *args, **kwargs):
		super(ContatoForm, self).__init__(*args, **kwargs)

		for name, field in self.fields.items():
			field.widget.attrs.update(
				{'class': 'input'}
			)