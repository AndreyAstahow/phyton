import requests 
import json

from config import keys # импорт ключей из файла 'config'

class APIException(Exception): # класс ошибок при неправильном вводе пользователем
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base: # Ошибка при конвертации одинаковых валют
            raise APIException('Конвертация одинаковых валют. Введите разные валюты.')
        
        try: # проверка введенной валюты и ключа доступной валюты
            quote_ticker = keys[quote]
        except KeyError: # если такой валюты нет - вызывается ошибка
            raise APIException(f'Не удалось обработать валюту {quote}')
        
        try: # проверка второй введенной валюты и доступной
            base_ticker = keys[base]
        except KeyError: # если такой валюты нет - вызывается ошибка
            raise APIException(f'Не удалось обработать валюту {base}')
        
        try: # проверка числа, которое ввел пользователь
            amount = float(amount) # тип 'float' для гибкости конвертации не только в целых числах
        except ValueError: # Если пользьзователь ввел не число - вызывается ошибка
            raise APIException(f'Не удалось обработать количество {amount}')
    
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}') # Получение через API актуального курса валют с помощью библиотеки 'requests'
        total_base = json.loads(r.content)[keys[base]]

        return round(total_base * amount, 4) # Округление числа до 4 цифры
