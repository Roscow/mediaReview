# Autor:   Nicolas Valdes 
# Nombre:  script de scraping mediaReview
# Descripcion: obtiene titulares de noticias de diferentes medio
#------------------------------------------
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
options = FirefoxOptions()
options.add_argument("--headless")
from bs4 import BeautifulSoup
import os
import requests
from dotenv import load_dotenv
import os
import psycopg2
from datetime import datetime

# Cargar variables de entorno desde el archivo .env
load_dotenv()

#limpia la pantalla en los diferentes sistemas
def limpiar_pantalla(time,mensaje):
    if os.name == 'nt':
        os.system('cls')
    # Comando específico para sistemas Unix/Linux
    else:
        os.system('clear')
    print(mensaje)
    sleep(time)

#conexion con la bd 
def conectar_bd():
    try:
        host = os.getenv("HOST_DB")
        database = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        print("se realizo una conexion a la BD mediaReview")
    except:
        print("No fue posible conectar a la bd")
    return conn

#determina si la cadena tiene una, mas de una o cero palabras
def verificar_palabras1(cadena):
    palabras = cadena.split()
    num_palabras = len(palabras)
    if num_palabras == 1:
        return False
    elif num_palabras > 1:
        return True
    else:
        return "La cadena está vacía."

#entrega un listado con titulares que fueron verificados que son oraciones
def verificar_listado(lista):
    lista_final = list()
    for e in lista:
        cadena_limpia = e.replace('“', '').replace('”', '’').replace('‘', '').replace('’', '')
        verificado = verificar_palabras1(cadena_limpia)
        if (verificado == True):
            lista_final.append(e)
    return lista_final

#scrapings 
def scraping_t13():   
    try:
        print("iniciando scraping t13")
        driver = webdriver.Firefox(options=options)
        url = "https://www.t13.cl"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        card__title_list = soup.find_all('h2', class_='vertical-card__title')
        card__title_list2 = soup.find_all('h3', class_='vertical-card__title')
        card__title_list3 = soup.find_all('h4', class_='vertical-card__title')
        titulares = list()
        for e in card__title_list2:
            titulares.append(e.text)
        for e in card__title_list:
            titulares.append(e.text)
        for e in card__title_list3:
            titulares.append(e.text)
        driver.quit()
        print(f"el total de elementos scrapeados fue de : {len(titulares)}")
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en t13 por {e}")

def scraping_cooperativa():
    try:    
        print("Iniciando scraping cooperativa")
        driver = webdriver.Firefox(options=options)
        url = "https://cooperativa.cl/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()
        card__title_list1 = soup.find_all('h1', class_='titular-noticia')
        for e in card__title_list1:
            titulares.append(e.text)
        card__title_list3 = soup.find_all('h3', class_='titular-noticia')
        for e in card__title_list3:
            titulares.append(e.text)
        card__title_list4 = soup.find_all('div', class_='texto-titular')
        for e in card__title_list4:
            titulares.append(e.text)
        card__title_list5 = soup.find_all('div', class_='titulo-ple')
        for e in card__title_list5:
            titulares.append(e.text)
        card__title_list6 = soup.find_all('h3', class_='texto-titular')
        for e in card__title_list6:
            titulares.append(e.text)
        container = soup.find('div', class_='container-cooperativaciencia')
        card__title_list8 = container.find_all('div', class_='card')
        for e in card__title_list8:
            tit = e.find('span')
            titulares.append(tit.text.strip())
        card__title_list10 = soup.find_all('h3', class_='titular-texto')
        for e in card__title_list10:
            titulares.append(e.text)
        card__title_list11 = soup.find_all('h3', class_='titular-encuesta')
        for e in card__title_list11:
            titulares.append(e.text) 
        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en cooperativa por {e}")

def scraping_24hrs():
    try:
        print("Iniciando scraping 24hrs")
        driver = webdriver.Firefox(options=options)
        url = "https://www.24horas.cl/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()
        card__title_list1 = soup.find_all('h1', class_='tit')
        for e in card__title_list1:
            titulares.append(e.text)
        card__title_list2 = soup.find_all('h3', class_='tit')
        for e in card__title_list2:
            titulares.append(e.text)
        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en 24hrs por {e}")

def scraping_dinamo():
    try:
        print("Iniciando scraping el dinamo")
        driver = webdriver.Firefox(options=options)
        url = "https://www.eldinamo.cl/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()
        card__title_list1 = soup.find_all('h2')
        for e in card__title_list1:
            titulares.append(e.text)
        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en dinamo por {e}")

def scraping_cnnchile():
    try:
        print("Iniciando scraping cnn chile")
        driver = webdriver.Firefox(options=options)
        url = "https://www.cnnchile.com/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()

        card__title_list1 = soup.find_all('h2', class_='frost-highlight__title')
        for e in card__title_list1:
            titulares.append(e.text.strip())

        card__title_list2 = soup.find_all('h3', class_='the-card__title')
        for e in card__title_list2:
            titulares.append(e.text.strip())
        
        card__title_list3 = soup.find_all('h2', class_='_coronavirus-box-list__title' )
        for e in card__title_list3:
            titulares.append(e.text.strip())

        card__title_list4 = soup.find_all('h3', class_='card__title')
        for e in card__title_list4:
            titulares.append(e.text.strip())

        card__title_list5 = soup.find_all('h2', class_='c-digitalizados-box-card__title')
        for e in card__title_list5:
            titulares.append(e.text.strip())

        card__title_list6 = soup.find_all('h2', class_='after-card__title')
        for e in card__title_list6:
            titulares.append(e.text.strip())

        card__title_list7 = soup.find_all('div', class_ ='main-list__item')
        for e in card__title_list7:
            titulares.append(e.text.strip())

        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en cnn chile por {e}")

def scraping_elpais():
    try:
        print("Iniciando scraping el pais")
        driver = webdriver.Firefox(options=options)
        url = "https://elpais.com/noticias/chile/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()

        card__title_list1 = soup.find_all('h2', class_='c_t')
        for e in card__title_list1:
            titulares.append(e.text.strip())

        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en elpais por {e}")

def scraping_biobio():
    try:
        print("Iniciando scraping biobio")
        driver = webdriver.Firefox(options=options)
        url = "https://www.biobiochile.cl/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()

        card__title_list1 = soup.find_all('h2', class_='article-title')
        for e in card__title_list1:
            titulares.append(e.text.strip())
        
        card__title_list2 = soup.find_all('h3', class_='titular')
        for e in card__title_list2:
            titulares.append(e.text.strip())

        card__title_list3 = soup.find_all('h3', class_='article-title')
        for e in card__title_list3:
            titulares.append(e.text.strip())

        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en biobio por {e}")

def scraping_chilevisionNoticias():
    try:
        print("Iniciando scraping chilevision noticias")
        driver = webdriver.Firefox(options=options)
        url = "https://www.chvnoticias.cl/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()

        card__title_list1 = soup.find_all('h2', class_='the-card__title')
        for e in card__title_list1:
            titulares.append(e.text.strip())

        card__title_list2 = soup.find_all('h2', class_='headlines-list__title')
        for e in card__title_list2:
            titulares.append(e.text.strip())
        
        card__title_list3 = soup.find_all('img', class_='overlay-card__image')
        for e in card__title_list3:
            titulares.append(e.text.strip())

        card__title_list4 = soup.find_all('h2', class_='the-text-card__title')
        for e in card__title_list4:
            titulares.append(e.text.strip())
        
        card__title_list5 = soup.find_all('h2', class_='alt-card__title')
        for e in card__title_list5:
            titulares.append(e.text.strip())

        card__title_list6 = soup.find_all('h2', class_='media-card__title')
        for e in card__title_list6:
            titulares.append(e.text.strip())

        titulares = verificar_listado(titulares)
        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en chilevision por {e}")

def scraping_ciper():
    try:
        print("Iniciando scraping ciperchile")
        driver = webdriver.Firefox(options=options)
        url = "https://www.ciperchile.cl/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()
        card__title_list1 = soup.find_all('a', class_='alticle-link')
        print(f" elementos a revisar: {len (card__title_list1)}")
        sleep(3)
        for e in card__title_list1:
            titulares.append(e.text.strip())
        titulares = verificar_listado(titulares)
        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en ciper por {e}")
    
def scraping_soychile():
    try:
        print("Iniciando scraping soy chile")
        driver = webdriver.Firefox(options=options)
        url = "https://www.soychile.cl/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()

        card__title_list1 = soup.find_all('h1', class_='media-heading--principal')
        for e in card__title_list1:
            titulares.append(e.text.strip())

        card__title_list2 = soup.find_all('h2', class_='media-heading')
        for e in card__title_list2:
            titulares.append(e.text.strip())
        
        card__title_list3 = soup.find_all('div', class_='stv-widget__footer')
        for e in card__title_list3:
            titulares.append(e.text.strip())
        
        card__title_list4 = soup.find_all('h3', class_='note-sidebar-title')
        for e in card__title_list4:
            titulares.append(e.text.strip())
        
    #    card__title_list5 = soup.select('.carousel span:not([class])')
    #    for e in card__title_list5:
    #        titulares.append(e.text.strip())
        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en soychile por {e}")

def scraping_elmostrador():
    try:
        print("Iniciando scraping elmostrador")
        driver = webdriver.Firefox(options=options)
        url = "https://www.elmostrador.cl/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()

        card__title_list1 = soup.find_all('h2', class_='d-main-card__title')
        for e in card__title_list1:
            titulares.append(e.text.strip())

        card__title_list2 = soup.find_all('h2', class_='d-text-card__title')
        for e in card__title_list2:
            titulares.append(e.text.strip())
        
        card__title_list3 = soup.find_all('strong', class_='d-opinion-box-card__title')
        for e in card__title_list3:
            titulares.append(e.text.strip())
        
        card__title_list4 = soup.find_all('h1', class_='d-main-card__title')
        for e in card__title_list4:
            titulares.append(e.text.strip())

        card__title_list5 = soup.find_all('h3', class_='numbered-box__title')
        for e in card__title_list5:
            titulares.append(e.text.strip())
    
        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en elmostrador por {e}")

def scraping_latercera():
    try:
        print("Iniciando scraping la tercera")
        driver = webdriver.Firefox(options=options)
        url = "https://www.latercera.com/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()

        card__title_list1 = soup.find_all('div', class_='headline')
        for e in card__title_list1:
            titulares.append(e.text.strip())

        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en latercera por {e}")

def scraping_lacuarta():
    try:
        print("Iniciando scraping la cuarta")
        driver = webdriver.Firefox(options=options)
        url = "https://www.lacuarta.com/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()

        card__title_list1 = soup.find_all('h1', class_='article-title')
        for e in card__title_list1:
            titulares.append(e.text.strip())

        card__title_list1 = soup.find_all('h2', class_='article-title')
        for e in card__title_list1:
            titulares.append(e.text.strip())
        
        card__title_list1 = soup.find_all('div', class_='headline')
        for e in card__title_list1:
            titulares.append(e.text.strip())

        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en lacuarta por {e}")

def scraping_emol():
    try:
        print("Iniciando scraping el mercurio online")
        driver = webdriver.Firefox(options=options)
        url = "https://www.emol.com/"
        driver.get(url)
        sleep(30)
        for i in range(5):  # Ajusta la cantidad de veces que deseas hacer scroll
            print(f" scroll {i}")
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            sleep(10)   
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()

        list1 = soup.select('h1 a')
        for e in list1:
            titulares.append(e.text.strip())

        list2 = soup.select('h2 a')
        for e in list2:
            titulares.append(e.text.strip())

        list3 =  soup.select('h3 a')
        for e in list3:
            titulares.append(e.text.strip())
        
        list4 = soup.select('h4 a')
        for e in list4:
            titulares.append(e.text.strip())

        list5 = soup.select('h5 a')
        for e in list5:
            titulares.append(e.text.strip())

        list6 = soup.find_all('div', class_='divico_txt')
        for e in list6:
            titulares.append(e.text.strip())

        list7 = soup.select('.contenedor-titulo a')
        for e in list7:
            titulares.append(e.text.strip())
        
        list8 = soup.select('.noticias_caja_texto a')
        for e in list8:
            titulares.append(e.text.strip())

        list9 = soup.find_all('div', class_='caja_contenedor_masvistos_modulo_texto')
        for e in list9:
            titulares.append(e.text.strip())

        list10 = soup.select('.titulo_mag1 a')
        for e in list10:
            titulares.append(e.text.strip())

        list11 = soup.select('.titulo1 a')
        for e in list11:
            titulares.append(e.text.strip())

        list12 = soup.select('.titulo2 a')
        for e in list12:
            titulares.append(e.text.strip())

        list13 = soup.select('.titulo_dep1 a')
        for e in list13:
            titulares.append(e.text.strip())

        list13 = soup.select('.titulo_dep2 a')
        for e in list13:
            titulares.append(e.text.strip())

        list13 = soup.select('.titulo_dep3 a')
        for e in list13:
            titulares.append(e.text.strip())

        list13 = soup.select('.titulo_tend1 a')
        for e in list13:
            titulares.append(e.text.strip())
        
        list13 = soup.select('.titulo_tend2 a')
        for e in list13:
            titulares.append(e.text.strip())

        list13 = soup.select('.titulo_tend3 a')
        for e in list13:
            titulares.append(e.text.strip())

        list13 = soup.select('.caja_multi_model_txt a')
        for e in list13:
            titulares.append(e.text.strip())

        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en emol por {e}")

def scraping_lasegunda():
    try:
        print("Iniciando scraping la segunda")
        driver = webdriver.Firefox(options=options)
        url = "https://impresa.lasegunda.com/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()

        list1 = soup.select('.contenedor_der_nota_rank')
        for e in list1:
            h2_element = e.find('h2')
            h3_element = e.find('h3')
            tit = h2_element.text.strip()+ " "+h3_element.text.strip()
            titulares.append(tit)

        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en lasegunda por {e}")
#pendiente
def scraping_lun():
    print("Iniciando scraping LUN")
    driver = webdriver.Firefox(options=options)
    url = "https://www.lun.com/"
    driver.get(url)
    sleep(30)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    titulares = list()

    list1 = soup.select('a')
    for e in list1:
        titulares.append( e.text.strip())

    driver.quit()
    print(f"total : {len(titulares)}")
    sleep(10)
    print("finalizando scraping")
    sleep(10)
    datos_obtenidos= len(titulares)
    titulares = verificar_listado(titulares)
    dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
    return dic
   
def scraping_df():
    try:
        print("Iniciando scraping diario financiero")
        driver = webdriver.Firefox(options=options)
        url = "https://www.df.cl/"
        driver.get(url)
        sleep(60)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()

        list1 = soup.select('h2 a')
        for e in list1:
            titulares.append( e.text.strip())
        list1 = soup.select('.titular')
        for e in list1:
            titulares.append( e.text.strip())
        list1 = soup.select('h3 a')
        for e in list1:
            titulares.append( e.text.strip())
        list1 = soup.select('h6')
        for e in list1:
            titulares.append( e.text.strip())
        list1 = soup.select('.imagecover-titulo a')
        for e in list1:
            titulares.append( e.text.strip())
        list1 = soup.select('.titulo-reportaje a')
        for e in list1:
            titulares.append( e.text.strip())    
            
        list1 = soup.select('.titular strong a')
        for e in list1:
            titulares.append( e.text.strip())  

        list1 = soup.select('.txt-caja-video')
        for e in list1:
            titulares.append( e.text.strip()) 

        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en diariofinanciero por {e}")

def scraping_meganoticias():
    try:
        print("Iniciando scraping meganoticias")
        driver = webdriver.Firefox(options=options)
        url = "https://www.meganoticias.cl/"
        driver.get(url)
        sleep(30)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        titulares = list()

        list1 = soup.select('.titular')
        for e in list1:
            titulares.append( e.text.strip())

        driver.quit()
        print(f"total : {len(titulares)}")
        sleep(10)
        print("finalizando scraping")
        sleep(10)
        datos_obtenidos= len(titulares)
        titulares = verificar_listado(titulares)
        dic = {'link':url, 'data_scraping': datos_obtenidos, 'titulares':titulares}
        return dic
    except Exception as e:
        print(f"no se pudo hacer scraping en meganoticias por {e}")
      
#obtener noticias para un medio
def obtener_noticias_medio_diario(medio_diario):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM noticia where medio_diario={medio_diario};")
    lista_noticias = cursor.fetchall()
    cursor.close()
    conn.close()
    return lista_noticias

#obtener determinacion_ia para una noticia
def obtener_determinacion_id(noticia_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM determinacion_ia where noticia={noticia_id};")
    data= cursor.fetchall()
    determinacion = data[0][0]
    cursor.close()
    conn.close()
    return determinacion

#obtener un medio_diario para una fecha y para un medio
def obtener_medio_diario(fecha, medio):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM medio_diario where medio={medio} and fecha='{fecha}' ;")
    datos = cursor.fetchall()
    medio_diario= datos[0][0]
    cursor.close()
    conn.close()
    return medio_diario

#obtener un medio con un link
def obtener_medio(link):
    subconsulta_medio = (f"select id from medio where direccion_web='{link}';")
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(subconsulta_medio)
    datos = cursor.fetchall()
    medio= datos[0][0]
    cursor.close()
    conn.close()
    return medio

#eliminar determinaciones 
def eliminar_determinaciones(lista_noticias,conexion):
    cur = conexion.cursor()
    for d in lista_noticias:
        cur.execute(f"DELETE FROM determinacion_ia where noticia ={d[0]};")
        print(f"eliminando determinacion con noticia id {d[0]}")
        conexion.commit()
    cur.close()

#eliminar medio diario
def eliminar_medio_diario(medio,fecha,conexion):
    try:
        cur = conexion.cursor()
        cur.execute(f"select id from medio_diario where medio={medio} and fecha='{fecha}';")
        data = cur.fetchall()
        id_medio_diario = data[0][0]
        cur.execute(f"DELETE FROM medio_diario where id ={id_medio_diario};")
        conexion.commit()
        cur.close()
        print(f"se elimino medio diario id ={id_medio_diario}")
    except:
        print(f"no se pudo eliminar medio diario")

#eliminar noticias
def eliminar_noticias(medio_diario,conexion):
    cur = conexion.cursor()
    cur.execute(f"delete from noticia WHERE medio_diario={medio_diario} ;")
    conexion.commit()
    cur.close()

#eliminar datos
def eliminar_data(datos,fecha):
    conn = conectar_bd()
    link=datos.get("link")
    medio = obtener_medio(link)
    medio_diario = obtener_medio_diario(fecha,medio)
    lista_noticias = obtener_noticias_medio_diario(medio_diario)
    eliminar_determinaciones(lista_noticias,conn)
    eliminar_noticias(medio_diario,conn)
    eliminar_medio_diario(medio,fecha,conn)
    conn.close()

def verificar_integridad(datos, fecha):
    try:
        #obtener los datos titulares de scraping
        titulares= datos.get('titulares')
        total_datos_scraping = len(titulares)
        #obtener los datos insertados en la bd para ese dia /medio
        conn =  conectar_bd()
        cursor = conn.cursor()
        link= datos.get('link')
        print(f"verificando datos en {link}")
        subconsulta_medio = (f"select id from medio where direccion_web='{link}'")
        cursor.execute(f"SELECT id FROM medio_diario where medio=({subconsulta_medio}) and fecha='{fecha}' ;")
        datos = cursor.fetchall()
        medio_diario= datos[0][0]
        cursor.execute(f"SELECT count(id) FROM noticia where medio_diario={medio_diario};")
        datos = cursor.fetchall()
        datos_insertados= datos[0][0]
        cursor.close()
        conn.close()
        #comparar ambos
        print(f"insertados: {datos_insertados} --- scrapeados: {total_datos_scraping}")
        if(abs(datos_insertados-total_datos_scraping) >10 ):
            print("datos no fueron validados")
            return False
        else:
            print("datos validados")
            return True
    except Exception as e:
        print(f"datos no fueron validados por {e}")
        return True

def eliminar_datos_posibles(datos,fecha):
    try:
        conn =  conectar_bd()
        cursor = conn.cursor()
        link= datos.get('link')
        subconsulta_medio = (f"select id from medio where direccion_web='{link}'")
        cursor.execute(f"SELECT id FROM medio_diario where medio=({subconsulta_medio}) and fecha='{fecha}' ;")
        datos = cursor.fetchall()
        medio_diario= datos[0][0]
        cursor.execute(f"SELECT id FROM noticia WHERE medio_diario={medio_diario};")
        noticias = cursor.fetchall()
        lista_determinaciones=list()

        for d in noticias:
            id_noticia = d[0]
            cursor.execute(f"select id FROM determinacion_ia where noticia={id_noticia};")
            datos = cursor.fetchall()
            if(len(datos)>0):
                id_determinacion = datos[0][0]
                lista_determinaciones.append(id_determinacion)
            conn.commit()
            #eliminar noticias
            print(f"eliminando noticia con id {id_noticia}")

        for det in lista_determinaciones:
            cursor.execute(f"delete from determinacion_ia where id={det}")
            print(f"se elimino determinacion_ia para id {det} ")
        conn.commit()
        for d in noticias:
            cursor.execute(f"delete from noticia where id={d[0]}")
            print(f"se elimino noticia para noticia {d[0]} ")
        conn.commit()    

        #eliminar medio diario
        cursor.execute(f"DELETE FROM medio_diario where id={medio_diario};")
        print(f"se elimino medio_diario para id {medio_diario} ")
        conn.commit()
        #eliminar analisis diario
        cursor.execute(f"DELETE FROM analisis_diario where medio = ({subconsulta_medio}) and fecha ='{fecha}' ;")
        print(f"se elimino analisis_diario para medio {subconsulta_medio} ")
        conn.commit()
        print(f"datos eliminados para {link} en {fecha}")
    except Exception as e:
        print(f"no fue posible elimnar por: {e}")

def ciclo_scraping():
    ejecutar_nuevo_ciclo=True
    contador_nuevo_ciclo=0
    fecha = datetime.now()
    while(ejecutar_nuevo_ciclo==True):
        print("iniciando ciclo de scraping ")
        tiempo_inicio = time.time()
        
        datos= scraping_t13()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_cooperativa()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_24hrs()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_dinamo()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_cnnchile()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_elpais()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        #problemas con la verificacion
        datos = scraping_biobio()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_chilevisionNoticias()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_ciper()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_soychile()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_elmostrador()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1
        
        datos = scraping_latercera()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_lacuarta()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_emol()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_lasegunda()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_df()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1

        datos = scraping_meganoticias()
        if(verificar_integridad(datos,fecha)==False):
            eliminar_datos_posibles(datos,fecha)
            insertar_data(datos)
            contador_nuevo_ciclo +=1
        print("ciclo finalizado ")

        if(contador_nuevo_ciclo<0):
            ejecutar_nuevo_ciclo=True

    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio
    realizar_analisis_general(fecha)
    print(f"tiempo transcurrido: {tiempo_total}")

def ciclo_scraping2():
    codigo_ejecutar = list()
    fecha = datetime.now()
    tiempo_inicio = time.time()
    for e in range(17):
        codigo_ejecutar.append(e)
    while(len(codigo_ejecutar)>0 ):
        print(f"codigo a ejecutar: {codigo_ejecutar}")
        sleep(3)
        #recorrer el arreglo
        if(0 in codigo_ejecutar):
            datos= scraping_t13()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(0)

        if(1 in codigo_ejecutar):
            datos = scraping_cooperativa()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(1)

        if(2 in codigo_ejecutar):
            datos = scraping_24hrs()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)   
            else:
                codigo_ejecutar.remove(2)     

        if(3 in codigo_ejecutar):
            datos = scraping_dinamo()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(3)
                
        if(4 in codigo_ejecutar):
            datos = scraping_cnnchile()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(4)
                
        if(5 in codigo_ejecutar):  
            datos = scraping_elpais()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(5)
                
        if(6 in codigo_ejecutar):
            datos = scraping_biobio()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(6)
        if(7 in codigo_ejecutar):
            datos = scraping_chilevisionNoticias()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(7)

        if(8 in codigo_ejecutar):
            datos = scraping_ciper()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(8)

        if(9 in codigo_ejecutar):
            datos = scraping_soychile()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(9)    
            
        if(10 in codigo_ejecutar):
            datos = scraping_elmostrador()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(10)

        if(11 in codigo_ejecutar):
            datos = scraping_latercera()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)  
            else:
                codigo_ejecutar.remove(11)

        if(12 in codigo_ejecutar):
            datos = scraping_lacuarta()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(12)

        if(13 in codigo_ejecutar):
            datos = scraping_emol()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(13)

        if(14 in codigo_ejecutar):
            datos = scraping_lasegunda()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(14)

        if(15 in codigo_ejecutar):
            datos = scraping_df()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(15)

        if(16 in codigo_ejecutar):
            datos = scraping_meganoticias()
            if(verificar_integridad(datos,fecha)==False):
                eliminar_datos_posibles(datos,fecha)
                insertar_data(datos)
            else:
                codigo_ejecutar.remove(16)
                
    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio
    #consultar
    realizar_analisis_general(fecha)
    print(f"tiempo transcurrido: {tiempo_total}")

def ciclo_scraping3():
    fecha = datetime.now()
    tiempo_inicio = time.time()
    print("Iniciando nuevo ciclo de scraping ")
    lista_datos = list()

    datos= scraping_t13()
    lista_datos.append(datos)
    
    datos = scraping_cooperativa()
    lista_datos.append(datos)

    datos = scraping_24hrs()
    lista_datos.append(datos)

    datos = scraping_dinamo()
    lista_datos.append(datos)
                
    datos = scraping_cnnchile()
    lista_datos.append(datos)
         
    datos = scraping_elpais()
    lista_datos.append(datos)
                
    datos = scraping_biobio()
    lista_datos.append(datos)

    datos = scraping_chilevisionNoticias()
    lista_datos.append(datos)

    datos = scraping_ciper()
    lista_datos.append(datos)

    datos = scraping_soychile()
    lista_datos.append(datos)

    datos = scraping_elmostrador()
    lista_datos.append(datos)

    datos = scraping_latercera()
    lista_datos.append(datos)

    datos = scraping_lacuarta()
    lista_datos.append(datos)

    datos = scraping_emol()
    lista_datos.append(datos)

    datos = scraping_lasegunda()
    lista_datos.append(datos)

    datos = scraping_df()
    lista_datos.append(datos)

    datos = scraping_meganoticias()
    lista_datos.append(datos)

    for e in lista_datos:
        eliminar_data(e)
        insertar_data(e)

    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio
    realizar_analisis_general(fecha)
    print(f"tiempo transcurrido: {tiempo_total}")

def ciclo_scraping4():
    fecha = datetime.now()
    print("Iniciando nuevo ciclo de scraping ")
    datos3 = scraping_24hrs()
    if(verificar_integridad(datos3,fecha)==False):
        eliminar_data(datos3,fecha)
        insertar_data(datos3)

def determinar_contexto(titulares,nombreMedio):
    print(f"Verificando contexto de titulares en {nombreMedio}")
    totalTitulares = len(titulares)
    contador=1
    for e in titulares:
        print("--------------------------------")
        print(f"revisando: {contador}/{totalTitulares}")
        print(f"contexto en: {e}")
        respuesta = obtener_respuesta_openai(e)
        print(f"respuesta IA: {respuesta}")
        clasificacion = clasificar_titular(respuesta)
        print(f"determinacion final: {clasificacion}")
        contador= contador + 1

def determinar_contexto_singular(titular):
    respuesta = obtener_respuesta_openai(titular)
    print(f"IA: {respuesta}")
    clasificacion = clasificar_titular(respuesta)
    return clasificacion

def determinar_contexto_singular2(titular):
    respuesta = obtener_respuesta_openai(titular)
    print(f"IA: {respuesta}")
    #clasificacion = clasificar_titular(respuesta)
    return respuesta

def contar_palabras2(palabra, cadena):
    palabra = palabra.lower()
    cadena = cadena.lower()
    frecuencia = cadena.count(palabra)
    return frecuencia

def clasificar_titular(respuesta):
    contador_positivo = contar_palabras2('positiv',respuesta)
    contador_negativo = contar_palabras2('negativ',respuesta)
    contador_neutro = contar_palabras2('neutr',respuesta)
    dic = {'positivo':contador_positivo, 'negativo':contador_negativo, 'neutro':contador_neutro  }
    print(f"Pos:{dic.get('positivo')}  Neg:{dic.get('negativo')}  Neutro:{dic.get('neutro')}")

    # todos iguales
    if(dic.get('positivo') == dic.get('negativo') == dic.get('neutro') ):
        return 'neutro'
    else:
        # todos diferentes (habra uno mayor)
        if(dic.get('positivo') != dic.get('negativo') and dic.get('positivo') != dic.get('neutro') and dic.get('negativo') != dic.get('neutro') ):
            return max(dic, key=dic.get)
        else:
            # 2 iguales el otro mayor que los otros
            # 2 iguales el otro menor que los otros 
            return max(dic, key=dic.get)
    
def obtener_respuesta_openai(prompt):
    url = "https://api.openai.com/v1/chat/completions"  # Asegúrate de tener la URL correcta según la documentación de OpenAI
    clave_api = os.getenv("CLAVE_API_AI")  # Reemplaza con tu clave API de OpenAI
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {clave_api}",
    }
    data = {
        "model": "gpt-3.5-turbo",  # Modelo específico de ChatGPT
        "messages": [{"role": "system", "content": "Eres un asistente que determinara si un titular de noticia tiene un contexto negativo, positivo o neutro. responder concreta y brevemente"}, {"role": "user", "content": prompt}],
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error en la solicitud: {response.status_code} - {response.text}"

def realizar_analisis_general(fecha):
    print("realizando analisis general")
    conn = conectar_bd()
    cursor = conn.cursor()
    cadena_fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
    fecha_date , fecha_time = cadena_fecha.split(' ')
    fecha=fecha_date
    #ver si existe
    cursor.execute(f"Select id from analisis_general where fecha='{fecha}';")
    resultados = cursor.fetchall()
    subconsulta_medio_diario =(f"SELECT id FROM medio_diario WHERE fecha= '{fecha}'")
    # Verificar si hay resultados
    if resultados:  
        id_analisis = resultados[0]
        print("analisis ya existe para esa fecha")
        cursor.execute(f"delete from analisis_general where id={id_analisis};")
        print("se elimino registro existente")

        #el total de noticias para ese dia
        cursor.execute(f"SELECT COUNT(id) FROM  noticia where medio_diario in ({subconsulta_medio_diario});")
        datos = cursor.fetchall()
        total_general = datos[0][0]
        #el total de noticias con contexto positivo
        cursor.execute(f"SELECT COUNT(id) FROM  noticia where medio_diario in ({subconsulta_medio_diario}) and contexto = (select id from contexto where tipo ilike 'positivo')  ;")
        datos = cursor.fetchall()
        total_positivo = datos[0][0]
        #el total de noticias con contexto negativo
        cursor.execute(f"SELECT COUNT(id) FROM  noticia where medio_diario in ({subconsulta_medio_diario}) and contexto = (select id from contexto where tipo ilike 'negativo')  ;")
        datos = cursor.fetchall()
        total_negativo = datos[0][0]
        #el total de noticias con contexto neutro
        cursor.execute(f"SELECT COUNT(id) FROM  noticia where medio_diario in ({subconsulta_medio_diario}) and contexto = (select id from contexto where tipo ilike 'neutro')  ;")
        datos = cursor.fetchall()
        total_neutro = datos[0][0]
        #insertar en analisis general
        cursor.execute(f"INSERT INTO analisis_general(fecha,buenas,malas,neutra,total) VALUES('{fecha}',{total_positivo},{total_negativo},{total_neutro},{total_general} );")
        conn.commit()
        print(" analisis general completado")

    else:
        #el total de noticias para ese dia
        cursor.execute(f"SELECT COUNT(id) FROM  noticia where medio_diario in ({subconsulta_medio_diario});")
        datos = cursor.fetchall()
        total_general = datos[0][0]
        #el total de noticias con contexto positivo
        cursor.execute(f"SELECT COUNT(id) FROM  noticia where medio_diario in ({subconsulta_medio_diario}) and contexto = (select id from contexto where tipo ilike 'positivo')  ;")
        datos = cursor.fetchall()
        total_positivo = datos[0][0]
        #el total de noticias con contexto negativo
        cursor.execute(f"SELECT COUNT(id) FROM  noticia where medio_diario in ({subconsulta_medio_diario}) and contexto = (select id from contexto where tipo ilike 'negativo')  ;")
        datos = cursor.fetchall()
        total_negativo = datos[0][0]
        #el total de noticias con contexto neutro
        cursor.execute(f"SELECT COUNT(id) FROM  noticia where medio_diario in ({subconsulta_medio_diario}) and contexto = (select id from contexto where tipo ilike 'neutro')  ;")
        datos = cursor.fetchall()
        total_neutro = datos[0][0]
        #insertar en analisis general
        cursor.execute(f"INSERT INTO analisis_general(fecha,buenas,malas,neutra,total) VALUES('{fecha}',{total_positivo},{total_negativo},{total_neutro},{total_general} );")
        conn.commit()
        print(" analisis general completado")

def insertar_data(dic):
    try:
        titulares= dic.get('titulares')
        link=dic.get('link')
        data_scraping = dic.get('data_scraping')
        print(f"Insertando datos en {link}")
        conn = conectar_bd()
        cursor = conn.cursor()

        #insertar medio_diario
        fecha = datetime.now()
        cursor.execute(f"SELECT id FROM medio WHERE direccion_web='{link}' LIMIT 1;")
        datos = cursor.fetchall()
        medio= datos[0][0]
        cursor.execute(f"INSERT INTO medio_diario(medio,fecha) VALUES({medio},'{fecha}');")
        print(f"se inserto medio diario :  {medio} , {fecha}")
        conn.commit()

        #obtener el id del medio_diario recien creado
        cursor.execute(f"SELECT id FROM medio_diario WHERE medio={medio} and fecha ='{fecha}' LIMIT 1;")
        datos = cursor.fetchall()
        medio_diario = datos[0][0]
        total_titulares = len(titulares)
        #insertar noticias 
        contador=1
        for e in titulares:
            #determinar contexto
            e = e.replace("'",'')
            e = e.replace("´",'')
            e = e.replace("`",'')
            print("...................................")
            print(f"Analizando {contador}/{total_titulares}")
            print(f"determinando contexto en : {e} ")
            #clasificacion = determinar_contexto_singular(e)
            respuesta_ia = determinar_contexto_singular2(e)
            clasificacion = clasificar_titular(respuesta_ia)
            print(f"contexto: {clasificacion}")
            contexto = (f"SELECT id FROM contexto WHERE tipo ilike '{clasificacion}' ")
            cursor.execute(f"INSERT INTO noticia(medio_diario,titular,contexto ) VALUES({medio_diario},'{e}',({contexto}) );")
            print(f"se inserto noticia con medio_diario {medio_diario}")
            conn.commit()
            contador=contador+1

            #obtener id de la noticia recien creada
            cursor.execute(f"SELECT id FROM noticia WHERE medio_diario={medio_diario} and titular='{e}' ;")
            id_noticia = cursor.fetchall()
            id_noticia= id_noticia[0][0]
            #insertar ia response 
            cursor.execute(f"INSERT INTO determinacion_ia(noticia,respuesta ) VALUES({id_noticia},'{respuesta_ia}');")
            print(f"se inserto determinacion con {id_noticia}, {respuesta_ia}")
            conn.commit()

        #analisis diario
        query_buenas = cursor.execute(f"SELECT COUNT(id) FROM noticia WHERE medio_diario={medio_diario} and contexto=(select id from contexto where tipo ilike 'positivo');")
        datos = cursor.fetchall()
        query_buenas= datos[0][0]
        query_malas = cursor.execute(f"SELECT COUNT(id) FROM noticia WHERE medio_diario={medio_diario} and contexto=(select id from contexto where tipo ilike 'negativo');")
        datos = cursor.fetchall()
        query_malas= datos[0][0]
        query_neutro = cursor.execute(f"SELECT COUNT(id) FROM noticia WHERE medio_diario={medio_diario} and contexto=(select id from contexto where tipo ilike 'neutro');")
        datos = cursor.fetchall()
        query_neutro= datos[0][0]
        cursor.execute(f"INSERT INTO analisis_diario(medio,fecha,buenas,malas,neutra,total,data_scraping) VALUES({medio},'{fecha}',{query_buenas},{query_malas},{query_neutro},{total_titulares},{data_scraping});")
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error durante insertar data: {e}")

ciclo_scraping3()


