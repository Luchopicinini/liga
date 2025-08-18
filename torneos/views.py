from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Division, TablaPosiciones, Partido, Jugador, Equipo

def home(request):
    divisiones = Division.objects.all()
    divisiones_partidos = []

    for division in divisiones:
        equipos = division.equipo_set.all()
        ultimos_resultados = Partido.objects.filter(
            fecha__lte=timezone.now(),
            equipo_local__in=equipos
        ).order_by('-fecha')[:5]

        proximos_partidos = Partido.objects.filter(
            fecha__gt=timezone.now(),
            equipo_local__in=equipos
        ).order_by('fecha')[:5]

        divisiones_partidos.append({
            'division': division,
            'ultimos_resultados': ultimos_resultados,
            'proximos_partidos': proximos_partidos
        })

    return render(request, 'torneos/home.html', {
        'divisiones_partidos': divisiones_partidos
    })

def ver_torneo(request):
    divisiones = Division.objects.all().order_by('nombre')
    divisiones_con_tabla = []

    for division in divisiones:
        equipos = division.equipo_set.all()
        tabla_division = list(TablaPosiciones.objects.filter(equipo__in=equipos))
        tabla_division.sort(key=lambda x: (x.puntos, x.diferencia_goles, x.goles_favor), reverse=True)
        divisiones_con_tabla.append({'division': division, 'tabla': tabla_division})

    return render(request, 'torneos/torneo.html', {'divisiones_con_tabla': divisiones_con_tabla})

def tabla_division(request, division_id):
    division = get_object_or_404(Division, id=division_id)
    equipos = division.equipo_set.all()
    tabla = list(TablaPosiciones.objects.filter(equipo__in=equipos))
    tabla.sort(key=lambda x: (x.puntos, x.diferencia_goles, x.goles_favor), reverse=True)

    return render(request, 'torneos/tabla_division.html', {
        'division': division,
        'tabla': tabla
    })

def goleadores(request):
    divisiones = Division.objects.all().order_by('nombre')
    divisiones_con_jugadores = []

    for division in divisiones:
        jugadores = Jugador.objects.filter(equipo__division=division).order_by('-goles')
        divisiones_con_jugadores.append({
            'division': division,
            'jugadores': jugadores
        })

    return render(request, 'torneos/goleadores.html', {
        'divisiones_con_jugadores': divisiones_con_jugadores
    })

def partidos(request):
    divisiones = Division.objects.all()
    divisiones_partidos = []

    for division in divisiones:
        equipos = division.equipo_set.all()
        ultimos_resultados = Partido.objects.filter(
            fecha__lte=timezone.now(),
            equipo_local__in=equipos
        ).order_by('-fecha')[:5]

        proximos_partidos = Partido.objects.filter(
            fecha__gt=timezone.now(),
            equipo_local__in=equipos
        ).order_by('fecha')[:5]

        divisiones_partidos.append({
            'division': division,
            'ultimos_resultados': ultimos_resultados,
            'proximos_partidos': proximos_partidos
        })

    return render(request, 'torneos/partidos.html', {
        'divisiones_partidos': divisiones_partidos
    })
