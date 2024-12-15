import mediapipe as mp
import cv2
import numpy as np
import pickle

class ClasificadorSenia:
    def __init__(self):
        # Inicialización de MediaPipe para detección de manos
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False,
                                         max_num_hands=1,
                                         min_detection_confidence=0.7,
                                         min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.abecedario = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        model_dict = pickle.load(open('./model.p', 'rb'))
        self.model = model_dict['model']
        self.labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'Ñ', 15: 'O'
               , 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}
    def procesar_mano(self, frame):
        """Procesa la imagen para detectar puntos clave de la mano."""
        data_aux = []
        x_ = []
        y_ = []
    
        H, W, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            self.mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                self.mp_hands.HAND_CONNECTIONS,  # hand connections
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style())

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10
            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10
            
            if len(data_aux) != 42:
                print(f"Error: Se esperaban 42 características, pero se generaron {len(data_aux)}")
                return None, frame
                
            prediction = self.model.predict([np.asarray(data_aux)])

            predicted_character = self.labels_dict[int(prediction[0])]
            return predicted_character, frame,[x1,y1,x2,y2]
        
        return None, frame,[0,0,0,0]
    
    def extraer_coordenadas(self, landmarks, frame_shape):
        """Extrae las coordenadas normalizadas de los puntos de la mano."""
        altura, ancho, _ = frame_shape
        coordenadas = [(int(p.x * ancho), int(p.y * altura)) for p in landmarks.landmark]
        return coordenadas
