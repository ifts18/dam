#!/usr/bin/env python
# coding: utf-8

import pilasengine
import random

pilas = pilasengine.iniciar()

# Variables y Constantes
monos = []
tiempo = 6
fin_de_juego = False

# Funciones

def crear_mono():
    enemigo = pilas.actores.Mono()
    enemigo.escala = 0
    pilas.utils.interpolar(enemigo, 'escala', 0.5, duracion=0.5)
    enemigo.aprender(pilas.habilidades.PuedeExplotar)

    x = random.randrange(-320, 320)
    y = random.randrange(-240, 240)

    if x >= 0 and x <= 100:
        x = 180
    elif x <= 0 and x >= -100:
        x = -180

    if y >= 0 and y <= 100:
        y = 180
    elif y <= 0 and y >= -100:
        y = -180

    enemigo.x = x
    enemigo.y = y

    tipo_interpolacion = ['lineal',
                          'aceleracion_gradual',
                          'desaceleracion_gradual',
                          'rebote_inicial',
                          'rebote_final'
                        ]

    pilas.utils.interpolar(enemigo, 'x', 0, tiempo)
    pilas.utils.interpolar(enemigo, 'y', 0, tiempo)

    monos.append(enemigo)

    if fin_de_juego:
        return False
    else:
        return True


def mono_destruido(disparo, enemigo):
    enemigo.eliminar()
    disparo.eliminar()

    puntos.escala = 0
    pilas.utils.interpolar(puntos, 'escala', 1, duracion=0.5)
    puntos.aumentar(1)

def perder(torreta, enemigo):
    global fin_de_juego

    enemigo.sonreir()
    torreta.eliminar()

    fin_de_juego = True
    pilas.avisar("PERDISTE! Conseguiste {} puntos".format(puntos.obtener()))

# Usar fondo estándar
pilas.fondos.Pasto()

# Añadir un marcador
puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.blanco)
puntos.magnitud = 40

# Añadimos el conmutador de sonido
pilas.actores.Sonido()

# Agregamos la torreta del jugador
torreta = pilas.actores.Torreta(enemigos=monos,
                                cuando_elimina_enemigo=mono_destruido)

# Agregamos un mono enemigo cada 1 segundo
pilas.tareas.agregar(1, crear_mono)

pilas.colisiones.agregar(torreta, monos, perder)

# Arrancamos el juego
pilas.ejecutar()
