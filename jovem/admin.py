from django.contrib import admin
from .models import Instituicao, Usuario, TipoUser, indicado, Indicado_status, TipoTexto, Textos


admin.site.register(Instituicao)
admin.site.register(Usuario)
admin.site.register(TipoUser)
admin.site.register(indicado)
admin.site.register(Indicado_status)
admin.site.register(TipoTexto)
admin.site.register(Textos)
