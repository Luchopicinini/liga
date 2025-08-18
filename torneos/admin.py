from django.contrib import admin
from .models import Division, Equipo, Jugador, Partido, TablaPosiciones

# ===============================
# Admin de Divisiones
# ===============================
@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    ordering = ('nombre',)
    search_fields = ('nombre',)


# ===============================
# Admin de Equipos
# ===============================
@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'division')
    list_filter = ('division',)
    search_fields = ('nombre',)
    ordering = ('division__nombre', 'nombre')
    list_display_links = ('nombre',)

    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'division')
        }),
    )


# ===============================
# Admin de Jugadores
# ===============================
@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'equipo', 'goles')
    list_filter = ('equipo__division', 'equipo')
    search_fields = ('nombre',)
    ordering = ('equipo__division__nombre', 'equipo__nombre', '-goles')
    list_display_links = ('nombre',)

    fieldsets = (
        ('Datos del Jugador', {
            'fields': ('nombre', 'equipo', 'goles')
        }),
    )


# ===============================
# Admin de Partidos
# ===============================
@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = (
        'fecha', 'hora', 'cancha',
        'equipo_local', 'equipo_visitante',
        'goles_local', 'goles_visitante'
    )
    list_filter = ('equipo_local__division', 'equipo_visitante__division', 'fecha')
    search_fields = ('equipo_local__nombre', 'equipo_visitante__nombre')
    ordering = ('-fecha', 'hora')
    list_display_links = ('equipo_local', 'equipo_visitante')

    fieldsets = (
        ('Detalles del Partido', {
            'fields': (
                'fecha', 'hora', 'cancha',
                'equipo_local', 'equipo_visitante',
                'goles_local', 'goles_visitante'
            )
        }),
    )


# ===============================
# Admin de Tabla de Posiciones
# ===============================
@admin.register(TablaPosiciones)
class TablaPosicionesAdmin(admin.ModelAdmin):
    list_display = (
        'equipo', 'partidos_jugados', 'ganados',
        'empatados', 'perdidos', 'goles_favor',
        'goles_contra', 'diferencia_goles', 'puntos'
    )
    list_filter = ('equipo__division',)
    search_fields = ('equipo__nombre',)
    ordering = ('equipo__division__nombre', '-ganados', '-goles_favor', 'equipo__nombre')
    list_display_links = ('equipo',)

    fieldsets = (
        ('Resumen de Posiciones', {
            'fields': (
                'equipo', 'partidos_jugados', 'ganados',
                'empatados', 'perdidos', 'goles_favor',
                'goles_contra'
            )
        }),
    )

    # Campos calculados
    def diferencia_goles(self, obj):
        return obj.goles_favor - obj.goles_contra
    diferencia_goles.admin_order_field = 'goles_favor'
    diferencia_goles.short_description = 'Dif. Goles'

    def puntos(self, obj):
        return obj.ganados * 3 + obj.empatados
    puntos.admin_order_field = 'ganados'
    puntos.short_description = 'Puntos'


# ===============================
# Personalización del panel Admin
# ===============================
admin.site.site_header = "⚽ Liga San José - Panel Admin"
admin.site.site_title = "Liga San José"
admin.site.index_title = "Bienvenido al Panel de Administración"
