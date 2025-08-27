#!/bin/bash
# Script de configuración para Raspberry Pi
# Ejecuta: bash raspberry_pi_setup.sh

echo "🍓 Configurando Raspberry Pi para Detector de Colores..."
echo "=================================================="

# Actualizar sistema
echo "📦 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
echo "🔧 Instalando dependencias del sistema..."
sudo apt install -y python3-pip python3-dev python3-opencv libatlas-base-dev

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip3 install --upgrade pip

# Instalar dependencias de Python
echo "🐍 Instalando dependencias de Python..."
pip3 install -r requirements.txt

# Configurar cámara
echo "📷 Configurando cámara..."
echo "Si tienes cámara oficial de Raspberry Pi, ejecuta:"
echo "sudo raspi-config"
echo "Y habilita la cámara en 'Interface Options'"

echo ""
echo "✅ Configuración completada!"
echo ""
echo "Para ejecutar la aplicación:"
echo "python3 start.py"
echo ""
echo "Para acceso remoto, usa la IP de tu Raspberry Pi:"
echo "http://[IP-DE-RASPBERRY-PI]:5000"
