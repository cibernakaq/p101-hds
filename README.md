# Sistema de recomendación  de juegos.

El presente proyecto desarrolló un sistema de recomendación de juegos,basado en un dataset de la plataforma `Steam`.

Mediante la elaboración de un API (quese describirá más adelante), se podrá ingresar el `id` de juego y se obtendrá un top-5 de los juegos con mayor similitud a este. Además, se podrá hacer consultas sobre las horas jugadas por género, el usuario con más tiempo de juego en un género dado, los juegos más recomendados y los menos recomendados por los usuarios, así como la polaridad (negativa, neutral o positiva) de los sentimientos expresados en los "reviews"  de los usuarios.

Para el desarrollo del proyecto se ejecutaron las fases:
 - Transformaciones: selección del algunos campos y ajuste de los tipos de datos de los datasets.
 - Feature Engineering: Se usó la red neuronal `distilroBERTa` para determinar la polaridad del sentimiento de los comentarios de los usuarios sobre los videojuegos.
 - Desarrollo del API: Se usó la librería `FastAPI` para crear una API que permitierá consumir los datos del sistema de recomendación y se desplegó como servicio web mediante `railway.app`. Ver [**aquí**](https://p101-hds-production.up.railway.app/docs).
  - EDA: Se realizó un anĺisis exploratorio donde se determinó las tendencias en el consumo por género, año, recomendación y sentimiento predominante, así como una aproximación a los términos más significativos para identificar la similitud de los juegos del dataset.
  - Modelo de apredizaje: Se usó vectorización TF-IDF y similaridad de cocenos para elaborar una función que permita hacer la recomedación de juegos. Está se integró al API.

 Cada una de estas está acompañada por un notebook de `Jupyter`. Véase el directorio `notebooks` del repositorio.

Debido a los límites de tamaño de archivo que impone `Github`, los datasets usados por los notebook se acceder externamente. Estos pueden descargarse desde [**aquí**](https://drive.google.com/drive/folders/1TRqbeh8heW4tZsrUqcPX71me-T5iZdSq?usp=drive_link).
