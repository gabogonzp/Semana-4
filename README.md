Descripción

Este proyecto implementa un Monitor de Temperatura que registra mediciones en tiempo real utilizando recursividad y programación concurrente. El programa captura datos de temperatura, los procesa y verifica si superan los umbrales definidos, generando alertas en caso necesario.

Tecnologías Utilizadas:
Python
Módulos: threading, queue, random, time, logging

Funcionamiento del Código:

Recursividad en la Captura de Datos:
La función sensor_temperatura() obtiene una nueva medición cada 0.1 segundos y se llama a sí misma recursivamente.
Se detiene cuando self.ejecutando es False.

Procesamiento Concurrente:
Se utilizan hilos (threads) para ejecutar en paralelo:
sensor_temperatura(): Captura datos de temperatura.
procesar_datos(): Procesa los datos y verifica alertas.

Gestión de Alertas:
Se comparan los valores de temperatura con los umbrales establecidos.
Si hay un riesgo extremo, se genera una alerta y se simula una llamada a bomberos.

