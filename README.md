# 🎨 Detector de Colores con OpenCV y Servo

Aplicación de detección de colores en tiempo real usando OpenCV y Flask, con control automático de servo. Funciona tanto en PC como en Raspberry Pi 3B+.

## Características

- ✅ **Detección de color predominante** en cuadro central de 100x100 píxeles
- ✅ **4 selectores de color configurables** con márgenes ajustables
- ✅ **Control automático de servo** que se mueve según el color detectado
- ✅ **Configuración persistente** guardada en archivo JSON
- ✅ **Sistema de detección inteligente** con indicadores visuales
- ✅ **Interfaz web responsive y moderna** con gradientes y animaciones
- ✅ **Streaming de video en vivo** con overlay del área de detección
- ✅ **Indicador de color RGB y hexadecimal** en tiempo real
- ✅ **API REST completa** para integración con otras aplicaciones
- ✅ **Compatible con PC y Raspberry Pi** con optimizaciones automáticas
- ✅ **Detección en tiempo real** con actualización cada 100ms

## 🎯 **Nuevas Funcionalidades**

### **Selectores de Color Inteligentes:**
- **4 selectores configurables** con colores predefinidos
- **Slider de margen** (0-100) para ajustar la sensibilidad
- **Control de ángulo de servo** (0-180°) para cada color
- **Indicadores visuales** que se encienden cuando detectan coincidencias
- **Colores predefinidos**: Rojo, Verde, Azul, Amarillo
- **Actualización en tiempo real** de coincidencias

### **Control de Servo Automático:**
- **Pin configurable** para conectar el servo (por defecto pin 18)
- **Movimiento automático** al detectar colores coincidentes
- **Ángulos personalizables** para cada selector de color
- **Detección de Raspberry Pi** para habilitar funcionalidad de servo
- **Control PWM preciso** para movimientos suaves

### **Sistema de Configuración:**
- **Archivo JSON persistente** (`config.json`)
- **Carga automática** de configuración al iniciar
- **Guardado automático** de cambios en tiempo real
- **Configuración por defecto** si no existe archivo
- **Interfaz de gestión** para modificar configuraciones

### **Detección Precisa:**
- **Cuadro central de 100x100 píxeles** para detección focalizada
- **Algoritmo de distancia euclidiana RGB** para comparación precisa
- **Overlay visual** que muestra el área de detección
- **Margen configurable** para cada selector individual

## Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone <tu-repositorio>
cd clasificador
```

### 2. Instalar dependencias

#### En PC (Windows/Linux/Mac):
```bash
pip install -r requirements.txt
```

#### En Raspberry Pi:
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
sudo apt install python3-pip python3-opencv libatlas-base-dev -y

# Instalar dependencias de Python
pip3 install -r requirements.txt

# Configurar GPIO (solo para servo)
sudo usermod -a -G gpio $USER
```

### 3. Configurar cámara y servo

#### En PC:
- Conecta una webcam USB
- La aplicación detectará automáticamente la cámara
- El servo no estará disponible (se mostrará mensaje informativo)

#### En Raspberry Pi:
- Conecta la cámara oficial de Raspberry Pi o webcam USB
- Habilita la cámara en `raspi-config` si es necesario
- Conecta el servo al pin configurado (por defecto GPIO 18)
- El servo se inicializará automáticamente

## Uso

### Ejecutar la aplicación:

```bash
# Opción 1: Script principal
python color_detector.py

# Opción 2: Script de inicio (recomendado)
python start.py
```

### Acceder a la interfaz web:

1. Abre tu navegador
2. Ve a `http://localhost:5000`
3. ¡Listo! Verás la cámara en vivo y el color detectado

### En Raspberry Pi (acceso remoto):

1. Ejecuta la aplicación
2. Accede desde cualquier dispositivo en la red:
   - `http://[IP-DE-RASPBERRY-PI]:5000`
   - Ejemplo: `http://192.168.1.100:5000`

## 🎨 **Uso de los Selectores de Color y Servo**

### **Configuración Básica:**
1. **Configura el pin del servo** en la sección superior
2. **Selecciona el color objetivo** usando el input de color
3. **Ajusta el margen** con el slider (0-100)
4. **Establece el ángulo** del servo (0-180°)
5. **Coloca objetos** en el cuadro central verde
6. **Observa los indicadores** y el movimiento del servo

### **Ajuste de Sensibilidad:**
- **Margen bajo (0-20)**: Detección muy precisa, solo colores muy similares
- **Margen medio (20-50)**: Detección equilibrada, colores similares
- **Margen alto (50-100)**: Detección amplia, colores relacionados

### **Configuración del Servo:**
- **Pin por defecto**: GPIO 18 (configurable)
- **Frecuencia**: 50Hz (estándar para servos)
- **Rango de movimiento**: 0° a 180°
- **Movimiento automático**: Se activa al detectar coincidencias

### **Colores Predefinidos:**
- **Rojo** (#ff0000) - Ángulo: 0° - Ideal para detectar objetos rojos
- **Verde** (#00ff00) - Ángulo: 45° - Perfecto para plantas y objetos verdes
- **Azul** (#0000ff) - Ángulo: 90° - Excelente para agua y objetos azules
- **Amarillo** (#ffff00) - Ángulo: 135° - Ideal para objetos amarillos brillantes

## Estructura del Proyecto

```
clasificador/
├── color_detector.py      # Aplicación principal con OpenCV y servo
├── start.py              # Script de inicio simplificado
├── config.json           # Archivo de configuración JSON
├── requirements.txt      # Dependencias de Python
├── README.md             # Este archivo
├── raspberry_pi_setup.sh # Script de configuración para Raspberry Pi
└── templates/
    └── index.html        # Interfaz web con selectores y controles de servo
```

## API Endpoints

- `GET /` - Interfaz web principal con selectores y servo
- `GET /video_feed` - Stream de video en vivo
- `GET /api/color` - Color actual detectado en el cuadro central (JSON)
- `GET /api/status` - Estado de la cámara y servo (JSON)
- `GET /api/config` - Configuración actual (JSON)
- `POST /api/config` - Guardar nueva configuración
- `POST /api/servo` - Mover servo a ángulo específico

### Ejemplo de respuesta de `/api/color`:
```json
{
  "r": 255,
  "g": 128,
  "b": 64,
  "hex": "#ff8040"
}
```

### Ejemplo de respuesta de `/api/status`:
```json
{
  "camera_running": true,
  "camera_opened": true,
  "servo_available": true
}
```

### Ejemplo de configuración (`config.json`):
```json
{
  "servo_pin": 18,
  "selectors": [
    {
      "id": 1,
      "color": "#ff0000",
      "margin": 20,
      "name": "Rojo",
      "angle": 0
    }
  ]
}
```

## 🔧 **Personalización Avanzada**

### **Modificar Selectores de Color:**
Edita el array `selectors` en `templates/index.html` o usa la interfaz web:
```javascript
const selectors = [
    { id: 1, color: '#ff0000', margin: 20, name: 'Rojo', angle: 0 },
    { id: 2, color: '#00ff00', margin: 20, name: 'Verde', angle: 45 },
    // Agrega más selectores aquí
];
```

### **Cambiar Pin del Servo:**
Modifica el valor en la interfaz web o edita `config.json`:
```json
{
  "servo_pin": 12,
  "selectors": [...]
}
```

### **Ajustar Algoritmo de Detección:**
Modifica la función `colorDistance()` en `templates/index.html` para usar diferentes métricas de color.

### **Cambiar Tamaño del Cuadro de Detección:**
Modifica la variable `box_size` en `color_detector.py`:
```python
box_size = 150  # Cambia de 100 a 150 píxeles
```

### **Configurar Frecuencia del Servo:**
Modifica la frecuencia en `init_servo()`:
```python
self.servo_pwm = GPIO.PWM(self.servo_pin, 60)  # 60Hz en lugar de 50Hz
```

## Solución de Problemas

### Error: "No se pudo abrir la cámara"
- Verifica que la cámara esté conectada
- En Raspberry Pi, ejecuta `sudo raspi-config` y habilita la cámara
- Prueba diferentes índices de cámara modificando `camera_index` en el código

### Error de dependencias en Raspberry Pi:
```bash
sudo apt install python3-dev
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### El servo no se mueve:
- Verifica que estés en Raspberry Pi
- Comprueba la conexión del servo al pin correcto
- Verifica que el servo tenga alimentación adecuada (5V)
- Ejecuta `sudo usermod -a -G gpio $USER` y reinicia

### Rendimiento lento en Raspberry Pi:
- Reduce la resolución en `color_detector.py`:
```python
self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
```

### Los selectores no detectan colores:
- Verifica que los márgenes no sean muy bajos
- Asegúrate de que los objetos estén en el cuadro central verde
- Prueba ajustando los márgenes con los sliders

### Error al guardar configuración:
- Verifica permisos de escritura en el directorio
- Asegúrate de que el archivo `config.json` no esté bloqueado
- Reinicia la aplicación si persiste el problema

## Personalización

### Cambiar puerto del servidor:
```python
app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
```

### Modificar algoritmo de detección:
Edita la función `detect_dominant_color()` en `color_detector.py`

### Cambiar resolución:
Modifica las líneas de configuración de cámara en `start_camera()`

### Agregar más selectores:
Edita el HTML y JavaScript en `templates/index.html`

### Configurar múltiples servos:
Modifica la clase `ColorDetector` para manejar múltiples pines de servo

## Tecnologías Utilizadas

- **Python 3.7+** - Lógica de backend y control de servo
- **OpenCV 4.8+** - Procesamiento de imagen y detección de colores
- **Flask 3.0+** - Servidor web y API REST
- **NumPy** - Operaciones matemáticas y procesamiento de arrays
- **RPi.GPIO** - Control de GPIO y PWM para servo (Raspberry Pi)
- **HTML5/CSS3/JavaScript** - Interfaz web moderna y responsive
- **Canvas API** - Procesamiento de video en tiempo real

## 🚀 **Casos de Uso**

### **Educación:**
- Enseñar teoría del color
- Demostrar espacios de color RGB
- Experimentos de mezcla de colores
- Control de dispositivos físicos

### **Industria:**
- Control de calidad de productos
- Clasificación automática por color
- Detección de defectos en superficies
- Automatización de procesos

### **Arte y Diseño:**
- Paletas de colores en tiempo real
- Análisis de composiciones
- Inspiración para proyectos creativos
- Control de iluminación automática

### **IoT y Raspberry Pi:**
- Sistemas de monitoreo automático
- Detección de cambios en entornos
- Automatización domótica
- Control de dispositivos mecánicos
- Sistemas de clasificación automática

### **Robótica:**
- Control de brazos robóticos
- Sistemas de clasificación por color
- Automatización de tareas repetitivas
- Control de movimientos precisos

## Licencia

Este proyecto es de código abierto. ¡Siéntete libre de modificarlo y distribuirlo!

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📝 **Changelog**

### **v3.0.0** - Control de Servo y Configuración Persistente
- ✨ Control automático de servo con ángulos configurables
- 💾 Sistema de configuración JSON persistente
- 🔧 Pin de servo configurable desde la interfaz
- 📁 Carga/guardado automático de configuraciones
- 🎯 Movimiento automático del servo al detectar colores
- 🔄 Botones de gestión de configuración

### **v2.0.0** - Selectores de Color Inteligentes
- ✨ Agregados 4 selectores de color configurables
- 🎯 Detección en cuadro central de 100x100 píxeles
- 🔧 Sliders de margen ajustables (0-100)
- ✅ Indicadores visuales de coincidencia
- 🎨 Interfaz web completamente rediseñada

### **v1.0.0** - Funcionalidad Básica
- 🎥 Detección de color en tiempo real
- 🌐 Servidor web con Flask
- 📱 Interfaz responsive
- 🔌 API REST completa

---

¡Disfruta detectando colores y controlando servos con precisión! 🎨⚙️✨
