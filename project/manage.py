#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time
import logging
import py_eureka_client.eureka_client as eureka_client

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_with_eureka():
    """Enregistre le microservice dans Eureka"""
    try:
        logger.info("🔄 Tentative d'enregistrement dans Eureka...")
        
        # Initialiser le client Eureka
        eureka_client.init(
            eureka_server="http://localhost:8761/eureka",
            app_name="RESERVATION-DJANGO",
            instance_port=8000,
            instance_ip="127.0.0.1",
            renewal_interval_in_secs=30,
            duration_in_secs=90,
            metadata={
                "microservice": "reservation",
                "framework": "django",
                "database": "mongodb",
                "version": "1.0.0"
            }
        )
        
        logger.info("✅ Microservice RESERVATION-DJANGO enregistré dans Eureka avec succès!")
        logger.info("   → Interface Eureka: http://localhost:8761")
        
        # Garder le thread actif
        while True:
            time.sleep(10)
            
    except Exception as e:
        logger.error(f"❌ Erreur d'enregistrement dans Eureka: {e}")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    
    # Démarrer l'enregistrement Eureka dans un thread séparé
    eureka_thread = threading.Thread(target=register_with_eureka, daemon=True)
    eureka_thread.start()
    logger.info("🚀 Thread Eureka démarré")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()