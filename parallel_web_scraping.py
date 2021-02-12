from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import time
from csv import DictWriter

d_lable=[
    "car_name",
    "year",
    "price",
    "لون السيارة",
    "نوع الوقود",
    "أصل السيارة",
    "رخصة السيارة",
    "نوع الجير",
    "قوة الماتور",
    "عداد السيارة",
    "أصحاب سابقون",
    "تاريخ نشر الإعلان",
    "إضافات",
    "add_info",
    "url",
    "عدد الركاب",
    "وسيلة الدفع",
    "معروضة",
    "الزجاج",
    "اسم المُعلن",
    "رقم الهاتف",
    "موبايل",
    "Email",
    "Website",
    "المدينة",
    "العنوان",
    "تاريخ إنتهاء الإعلان",
    "حالة الإعلان"]

name_file='new.csv'

myFile = open(name_file, 'w')
with myFile:    
    writer = DictWriter(myFile, fieldnames=d_lable)    
    writer.writeheader()

def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)

start_time = time.time()

base_url = 'https://shobiddak.com/cars/'


all_urls = list()
all_html=list()
def generate_urls():
    for i in range(672966,672976):
        all_urls.append(base_url + str(i))


def marge_list(featue_list):
    text=""
    
    for li in featue_list:
        text+=li.text
        text+=","
    return text[:len(text)-1]



def give_html(url):
    global all_html
    res = requests.get(url)
    print(res.status_code, res.url,len(all_html))
    if res.url == base_url[:len(base_url)-1]:
        return None

    return res


def save_csv(lable,data,name_file):
    df=pd.DataFrame(data)
    df=df.append(data,ignore_index=True)
    df.to_csv(name_file)

def scrape(html_text):
    print("scrape ->" + html_text.url)
    soup =BeautifulSoup(html_text.text,'lxml')
    car_row={
        "car_name":None,
        "year":None,
        "price":None,
        "لون السيارة":None,
        "نوع الوقود":None,
        "أصل السيارة":None,
        "رخصة السيارة":None,
        "نوع الجير":None,
        "قوة الماتور":None,
        "عداد السيارة":None,
        "وسيلة الدفع":None,
        "معروضة":None,
        "أصحاب سابقون":None,
        "المدينة":None,
        "العنوان":None,
        "تاريخ نشر الإعلان":None,
        "تاريخ إنتهاء الإعلان":None,
        "url":None,
        "add_info":None,
        "إضافات":None,
        "اسم المُعلن":None,
        "رقم الهاتف":None,
        "موبايل":None,
        "Email":None,
        "Website":None,
        "عدد الركاب":None,
        "الزجاج":None,
        "حالة الإعلان":None
        }
    car_row["car_name"]=soup.find('h1',class_="section_title").text
    car_row["year"]=soup.find('h3',class_="section_title").text.split()[-1]
    car_row["price"]=soup.find('div', class_='post-price').text.split()[0]
    car_row["url"]=html_text.url
    spec_list = soup.find_all('tr',class_="list-row")
    additiion_spac_list = soup.select("table.create_post td.list-additions ul li")

    for index in spec_list:
        iii=index.find_all("td")
        if iii[0].text == "إضافات":
            list_li= iii[1].find_all("li")
            car_row[iii[0].text.strip()]=marge_list(list_li)
            continue

        car_row[iii[0].text.strip()]=iii[1].text

    car_row["add_info"]=marge_list(additiion_spac_list)

    # return car_row
    append_dict_as_row(name_file, car_row, d_lable)
    

if __name__ == '__main__':
    generate_urls()
    with Pool(10) as p:
        results=p.map(give_html, all_urls)

    # results=pp(results)
    results=list(filter(None, results))
    
    with Pool(10) as p:
        data=p.map(scrape, results)
    
    print("time request--- %s seconds ---" % (time.time() - start_time))
    # start_time = time.time()
    # save_csv(d_lable,data,"file1.csv")
    # print("time save--- %s seconds ---" % (time.time() - start_time))
