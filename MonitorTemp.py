import threading
import queue
import random
import time
import logging

logging.basicConfig(
    filename="temperature_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class MonitorTemperatura:
    def __init__(self, umbral_min, umbral_max):
        self.umbral_min = umbral_min
        self.umbral_max = umbral_max
        self.temperatura_actual = 0
        self.temp_queue = queue.Queue()
        self.ejecutando = True
        self.llamado_bomberos = False  
        self.semaforo_alerta = threading.Semaphore(1)  

    def sensor_temperatura(self):
        #Genera lecturas aleatorias de temperatura
        while self.ejecutando:
            temperatura = random.uniform(-10, 180)
            timestamp = time.time()
            self.temp_queue.put((temperatura, timestamp))
            time.sleep(0.1) 

    def procesar_datos(self):
        #Procesa temperatura y chequea por alertas
        while self.ejecutando:
            if not self.temp_queue.empty():
                self.temperatura_actual, timestamp = self.temp_queue.get()
                log_message = f"Temperatura: {self.temperatura_actual:.2f}°C"
                logging.info(log_message)
                self.verificar_alerta()

    def verificar_alerta(self):
        #Chequea temperatura actual contra umbrales definidos
        if self.temperatura_actual > self.umbral_max:
            logging.warning(f"ALERTA: Temperatura ALTA ({self.temperatura_actual:.2f}°C) supera {self.umbral_max}°C")
            self.manejar_alerta()
        elif self.temperatura_actual < self.umbral_min:
            logging.warning(f"ALERTA: Temperatura BAJA ({self.temperatura_actual:.2f}°C) está por debajo de {self.umbral_min}°C")
            self.manejar_alerta()

    def manejar_alerta(self):
        #Implementa semaforo para evitar llamadas consecutivas a bomberos
        with self.semaforo_alerta:  
            if not self.llamado_bomberos:
                self.llamar_bomberos()
                self.llamado_bomberos = True  

    def llamar_bomberos(self):
        #Simular llamada de emergencia a bomberos
        logging.error("LLAMADO A BOMBEROS: Se ha generado una alerta crítica de temperatura.")
        print("Llamando a los bomberos...")

    def iniciar(self):
        #Iniciar los threads del monitor de temperatura
        threading.Thread(target=self.sensor_temperatura, daemon=True).start()
        threading.Thread(target=self.procesar_datos, daemon=True).start()

# Solicitar umbrales del usuario
umbral_min = float(input("Ingrese el umbral mínimo de temperatura (°C): "))
umbral_max = float(input("Ingrese el umbral máximo de temperatura (°C): "))

# Iniciar monitoreo
monitor = MonitorTemperatura(umbral_min, umbral_max)
monitor.iniciar()

# Mantener programa corriendo
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    monitor.ejecutando = False
    logging.info("Monitoreo detenido.")
    print("\nMonitoreo detenido.")
