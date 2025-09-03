#!/usr/bin/env python3
import pytest
import sys
from pathlib import Path

# Добавляем путь к ex03 в Python path
sys.path.append(str(Path(__file__).parent.parent / 'ex03'))
from financial import get_financial_data

# Тестовые случаи для корректных данных
def test_total_revenue_for_aapl():
    """Проверяем, что для AAPL возвращаются данные по Total Revenue"""
    result = get_financial_data('AAPL', 'Total Revenue')
    assert isinstance(result, tuple)
    assert len(result) > 0
    assert all(isinstance(x, str) for x in result)

def test_return_type():
    """Проверяем, что возвращается tuple"""
    result = get_financial_data('MSFT', 'Total Revenue')
    assert isinstance(result, tuple)

# Тестовые случаи для ошибочных данных
def test_invalid_ticker():
    """Проверяем обработку несуществующего тикера"""
    with pytest.raises(Exception):
        get_financial_data('INVALIDTICKER', 'Total Revenue')

def test_invalid_field():
    """Проверяем обработку несуществующего поля"""
    with pytest.raises(Exception):
        get_financial_data('AAPL', 'Invalid Field Name')

# Тест на структуру возвращаемых данных
def test_data_structure():
    """Проверяем структуру возвращаемых данных"""
    result = get_financial_data('GOOG', 'Total Revenue')
    assert len(result) == 6  # Ожидаем 6 значений (кварталы)
    assert all(',' in x for x in result[1:])  # Проверяем формат чисел

# Запуск тестов (если файл запущен напрямую)
if __name__ == '__main__':
    pytest.main()