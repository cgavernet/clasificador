import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify
import threading
import time


app = Flask(__name__)


class ColorDetector:
    def __init__(self):
        self.camera = None
        self.is_running = False
        self.current_color = (0, 0, 0)
        self.frame = None
        self.lock = threading.Lock()
        
    def start_camera(self, camera_index=0):
        """Inicia la cámara"""
        try:
            self.camera = cv2.VideoCapture(camera_index)
            if not self.camera.isOpened():
                # Intenta con diferentes índices de cámara
                for i in range(4):
                    self.camera = cv2.VideoCapture(i)
                    if self.camera.isOpened():
                        break
                if not self.camera.isOpened():
                    raise Exception("No se pudo abrir la cámara")
            
            # Configura resolución para Raspberry Pi
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_running = True
            print("Cámara iniciada correctamente")
            return True
        except Exception as e:
            print(f"Error al iniciar cámara: {e}")
            return False
    
    def stop_camera(self):
        """Detiene la cámara"""
        self.is_running = False
        if self.camera:
            self.camera.release()
            print("Cámara detenida")
    
    def detect_dominant_color(self, frame):
        """Detecta el color dominante en un cuadro central de 100x100 píxeles"""
        try:
            # Obtiene dimensiones del frame
            height, width = frame.shape[:2]
            
            # Calcula el centro del frame
            center_x = width // 2
            center_y = height // 2
            
            # Define el tamaño del cuadro de detección (100x100)
            box_size = 100
            
            # Calcula las coordenadas del cuadro central
            x1 = max(0, center_x - box_size // 2)
            y1 = max(0, center_y - box_size // 2)
            x2 = min(width, center_x + box_size // 2)
            y2 = min(height, center_y + box_size // 2)
            
            # Extrae el cuadro central
            center_box = frame[y1:y2, x1:x2]
            
            # Convierte BGR a RGB
            rgb_box = cv2.cvtColor(center_box, cv2.COLOR_BGR2RGB)
            
            # Reshape para análisis
            pixels = rgb_box.reshape(-1, 3)
            
            # Encuentra el color más común
            colors, counts = np.unique(pixels, axis=0, return_counts=True)
            dominant_color = colors[np.argmax(counts)]
            
            return tuple(map(int, dominant_color))
        except Exception as e:
            print(f"Error en detección de color: {e}")
            return (0, 0, 0)
    
    def process_frame(self):
        """Procesa frames continuamente"""
        while self.is_running:
            if self.camera and self.camera.isOpened():
                ret, frame = self.camera.read()
                if ret:
                    with self.lock:
                        self.frame = frame.copy()
                        self.current_color = self.detect_dominant_color(frame)
                else:
                    time.sleep(0.1)
            else:
                time.sleep(0.1)
    
    def get_frame(self):
        """Obtiene el frame actual"""
        with self.lock:
            if self.frame is not None:
                return self.frame.copy()
            return None
    
    def get_current_color(self):
        """Obtiene el color actual detectado"""
        with self.lock:
            return self.current_color


# Instancia global del detector
detector = ColorDetector()


def generate_frames():
    """Genera frames para streaming"""
    while True:
        frame = detector.get_frame()
        if frame is not None:
            # Obtiene dimensiones del frame
            height, width = frame.shape[:2]
            center_x = width // 2
            center_y = height // 2
            box_size = 100
            
            # Calcula coordenadas del cuadro central
            x1 = max(0, center_x - box_size // 2)
            y1 = max(0, center_y - box_size // 2)
            x2 = min(width, center_x + box_size // 2)
            y2 = min(height, center_y + box_size // 2)
            
            # Dibuja el cuadro de detección
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Dibuja el color detectado en el frame
            color = detector.get_current_color()
            cv2.rectangle(frame, (10, 10), (200, 60), color, -1)
            cv2.putText(frame, f"RGB: {color}", (15, 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Convierte a JPEG
            ret, buffer = cv2.imencode('.jpg', frame,
                                     [cv2.IMWRITE_JPEG_QUALITY, 80])
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' +
                       buffer.tobytes() + b'\r\n')
        
        time.sleep(0.033)  # ~30 FPS


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """Stream de video"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/color')
def get_color():
    """API para obtener el color actual"""
    color = detector.get_current_color()
    return jsonify({
        'r': color[0],
        'g': color[1], 
        'b': color[2],
        'hex': '#{:02x}{:02x}{:02x}'.format(*color)
    })


@app.route('/api/status')
def get_status():
    """API para obtener el estado de la cámara"""
    return jsonify({
        'camera_running': detector.is_running,
        'camera_opened': detector.camera.isOpened()
        if detector.camera else False
    })


def main():
    """Función principal"""
    print("Iniciando detector de colores...")
    
    # Inicia la cámara
    if not detector.start_camera():
        print("Error: No se pudo iniciar la cámara")
        return
    
    # Inicia el procesamiento en un hilo separado
    process_thread = threading.Thread(target=detector.process_frame,
                                   daemon=True)
    process_thread.start()
    
    print("Servidor web iniciando en http://localhost:5000")
    print("Presiona Ctrl+C para detener")
    
    try:
        # Inicia el servidor Flask
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\nDeteniendo aplicación...")
    finally:
        detector.stop_camera()
        print("Aplicación detenida")


if __name__ == '__main__':
    main()
