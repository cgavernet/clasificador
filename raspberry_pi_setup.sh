#!/bin/bash

echo "🚀 Configurando Raspberry Pi para Detector de Colores con Servo"
echo "================================================================"

# Actualizar sistema
echo "📦 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
echo "🔧 Instalando dependencias del sistema..."
sudo apt install -y python3-pip python3-opencv libatlas-base-dev python3-dev

# Configurar GPIO para el usuario
echo "⚡ Configurando GPIO..."
sudo usermod -a -G gpio $USER
sudo usermod -a -G video $USER

# Instalar dependencias de Python
echo "🐍 Instalando dependencias de Python..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Configurar cámara
echo "📷 Configurando cámara..."
if ! grep -q "camera_auto_detect=1" /boot/config.txt; then
    echo "camera_auto_detect=1" | sudo tee -a /boot/config.txt
fi

# Habilitar interfaz de cámara
echo "🔌 Habilitando interfaz de cámara..."
sudo raspi-config nonint do_camera 0

# Configurar permisos de GPIO
echo "🔐 Configurando permisos de GPIO..."
sudo chown root:gpio /dev/gpiomem
sudo chmod g+rw /dev/gpiomem

# Crear archivo de configuración por defecto
echo "📝 Creando archivo de configuración..."
if [ ! -f "config.json" ]; then
    cat > config.json << EOF
{
  "servo_pin": 18,
  "selectors": [
    {
      "id": 1,
      "color": "#ff0000",
      "margin": 20,
      "name": "Rojo",
      "angle": 0
    },
    {
      "id": 2,
      "color": "#00ff00",
      "margin": 20,
      "name": "Verde",
      "angle": 45
    },
    {
      "id": 3,
      "color": "#0000ff",
      "margin": 20,
      "name": "Azul",
      "angle": 90
    },
    {
      "id": 4,
      "color": "#ffff00",
      "margin": 20,
      "name": "Amarillo",
      "angle": 135
    }
  ]
}
EOF
    echo "✅ Archivo config.json creado"
else
    echo "ℹ️ Archivo config.json ya existe"
fi

# Configurar inicio automático (opcional)
echo "🤔 ¿Deseas configurar inicio automático? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "📋 Creando servicio systemd..."
    sudo tee /etc/systemd/system/color-detector.service > /dev/null << EOF
[Unit]
Description=Detector de Colores con Servo
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 color_detector.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable color-detector.service
    echo "✅ Servicio configurado. Inicia con: sudo systemctl start color-detector"
fi

echo ""
echo "🎉 ¡Configuración completada!"
echo ""
echo "📋 Pasos siguientes:"
echo "1. Reinicia tu Raspberry Pi: sudo reboot"
echo "2. Conecta el servo al pin GPIO 18 (o cambia en config.json)"
echo "3. Ejecuta: python3 color_detector.py"
echo "4. Abre http://localhost:5000 en tu navegador"
echo ""
echo "🔧 Conexiones del servo:"
echo "   - Cable rojo: 5V (pin 2 o 4)"
echo "   - Cable marrón/negro: GND (pin 6, 9, 14, 20, 25, 30, 34, 39)"
echo "   - Cable naranja/amarillo: Señal (pin 18 por defecto)"
echo ""
echo "📚 Para más información, consulta el README.md"
