FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python train_model.py

CMD ["uvicorn", "front:app", "--host", "0.0.0.0", "--port", "8000"]
