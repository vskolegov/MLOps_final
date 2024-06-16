FROM python:3.8-slim

# Установим зависимости
RUN apt-get update && \
    apt-get install -y git

# Установим рабочую директорию
WORKDIR /app

# Скопируем requirements.txt и установим зависимости Python
COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Скопируем все файлы проекта
COPY . .

# Установим DVC
RUN pip install dvc[all]

# Скопируем конфигурацию DVC и подтянем данные
RUN mkdir /root/.dvc && \
    cp .dvc/config /root/.dvc/config && \
    dvc pull

# Запустим приложение
CMD ["uvicorn", "src.front:app", "--host", "0.0.0.0", "--port", "8000"]
