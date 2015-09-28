#!/usr/bin/env python
# coding: utf-8

import pilasengine
import random

pilas = pilasengine.iniciar()


class PantallaBienvenida(pilasengine.escenas.Escena):
    def iniciar(self, mensaje):
        self.fondo = self.pilas.fondos.Selva()
        self.texto = pilas.actores.Texto(mensaje)
        self.texto.y = 150
        boton = pilas.interfaz.Boton("Empezar el juego")
        boton.conectar(self._arrancar_juego)

    def _arrancar_juego(self):
        self.pilas.escenas.EscenaJuego()


class EscenaJuego(pilasengine.escenas.Escena):
    def iniciar(self):
        self.pilas.fondos.Pasto()
        self.monos = []
        self.tiempo = 6
        self.puntos = pilas.actores.Puntaje(x=230, y=200,
                                            color=pilas.colores.blanco)
        self.puntos.magnitud = 40
        self.pilas.actores.Sonido()

        self.torreta = pilas.actores.Torreta(enemigos=self.monos,
                                    cuando_elimina_enemigo=self._mono_destruido)

        # Agregamos un mono enemigo cada 1 segundo
        self.pilas.tareas.agregar(1, self._crear_mono)
        self.pilas.colisiones.agregar(self.torreta, self.monos, self._perder)
        self.fin_de_juego = False

    def _crear_mono(self):
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

        pilas.utils.interpolar(enemigo, 'x', 0, self.tiempo)
        pilas.utils.interpolar(enemigo, 'y', 0, self.tiempo)

        self.monos.append(enemigo)

        if self.fin_de_juego:
            return False
        else:
            return True

    def _mono_destruido(self, disparo, enemigo):
        enemigo.eliminar()
        disparo.eliminar()

        self.puntos.escala = 0
        pilas.utils.interpolar(self.puntos, 'escala', 1, duracion=0.5)
        self.puntos.aumentar(1)

    def _perder(self):
        self.fin_de_juego = True
        self.pilas.tareas.eliminar_todas()
        for mono in self.monos:
            mono.sonreir()
        self.torreta.eliminar()
        self.pilas.escenas.EscenaFin(self.puntos.obtener())


class EscenaFin(pilasengine.escenas.Escena):
    def iniciar(self, puntaje):
        self.pilas.fondos.Selva()
        mensaje = "PERDISTE! Hiciste {} puntos.".format(puntaje)
        self.texto = pilas.actores.Texto(mensaje)
        boton = pilas.interfaz.Boton("Volver a intentarlo")
        boton.y = 100
        boton.conectar(self._arrancar_juego)
        salir = pilas.interfaz.Boton("Salir")
        salir.y = -100
        salir.conectar(self._salir)

    def _arrancar_juego(self):
        self.pilas.escenas.EscenaJuego()

    def _salir(self):
        pilas.terminar()

pilas.escenas.vincular(PantallaBienvenida)
pilas.escenas.vincular(EscenaJuego)
pilas.escenas.vincular(EscenaFin)
pilas.escenas.PantallaBienvenida("Bienvenido...")

# Arrancamos el juego
pilas.ejecutar()
