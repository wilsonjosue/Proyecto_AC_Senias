import time
from asistente import AsistenteVoz
#from aprendizaje import Aprendizaje
#from test import Test
from juego_AH import Juego_senias
#from juego_nuevo import 
#from juego_CS import 
import customtkinter as ctk

class VirtualAssistant:
    def __init__(self):
        self.asistente_voz = AsistenteVoz()
        #self.mi_aprendizaje = Juego_Nuevo(callback=self.presentar_opciones)
        #self.mi_juego2 = Juego_CS(callback=self.presentar_opciones)
        self.mi_juego = Juego_senias(callback=self.presentar_opciones)
        self.option_label = None
        self.win_choose = None
        
    def texto_a_audio(self, comando):
        self.asistente_voz.texto_a_audio(comando)

    def capturar_voz(self):
        return self.asistente_voz.capturar_voz()

    def enviar_voz(self):
        return self.asistente_voz.enviar_voz()

    def do_learn(self):
        self.option_label.configure(text="Escogiste Aprendizaje")
        self.win_choose.destroy()

    def do_test(self):
        self.option_label.configure(text="Escogiste Test")
        self.win_choose.destroy()

    def do_game(self):
        self.option_label.configure(text="Escogiste Juego")
        self.win_choose.destroy()
    
    # Se ejecuta
    def presentar_opciones(self):

        self.win_choose = ctk.CTk()
        self.win_choose.geometry("600x75")

        text = (
            "\n 1) Aprendizaje"
            "\n 2) Test"
            "\n 3) Juego"
        )
        print(text)

        text = "¿Qué opción eliges?"
        print(text)
        self.texto_a_audio(text)
        time.sleep(0.5)
        self.texto_a_audio("¿Aprendizaje? ¿Tests? ¿Juegos?")
        print("dime")
        self.texto_a_audio("dime")

        title = ctk.CTkLabel(self.win_choose, text = "Escoja su modo")
        title.pack(side=ctk.LEFT, padx=(20, 20))
    
        learn = ctk.CTkButton(self.win_choose, text = 'Aprendizaje', command=self.do_learn)
        learn.pack(side=ctk.LEFT, padx=(5, 5))
    
        prueba = ctk.CTkButton(self.win_choose, text = 'Test', command=self.do_test)
        prueba.pack(side=ctk.LEFT, padx=(5, 5))
    
        juego = ctk.CTkButton(self.win_choose, text = 'Juego', command=self.do_game)
        juego.pack(side=ctk.LEFT, padx=(5, 5))

        self.option_label = ctk.CTkLabel(self.win_choose, text = "")
        self.option_label.pack(side=ctk.LEFT, padx=(5, 5))
        
        self.win_choose.mainloop()

        if (self.option_label.cget("text") == "Escogiste Aprendizaje"):
            self.mi_aprendizaje.ejecutar()      
        elif (self.option_label.cget("text") == "Escogiste Test"):
            self.mi_test.ejecutar()      
        elif (self.option_label.cget("text") == "Escogiste Juego"):
            self.mi_juego.ejecutar()

    # No se ejecuta
    def saludar_usuario(self):
        print("\nSALUDO:")
        bienvenida = "Hola. Soy tu Asistente Virtual. Fui creada para instruirte sobre el lenguaje de señas. Antes de empezar ¿Podrías decirme tu nombre?"
        self.texto_a_audio(bienvenida)
        print("Di tu nombre: ")
        nombre = self.enviar_voz()
        text = f"Hola {nombre}, mucho gusto"
        print(text)
        self.texto_a_audio(text)
        return nombre
    # No se ejecuta
    def introduccion(self):
        print("\nINTRODUCCIÓN:")
        concepto = "El lenguaje de señas es un sistema de comunicación que utiliza gestos, movimientos de manos y expresiones faciales para transmitir mensajes, especialmente diseñado para personas con discapacidad auditiva."
        print(concepto)
        self.texto_a_audio(concepto)

    def opciones(self, nombre):
        print("\nOPCIONES:")
        text = f"{nombre} ahora voy a explicarte sobre las opciones que tiene este programa. Tienes 3 opciones para escoger."
        print(text)
        self.texto_a_audio(text)

        text = (
            "\n 1) Aprendizaje"
            "\n 2) Test"
            "\n 3) Juego"
        )
        self.texto_a_audio(text)

        text = (
            "\n La opción Aprendizaje es donde podrás aprender todo con respecto al lenguaje de señas."
            "\n La opción Tests es donde podrás poner en práctica lo que aprendiste mediante exámenes."
            "\n Y por último, la tercer opción, es Juego, donde también podrás demostrar lo que aprendiste jugando."
        )
        print(text)
        self.texto_a_audio(text)

    def ejecutar_programa(self):

        # nombre = self.saludar_usuario()
        # self.introduccion()
        # self.opciones(nombre)
        self.presentar_opciones()

        
# Usage
if __name__ == "__main__":
    virtual_assistant = VirtualAssistant()
    virtual_assistant.ejecutar_programa()
