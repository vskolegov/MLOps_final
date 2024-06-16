import pytest
import pandas as pd

DATA_PATH = 'data/wine_data_full.csv'

EXPECTED_COLUMNS = [
    'Class', 'Alcohol', 'Malic_acid', 'Ash', 'Alcalinity_of_ash', 'Magnesium', 
    'Total_phenols', 'Flavanoids', 'Nonflavanoid_phenols', 'Proanthocyanins', 
    'Color_intensity', 'Hue', 'OD280_OD315_of_diluted_wines', 'Proline'
]

@pytest.fixture
def dataset():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.replace(' ', '_').str.replace('/', '_').str.replace('(', '').str.replace(')', '')
    return df

def test_data_quality(dataset):
    dataset.columns = dataset.columns.str.strip().str.replace(' ', '_').str.replace('/', '_').str.replace('(', '').str.replace(')', '')
    
    print("Columns in dataset:", dataset.columns)
    print("Expected columns:", EXPECTED_COLUMNS)
    
    assert all(column in dataset.columns for column in EXPECTED_COLUMNS), "Dataset is missing expected columns"
    assert dataset.isnull().sum().sum() == 0, "Dataset contains missing values"
    for column in EXPECTED_COLUMNS:
        assert pd.api.types.is_numeric_dtype(dataset[column]), f"Column {column} is not numeric"
