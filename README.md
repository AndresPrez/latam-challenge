# NeuralWorks: Latama Challenge
#### by Andrés Pérez Manríquez  

<br><br>
  
## Challenge Responses

1. ¿Cómo se distribuyen los datos? ¿Qué te llama la atención o cuál es tu conclusión sobre esto?

    Analásis exploratorio de datos en el notebook [analysis.ipynb](./latam/notebooks/analysis.ipynb). Específicamente
    en las secciones Anomaly Detection, Categorical Data y Feature Importance.

    En resumen, se observa que los datos siguen una distribución incial quasi normal, con valores altos de Skewness y Kurtosis.
    Sin embargo, luego de aplicar un algoritmo para detección y remoción de outliers, el dataset se reduce cerca de un 5%, lo que genera que se ajuste a una distribución normal con valores de Skewness y Kurtosis aceptables.

    En cuanto a las variables categóricas del dataset, se detectó algunas con una alta cardinalidad y otras con cardinalidad bien baja. Dado esto se optó por usar una codificacíon conocida como "Target Encoding", la cual reduce la cardinalidad de las variables categóricas.

    Finalmente se analizó la importancia de las variables, donde se observó que la variable más relevante es "Vlo-I" (número de vuelo programado).

    NOTA: más información sobre estos análisis quedó organizado en secciones dentro del notebook mencionado.

2. Genera las columnas adicionales y luego expórtelas en un archivo synthetic_features.csv

    Con el siguiente comando se genera el CSV <b>synthetic_features.csv</b> solictiado:

    ```cd latam/service && python3 synthetic_features.py```

3. Entrena uno o varios modelos usando los algoritmos que prefieras para estimar la probabilidad de
atraso de un vuelo. Siéntete libre de generar variables adicionales y/o complementar con variables
externas.
    
    Se generaron variables adicionales al codificar la variable de tipo fecha "Fecha-I" (fecha y hora programada del vuelo) utilizando nua técnica conocida como "Cyclica Encoding", especial para variables cuya naturaleza es cíclica como lo son el mes, día y hora de una fecha. A partir de esta variable se generaron entonces otras 4: año (no codificada) y las variables cíclicas de mes, día y hora. Estas fueron codificadas utilizando una sinusoide con periodicidad igual a la duración de cada variable.

4. Escoge el modelo que a tu criterio tenga una mejor performance, argumentando tu decisión.

    El modelo seleccionado fue XGBoost ya que este implementa bagging, boosting y cross validation internamente, lo cual acelara la implementación y parece ser un bueno modelo con el cual comenzar para lograr un deployment en corto tiempo. 
    
    Se compararon sus modos regresión y clasificación, y dado los resultados de "Feature Importance", so optó por uno de clasficación. Además este modo le permite al modelo obviar de cierta manera la necesidad de "fitearse" para restraso menores.

5. Serializa el mejor modelo seleccionado e implementa una API REST para poder predecir atrasos de nuevos vuelos.
    XGBoost provides a metho to serialize the trained model which commited in the repo located in `latam-layer/latam/data/model.bin`.

6. Automatiza el proceso de build y deploy de la API, utilizando uno o varios servicios cloud. Argumenta
tu decisión sobre los servicios utilizados.

    El framework the [Serverless](https://www.serverless.com/) permite mediante un archivo de configuración (e.g., yaml o json) definir los servicios Cloud que se necesiten. Funciona originalmente con AWS, aunque se encuentran en modo experimental con GCP. En fin, se optó por este framework porque es realtivamente sencillo de configurar para levantar los siguientes servicios cloud: AWS Lambda Function + AWS LAmbda Layers + AWS API GAteway y un Bucket de S3 para alojar los archivos. A pesar de poder deployar correctamente la librería de XGBoost supera el mínimo requerido de 250MB para una AWS Lambda Layer, por lo que en trabajos futuros se podría optar por otro modelo o utilizar AWS SageMaker el cual pareciera permitir hostear este modelo.

7. Realiza pruebas de estrés a la API con el modelo expuesto con al menos 50.000 requests durante 45
segundos. Para esto debes utilizar esta herramienta y presentar las métricas obtenidas. ¿Cómo podrías mejorar la performance de las pruebas anteriores?

    Dado que no se quedo el modelo deployado, este paso no se ejecutó.