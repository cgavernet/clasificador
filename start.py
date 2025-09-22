#!/usr/bin/env python3
"""
Script de inicio para el Detector de Colores
Ejecuta: python start.py
"""

import sys
import logging

# Configurar logging a un archivo
logging.basicConfig(filename='camera_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    try:
        import cv2
        import numpy
        from flask import Flask
        logging.info("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        logging.error(f"❌ Error: {e}")
        logging.error("Instala las dependencias con: pip install -r requirements.txt")
        return False


def main():
    """Función principal"""
    logging.info("🎨 Iniciando Detector de Colores...")
    logging.info("=" * 40)
    
    # Verifica dependencias
    if not check_dependencies():
        sys.exit(1)
    
    # Importa y ejecuta la aplicación
    try:
        from color_detector import app, detector
        
        # Iniciar cámara
        logging.info("🎨 Iniciando cámara...")
        if not detector.start_camera():
            logging.error("❌ No se pudo iniciar la cámara. Saliendo.")
            sys.exit(1)
        
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        logging.info("\n👋 Aplicación detenida por el usuario")
    except Exception as e:
        logging.error(f"❌ Error al ejecutar la aplicación: {e}")
        sys.exit(1)
    finally:
        if 'detector' in locals() and detector.camera_running:
            detector.cleanup()
            logging.info("🧹 Recursos de cámara limpiados.")


if __name__ == '__main__':
    main()
