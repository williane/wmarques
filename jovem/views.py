from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db.models import Avg, Count, Min, Sum
from .models import Instituicao, Usuario, indicado, Indicado_status, Textos
from .forms import InstituicaoForm, UsuarioForm, IndicadoForm, IndicadoForm2, TextoForm
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
    declinadas = indicado.objects.filter(status__id=3)
    jovens = Usuario.objects.all()

    urls = request.build_absolute_uri().find('/', 8)+1
    final_url = request.build_absolute_uri()[:urls]

    if usu.tipo.nome == 'jovem' or usu.tipo.nome == 'instituiçao':
        return render(request, 'acompanhar_status.html', {'usu': usu})
    return render(request, 'index.html', {'usu': usu, 'indicados': indicados, 'fechadas': fechadas,
                                          'pendentes': pendentes,'declinadas': declinadas, 'jovens': jovens,
                                          'final_url': final_url})


@login_required
def indicado_update(request, id):
    indicados = get_object_or_404(indicado, pk=id)
    form = IndicadoForm2(request.POST or None, request.FILES or None, instance=indicados)
    usu = get_object_or_404(Usuario, user=request.user)

    if form.is_valid():
        form.save()
        if str(form.cleaned_data['status']) == 'Fechado':
            email_jovem = get_object_or_404(Textos, descricao='Seguro Fechado - Jovem')
            email_indicado = get_object_or_404(Textos, descricao='Seguro Fechado - Indicado')
            body = email_jovem.texto
            send_email(request, body.format(usu.nome, indicados.nome), indicados.resp_indicacao.email1)
            body = email_indicado.texto
            send_email(request, body.format(indicados.nome), indicados.email)

        if str(form.cleaned_data['status']) == 'Declinado':
            email_jovem = get_object_or_404(Textos, descricao='Seguro Declinado - Jovem')
            email_indicado = get_object_or_404(Textos, descricao='Seguro Declinado - Indicado')
            body = email_jovem.texto
            send_email(request, body.format(usu.nome, indicados.nome), indicados.resp_indicacao.email1)
            body = email_indicado.texto
            send_email(request, body.format(indicados.nome, usu.nome), indicados.email)

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
    texto = get_object_or_404(Textos, descricao='Cadastro novo Usuario')
    txt = texto.texto

    print(txt)

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
                    body = txt

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
                body = txt

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
    email_wassis = get_object_or_404(Textos, descricao='nova indicação - WAssis')
    email_jovem = get_object_or_404(Textos, descricao='nova indicação - Jovem')
    email_indicado = get_object_or_404(Textos, descricao='nova indicação - Indicado')

    try:
        if str(usu.tipo) == 'jovem':
            texto = get_object_or_404(Textos, pk=1)

        if str(usu.tipo) == 'instituição':
            texto = get_object_or_404(Instituicao, nome=usu.instituicao.nome)

        txt = paragrafos(texto.texto)
    except Exception as e:
        txt = ''

    if form.is_valid():
        post1 = form.save(commit=False)
        post1.resp_indicacao = usu
        post1.status = status
        post1.save()
        body = email_wassis.texto
        send_email(request, body.format(usu.nome, form.cleaned_data['nome'], form.cleaned_data['email'],
                                        form.cleaned_data['telefone']), 'wassis@wassis.com.br')
        body = email_indicado.texto
        send_email(request, body.format(form.cleaned_data['nome'], usu.nome, usu.nome), form.cleaned_data['email'])
        body = email_jovem.texto
        send_email(request, body.format(usu.nome, form.cleaned_data['nome']), usu.email1)

        return redirect('https://www.wassis.com.br/obrigado.html')

    return render(request, 'indicacao.html', {'form': form, 'usu': usu, 'txt': txt})


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
    smtp_ssl_host = 'smtp.umbler.com'    #'smtp.gmail.com'
    smtp_ssl_port = 587                 # 465
    # username ou email para logar no servidor
    username = 'wassis@wassis.com.br'           #'wassis.teste@gmail.com'
    password = 'Was2507**'            #'Wassis2020'

    from_addr = 'wassis@wassis.com.br'
    to_addrs = [email]

    # a biblioteca email possuí vários templates
    # para diferentes formatos de mensagem
    # neste caso usaremos MIMEText para enviar
    # somente texto
    message = MIMEText(body, _subtype='html')
    message['subject'] = 'W.Assis - Corretora de Seguros'
    message['from'] = from_addr
    message['to'] = ', '.join(to_addrs)

    # conectaremos de forma segura usando SSL
    server = smtplib.SMTP(smtp_ssl_host, smtp_ssl_port)
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


@login_required
def texto_list(request):
    inst = Textos.objects.all()
    usu = get_object_or_404(Usuario, user=request.user)
    return render(request, 'textos.html', {'inst': inst, 'usu': usu})


@login_required
def textos_update(request, id):
    texto = get_object_or_404(Textos, pk=id)
    form = TextoForm(request.POST or None, request.FILES or None, instance=texto)
    usu = get_object_or_404(Usuario, user=request.user)

    if form.is_valid():
        form.save()
        return redirect('textos_list')

    return render(request, 'form_textos.html', {'form': form, 'usu': usu})


def paragrafos(txt):
    texto = txt

    p1_ini = texto.find('<p>') + 3
    p1_fim = texto.find('</p>', p1_ini)
    p2_ini = texto.find('<p>', p1_ini) + 3
    p2_fim = texto.find('</p>', p2_ini)
    p3_ini = texto.find('<p>', p2_fim) + 3
    p3_fim = texto.find('</p>', p3_ini)
    p4_ini = texto.find('<p>', p3_fim) + 3
    p4_fim = texto.find('</p>', p4_ini)

    p1 = texto[p1_ini:p1_fim]
    p2 = texto[p2_ini:p2_fim]
    p3 = texto[p3_ini:p3_fim]
    p4 = texto[p4_ini:p4_fim]

    paragrafo = [p1, p2, p3, p4]

    return paragrafo
