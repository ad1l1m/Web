import eel
import requests
from bs4 import BeautifulSoup
import re


@eel.expose
def get_pars(price):
    link = "https://tenderplus.kz/zakupki"
    response = requests.get(link).text
    soup = BeautifulSoup(response, 'lxml')
    describe = soup.find_all("div", class_="description-inner")
    amount = soup.find_all("div", class_="amount")
    list_amount = []
    save = ""
    list_describe = []
    for i in describe:
        list_describe.append(i.text.strip())
    for a in amount:
        list_amount.append(a.text.strip())
    count=0
    for i in range(len(list_amount)):
        amount_line = re.sub(r"\s+", "", list_amount[i])
        if (round(float(amount_line)) <= round(float(price))):
                count+=1
                save += (str(count)+". "+list_describe[i].strip() + "\nЦена: " + str(float(amount_line)) + "\n\n")
    return save



@eel.expose
#Функция будет выводить результат поиска по региону
def get_parsbyreg(region):
    region_ = re.sub(r"\s+", "", region)
    link = "https://tenderplus.kz/zakupki"
    response = requests.get(link).text
    soup = BeautifulSoup(response, 'lxml')
    describe = soup.find_all("div", class_="description-inner") #Содержит в себе описания тендера
    amount = soup.find_all("div", class_="amount")# Цена тендера
    save = "" #Будет сохранять и возращать полученный результат
    count_amount=0
    count = 0
    list_amount=[]
    for i in amount:
        list_amount.append(i.text.strip())
    for i in describe:
        information = i.text.split("\n")
        current_cost = re.sub(r"\s+", "", list_amount[count_amount])
        count_amount+=1
        for w in range(len(information)):
            name = information[w].split()
            for s in range(len(name)):
                if (len(name) > 0):
                    if (name[0] == "Регион:"):
                        if (name[s] == str(region_)):
                            count+=1
                            save += str(count)+". " + (i.text).strip() +"\nЦена: "+current_cost +"\n\n"
                            break
    return save

eel.init("C:/Users/Adil/OneDrive/Рабочий стол/web")#запуск приложения
eel.start("main.html", size=(800,1000))

