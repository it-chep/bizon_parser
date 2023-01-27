from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import shutil
import os
from time import sleep
import zipfile
from selenium.webdriver.common.keys import Keys
import pickle

def get_html(url):
        
        # options
    options = webdriver.FirefoxOptions()
    
    options.headless = True
    print("headless")
    
    driver = webdriver.Firefox(
        executable_path="/snap/bin/geckodriver",
        options=options)
    print("OK 200")
    
    driver.get(url=url)

    authorize_page = driver.page_source

    soup = BeautifulSoup(authorize_page, 'lxml')

    inputs = soup.find_all("div", class_="input-group group")

    dopi = soup.find_all("div", class_="input-group group customFieldGroup")

    if soup.find("div", class_="row form-group has-feedback hidden") is None:
        if_phone = soup.find("div", class_="row form-group has-feedback").find("input", class_="form-control")
    else:
        if_phone = None

    for inp in inputs:
        if inp.find("input").get("id") == "input-useremail":
            driver.find_element(By.ID, "input-useremail").send_keys('123@qwe.ru')
        else:
            idi = inp.find("input").get("id")
            driver.find_element(By.ID, f'{idi}').send_keys('1234')

    for dop in dopi:
        name = dop.find("input", class_="form-control").get('name')
        driver.find_element(By.NAME, f'{name}').send_keys('123')

    if if_phone is not None:
        driver.find_element(By.ID, 'input-userphone').send_keys('89326586327')

    button = driver.find_element(By.ID, 'btnLogin')
    button.click()

    sleep(4)

    main_page = driver.page_source

    return main_page

    # driver.close()
    # driver.quit()


def get_links(message, bot, main_page):

    soup = BeautifulSoup(main_page, 'lxml')

    links = soup.find_all('iframe')

    val_youtube_link = links[0].get('src')

    ind1 = val_youtube_link.find('?')

    val_youtube_link = val_youtube_link[:ind1]

    pres_link = (soup.find("img").get('src') if soup.find("img") is not None else None)

    val_pres_link = None

    if pres_link is not None:
        ind1 = pres_link.find('s')
        val_pres_link = pres_link[ind1:-1]
        mess = f'На вебинаре есть ссылка на презентацию!\n' \
               f'Приступаю к скачиванию всех слайдов.'
    else:
        mess = 'На вебинаре нет ссылки на презентацию,' \
               ' я обязательно помогу тебе в следующий раз'

    bot.send_message(message.chat.id, mess)

    if "youtube.com" in val_youtube_link:
        mess = f'Держи ссылочки на трансляцию\n{val_youtube_link}'
    else:
        mess = 'К сожалению, вебинаре нет ссылки на YouTube'

    bot.send_message(message.chat.id, mess)

    return val_pres_link


def download_slides(url=''):
    url = 'https://' + url
    count = 0
    url_ind = None

    for i in range(len(url)):
        if url[i] == '/':
            count += 1
            if count == 7:
                url_ind = i + 1
                break

    count_slides = 0

    url = url[:url_ind] + str(count_slides) + '.png'

    response = requests.get(url=url)

    while response.status_code == 200:

        url = url[:url_ind] + str(count_slides) + '.png'
        response = requests.get(url=url)
        count_slides += 1

        if response.status_code == 200:
            with open(f'{count_slides}.jpg', 'wb') as file:
                file.write(response.content)

    return count_slides


def make_zip(count_slides):
    os.mkdir('Presentation.zip')
    zip_object = zipfile.ZipFile('Presentation.zip', 'w')
    for i in range(1, count_slides):
        path = str(i) + '.jpg'
        zip_object.write(path)
        # os.replace(path, f'Presentation/{path}')
    # os.mkdir('Root')
    # os.replace('Presentation', 'Root/Presentation')


def send_pres(message, bot):
    with open('Presentation.zip', 'rb') as F:
        bot.send_document(message.chat.id, F, caption='Сделал для тебя zip-архив всех слайдов!')


def remove():
    # os.remove('Root')
    # shutil.rmtree('Root')
    os.remove('Presentation.zip')