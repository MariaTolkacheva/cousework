# 🧠 Behavioral Economics Quiz Platform

Этот проект — курсовая работа, в рамках которой был разработан **асинхронный веб-сайт на Django** с поддержкой **Redis**, **Celery** и **LLM-интеграции**, позволяющий проходить тестирование по поведенческой экономике и взаимодействовать с LLM моделью.

## 🔍 Описание

Платформа предоставляет пользователю возможность:

* Проходить **тесты по поведенческой экономике** и **задавать вопросы ollama-модели** на основе книг:

  * *Predictably Irrational* — Dan Ariely
  * *Nudge* — Richard Thaler
  * *Aldhemy* - Rory Sutherland
  * *Behavioral Science in the Wild* - Dilip Soman
  * *Freakonomics Revised and Expanded Edition* - Steven D. Levitt
  * *Good Economics for Hard Times* - Abhijit V. Banerjee
  * *The Choice Factory* - Richard Shotton
  * *Thinking, Fast and Slow* - Daniel Kahneman

* **LLM-модель**, использует:

  * **RAG-подход (Retrieval-Augmented Generation)** на основе загруженной литературы.
  * **Векторный поиск** по эмбеддингам документов, в частности OllamaEmbeddings.
  * **Оценку релевантности и формулировку ответа** с помощью LLM.

## ⚙️ Технологии

* **Python + Django (async)** — серверная логика
* **PostgreSQL** — база данных
* **Redis + Celery** — асинхронная обработка задач (пользователь задает вопрос, запуская асинхронную задачу celery)
* **LLM (OpenAI / HuggingFace)** — генерация и оценка ответов
* **Vector Store ( Chroma)** — поиск по векторам
* **JavaScript** + **HTML** - для оформления страниц и обработки событий

## 🚀 Основные возможности

* 📚 Хранилище контента (главы книг) для последующего поиска
* 🧪 Тестирование пользователей с сохранением истории и результатов
* 🤖 Интеграция с LLM: ответы на пользовательские вопросы на основе знаний из книг
* 🧠 Использование RAG для генерации точных и осмысленных ответов
* 🪄 Асинхронная генерация и отправка данных пользователю

## 📚 Используемая литература и другие источники
  * *Predictably Irrational* — Dan Ariely
  * *Nudge* — Richard Thaler
  * *Aldhemy* - Rory Sutherland
  * *Behavioral Science in the Wild* - Dilip Soman
  * *Freakonomics Revised and Expanded Edition* - Steven D. Levitt
  * *Good Economics for Hard Times* - Abhijit V. Banerjee
  * *The Choice Factory* - Richard Shotton
  * *Thinking, Fast and Slow* - Daniel Kahneman
  * https://dev.to/hussainislam/django-fixtures-seeding-databases-5ai
  * http://docs.djangoproject.com/en/5.2/topics/db/fixtures/
  * https://www.geeksforgeeks.org/how-to-import-a-json-file-to-a-django-model/
