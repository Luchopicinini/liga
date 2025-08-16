from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# ------------------
# DIVISIONES
# ------------------
class Division(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# ------------------
# EQUIPOS
# ------------------
class Equipo(models.Model):
    nombre = models.CharField(max_length=50)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# ------------------
# JUGADORES
# ------------------
class Jugador(models.Model):
    nombre = models.CharField(max_length=50)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    goles = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

# ------------------
# PARTIDOS
# ------------------
class Partido(models.Model):
    fecha = models.DateField()
    hora = models.TimeField(null=True, blank=True)  # Nuevo campo
    cancha = models.CharField(max_length=100, null=True, blank=True)  # Nuevo campo
    equipo_local = models.ForeignKey(Equipo, related_name='locales', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='visitantes', on_delete=models.CASCADE)
    goles_local = models.PositiveIntegerField(default=0)
    goles_visitante = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"

# ------------------
# TABLA DE POSICIONES (MANUAL)
# ------------------
class TablaPosiciones(models.Model):
    equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE)
    partidos_jugados = models.PositiveIntegerField(default=0)
    ganados = models.PositiveIntegerField(default=0)
    empatados = models.PositiveIntegerField(default=0)
    perdidos = models.PositiveIntegerField(default=0)
    goles_favor = models.PositiveIntegerField(default=0)
    goles_contra = models.PositiveIntegerField(default=0)

    @property
    def diferencia_goles(self):
        return self.goles_favor - self.goles_contra

    @property
    def puntos(self):
        return self.ganados * 3 + self.empatados

    def __str__(self):
        return f"{self.equipo.nombre} - {self.puntos} pts"

receiver(post_save, sender=Partido)
def actualizar_tabla_post_partido(sender, instance, **kwargs):
    # Actualizamos tabla del equipo local y visitante
    for equipo in [instance.equipo_local, instance.equipo_visitante]:
        tabla, created = TablaPosiciones.objects.get_or_create(equipo=equipo)
        tabla.actualizar_tabla()