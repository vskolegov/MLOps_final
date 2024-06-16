import pytest
from train_model import train_and_save_model  # Обновлен путь импорта
import os

def test_train_and_save_model():
    train_and_save_model()
    assert os.path.exists('model.pkl'), "Model file not found"
    assert os.path.exists('label_encoder.pkl'), "Label encoder file not found"
