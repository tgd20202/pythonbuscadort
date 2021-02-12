import requests
from bs4 import BeautifulSoup
from lxml import html
import re


def politecnico(filterCatalogue):
    # poli
    hostUrl = "http://prometeo-politecnicojic.hosted.exlibrisgroup.com"
    constUrl = hostUrl + "/F/?func=find-b&request=" + filterCatalogue + "&find_code=WRD&adjacent=N&x=32&y=94=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5=";
    # //tr[@valign="baseline"]
    reponse = []
    for index, item in enumerate(
            BeautifulSoup(requests.get(constUrl).content, 'lxml').find_all('tr', {"valign": "baseline"})):
        try:
            reponse.append({
                "id": index,
                "autor": item.find_all('td')[2].getText(),
                "titulo": re.search("(title='(.*)recordLink)", item.find_all('td')[4].find('script').contents[0]).group(
                    0).replace("title='", "").replace("recordLink", ""),
                "url": item.find_all('td')[9].find('a', href=True)['href'].replace('javascript:open_window("',
                                                                                   "").replace('");', "")
            })
        except:
            print("OCURRIO UN ERROR")

    return reponse


def uni_antioquia(filterCatalogue):
    hostUrl = "http://opac.udea.edu.co"
    constUrl = hostUrl + "/cgi-olib/?keyword=" + filterCatalogue + "&session=10442211&nh=20&infile=presearch.glue"
    reponse = []
    # //table[@class="hitlist-alt"]
    r = requests.get(constUrl)
    for index, item in enumerate(BeautifulSoup(r.content, 'lxml').find_all('tr', {"class": "olib_hitlist_item_even"})):
        try:
            reponse.append({
                "id": index,
                "autor": item.find_all('td')[2].find('i').getText() if item.find_all('td')[2] else None,
                "titulo": item.find_all('td')[2].find('a').getText() if item.find_all('td')[2] else None,
                "url": hostUrl + item.find_all('td')[2].find('a')['href'] if item.find_all('td')[2] else None
            })
        except:
            print("OCURRIO UN ERROR")

    for index, item in enumerate(BeautifulSoup(r.content, 'lxml').find_all('tr', {"class": "olib_hitlist_item_odd"})):
        try:
            reponse.append({
                "id": 10 + index,
                "autor": item.find_all('td')[2].find('i').getText() if item.find_all('td')[2] else None,
                "titulo": item.find_all('td')[2].find('a').getText() if item.find_all('td')[2] else None,
                "url": hostUrl + item.find_all('td')[2].find('a')['href'] if item.find_all('td')[2] else None
            })
        except:
            print("OCURRIO UN ERROR")

    return reponse


def itm(filterCatalogue):
    hostUrl = "https://catalogobibliotecas.itm.edu.co"
    constUrl = hostUrl + "/cgi-olib/?keyword=" + filterCatalogue + "&session=46810913&nh=20&infile=presearch.glue";

    reponse = []

    r = requests.get(constUrl, verify=False)
    for index, item in enumerate(BeautifulSoup(r.content, 'lxml').find_all('tr', {"class": "olib_hitlist_item_even"})):
        try:
            reponse.append({
                "id": index,
                "autor": item.find_all('td')[2].find('i').getText() if item.find_all('td')[2].find('i') else None,
                "titulo": item.find_all('td')[2].find('a').getText() if item.find_all('td')[2] else None,
                "url": hostUrl + item.find_all('td')[2].find('a')['href'] if item.find_all('td')[2] else None
            })
        except:
            print("OCURRIO UN ERROR")

    for index, item in enumerate(BeautifulSoup(r.content, 'lxml').find_all('tr', {"class": "olib_hitlist_item_odd"})):
        try:
            reponse.append({
                "id": 10 + index,
                "autor": item.find_all('td')[2].find('i').getText() if item.find_all('td')[2].find('i') else None,
                "titulo": item.find_all('td')[2].find('a').getText() if item.find_all('td')[2] else None,
                "url": hostUrl + item.find_all('td')[2].find('a')['href'] if item.find_all('td')[2] else None
            })
        except:
            print("OCURRIO UN ERROR")
    return reponse


def san_buenaventura(filterCatalogue):
    hostUrl = "http://opac.biblioteca.usbmed.edu.co"
    url = hostUrl + "/catalogo?keyword=" + filterCatalogue + "&session=98864653&nh=20&infile=presearch.glue"
    print(url)


def politecnico_grancolombiano(filterCatalogue):
    hostUrl = "http://catalogo.poligran.edu.co"
    constUrl = hostUrl + "/cgi-bin/koha/opac-search.pl?idx=&q=" + filterCatalogue
    reponse = []

    r = requests.get(constUrl, verify=False)

    for index, item in enumerate(BeautifulSoup(r.content, 'lxml').find_all('tr')):
        try:
            reponse.append({
                "id": index,
                "autor": item.find_all('td')[2].find('p').find('span').getText().rstrip() if item.find_all('td')[
                    2].find('p').find('span') else None,
                "titulo": item.find_all('td')[2].find('a', {"class", "title"}).getText() if item.find_all('td')[
                    2] else None,
                "url": hostUrl + item.find_all('td')[2].find('a', {"class", "title"})['href'] if item.find_all('td')[
                    2] else None
            })
        except:
            print("OCURRIO UN ERROR")

    return reponse


def ceipa(filterCatalogue):
    hostUrl = "http://aplicaciones.ceipa.edu.co/biblioteca/biblio_digital/catalogo/"
    constUrl = hostUrl + "informe.jsp?cr1=T&cr2=A&cr3=M&con1=0&con2=0&con3=" + filterCatalogue + "&cole=Todos&ano=&ubi=Todos&idi=Todos"
    reponse = []

    r = requests.get(constUrl, verify=False)
    tree = html.fromstring(r.content)
    titulos = tree.xpath('//td[@width="660"]/div/span/text()')
    autores = tree.xpath('//td[@class="Estilo30"]/div/text()')
    urls = [url.attrib['href'].rstrip() for url in tree.xpath('//span[@class="Estilo17"]//a[1]')]
    index = 0
    for titulo, autor, url in zip(titulos, autores, urls):
        reponse.append({
            "id": index,
            "titulo": titulo.rstrip(),
            "autor": autor.rstrip(),
            "url": url
        })
        index = index + 1
    return reponse


def colegiatura(filterCatalogue):
    hostUrl = "https://colegiatura.com.co"
    constUrl = hostUrl + "/cgi-bin/koha/opac-search.pl?q=" + filterCatalogue
    reponse = []

    r = requests.get(constUrl, verify=False)

    for index, item in enumerate(BeautifulSoup(r.content, 'lxml').find_all('tr')):
        try:
            reponse.append({
                "id": index,
                "autor": item.find_all('td')[2].find_all('div')[1].find('p').find_all('span')[1].getText().rstrip() if
                item.find_all('td')[2] else None,
                "titulo": item.find_all('td')[2].find_all('div')[1].find('a').getText() if item.find_all('td')[
                    2] else None,
                "url": hostUrl + item.find_all('td')[2].find_all('div')[1].find('a')['href'] if item.find_all('td')[
                    2] else None
            })
        except:
            print("OCURRIO UN ERROR")

    return reponse
