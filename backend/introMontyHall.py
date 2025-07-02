import cv2
import pygame
import time

def reproducir_video(ruta_video, ruta_audio, ancho_ventana=800, alto_ventana=600, duracion=20):
    # Inicializa pygame para audio
    pygame.mixer.init()

    # Reproduce el archivo de audio
    pygame.mixer.music.load(ruta_audio)
    pygame.mixer.music.play(loops=0, start=0.0)  # Reproducir desde el inicio

    # Abre el video
    cap = cv2.VideoCapture(ruta_video)

    if not cap.isOpened():
        print(f"Error: No se puede abrir el video en {ruta_video}")
        return

    # Configura la ventana de OpenCV
    cv2.namedWindow('Video y Audio', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Video y Audio', ancho_ventana, alto_ventana)

    # Fotogramas por segundo del video
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(fps * duracion)  # Total de frames a mostrar

    start_time = time.time()  # Tiempo de inicio

    for frame_idx in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            print("Fin del video antes de tiempo.")
            break

        # Redimensiona el frame para que se ajuste a las dimensiones deseadas
        frame_alto, frame_ancho, _ = frame.shape
        escala_x = ancho_ventana / frame_ancho
        escala_y = alto_ventana / frame_alto
        escala = min(escala_x, escala_y)

        nuevo_ancho = int(frame_ancho * escala)
        nuevo_alto = int(frame_alto * escala)
        frame_redimensionado = cv2.resize(frame, (nuevo_ancho, nuevo_alto))

        # Crear un lienzo negro para centrar el video
        lienzo = cv2.copyMakeBorder(
            frame_redimensionado,
            top=(alto_ventana - nuevo_alto) // 2,
            bottom=(alto_ventana - nuevo_alto) // 2,
            left=(ancho_ventana - nuevo_ancho) // 2,
            right=(ancho_ventana - nuevo_ancho) // 2,
            borderType=cv2.BORDER_CONSTANT,
            value=(0, 0, 0)  # Negro
        )

        # Muestra el video
        cv2.imshow('Video y Audio', lienzo)

        # Controla el tiempo para mantener la sincronización
        elapsed_time = time.time() - start_time
        tiempo_por_frame = 1 / fps
        sleep_time = max(0, tiempo_por_frame - elapsed_time % tiempo_por_frame)
        time.sleep(sleep_time)

        # Permite cerrar la ventana con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Detiene la reproducción del audio y cierra todo
    pygame.mixer.music.stop()
    cap.release()
    cv2.destroyAllWindows()
