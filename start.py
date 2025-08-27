#!/usr/bin/env python3
"""
Script de inicio para el Detector de Colores
Ejecuta: python start.py
"""

import sys


def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import cv2
        import numpy
        from flask import Flask
        print("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Instala las dependencias con: pip install -r requirements.txt")
        return False


def main():
    """Función principal"""
    print("🎨 Iniciando Detector de Colores...")
    print("=" * 40)
    
    # Verifica dependencias
    if not check_dependencies():
        sys.exit(1)
    
    # Importa y ejecuta la aplicación
    try:
        from color_detector import main as run_app
        run_app()
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
    except Exception as e:
        print(f"❌ Error al ejecutar la aplicación: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
