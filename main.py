from bs4 import BeautifulSoup
import csv
import sqlite3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time

# Для кнопки (Загрузить еще)

driver = webdriver.Chrome('')  # Здесь нужно указать путь к драйверу
wait = WebDriverWait(driver, 5)
action = ActionChains(driver)

driver.get("https://russian.rt.com/news")


i = 0

while i < 5:
    try:
        time.sleep(4)

        # element = driver.find_element(By.XPATH, "//a[@class='button__item button__item_listing']")
        # driver.execute_script("arguments[0].scrollIntoView(true);", element)

        driver.execute_script("window.scrollBy(0, 3300)")
        Load_More = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='button__item button__item_listing']")))
        action.move_to_element(Load_More).click().perform()
        i += 1
        print(f"Clicked {i} time.")
    except:
        print("Reached End of the Page")
        break

page_source = driver.page_source

# Функция сохранения файла
def save(a):
  with open('news.txt', 'a') as file:
    file.write(F'{a["article"]}±{a["pre_body"]}±https://russian.rt.com{a["link"]}\n')

# Функция парсинга
def parse_news():
  soup = BeautifulSoup(page_source, 'lxml')
  items = soup.findAll('div', class_ = 'listing__card listing__card_all-news')
  newsM = []

  for item in items:
    newsM.append({
      'article': item.findAll('a', class_ = 'link link_color')[1].get_text(strip = True),
      'pre_body': item.findAll('a', class_='link link_color')[2].get_text(strip = True),
      'link': item.findAll('a', class_='link link_color')[2].get('href')
    })

  for news in newsM:
    # print(F'Article: {news["article"]} Pre_body: {news["pre_body"]}, Links: https://russian.rt.com{news["link"]}\n')
    save(news)

parse_news()

# SQLite3
# Создание базы данных
connection = sqlite3.connect('news_data.db')
cursor = connection.cursor()

# Создание таблицы
cursor.execute('DROP TABLE IF EXISTS news_data')
cursor.execute('''CREATE TABLE news_data (Article text, Pre_Body text, Link text)''')
connection.commit()

# Чтение текстового файла
csvfile = open('news.txt', 'r')
creader = csv.reader(csvfile, delimiter='±')

# Записываем данные из текстового файла в базу данных
for t in creader:
    cursor.execute('INSERT INTO  news_data VALUES (?,?,?)', t )

# Прерывание
csvfile.close()
connection.commit()
connection.close()

driver.quit()