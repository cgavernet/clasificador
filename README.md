# 🎨 Detector de Colores con OpenCV

Aplicación de detección de colores en tiempo real usando OpenCV y Flask. Funciona tanto en PC como en Raspberry Pi 3B+.

## Características

- ✅ **Detección de color predominante** en cuadro central de 100x100 píxeles
- ✅ **4 selectores de color configurables** con márgenes ajustables
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
- **Indicadores visuales** que se encienden cuando detectan coincidencias
- **Colores predefinidos**: Rojo, Verde, Azul, Amarillo
- **Actualización en tiempo real** de coincidencias

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
```

### 3. Configurar cámara

#### En PC:
- Conecta una webcam USB
- La aplicación detectará automáticamente la cámara

#### En Raspberry Pi:
- Conecta la cámara oficial de Raspberry Pi
- O conecta una webcam USB
- Habilita la cámara en `raspi-config` si es necesario

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

## 🎨 **Uso de los Selectores de Color**

### **Configuración Básica:**
1. **Selecciona el color objetivo** usando el input de color
2. **Ajusta el margen** con el slider (0-100)
3. **Coloca objetos** en el cuadro central verde
4. **Observa los indicadores** que se encienden al detectar coincidencias

### **Ajuste de Sensibilidad:**
- **Margen bajo (0-20)**: Detección muy precisa, solo colores muy similares
- **Margen medio (20-50)**: Detección equilibrada, colores similares
- **Margen alto (50-100)**: Detección amplia, colores relacionados

### **Colores Predefinidos:**
- **Rojo** (#ff0000) - Ideal para detectar objetos rojos
- **Verde** (#00ff00) - Perfecto para plantas y objetos verdes
- **Azul** (#0000ff) - Excelente para agua y objetos azules
- **Amarillo** (#ffff00) - Ideal para objetos amarillos brillantes

## Estructura del Proyecto

```
clasificador/
├── color_detector.py      # Aplicación principal con OpenCV
├── start.py              # Script de inicio simplificado
├── requirements.txt       # Dependencias de Python
├── README.md             # Este archivo
├── raspberry_pi_setup.sh # Script de configuración para Raspberry Pi
└── templates/
    └── index.html        # Interfaz web con selectores de color
```

## API Endpoints

- `GET /` - Interfaz web principal con selectores
- `GET /video_feed` - Stream de video en vivo
- `GET /api/color` - Color actual detectado en el cuadro central (JSON)
- `GET /api/status` - Estado de la cámara (JSON)

### Ejemplo de respuesta de `/api/color`:
```json
{
  "r": 255,
  "g": 128,
  "b": 64,
  "hex": "#ff8040"
}
```

## 🔧 **Personalización Avanzada**

### **Modificar Selectores de Color:**
Edita el array `selectors` en `templates/index.html`:
```javascript
const selectors = [
    { id: 1, color: '#ff0000', margin: 20, name: 'Rojo' },
    { id: 2, color: '#00ff00', margin: 20, name: 'Verde' },
    // Agrega más selectores aquí
];
```

### **Cambiar Algoritmo de Detección:**
Modifica la función `colorDistance()` en `templates/index.html` para usar diferentes métricas de color.

### **Ajustar Tamaño del Cuadro de Detección:**
Modifica la variable `box_size` en `color_detector.py`:
```python
box_size = 150  # Cambia de 100 a 150 píxeles
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

## Tecnologías Utilizadas

- **Python 3.7+** - Lógica de backend
- **OpenCV 4.8+** - Procesamiento de imagen y detección de colores
- **Flask 3.0+** - Servidor web y API REST
- **NumPy** - Operaciones matemáticas y procesamiento de arrays
- **HTML5/CSS3/JavaScript** - Interfaz web moderna y responsive
- **Canvas API** - Procesamiento de video en tiempo real

## 🚀 **Casos de Uso**

### **Educación:**
- Enseñar teoría del color
- Demostrar espacios de color RGB
- Experimentos de mezcla de colores

### **Industria:**
- Control de calidad de productos
- Clasificación automática por color
- Detección de defectos en superficies

### **Arte y Diseño:**
- Paletas de colores en tiempo real
- Análisis de composiciones
- Inspiración para proyectos creativos

### **IoT y Raspberry Pi:**
- Sistemas de monitoreo automático
- Detección de cambios en entornos
- Automatización domótica

## Licencia

Este proyecto es de código abierto. ¡Siéntete libre de modificarlo y distribuirlo!

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📝 **Changelog**

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

¡Disfruta detectando colores con precisión! 🎨✨
