# OzonWebScraper - Модуль для парсинга Ozon

### Удобный парсер, который собирает данные в Excel таблицы

### Модуль представляет собой класс Scraper со следующими методами:
- open_page() открывает главную страницу Ozon и вводит запрос в поисковую строку
- get_element_classes() возвращает словарь с актуальными классами html тегов
- extract_data() получает данные со страниц и записывает их в Excel таблицу
 

### Пример
```python
from OzonWebScraper import Scraper

def main():
    parser = Scraper(url='https://www.ozon.ru/')
    parser.open_page(search_query='монитор')
    parser.extract_data(parser.get_element_classes(), pages=5, table_name='Моники')

if __name__ == '__main__':
    main()
```
### Установка
```
pip install OzonWebScraper
```
