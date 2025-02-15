import threading
import queue
import random
import time

class MonitorTemperatura:
    def __init__(self, umbral_min, umbral_max):
        self.umbral_min = umbral_min
        self.umbral_max = umbral_max
        self.temperatura_actual = 0
        self.alerta_evento = threading.Event()  
        self.temp_queue = queue.Queue()  
        self.semaforo_alerta = threading.Semaphore(1)  
        self.llamado_realizado = False 
        self.ejecutando = True

    def sensor_temperatura(self):
        while self.ejecutando:
            temperatura = random.uniform(-10, 180)  
            timestamp = time.time()
            self.temp_queue.put((temperatura, timestamp))
            time.sleep(5)  

    def procesar_datos(self):
        while self.ejecutando:
            if not self.temp_queue.empty():
                self.temperatura_actual, timestamp = self.temp_queue.get()
                
                print(f"[{time.strftime('%H:%M:%S', time.localtime(timestamp))}] Temperatura: {self.temperatura_actual:.2f}°C")
                self.verificar_alerta()

    def verificar_alerta(self):

        if self.temperatura_actual > self.umbral_max:
            print(f"ALERTA: Temperatura ALTA ({self.temperatura_actual:.2f}°C) supera {self.umbral_max}°C")
            if not self.llamado_realizado:
                self.alerta_evento.set() 
        elif self.temperatura_actual < self.umbral_min:
            print(f"ALERTA: Temperatura BAJA ({self.temperatura_actual:.2f}°C) está por debajo de {self.umbral_min}°C")
        else:
            self.llamado_realizado = False  

    def manejar_alerta(self):
    
        while self.ejecutando:
            self.alerta_evento.wait()  
            
            with self.semaforo_alerta:  
                if not self.llamado_realizado:  
                    print("Llamando a los bomberos...")
                    time.sleep(3)  
                    print("Bomberos notificados correctamente.")
                    self.llamado_realizado = True 

            self.alerta_evento.clear() 

    def iniciar(self):
        threading.Thread(target=self.sensor_temperatura, daemon=True).start()
        threading.Thread(target=self.procesar_datos, daemon=True).start()
        threading.Thread(target=self.manejar_alerta, daemon=True).start()


umbral_min = float(input("Ingrese el umbral mínimo de temperatura (°C): "))
umbral_max = float(input("Ingrese el umbral máximo de temperatura (°C): "))

monitor = MonitorTemperatura(umbral_min, umbral_max)
monitor.iniciar()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    monitor.ejecutando = False
    print("Monitoreo detenido.")
