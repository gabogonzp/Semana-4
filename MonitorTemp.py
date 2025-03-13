import threading
import queue
import random
import time
import logging

# Configuración del sistema de logs
logging.basicConfig(
    filename="temperature_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class MonitorTemperatura:
    def __init__(self, umbral_min, umbral_max):
        try:
            self.umbral_min = float(umbral_min)
            self.umbral_max = float(umbral_max)
            if self.umbral_min >= self.umbral_max:
                raise ValueError("El umbral mínimo debe ser menor que el umbral máximo.")
        except ValueError as e:
            logging.error(f"Error en la inicialización: {e}")
            raise

        self.temperatura_actual = 0
        self.temp_queue = queue.Queue()
        self.ejecutando = True
        self.llamado_bomberos = False
        self.semaforo_alerta = threading.Semaphore(1)

    def sensor_temperatura(self):#Iniciar generacion de valores de temperatura
        try:
            if not self.ejecutando:
                return

            temperatura = random.uniform(-10, 180)
            timestamp = time.time()
            self.temp_queue.put((temperatura, timestamp))

            time.sleep(0.1)
            self.sensor_temperatura()
        except Exception as e:
            logging.error(f"Error en sensor_temperatura: {e}")

    def procesar_datos(self):#Iniciar procesamiento de datos en queue
        try:
            while self.ejecutando:
                if not self.temp_queue.empty():
                    self.temperatura_actual, timestamp = self.temp_queue.get()
                    log_message = f"Temperatura: {self.temperatura_actual:.2f}°C"
                    logging.info(log_message)
                    self.verificar_alerta()
        except Exception as e:
            logging.error(f"Error en procesar_datos: {e}")

    def verificar_alerta(self):#Verificacion de queue por datos de alerta
        try:
            if self.temperatura_actual > self.umbral_max:
                logging.warning(f"ALERTA: Temperatura ALTA ({self.temperatura_actual:.2f}°C) supera {self.umbral_max}°C")
                self.manejar_alerta()
            elif self.temperatura_actual < self.umbral_min:
                logging.warning(f"ALERTA: Temperatura BAJA ({self.temperatura_actual:.2f}°C) está por debajo de {self.umbral_min}°C")
                self.manejar_alerta()
        except Exception as e:
            logging.error(f"Error en verificar_alerta: {e}")

    def manejar_alerta(self):#Manejo de evento interno
        try:
            with self.semaforo_alerta:
                if not self.llamado_bomberos:
                    self.llamar_bomberos()
                    self.llamado_bomberos = True
        except Exception as e:
            logging.error(f"Error en manejar_alerta: {e}")

    def llamar_bomberos(self):
        try:
            logging.error("LLAMADO A BOMBEROS: Se ha generado una alerta crítica de temperatura.")
            print("Llamando a los bomberos...")
        except Exception as e:
            logging.error(f"Error en llamar_bomberos: {e}")

    def iniciar(self):
        try:
            threading.Thread(target=self.sensor_temperatura, daemon=True).start()
            threading.Thread(target=self.procesar_datos, daemon=True).start()
        except Exception as e:
            logging.error(f"Error al iniciar los hilos: {e}")

# Solicitar umbrales del usuario 
while True:
    try:
        umbral_min = float(input("Ingrese el umbral mínimo de temperatura (°C): "))
        umbral_max = float(input("Ingrese el umbral máximo de temperatura (°C): "))
        if umbral_min >= umbral_max:
            raise ValueError("El umbral mínimo debe ser menor que el umbral máximo.")
        break
    except ValueError as e:
        print(f"Entrada inválida: {e}. Intente de nuevo.")

# Iniciar monitoreo
monitor = MonitorTemperatura(umbral_min, umbral_max)
monitor.iniciar()

# Mantener el programa corriendo
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    monitor.ejecutando = False
    logging.info("Monitoreo detenido.")
    print("\nMonitoreo detenido.")
except Exception as e:
    logging.error(f"Error inesperado en la ejecución principal: {e}")
