from django.forms import ModelForm
from .models import Instituicao, Usuario, indicado


class InstituicaoForm(ModelForm):
    class Meta:
        model = Instituicao
        fields = ['nome']


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['instituicao', 'tipo', 'nome', 'cpf', 'email1', 'email2', 'celular1', 'celular2', 'photo']


class IndicadoForm(ModelForm):
    class Meta:
        model = indicado
        fields = ['nome', 'email', 'telefone', 'documento']


class IndicadoForm2(ModelForm):
    class Meta:
        model = indicado
        fields = ['status', 'valor_cotacao', 'valor_comissao']