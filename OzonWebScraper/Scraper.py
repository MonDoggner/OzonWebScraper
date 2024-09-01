import re
from tqdm import tqdm
from bs4 import BeautifulSoup

from openpyxl import Workbook

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class Scraper:
    def __init__(self, url: str) -> None:
        self.url = url
        self.driver = webdriver.Chrome()

    def open_page(self, search_query: str) -> None:
        '''
        Открытие страницы и поиск товара
        '''
        try:
            self.driver.get(self.url)

            # Для обхода блокировки требуется нажать кнопку

            button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "reload-button")))
            button.click()
            
            # Строка поиска находится через её placeholder
            # Одна из немногих постоянных вещей на сайте Ozon 

            search_bar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Искать на Ozon']"))
            )

            search_bar.click()
            search_bar.send_keys(search_query)
            search_bar.submit()

        except Exception as e:
            print(e)

    def find(self, xpath: str) -> (str | None):
        '''
        Нахождение класса элемента по его xpath
        '''        
        part = self.driver.find_element(
                By.XPATH, xpath
            )
        return part.get_attribute('class')

    def get_element_classes(self) -> dict:
        '''
        Получение классов элементов
        '''
        try:
            
            main_part = self.find('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[4]/div[1]/div')
            name_element = self.find('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[4]/div[1]/div/div/div[1]/div[2]/div/a/div')                   
            description_element = self.find('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[4]/div[1]/div/div/div[1]/div[2]/div/div[2]')                       
            price_element = self.find('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[4]/div[1]/div/div/div[1]/div[3]/div[1]')           
            button_element = self.find('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[4]/div[2]/div/div/a')

            elements = {
                'MAIN_PART': main_part,
                'NAME': name_element,
                'DESCRIPTION': description_element,
                'PRICE': price_element,
                'BUTTON': button_element
            }

        except Exception as e:
            print(e)

        return elements

    def extract_data(self, elements: dict, pages: int, table_name: str) -> (str | None):
        '''
        Извлечение данных с сайта\n
        Параметры:\n
        elements - словарь классов элементов, можно указать get_element_classes()\n
        pages - количество страниц\n
        table_name - название таблицы в файле Excel
        '''
        try:
            progress_bar = tqdm(total=pages, desc='Парсинг', unit='страницы')

            workbook = Workbook()
            worksheet = workbook.active
            
            worksheet.append(['Name', 'Description', 'Price'])

            for _ in range(pages):
                
                sleep(3)

                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                main_part = soup.find('div', class_=elements['MAIN_PART'])

                names = main_part.find_all('div', class_=elements['NAME'])
                descriptions = main_part.find_all('div', class_=elements['DESCRIPTION'])
                prices = main_part.find_all('div', class_=elements['PRICE'])
                
                for name, description, price in zip(names, descriptions, prices):
                    price_value = re.search(r'\d+\s\d+', price.text).group()
                    worksheet.append([name.text, description.text, price_value])

                button = self.driver.find_element(By.XPATH, f'//a[@class="{elements["BUTTON"]}"]')
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)                
                self.driver.execute_script("arguments[0].click();", button)

                progress_bar.update(1)
            
            workbook.save(f'{table_name}.xlsx')

        except Exception as e:
            print(e)

        progress_bar.close()        
        
    def __del__(self):
        self.driver.quit()
