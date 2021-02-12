from flask import Flask
from flask_cors import CORS, cross_origin
import requests
from model.universidades import Universidades

import requests
from bs4 import BeautifulSoup
import json

from  universidades_crawler import  politecnico, uni_antioquia , itm , politecnico_grancolombiano,ceipa,colegiatura

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


#AIzaSyBFUgorK0CT4v6qobJ-ay-1-TkVOSUK8zY
@app.route('/googleScholar/<tema>')
def googleAcademico(tema):
    print("lo que viene para google academics")
    print(tema)
    tema = tema.replace("|", " ")
    print(tema)
    urlGoogleAcademico = "https://scholar.google.com/scholar?hl=es&as_sdt=0%2C5&q={}&oq=".format(tema)
    r = requests.get(urlGoogleAcademico)
    print(r.content)

    reponse = []
    for index, item in enumerate(BeautifulSoup(requests.get(urlGoogleAcademico).content, 'lxml').find_all('div', {"class": "gs_r gs_or gs_scl"})):
        reponse.append({
            "id": index,
            "text": item.getText(),
            "urlText":item.find('a', href=True).getText(),
            "url": item.find('a', href=True)['href']
            })
    return json.dumps(reponse)

@app.route('/openJournal/<path:url>')
def openJournal(url):
    print("este es el de open jo")
    #url_Open_Journal = "{}".format(url)
    url_Open_Journal = url.replace("aaa","/").replace("bbb", "?").replace("mmm", "https://")
    # url_Open_Journal = url
    print(url_Open_Journal)
    r = requests.get(url_Open_Journal)
    # print(r.content)

    reponse = []
    for index, item in enumerate(BeautifulSoup(requests.get(url_Open_Journal).content, 'lxml').find_all('div', {
        "class": "obj_article_summary"})):
        # print(item.find('a', href=True).getText().strip())
        # print(item.find('a', href=True)['href'])
        reponse.append({
            "id": index,
            "urlText": item.find('a', href=True).getText().strip(),
            "url": item.find('a', href=True)['href']
        })
    return json.dumps(reponse)

@app.route('/openJournalPoli/<tema>')
def openJournalPoli(tema):
    print("Este es el del poli:")
    print(tema)
    tema = tema.replace("|", " ")
    print(tema)
    url_Poli = "https://revistas.elpoli.edu.co/index.php/pol/search/search?query={}".format(tema)
    r = requests.get(url_Poli)
    reponse = []
    content = BeautifulSoup(r.text, 'lxml')
    title = []
    link = []
    # Find table
    # tabla del poli aparace con la clse listing
    table = content.find('table', {'class': 'listing'})
    # Find all tr rows
    # cada uno de las filas con datos tiene el atributo valig=top
    tr = table.findAll('tr', {'valign': 'top'})
    for each_tr in tr:
        td = each_tr.find_all('td')
        # td que con un array desde cero y cada casilla es una columna, en este caso el titulo
        title.append(td[1].text)
        # se recorre todos los link en la terdera columna para extrer el link del pdf
        # poner un lenght mayor a 5 para que no coja las a de pdf o html
        td_aux = td[2].find_all('a')
        # aux=0
        for each_a in td_aux:
            if (each_a.text == 'PDF'):
                link.append(each_a['href'])

    # este for es para probar que cada campo del array este alineado titulo y link
    # for index in range(0,len(title)-1):
    #     print(title[index])
    #     print(link[index])

    for index in range(0, len(title) - 1):
        reponse.append({
            'tittle': title[index],
            'link': link[index]
            # 'description': description[index]
        })
    return json.dumps(reponse)


@app.route('/universidades/<filterCatalogue>')
def universidades(filterCatalogue):

    print("esta es la vaina que trae de java")
    print(filterCatalogue)
    filterCatalogue = filterCatalogue.replace("|", " ")
    #poli
    hostUrl="http://prometeo-politecnicojic.hosted.exlibrisgroup.com"
    consturl = hostUrl + "/F/?func=find-b&request=" + filterCatalogue + "&find_code=WRD&adjacent=N&x=32&y=94=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5=";
    #//tr[@valign="baseline"]
    print(consturl)

    universidades = Universidades(
                                    politecnico(filterCatalogue),
                                    uni_antioquia(filterCatalogue),
                                  itm(filterCatalogue)
                                  ,politecnico_grancolombiano(filterCatalogue),
                                  ceipa(filterCatalogue),
                                  colegiatura(filterCatalogue))

    return json.dumps(universidades.__dict__)




if __name__ == '__main__':
    app.run()