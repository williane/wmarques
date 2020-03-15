from django.db import models


class Instituicao(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class TipoUser(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    instituicao = models.ForeignKey(Instituicao, on_delete=models.PROTECT)
    tipo = models.ForeignKey(TipoUser, null=True, blank=True, on_delete=models.PROTECT)
    nome = models.CharField(max_length=200)
    user = models.CharField(max_length=200, null=True, blank=True)
    cpf = models.CharField(max_length=200)
    email1 = models.CharField(max_length=200)
    email2 = models.CharField(max_length=200, null=True, blank=True)
    celular1 = models.CharField(max_length=50)
    celular2 = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(upload_to='usuario_photos', null=True, blank=True)

    def __str__(self):
        return self.nome


class Indicado_status(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class indicado(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    resp_indicacao = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    nome = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200, null=True, blank=True)
    documento = models.FileField(upload_to='doc_indicado', null=True, blank=True)
    status = models.ForeignKey(Indicado_status, null=True, blank=True, on_delete=models.PROTECT)
    valor_cotacao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_comissao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nome






