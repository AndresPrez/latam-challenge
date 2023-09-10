# NeuralWorks: Latama Challenge
#### by Andrés Pérez Manríquez  

<br><br>
  
## Challenge Responses

1. ¿Cómo se distribuyen los datos? ¿Qué te llama la atención o cuál es tu conclusión sobre esto?



2. Genera las columnas adicionales y luego expórtelas en un archivo synthetic_features.csv

    Run the following command to generate the <b>synthetic_features.csv</b> file:

    ```python3 synthetic_features.py```

3. Entrena uno o varios modelos usando los algoritmos que prefieras para estimar la probabilidad de
atraso de un vuelo. Siéntete libre de generar variables adicionales y/o complementar con variables
externas.
    

4. Escoge el modelo que a tu criterio tenga una mejor performance, argumentando tu decisión. 

5. Serializa el mejor modelo seleccionado e implementa una API REST para poder predecir atrasos de nuevos vuelos.

6. Automatiza el proceso de build y deploy de la API, utilizando uno o varios servicios cloud. Argumenta
tu decisión sobre los servicios utilizados.

7. Realiza pruebas de estrés a la API con el modelo expuesto con al menos 50.000 requests durante 45
segundos. Para esto debes utilizar esta herramienta y presentar las métricas obtenidas. ¿Cómo podrías mejorar la performance de las pruebas anteriores?