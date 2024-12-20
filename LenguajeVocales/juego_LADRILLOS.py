import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk
import imageio
import threading
import cv2
import pygame 
from tkinter import Toplevel
from abecedario import ClasificadorSenia  # Importamos ClasificadorSenia




class Arkanoid:
    def __init__(self):
        pygame.init()
        self.ventana = tk.Tk()
        self.ventana.title("Arkanoid")
        self.ancho = 800
        self.alto = 600
        self.ventana.geometry(f"{self.ancho}x{self.alto}")
        self.ventana.resizable(False, False)
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.imageFondosGame=['./juego_ladrillosMEDIA/wood.png','./juego_ladrillosMEDIA/planets.png','./juego_ladrillosMEDIA/sea.jpeg']
        self.niveles = {
            1: [
                (50, 50, 100, 70), (120, 50, 170, 70), (190, 50, 240, 70),
                (260, 50, 310, 70), (330, 50, 380, 70), (400, 50, 450, 70),
                (50, 90, 100, 110), (120, 90, 170, 110), (190, 90, 240, 110),
                (50, 130, 100, 150), (120, 130, 170, 150),
                (260, 130, 310, 150), (330, 130, 380, 150),
                (50, 170, 100, 190), (400, 170, 450, 190),
            ],
            2: [
                (50, 50, 100, 70), (120, 50, 170, 70), (190, 50, 240, 70),
                (260, 50, 310, 70), (330, 50, 380, 70), (400, 50, 450, 70),
                (50, 90, 100, 110), (120, 90, 170, 110), (190, 90, 240, 110),
                (260, 90, 310, 110), (330, 90, 380, 110), (400, 90, 450, 110),
                (50, 130, 100, 150), (190, 130, 240, 150), (330, 130, 380, 150),
            ],
            3: [
                (50, 50, 100, 70), (120, 50, 170, 70), (190, 50, 240, 70), (260, 50, 310, 70),
                (330, 50, 380, 70), (400, 50, 450, 70), (470, 50, 520, 70),
                (70, 90, 120, 110), (150, 90, 200, 110), (230, 90, 280, 110), (310, 90, 360, 110),
                (390, 90, 440, 110), (470, 90, 520, 110),
                (90, 130, 140, 150), (170, 130, 220, 150), (250, 130, 300, 150), (330, 130, 380, 150),
            ],
        }
        self.video_running = False
        self.estilo_botones()
        #cv2
        self.clasificador_senia = ClasificadorSenia()
        self.camara = cv2.VideoCapture(0)

        # Establecer resolución de la cámara
        self.camara.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.en_juego =False
        if not self.camara.isOpened():
            print("Error: No se pudo acceder a la cámara")
            self.camara_activa =False
            return
        else:
            self.camara_activa =True
            
        self.menu_principal()

    def estilo_botones(self):
        # Crear un estilo para los botones
        style = ttk.Style()
        style.configure("Custom.TButton",
                        background="#00BFFF",  # Celeste
                        foreground="black",  # Texto blanco
                        font=("Arial", 12, "bold"),
                        padding=2,
                        borderwidth=0)
        style.map("Custom.TButton",
                  background=[("active", "#009ACD")]) 
    def menu_principal(self):
        pygame.mixer.music.stop()
        self.limpiar_ventana()
        self.canvas = tk.Canvas(self.ventana, width=self.ancho, height=self.alto, bg="black")
        self.canvas.pack()
        if not self.video_running:
            self.reproducir_video()
        boton_empezar = ttk.Button(self.ventana, text="Empezar Juego", style="Custom.TButton", command=self.seleccionar_nivel)
        self.canvas.create_window(self.ancho / 2, self.alto / 2 - 50, window=boton_empezar)

        boton_como_jugar = ttk.Button(self.ventana, text="Cómo Jugar", style="Custom.TButton",command=self.como_jugar)
        self.canvas.create_window(self.ancho / 2, self.alto / 2, window=boton_como_jugar)

        boton_salir = ttk.Button(self.ventana, text="Salir",style="Custom.TButton", command=self.cerrar)
        self.canvas.create_window(self.ancho / 2, self.alto / 2 + 50, window=boton_salir)
    def cerrar(self):
        # Detener la música
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
        # Detener el video
        self.video_running = False

        # Cerrar la ventana
        self.ventana.destroy()
        if self.camara.isOpened():
            self.camara.release()
    def reproducir_video(self):
        self.video_running = True
        video = imageio.get_reader('./juego_ladrillosMEDIA/stars.mp4', 'ffmpeg')

        def loop_video():
            for frame in video:
                if not self.video_running:
                    break
                
                # Redimensionar el frame al tamaño del canvas
                frame_image = Image.fromarray(frame)
                frame_image = frame_image.resize((self.ancho, self.alto), Image.ANTIALIAS)
                frame_tk = ImageTk.PhotoImage(frame_image)
                
                self.canvas.delete("video_frame")
                self.canvas.create_image(0, 0, image=frame_tk, anchor=tk.NW, tags="video_frame")

                self.canvas.update()
                self.canvas.after(33)  # Aproximadamente 30 fps
            video.close()

        threading.Thread(target=loop_video, daemon=True).start()
    def detener_video(self):
        self.video_running = False
        self.canvas.delete("video_frame")
        self.canvas.update()
        
            
    def como_jugar(self):
        self.detener_video()
        self.limpiar_ventana()
        self.canvas = tk.Canvas(self.ventana, width=self.ancho, height=self.alto, bg="black")
        self.canvas.pack()

        # Cargar y mostrar la imagen
        imagen = Image.open("./juego_ladrillosMEDIA/JUGAR.png")  # Cambia la ruta a tu archivo de imagen
        imagen = imagen.resize((self.ancho, self.alto), Image.ANTIALIAS)  # Ajusta el tamaño de la imagen
        self.imagen_tk = ImageTk.PhotoImage(imagen)  # Referencia necesaria para evitar recolección de basura
        self.canvas.create_image(0, 0, image=self.imagen_tk, anchor=tk.NW)

        # Crear un Frame para contener el botón
        frame_boton = tk.Frame(self.ventana, bg="black")

        # Botón "Volver"
        boton_volver = ttk.Button(frame_boton, text="Volver",style="Custom.TButton", command=self.menu_principal)
        boton_volver.pack()

        # Añadir el Frame al canvas
        self.canvas.create_window(self.ancho / 2, self.alto / 2 + 50, window=frame_boton, anchor=tk.CENTER)

    def seleccionar_nivel(self):
        self.detener_video()
        self.limpiar_ventana()
        self.canvas = tk.Canvas(self.ventana, width=self.ancho, height=self.alto, bg="black")
        self.canvas.pack()

        self.canvas.create_text(self.ancho / 2, self.alto / 2 - 100, text="Selecciona un nivel", fill="white", font=("Arial", 24))

        boton_nivel_1 = tk.Button(self.ventana, text="Nivel 1", command=lambda: self.empezar_juego(1))
        self.canvas.create_window(self.ancho / 2, self.alto / 2 - 50, window=boton_nivel_1)

        boton_nivel_2 = tk.Button(self.ventana, text="Nivel 2", command=lambda: self.empezar_juego(2))
        self.canvas.create_window(self.ancho / 2, self.alto / 2, window=boton_nivel_2)

        boton_nivel_3 = tk.Button(self.ventana, text="Nivel 3", command=lambda: self.empezar_juego(3))
        self.canvas.create_window(self.ancho / 2, self.alto / 2 + 50, window=boton_nivel_3)

    def empezar_juego(self, nivel):
        self.limpiar_ventana()
        
        self.canvas = tk.Canvas(self.ventana, width=self.ancho, height=self.alto, bg="black")
        self.canvas.pack()
        
        
        fondo = Image.open(self.imageFondosGame[nivel-1])  # Cambia por la ruta de tu imagen
        fondo = fondo.resize((self.ancho, self.alto), Image.ANTIALIAS)
        self.fondo_imagen = ImageTk.PhotoImage(fondo)
        self.canvas.create_image(0, 0, image=self.fondo_imagen, anchor=tk.NW)
        
        pygame.mixer.music.load("./juego_ladrillosMEDIA/aura.mp3")  # Cambia por la ruta de tu archivo MP3
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # Reproducir en bucle infinito
        
        self.paleta = self.canvas.create_rectangle(self.ancho / 2 - 40, self.alto - 20, self.ancho / 2 + 40, self.alto - 10, fill="white")
        self.bola = self.canvas.create_oval(self.ancho / 2 - 10, self.alto / 2 - 10, self.ancho / 2 + 10, self.alto / 2 + 10, fill="red")

        self.bola_dx = random.choice([-6, 6])
        self.bola_dy = -6

        self.bloques = []
        self.crear_bloques(nivel)

        self.en_juego = True
        # Crear una nueva ventana
        
        new_window = Toplevel(self.ventana)
        new_window.title("Video Capture")
        new_window.geometry("500x500")
        
        #poner a la derecha de la ventana principal
        self.ventana.update_idletasks()  # Asegurarse de que la geometría esté actualizada
        root_geometry = self.ventana.geometry()  # Ejemplo: "300x200+100+100"
        print("GEOMETRU")
        print(self.ventana.geometry())
        parts = root_geometry.split('+')
        size = parts[0].split('x')
        print(parts,size)
        root_width=size[0]
        root_height=size[1]
        root_x=parts[1]
        root_y =parts[2]

        # Calcular posición de la nueva ventana (a la derecha de la ventana principal)
        new_x = int(root_x) + int(root_width) + 10  # Añade un margen de 10 píxeles
        new_y = int(root_y)  # Mantener la misma altura

        # Establecer la posición de la nueva ventana
        new_window.geometry(f"500x500+{new_x}+{new_y}")
    
        # Crear un Label para mostrar el video
        self.video_label = tk.Label(new_window)
        self.video_label.pack()
        
        self.actualizacion = self.ventana.after(20, lambda:self.mover_bola(nivel))
        #self.procesar_camara()
    def procesar_camara(self):
        """Procesa las imágenes de la cámara para detectar la letra señalada."""

        ret, frame = self.camara.read()
        if not ret:
            print("Error: No se pudo leer el frame de la cámara")

        print("Frame capturado correctamente.")
        
        # Procesar el frame con el clasificador de señas
        letra, _,[x1,y1,x2,y2] = self.clasificador_senia.procesar_mano(frame)
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, letra, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                    cv2.LINE_AA)
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        # Mostrar el frame en el Label
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)    
            
        if letra:
            print(f"Letra detectada: {letra}")  # Mensaje cuando se detecta una letra
            if letra == 'A':
                self.mover_paleta_izquierda()
            if letra =='B':
                self.mover_paleta_derecha()

        # Pausar ligeramente el bucle para evitar un ciclo infinito rápido
        pygame.time.delay(10)  # Esto ralentiza el bucle del hilo de la cámara
        
        
    def limpiar_ventana(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

    def crear_bloques(self, nivel):
        colores = ["blue", "red", "green", "yellow", "purple", "orange", "pink"]  # Lista de colores
        for coords in self.niveles[nivel]:
            color_aleatorio = random.choice(colores)  # Escoge un color aleatorio
            bloque = self.canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill=color_aleatorio, outline="white")
            self.bloques.append(bloque)


    def mover_paleta_izquierda(self):
        
        pos_paleta=self.canvas.coords(self.paleta)
        if pos_paleta[0]-20 >= 0:
            self.canvas.move(self.paleta, -20, 0)
        

    def mover_paleta_derecha(self):
        
        pos_paleta=self.canvas.coords(self.paleta)
        if pos_paleta[0]+20 <= 720:
            self.canvas.move(self.paleta, 20, 0)
        

    def mover_bola(self,nivel):
        if not self.en_juego:
            return
        self.procesar_camara()
        
        self.canvas.move(self.bola, self.bola_dx, self.bola_dy)
        pos_bola = self.canvas.coords(self.bola)

        if pos_bola[0] <= 0 or pos_bola[2] >= self.ancho:
            self.bola_dx = -self.bola_dx

        if pos_bola[1] <= 0:
            self.bola_dy = -self.bola_dy

        if pos_bola[3] >= self.alto:
            self.fin_del_juego("Perdiste",nivel)

        pos_paleta = self.canvas.coords(self.paleta)
        if (pos_bola[2] >= pos_paleta[0] and pos_bola[0] <= pos_paleta[2] and
                pos_bola[3] >= pos_paleta[1] and pos_bola[3] <= pos_paleta[3]):
            self.bola_dy = -self.bola_dy

        for bloque in self.bloques[:]:
            pos_bloque = self.canvas.coords(bloque)
            if (pos_bola[2] >= pos_bloque[0] and pos_bola[0] <= pos_bloque[2] and
                    pos_bola[3] >= pos_bloque[1] and pos_bola[1] <= pos_bloque[3]):
                self.canvas.delete(bloque)
                self.bloques.remove(bloque)
                self.bola_dy = -self.bola_dy
                break

        if not self.bloques:
            self.fin_del_juego("Ganaste",nivel)

        self.actualizacion = self.ventana.after(20, lambda:self.mover_bola(nivel))

    def fin_del_juego(self, mensaje,nivel):
        self.en_juego = False
        self.canvas.create_text(self.ancho / 2, self.alto / 2, text=mensaje, fill="white", font=("Arial", 24))
        
        
        contenedor_botones = tk.Frame(self.ventana, bg="black")
        contenedor_botones.pack()

        # Crear botones
        boton_reintentar = tk.Button(contenedor_botones, text="Reintentar", command=lambda:self.reiniciar_juego(nivel))
        boton_reintentar.grid(row=0, column=0, padx=10)
        
        boton_menu = tk.Button(contenedor_botones, text="Menu", command=self.menu_principal)
        boton_menu.grid(row=0, column=1, padx=10)

        # Colocar el contenedor en el canvas
        self.canvas.create_window(self.ancho / 2, self.alto / 2 + 50, window=contenedor_botones)

    def reiniciar_juego(self,nivel):
        self.empezar_juego(nivel)

    def iniciar_juego(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    juego = Arkanoid()
    juego.iniciar_juego()
