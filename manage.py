#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import py_eureka_client.eureka_client as eureka_client

def register_with_eureka():
    """Enregistre le microservice Django dans Eureka"""
    try:
        eureka_client.init(
            eureka_server="http://localhost:8761/eureka",
            app_name="RESERVATION-DJANGO",  # Nom qui apparaîtra dans Eureka
            instance_port=8000,
            instance_ip="127.0.0.1",
             instance_host="localhost",
            renewal_interval_in_secs=30,
            duration_in_secs=90,
            metadata={
                "microservice": "reservation",
                "framework": "django"
            }
        )
        print("✅ Microservice RESERVATION-DJANGO enregistré dans Eureka")
    except Exception as e:
        print(f"❌ Erreur d'enregistrement: {e}")

# Démarrer l'enregistrement dans un thread séparé
eureka_thread = threading.Thread(target=register_with_eureka, daemon=True)
eureka_thread.start()

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()