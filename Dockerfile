FROM python:3.8-slim

WORKDIR /app

COPY src/requirements.txt .

RUN apt-get update && apt-get install -y git && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install dvc[all]

COPY . .

# Set DVC credentials
RUN mkdir /root/.dvc && \
    cp .dvc/config /root/.dvc/config && \
    dvc pull
    
# Train the model initially
RUN python src/train_model.py

EXPOSE 8000

CMD ["uvicorn", "src.front:app", "--host", "0.0.0.0", "--port", "8000"]
