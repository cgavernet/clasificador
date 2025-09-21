# ¿Qué hace esta app?

Detecta en tiempo real el color dominante que aparece en el centro de la imagen de la cámara y lo muestra en una interfaz web. Si el color coincide (según una tolerancia) con alguno de los selectores configurados, envía mensajes TCP al dispositivo de destino para accionar hardware (por ejemplo, un servo en otra placa) en el puerto 4210.

Cómo funciona (técnico, pero simple):
- Captura video con OpenCV a 640x480 y ~30 FPS.
- Toma un recorte central de 100x100 píxeles (ROI).
- Convierte BGR→RGB y calcula el color dominante contando píxeles.
- Compara ese color con los selectores de `config.json` usando distancia euclidiana en RGB y el `margin` como tolerancia.
- Si hay coincidencia:
  - Envía inmediatamente `servo1` por TCP a `tcp_ip:4210`.
  - Aplica cooldown de 0.75 s y una “ventana de silencio” de 10 s para evitar spam.
  - Programa el envío de `servo2` 5 s después (no bloquea; usa `threading.Timer`).
- La web (Flask) expone:
  - `GET /video_feed`: stream MJPEG con el cuadro verde del ROI y texto RGB/HEX.
  - `GET /api/color`: color actual.
  - `GET/POST /api/config`: lectura/guardado en `config.json`.

---

## Cómo se ejecuta

1. Instala dependencias: `pip install -r requirements.txt`
2. Inicia: `python start.py`
3. Abre `http://localhost:5000` en tu navegador.

> Sugerencia: si falla la cámara, prueba otra webcam o puerto USB.

---

## Flujo en 5 pasos

1. `start.py` verifica dependencias y llama a `color_detector.main()`.
2. `ColorDetector.start_camera()` abre la cámara (640x480 @ 30 FPS).
3. En cada frame, se calcula el color dominante del cuadro central (100x100 px).
4. El servidor Flask expone:
   - `GET /` interfaz web
   - `GET /video_feed` streaming MJPEG con overlay
   - `GET /api/color` color actual (RGB y HEX)
   - `GET /api/status` estado de la cámara
   - `GET/POST /api/config` leer/guardar configuración
   - `POST /api/send-tcp` enviar `servo1` a `ip:4210`
5. Si el color detectado coincide con un selector (con margen), se envía `servo1` y, 5s después, `servo2` a la IP configurada en `config.json`. Hay cooldown y silenciamiento para evitar spam.

---

## Configuración rápida (`config.json`)

- `tcp_ip`: IP destino para TCP (puerto 4210)
- `selectors`: lista de colores objetivo
  - `color`: HEX (por ejemplo `#ff0000`)
  - `margin`: tolerancia de coincidencia (0-100+)
  - `name`: etiqueta visible

La configuración se guarda automáticamente al cambiarla desde la interfaz.

---

## Dónde tocar si quiero modificar

- Tamaño del cuadro de detección: `box_size` en `color_detector.py`
- Resolución/FPS: `start_camera()` en `color_detector.py`
- Lógica de coincidencia: `_maybe_send_tcp_on_match()`
- Puerto/IP destino: `config.json` (campo `tcp_ip`)

---

## Problemas comunes

- "No se pudo abrir ninguna cámara": revisa conexiones, permisos y prueba otro índice de cámara.
- No envía TCP: verifica `tcp_ip`, firewall y que el receptor escuche en 4210.
- Detección inestable: sube `margin` o mejora iluminación.

---

Hecho para Python + OpenCV + Flask. Sencillo, directo y hackeable.
