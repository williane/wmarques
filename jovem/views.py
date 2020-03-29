from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db.models import Avg, Count, Min, Sum
from .models import Instituicao, Usuario, indicado, Indicado_status
from .forms import InstituicaoForm, UsuarioForm, IndicadoForm, IndicadoForm2
from random import choice
import smtplib
from email.mime.text import MIMEText


def gerador_senha(tamanho):
    caracteres = "0123456789abcdefghijklmnopqrstuwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@!#$%&*()_+}{`^?;:>/-+.,"
    senha = ""
    for i in range(tamanho):
        senha += choice(caracteres)
    return senha


@login_required
def index(request):
    usu = get_object_or_404(Usuario, user=request.user)
    indicados = indicado.objects.all()
    fechadas = indicado.objects.filter(status__id=2)
    pendentes = indicado.objects.filter(status__id=1)
    jovens = Usuario.objects.all()

    urls = request.build_absolute_uri().find('/', 8)+1
    final_url = request.build_absolute_uri()[:urls]

    if usu.tipo.nome == 'jovem' or usu.tipo.nome == 'instituiçao':
        return render(request, 'acompanhar_status.html', {'usu': usu})
    return render(request, 'index.html', {'usu': usu, 'indicados': indicados, 'fechadas': fechadas,
                                          'pendentes': pendentes, 'jovens': jovens, 'final_url': final_url})


@login_required
def indicado_update(request, id):
    indicados = get_object_or_404(indicado, pk=id)
    form = IndicadoForm2(request.POST or None, request.FILES or None, instance=indicados)
    usu = get_object_or_404(Usuario, user=request.user)

    if form.is_valid():
        form.save()
        return redirect('index')

    return render(request, 'form_indicado_update.html', {'form': form, 'usu': usu})


@login_required
def profile(request):
    usu = get_object_or_404(Usuario, user=request.user)
    return render(request, 'profile.html', {'usu': usu})


@login_required
def acompanhar_status(request):
    usu = get_object_or_404(Usuario, user=request.user)
    indicados = indicado.objects.filter(resp_indicacao=usu)
    valor = indicado.objects.filter(resp_indicacao=usu).aggregate(Sum('valor_comissao')).get('valor_comissao__sum', 0.00)
    nome = usu.nome.replace(" ", "-").lower()
    urls = request.build_absolute_uri().find('/', 8)
    final_url = request.build_absolute_uri()[:urls]

    return render(request, 'acompanhar_status.html', {'usu': usu, 'indicados': indicados, 'valor': valor, 'nome': nome,
                                                      'final_url': final_url})


@login_required
def form_user(request):
    form = UsuarioForm(request.POST or None, request.FILES or None)
    form2 = UserCreationForm(request.POST or None, request.FILES or None)
    usu = get_object_or_404(Usuario, user=request.user)
    senha = gerador_senha(10)
    validar = 'Validar'

    if form2.is_valid():
        if form.is_valid():
            print(form.cleaned_data['tipo'])
            if str(form.cleaned_data['tipo']) != 'instituição':
                if form.cleaned_data['cpf'] is None or form.cleaned_data['email1'] is None or \
                        form.cleaned_data['celular1'] is None:
                    return render(request, 'form_user.html', {'form': form, 'form2': form2, 'usu': usu, 'senha': senha,
                                                              'validar': validar})
                else:
                    post1 = form2.save(commit=False)
                    post1.save()
                    post = form.save(commit=False)
                    post.user = form2.cleaned_data['username']
                    post.save()
                    email = form.cleaned_data['email1']
                    body = '<p> Olá {},</p> <p> Você esta cadastrado para o projeto de indicações da seguradora WAssis,' \
                           'segue abaixo seu usuario e senha:</p><br><p> usuario: {}</p> <p>Senha: {}</p><br>' \
                           '<p>Entre atraves deste link: https://wassis.herokuapp.com/jovem/</p>'

                    if email:
                        send_email(request, body.format(form.cleaned_data['nome'], form2.cleaned_data['username'],
                                                        form2.cleaned_data['password1']), email)
                    return redirect('usuario_list')
            else:
                post1 = form2.save(commit=False)
                post1.save()
                post = form.save(commit=False)
                post.user = form2.cleaned_data['username']
                post.save()
                email = form.cleaned_data['email1']
                body = '<p> Olá {},</p> <p> Você esta cadastrado para o projeto de indicações da seguradora WAssis,' \
                   'segue abaixo seu usuario e senha:</p><br><p> usuario: {}</p> <p>Senha: {}</p><br>' \
                   '<p>Entre atraves deste link: https://wassis.herokuapp.com/jovem/</p>'

                if email:
                    send_email(request, body.format(form.cleaned_data['nome'], form2.cleaned_data['username'],
                                                form2.cleaned_data['password1']), email)
                return redirect('usuario_list')

    return render(request, 'form_user.html', {'form': form, 'form2': form2, 'usu': usu, 'senha': senha})


@login_required
def form_instituicao(request):
    form = InstituicaoForm(request.POST or None, request.FILES or None)
    usu = get_object_or_404(Usuario, user=request.user)

    if form.is_valid():
        form.save()
        return redirect('instituicao_list')

    return render(request, 'form_instituicao.html', {'form': form, 'usu': usu})



def indicacao(request, id, nome):
    form = IndicadoForm(request.POST or None, request.FILES or None)
    usu = get_object_or_404(Usuario, pk=id)
    status = get_object_or_404(Indicado_status, pk=1)

    if form.is_valid():
        post1 = form.save(commit=False)
        post1.resp_indicacao = usu
        post1.status = status
        post1.save()
        return redirect('https://www.wassis.com.br/obrigado.html')
    return render(request, 'indicacao.html', {'form': form, 'usu': usu})


@login_required
def instituicao_list(request):
    inst = Instituicao.objects.all()
    usu = get_object_or_404(Usuario, user=request.user)
    return render(request, 'instituicao.html', {'inst': inst, 'usu': usu})


@login_required
def usuario_list(request):
    inst = Usuario.objects.all()
    usu = get_object_or_404(Usuario, user=request.user)
    return render(request, 'usuario.html', {'inst': inst, 'usu': usu})


@login_required
def usuario_update(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    form = UsuarioForm(request.POST or None, request.FILES or None, instance=usuario)
    usu = get_object_or_404(Usuario, user=request.user)

    if form.is_valid():
        form.save()
        return redirect('usuario_list')

    return render(request, 'form_user_update.html', {'form': form, 'usu': usu})


@login_required
def instituicao_update(request, id):
    usuario = get_object_or_404(Instituicao, pk=id)
    form = InstituicaoForm(request.POST or None, request.FILES or None, instance=usuario)
    usu = get_object_or_404(Usuario, user=request.user)

    if form.is_valid():
        form.save()
        return redirect('instituicao_list')

    return render(request, 'form_instituicao.html', {'form': form, 'usu': usu})


@login_required
def send_email(request, body, email):
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    # username ou email para logar no servidor
    username = 'wassis.teste@gmail.com'
    password = 'Wassis2020'

    from_addr = 'wassis.teste@gmail.com'
    to_addrs = [email]

    # a biblioteca email possuí vários templates
    # para diferentes formatos de mensagem
    # neste caso usaremos MIMEText para enviar
    # somente texto
    message = MIMEText(body, _subtype='html')
    message['subject'] = 'Hello'
    message['from'] = from_addr
    message['to'] = ', '.join(to_addrs)

    # conectaremos de forma segura usando SSL
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    # para interagir com um servidor externo precisaremos
    # fazer login nele
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, message.as_string())
    server.quit()

    return redirect('instituicao_list')


@login_required
def form_resetpassword(request):
    usu = get_object_or_404(Usuario, user=request.user)

    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your Password Changed", extra_tags='green')
            return redirect('acompanhar_status')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'form_resetpwr.html', {'form': form, 'usu': usu})