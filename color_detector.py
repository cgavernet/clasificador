import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify, request
import json
import os
import time

# Configuración por defecto
DEFAULT_CONFIG = {
    "servo_pin": 18,
    "selectors": [
        {"id": 1, "color": "#ff0000", "margin": 20, "name": "Rojo", 
         "angle": 0},
        {"id": 2, "color": "#00ff00", "margin": 20, "name": "Verde", 
         "angle": 45},
        {"id": 3, "color": "#0000ff", "margin": 20, "name": "Azul", 
         "angle": 90},
        {"id": 4, "color": "#ffff00", "margin": 20, "name": "Amarillo", 
         "angle": 135}
    ]
}


class ColorDetector:
    def __init__(self):
        self.camera = None
        self.camera_running = False
        self.current_color = (0, 0, 0)
        self.config_file = 'config.json'
        self.config = self.load_config()
            # Eliminado código relacionado al servo
    
    # ...función init_servo eliminada...
    
    # ...función move_servo eliminada...
    
    def load_config(self):
        """Carga la configuración desde el archivo JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    print("✅ Configuración cargada desde config.json")
                    return config
            else:
                # Crear archivo de configuración por defecto
                self.save_config(DEFAULT_CONFIG)
                print("📝 Archivo de configuración creado con valores por defecto")
                return DEFAULT_CONFIG
        except Exception as e:
            print(f"❌ Error al cargar configuración: {e}")
            print("📝 Usando configuración por defecto")
            return DEFAULT_CONFIG
    
    def save_config(self, config):
        """Guarda la configuración en el archivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print("✅ Configuración guardada en config.json")
            return True
        except Exception as e:
            print(f"❌ Error al guardar configuración: {e}")
            return False
    
    def start_camera(self):
        """Inicia la cámara"""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                # Intentar con diferentes índices de cámara
                for i in range(1, 5):
                    self.camera = cv2.VideoCapture(i)
                    if self.camera.isOpened():
                        break
            
            if not self.camera.isOpened():
                raise Exception("No se pudo abrir ninguna cámara")
            
            # Configurar resolución para mejor rendimiento
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.camera_running = True
            print("✅ Cámara iniciada correctamente")
            return True
        except Exception as e:
            print(f"❌ Error al iniciar cámara: {e}")
            return False
    
    def stop_camera(self):
        """Detiene la cámara"""
        if self.camera:
            self.camera.release()
        self.camera_running = False
        print("🛑 Cámara detenida")
    
    def detect_dominant_color(self, frame):
        """Detecta el color dominante en un cuadro central de 100x100 píxeles"""
        try:
            height, width = frame.shape[:2]
            center_x = width // 2
            center_y = height // 2
            box_size = 100
            
            # Calcular coordenadas del cuadro central
            x1 = max(0, center_x - box_size // 2)
            y1 = max(0, center_y - box_size // 2)
            x2 = min(width, center_x + box_size // 2)
            y2 = min(height, center_y + box_size // 2)
            
            # Extraer el cuadro central
            center_box = frame[y1:y2, x1:x2]
            
            # Convertir BGR a RGB
            rgb_box = cv2.cvtColor(center_box, cv2.COLOR_BGR2RGB)
            
            # Reshape para procesar todos los píxeles
            pixels = rgb_box.reshape(-1, 3)
            
            # Encontrar colores únicos y sus conteos
            colors, counts = np.unique(pixels, axis=0, return_counts=True)
            
            # Obtener el color más frecuente
            dominant_color = colors[np.argmax(counts)]
            return tuple(map(int, dominant_color))
        except Exception as e:
            print(f"Error en detección de color: {e}")
            return (0, 0, 0)
    
    def process_frame(self, frame):
        """Procesa un frame y detecta el color dominante"""
        if frame is not None:
            self.current_color = self.detect_dominant_color(frame)
        return frame
    
    def get_frame(self):
        """Obtiene un frame de la cámara"""
        if self.camera and self.camera_running:
            ret, frame = self.camera.read()
            if ret:
                return self.process_frame(frame)
        return None
    
    def get_current_color(self):
        """Obtiene el color actual detectado"""
        r, g, b = self.current_color
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        return {
            'r': r,
            'g': g,
            'b': b,
            'hex': hex_color
        }
    
    def cleanup(self):
        """Limpia recursos"""
        self.stop_camera()


# Instancia global del detector
detector = ColorDetector()

# Inicializar Flask
app = Flask(__name__)


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
def api_color():
    """API para obtener el color actual"""
    return jsonify(detector.get_current_color())


@app.route('/api/status')
def api_status():
    """API para obtener el estado de la cámara"""
    return jsonify({
        'camera_running': detector.camera_running,
        'camera_opened': (detector.camera is not None and 
                          detector.camera.isOpened())
    })


@app.route('/api/config', methods=['GET'])
def api_get_config():
    """API para obtener la configuración actual"""
    return jsonify(detector.config)


@app.route('/api/config', methods=['POST'])
def api_save_config():
    """API para guardar la configuración"""
    try:
        config = request.get_json()
        
        # Validar configuración
        if not isinstance(config, dict):
            return jsonify({'error': 'Configuración inválida'}), 400
        
        if 'selectors' not in config:
            return jsonify({'error': 'Configuración incompleta'}), 400
        # Actualizar configuración
        detector.config = config
        
        # Guardar en archivo
        if detector.save_config(config):
            return jsonify({'message': 'Configuración guardada exitosamente'})
        else:
            return jsonify({'error': 'Error al guardar configuración'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500


    # ...ruta /api/servo eliminada...


def generate_frames():
    """Genera frames para streaming"""
    while True:
        frame = detector.get_frame()
        if frame is not None:
            height, width = frame.shape[:2]
            center_x = width // 2
            center_y = height // 2
            box_size = 100
            
            # Calcular coordenadas del cuadro central
            x1 = max(0, center_x - box_size // 2)
            y1 = max(0, center_y - box_size // 2)
            x2 = min(width, center_x + box_size // 2)
            y2 = min(height, center_y + box_size // 2)
            
            # Dibujar rectángulo verde alrededor del área de detección
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Agregar texto informativo
            cv2.putText(frame, 'Area de Deteccion', (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Obtener color actual para mostrar
            color_info = detector.get_current_color()
            color_text = f"RGB: ({color_info['r']}, {color_info['g']}, {color_info['b']})"
            
            # Mostrar información del color en la parte superior
            cv2.putText(frame, color_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"HEX: {color_info['hex']}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Codificar frame para streaming
            ret, buffer = cv2.imencode('.jpg', frame, 
                                     [cv2.IMWRITE_JPEG_QUALITY, 80])
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        time.sleep(0.033)  # ~30 FPS


def main():
    """Función principal"""
    print("🎨 Iniciando Clasificador inteligente de residuos...")
    print("=" * 50)
    
    # Iniciar cámara
    if not detector.start_camera():
        print("❌ No se pudo iniciar la cámara")
        return
    
    try:
        print("🌐 Iniciando servidor web en http://localhost:5000")
        print("📱 Abre tu navegador y ve a la URL anterior")
    # ...mensaje de servo eliminado...
        print("💾 La configuración se guarda automáticamente en config.json")
        print("=" * 50)
        
        # Ejecutar Flask
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
        
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
    except Exception as e:
        print(f"❌ Error en la aplicación: {e}")
    finally:
        detector.cleanup()
        print("🧹 Recursos limpiados")


if __name__ == '__main__':
    main()
