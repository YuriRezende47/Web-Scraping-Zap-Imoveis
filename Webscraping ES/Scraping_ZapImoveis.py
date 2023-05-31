from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager #Precisa estar usando Chrome. Caso esteja usando outro navegador. Procurar o driver necessário para aplicação com ele e fazer as mudanças. 
import pandas as pd



options = Options()
options.add_argument('--disable-notifications')
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico, options=options)
navegador.set_window_size(1200, 1200)
navegador.get('') #Colocar URL que você deseja extrair (Precisa ser da região de ES)
navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
page_content = navegador.page_source

site = BeautifulSoup(page_content, 'html.parser')

imoveiss = site.findAll('div', attrs={'class': 'card-container js-listing-card'})

lista_deImo = []
for el in imoveiss:
    lista_deImo.append(str(el))
data_idList = []
for i in lista_deImo:
    data_idList.append(i[i.find('data-id="')+9:i.find('data-id="')+19])


dados_terrenos = []

for iterate, imoveis in enumerate(imoveiss):
    distrito_imoveis = imoveis.find('h2', attrs={'class': 'simple-card__address color-dark text-regular', 'ellipsis-lines': '1'})
    distrito_imoveis = distrito_imoveis.text.strip()
    precos = imoveis.find('p', attrs={'class': 'simple-card__price js-price color-darker heading-regular heading-regular__bolder align-left'})
    preco_texto = " ".join(precos.text.split())
    try:
        metro_quadrado = imoveis.find('span', attrs={'itemprop': 'floorSize'})
        area = metro_quadrado.text.strip()
    except AttributeError:
        area = 'Não informado'

    dist = (distrito_imoveis[distrito_imoveis.find(",")+1:].lower()).replace(" ", "-")
    muni = (distrito_imoveis[0:distrito_imoveis.find(",")].lower()).replace(" ", "-")

    url = f'https://www.zapimoveis.com.br/imovel/venda-terreno-lote-condominio-{muni}{dist}-es-id-{data_idList[iterate]}/'  #Está programado para gerar uma "url" artificial sendo possivel alterar trocando as informações padronizadas. O resto o próprio codigo vai fazer.

    navegador.get(url)
    sub_page_content = navegador.page_source
    sub_aba = BeautifulSoup(sub_page_content, 'html.parser')
    try:
        vendedores = sub_aba.find('p', attrs={'class': 'publisher__title heading-small align-left'})
        vendedor = {vendedores.text.strip()}
    except AttributeError:
        vendedor = "Não Informado"
    try:
        crecis = sub_aba.find('p', attrs={'class': 'publisher__license text-regular'})
        creci = {crecis.text.strip()}
    except AttributeError:
        creci = "Não informado"

    
    

    try:
        print(f'Distrito: {distrito_imoveis}')
    except AttributeError:
        print("Distrito não informado.")
    try:
        print(f'Area: {area}')
    except AttributeError:
        print("Area não informado.")
    try:
        print(f'URL: {url}')
    except AttributeError:
        print('URL não informado.')
    try:
        print(f'Vendedor: {vendedor}')
    except AttributeError:
        print("Vendedor não informado.")
    try:
        print(f'Creci: {creci}')
    except AttributeError:
        print("Creci não informada.")
    try:
        print(f'Preço: {preco_texto}')
    except AttributeError:
        print("Preço não informado.")
    print("-="*30)

    if (iterate + 1) % 25 == 0:
        print("Pausando por 3 minutos...")
        sleep(250)
    
    dados_terrenos.append([distrito_imoveis, area, preco_texto, vendedor, creci, url])

terreno_csv = pd.DataFrame(dados_terrenos, columns=['cidade e distrito', 'Area', 'Preço', 'Anunciante', 'Creci', 'url'])
print(terreno_csv)

terreno_csv.to_csv('', index=False, encoding='utf-8-sig')

