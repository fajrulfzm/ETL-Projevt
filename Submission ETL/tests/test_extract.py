import pytest
from unittest.mock import patch, MagicMock
from utils.extract import extract_data

@patch('utils.extract.requests.get')
def test_extract_data_success(mock_get):
    # Simulasi HTML yang memiliki komponen lengkap
    mock_html = """
    <div class="collection-card">
        <h3 class="product-title">Produk Test</h3>
        <span class="price">$10.00</span>
        <p>Rating: 4.5 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    """
    mock_response = MagicMock()
    mock_response.content = mock_html.encode('utf-8')
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Tes ambil 1 halaman saja agar cepat
    result = extract_data(total_pages=1)
    
    assert result is not None
    assert len(result) == 1
    assert result[0]['Title'] == 'Produk Test'
    assert 'Timestamp' in result[0]

@patch('utils.extract.requests.get')
def test_extract_data_network_error(mock_get):
    # Simulasi internet mati
    mock_get.side_effect = Exception("Network Error")
    result = extract_data(total_pages=1)
    # Harus tetap mengembalikan None karena ada try-except di extract.py
    assert result is None