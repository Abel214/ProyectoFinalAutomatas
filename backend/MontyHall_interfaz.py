import tkinter
from tkinter import *
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import random
import pygame
from introMontyHall import reproducir_video


class MontyHall_interfaz:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        # Rutas de imágenes
        self.ruta_imagen_puerta_animada = "files/Puerta_abierta.png"
        self.ruta_imagen_puerta_estatica = "files/Puerta_estatica.png"
        self.ruta_imagen_cabra = "files/Cabra.gif"
        self.ruta_imagen_carro = "files/carro.gif"
        self.ruta_imagen_presentador = "files/Presentador1.jpeg"

        # Estado del juego
        self.puerta_seleccionada = None
        self.animacion_actual = None
        self.juego_terminado = False
        self.ganadas = 0
        self.perdidas = 0
        # Inicializar el juego
        self._inicializar_juego()

        # Preparar fotogramas de animación
        self.fotogramas_cabra = self._cargar_fotogramas(self.ruta_imagen_cabra)
        self.fotogramas_carro = self._cargar_fotogramas(self.ruta_imagen_carro)

    def iniciar_video_audio(self):
        # Rutas de los archivos de video y audio
        ruta_video = r"files/TrailerMontyGameVideo.mp4"
        ruta_audio = r"files/TrailerMontyGameAudio.MP3"
        # Función para reproducir video y audio (debes implementarla)
        reproducir_video(ruta_video, ruta_audio)

    def _inicializar_juego(self):
        """Inicializar los elementos del juego Monty Hall"""
        # Definir puertas
        self.puertas = ['A', 'B', 'C']

        # Asignar premio aleatoriamente
        self.premio = random.randint(0, 2)

        # Inicializar premios
        self.back = ['Cabra', 'Cabra', 'Cabra']
        self.back[self.premio] = 'Carro'

        # Crear diccionario de premios por puerta
        self.picks = dict(zip(self.puertas, self.back))

        # Resetear estado del juego
        self.puerta_seleccionada = None
        self.juego_terminado = False

    def _cargar_fotogramas(self, ruta):
        """Cargar y redimensionar fotogramas de un GIF"""
        ancho_deseado = 133
        altura_deseada = 266
        fotogramas = []

        try:
            # Abrir el archivo GIF
            gif_imagen = Image.open(ruta)

            while True:
                # Redimensionar el fotograma actual
                fotograma_redimensionado = gif_imagen.copy().resize((ancho_deseado, altura_deseada),
                                                                    Image.Resampling.LANCZOS)
                # Convertir el fotograma a un objeto compatible con Tkinter
                fotogramas.append(ImageTk.PhotoImage(fotograma_redimensionado))
                # Avanzar al siguiente fotograma
                gif_imagen.seek(len(fotogramas))

        except EOFError:
            # Fin de los fotogramas
            pass
        except Exception as e:
            print(f"Error al cargar fotogramas de {ruta}: {e}")

        return fotogramas

    def _detener_animacion(self):
        """Detener la animación actual"""
        if self.animacion_actual is not None:
            self.v1.after_cancel(self.animacion_actual)
            self.animacion_actual = None

    def _calcular_porcentaje(self):
        """Calcular porcentaje de victorias"""
        total_juegos = self.ganadas + self.perdidas
        return (self.ganadas / total_juegos * 100) if total_juegos > 0 else 0

    def _animar_puerta(self, label, fotogramas, indice=0):
        """Animar una puerta con los fotogramas dados"""
        if label.winfo_exists():
            frame_actual = fotogramas[indice]
            label.config(image=frame_actual)
            indice = (indice + 1) % len(fotogramas)

            self._detener_animacion()

            self.animacion_actual = self.v1.after(300, self._animar_puerta, label, fotogramas, indice)
        else:
            print("La etiqueta ha sido destruida.")

    def _mostrar_premio(self, puerta_letra):
        """Mostrar el premio detrás de la puerta"""
        label = getattr(self, f'label_puerta{self.puertas.index(puerta_letra) + 1}')

        # Seleccionar fotogramas según el premio
        if self.picks[puerta_letra] == 'Carro':
            fotogramas = self.fotogramas_carro
        else:
            fotogramas = self.fotogramas_cabra

        # Detener cualquier animación que esté corriendo
        self._detener_animacion()

        # Reemplazar la imagen de la puerta por la del premio
        premio_img = fotogramas[0]  # Seleccionar la primera imagen del premio
        label.config(image=premio_img)

        # Si hay una animación, puedes iniciar la animación del premio
        if len(fotogramas) > 1:
            self._animar_puerta(label, fotogramas)

    def _cambiar_puerta(self, puerta_seleccionada, label):
        """Lógica para cambiar la puerta seleccionada"""
        ruta_audio_ganar = r"files/Win.MP3"
        ruta_audio_perder = r"files/Fail.MP3"
        ruta_audio_door = r"files/OpenDoor.MP3"

        # Si el juego ya terminó, preguntar si quiere jugar de nuevo
        if self.juego_terminado:
            respuesta = messagebox.askyesno("Juego Terminado", "¿Deseas jugar de nuevo?")
            if respuesta:
                self._inicializar_juego()
                self._restablecer_puertas()

                # Cambiar la imagen del presentador de vuelta a Presentador1
                presentador_imagen = Image.open("files/Presentador1.jpeg")
                presentador_imagen = presentador_imagen.resize((100, 150))  # Ajustar el tamaño si es necesario
                presentador_imagen_tk = ImageTk.PhotoImage(presentador_imagen)

                # Actualizar la imagen en el canvas
                self.canvas.create_image(10, 450, image=presentador_imagen_tk, anchor="nw")
                self.canvas.presentador_imagen_tk = presentador_imagen_tk  # Evitar que la imagen sea recolectada por el GC

            else:
                # Mensaje de despedida con estadísticas
                porcentaje_ganadas = self._calcular_porcentaje()
                despedida = (
                    "Gracias por jugar, ¡BAY BAY!\n\n"
                    f"Estadísticas finales:\n"
                    f"Ganadas: {self.ganadas}\n"
                    f"Perdidas: {self.perdidas}\n"
                    f"Porcentaje final de victorias: {porcentaje_ganadas:.2f}%"
                )
                messagebox.showinfo("Estadísticas", despedida)
                # Cerrar la ventana de Monty Hall
                self.v1.destroy()
                # Mostrar la ventana principal
                self.ventana_principal.deiconify()
            return

        # Convertir número de puerta a letra
        puerta_letra = self.puertas[puerta_seleccionada - 1]

        # Primera selección de puerta
        if self.puerta_seleccionada is None:
            # Mensaje inicial
            messagebox.showinfo("Monty Hall", f"Has seleccionado la puerta {puerta_letra}")

            # Recordar puerta seleccionada
            self.puerta_seleccionada = puerta_letra

            # Encontrar una puerta para abrir (que no sea la seleccionada y no tenga el premio)
            puertas_disponibles = [p for p in self.puertas if p != puerta_letra and self.picks[p] == 'Cabra']
            abrir_puerta = random.choice(puertas_disponibles)

            pygame.mixer.music.load(ruta_audio_door)  # Cargar audio de ganar
            pygame.mixer.music.play()  # Reproducir audio

            label = getattr(self, f'label_puerta{self.puertas.index(abrir_puerta) + 1}')

            # Seleccionar fotogramas según el contenido (siempre será cabra para el presentador)
            fotogramas = self.fotogramas_cabra

            # Detener cualquier animación que esté corriendo
            self._detener_animacion()

            # Reemplazar la imagen de la puerta por la del premio (caballo o cabra)
            premio_img = fotogramas[0]  # Seleccionar la primera imagen del premio
            label.config(image=premio_img)

            # Iniciar la animación si tiene más de un fotograma
            if len(fotogramas) > 1:
                self._animar_puerta(label, fotogramas)

            # Mensaje del presentador sobre la puerta abierta
            messagebox.showinfo("Monty Hall",
                                f"El presentador abrió la puerta {abrir_puerta} y mostró una {self.picks[abrir_puerta]}.")

            # Preguntar si desea cambiar de puerta
            cambiar = messagebox.askyesno("Monty Hall", "¿Deseas cambiar de puerta?")

            # Si cambia, seleccionar la otra puerta
            if cambiar:
                otras_puertas = [p for p in self.puertas if p != puerta_letra and p != abrir_puerta]
                puerta_letra = otras_puertas[0]
                puerta_seleccionada = self.puertas.index(puerta_letra) + 1

            # Mostrar premio
            self._mostrar_premio(puerta_letra)

            # Mostrar resultado final
            r = self.picks[puerta_letra]
            if r == 'Carro':
                pygame.mixer.music.load(ruta_audio_ganar)  # Cargar audio de ganar
                pygame.mixer.music.play()  # Reproducir audio
                messagebox.showinfo("¡Felicidades!", f"Tu premio es: {r}\n¡Ganaste el carro!")
                self.ganadas += 1  # Incrementar victorias
            else:
                # Cambiar la imagen del presentador a la imagen de perder
                presentador_imagen = Image.open("files/Presentador2.jpeg")
                presentador_imagen = presentador_imagen.resize((100, 150))  # Ajustar el tamaño si es necesario
                presentador_imagen_tk = ImageTk.PhotoImage(presentador_imagen)

                # Actualizar la imagen en el canvas
                self.canvas.create_image(10, 450, image=presentador_imagen_tk, anchor="nw")
                self.canvas.presentador_imagen_tk = presentador_imagen_tk  # Evitar que la imagen sea recolectada por el GC

                pygame.mixer.music.load(ruta_audio_perder)  # Cargar audio de perder
                pygame.mixer.music.play()  # Reproducir audio
                messagebox.showinfo("Lo siento", f"Tu premio es: {r}\nNo ganaste el carro.")
                self.perdidas += 1  # Incrementar derrotas
            porcentaje = self._calcular_porcentaje()
            self.label_estadisticas.config(
                text=f"Ganadas: {self.ganadas} | Perdidas: {self.perdidas} | % de victorias: {porcentaje:.2f}%")

            # Marcar juego como terminado
            self.juego_terminado = True

    def _restablecer_puertas(self):
        """Restablecer las puertas a su estado inicial"""
        # Detener cualquier animación en curso
        self._detener_animacion()

        # Restaurar imágenes de puertas a la imagen estática original
        self.label_puerta1.config(image=self.puerta1)
        self.label_puerta2.config(image=self.puerta2)
        self.label_puerta3.config(image=self.puerta3)

        # Restablecer eventos de clic
        self.label_puerta1.bind("<Button-1>", lambda e: self._cambiar_puerta(1, self.label_puerta1))
        self.label_puerta2.bind("<Button-1>", lambda e: self._cambiar_puerta(2, self.label_puerta2))
        self.label_puerta3.bind("<Button-1>", lambda e: self._cambiar_puerta(3, self.label_puerta3))

        # Restaurar cursor a "hand2"
        self.label_puerta1.config(cursor="hand2")
        self.label_puerta2.config(cursor="hand2")
        self.label_puerta3.config(cursor="hand2")

    def mostrar_perdida(self):
        """Actualizar la imagen del presentador cuando el jugador pierde"""
        # Cambiar la imagen del presentador a la de perder
        presentador_imagen_perdida = Image.open("files/Presentador2.jpeg")
        presentador_imagen_perdida = presentador_imagen_perdida.resize((100, 150))  # Ajustar tamaño si es necesario
        presentador_imagen_perdida_tk = ImageTk.PhotoImage(presentador_imagen_perdida)

        # Actualizar la imagen en el canvas
        pos_x_presentador = 10
        pos_y_presentador = 450  # Puedes ajustar esta posición si es necesario
        self.canvas.create_image(pos_x_presentador, pos_y_presentador, image=presentador_imagen_perdida_tk, anchor="nw")
        self.canvas.presentador_imagen_perdida_tk = presentador_imagen_perdida_tk  # Evitar que sea recolectada por el GC

        # Mostrar un mensaje de que el jugador ha perdido
        messagebox.showinfo("Monty Hall", "¡Perdiste! El presentador ahora cambia de imagen.")

    def abrir_ventana(self):
        """Abrir la ventana de Monty Hall"""
        # Ocultar la ventana principal
        self.ventana_principal.withdraw()

        # Crear la nueva ventana
        self.v1 = Toplevel(self.ventana_principal)
        self.v1.title("Monty Hall - Selecciona una puerta")
        self.v1.geometry("600x400")
        # Obtener el tamaño de la pantalla
        pantalla_ancho = self.v1.winfo_screenwidth()
        pantalla_alto = self.v1.winfo_screenheight()

        # Obtener el tamaño de la ventana de Monty Hall
        ventana_ancho = 800
        ventana_alto = 600

        # Calcular las coordenadas para centrar la ventana
        pos_x = (pantalla_ancho // 2) - (ventana_ancho // 2)
        pos_y = (pantalla_alto // 2) - (ventana_alto // 2)

        # Posicionar la ventana de Monty Hall en el centro de la pantalla
        self.v1.geometry(f"{ventana_ancho}x{ventana_alto}+{pos_x}+{pos_y}")
        # Crear el Canvas
        self.canvas = Canvas(self.v1, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        fondo_imagen = Image.open("files/Fondo.jpg")
        fondo_imagen = fondo_imagen.resize((800, 600))  # Ajustar tamaño de la imagen si es necesario
        fondo_imagen_tk = ImageTk.PhotoImage(fondo_imagen)

        # Cargar imagen del presentador
        presentador_imagen = Image.open("files/Presentador1.jpeg")
        presentador_imagen = presentador_imagen.resize((100, 150))  # Ajustar el tamaño si es necesario
        presentador_imagen_tk = ImageTk.PhotoImage(presentador_imagen)

        # Colocar la imagen de fondo en el canvas
        self.canvas.create_image(0, 0, image=fondo_imagen_tk, anchor="nw")
        self.canvas.fondo_imagen_tk = fondo_imagen_tk

        # Ajustar las coordenadas de la imagen del presentador
        pos_x_presentador = 10
        pos_y_presentador = 450  # Ajusta esta posición según lo necesites
        self.canvas.create_image(pos_x_presentador, pos_y_presentador, image=presentador_imagen_tk, anchor="nw")
        self.canvas.presentador_imagen_tk = presentador_imagen_tk  # Necesario para evitar que la imagen sea recolectada por el GC

        # Cargar imágenes de las puertas
        self.puerta1 = ImageTk.PhotoImage(Image.open(self.ruta_imagen_puerta_estatica).resize((133, 266)))
        self.puerta2 = ImageTk.PhotoImage(Image.open(self.ruta_imagen_puerta_estatica).resize((133, 266)))
        self.puerta3 = ImageTk.PhotoImage(Image.open(self.ruta_imagen_puerta_estatica).resize((133, 266)))

        # Posicionar las puertas
        x1, y1 = 133, 133  # Nueva posición para puerta 1
        x2, y2 = 333, 133  # Nueva posición para puerta 2
        x3, y3 = 532, 133  # Nueva posición para puerta 3
        self.puerta1_img = self.canvas.create_image(x1, y1, image=self.puerta1, anchor="nw")
        self.puerta2_img = self.canvas.create_image(x2, y2, image=self.puerta2, anchor="nw")
        self.puerta3_img = self.canvas.create_image(x3, y3, image=self.puerta3, anchor="nw")

        # Crear botón de Regresar
        boton_regresar = Button(self.v1, text="Regresar al Menú", command=self._regresar)
        boton_regresar.place(x=350, y=540)

        # Crear etiquetas de puertas
        self.label_puerta1 = Label(self.v1, image=self.puerta1, cursor="hand2")
        self.label_puerta1.place(x=133, y=133)
        self.label_puerta1.bind("<Button-1>", lambda e: self._cambiar_puerta(1, self.label_puerta1))

        self.label_puerta2 = Label(self.v1, image=self.puerta2, cursor="hand2")
        self.label_puerta2.place(x=333, y=133)
        self.label_puerta2.bind("<Button-1>", lambda e: self._cambiar_puerta(2, self.label_puerta2))

        self.label_puerta3 = Label(self.v1, image=self.puerta3, cursor="hand2")
        self.label_puerta3.place(x=532, y=133)
        self.label_puerta3.bind("<Button-1>", lambda e: self._cambiar_puerta(3, self.label_puerta3))

        # Etiquetas de las puertas A, B y C sobre las puertas
        self.etiqueta_puerta1 = Label(self.v1, text="A", font=("Arial", 12, "bold"))
        # Centro de la puerta 1 (x1 + ancho de la puerta / 2) y centrado de la etiqueta
        self.etiqueta_puerta1.place(x=x1 + 133 / 2 - 15, y=y1 - 20)  # Ajustar '15' para que esté centrado

        self.etiqueta_puerta2 = Label(self.v1, text="B", font=("Arial", 12, "bold"))
        # Centro de la puerta 2 (x2 + ancho de la puerta / 2) y centrado de la etiqueta
        self.etiqueta_puerta2.place(x=x2 + 133 / 2 - 15, y=y2 - 20)  # Ajustar '15' para que esté centrado

        self.etiqueta_puerta3 = Label(self.v1, text="C", font=("Arial", 12, "bold"))
        # Centro de la puerta 3 (x3 + ancho de la puerta / 2) y centrado de la etiqueta
        self.etiqueta_puerta3.place(x=x3 + 133 / 2 - 15, y=y3 - 20)  # Ajustar '15' para que esté centrado

        # Mostrar mensaje inicial de selección de puerta
        messagebox.showinfo("Monty Hall", "Selecciona una puerta entre A, B y C")
        self.label_estadisticas = Label(self.v1, text="Ganadas: 0 | Perdidas: 0 | % de victorias: 0.00%",
                                        font=("Arial", 10))
        self.label_estadisticas.place(x=266, y=500)

    def _regresar(self):
        # Regresar a la ventana principal
        self.ventana_principal.deiconify()
        self.v1.destroy()