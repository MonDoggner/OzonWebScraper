from OzonWebScraper import Scraper

def main():
    parser = Scraper(url='https://www.ozon.ru/')
    parser.open_page(search_query='монитор')
    parser.extract_data(parser.get_element_classes(), pages=5, table_name='Моники')

if __name__ == '__main__':
    main()
    