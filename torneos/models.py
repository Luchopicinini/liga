# ===============================
# MODELOS
# ===============================
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# ------------------
# DIVISIONES
# ------------------
class Division(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        ordering = ['nombre']  # Orden alfabético

    def __str__(self):
        return self.nombre


# ------------------
# EQUIPOS
# ------------------
class Equipo(models.Model):
    nombre = models.CharField(max_length=50)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    class Meta:
        ordering = ['division__nombre', 'nombre']  # Orden admin y consultas

    def __str__(self):
        return self.nombre


# ------------------
# JUGADORES
# ------------------
class Jugador(models.Model):
    nombre = models.CharField(max_length=50)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    goles = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['equipo__division__nombre', 'equipo__nombre', '-goles']

    def __str__(self):
        return self.nombre


# ------------------
# PARTIDOS
# ------------------
class Partido(models.Model):
    fecha = models.DateField()
    hora = models.TimeField(null=True, blank=True)
    cancha = models.CharField(max_length=100, null=True, blank=True)
    equipo_local = models.ForeignKey(Equipo, related_name='locales', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='visitantes', on_delete=models.CASCADE)
    goles_local = models.PositiveIntegerField(default=0)
    goles_visitante = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-fecha', 'hora']

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"


# ------------------
# TABLA DE POSICIONES
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

    def actualizar_tabla(self):
        # Reiniciar valores
        self.partidos_jugados = 0
        self.ganados = 0
        self.empatados = 0
        self.perdidos = 0
        self.goles_favor = 0
        self.goles_contra = 0

        partidos = Partido.objects.filter(
            models.Q(equipo_local=self.equipo) | models.Q(equipo_visitante=self.equipo)
        )

        for partido in partidos:
            if partido.equipo_local == self.equipo:
                gf = partido.goles_local
                gc = partido.goles_visitante
            else:
                gf = partido.goles_visitante
                gc = partido.goles_local

            self.partidos_jugados += 1
            self.goles_favor += gf
            self.goles_contra += gc

            if gf > gc:
                self.ganados += 1
            elif gf == gc:
                self.empatados += 1
            else:
                self.perdidos += 1

        self.save()

    class Meta:
        ordering = ['equipo__division__nombre', '-ganados', '-goles_favor', 'equipo__nombre']

    def __str__(self):
        return f"{self.equipo.nombre} - {self.puntos} pts"


# ------------------
# SIGNAL: actualizar tabla post partido
# ------------------
@receiver(post_save, sender=Partido)
def actualizar_tabla_post_partido(sender, instance, **kwargs):
    for equipo in [instance.equipo_local, instance.equipo_visitante]:
        tabla, created = TablaPosiciones.objects.get_or_create(equipo=equipo)
        tabla.actualizar_tabla()
