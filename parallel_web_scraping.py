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

name_file='new1.csv'

myFile = open(name_file, 'w')
with myFile:    
    writer = DictWriter(myFile, fieldnames=d_lable)    
    writer.writeheader()

def append_dict_as_row(file_name, dict_of_elem, field_names):
    """function to append csv file 

    Args:
        file_name (str): name file 
        dict_of_elem (dictionary): data
        field_names (list): lable data
    """
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
def generate_urls(start,end):
    for i in range(start,end):
        all_urls.append(base_url + str(i))


def marge_list(featue_list):
    """function to convert html list to string 

    Args:
        featue_list (ResultSet): list html 

    Returns:
        string: list in string 
    """
    text=""
    
    for li in featue_list:
        text+=li.text
        text+=","
    return text[:len(text)-1]



def give_html(url):
    """function to open html page and scrape it 

    Args:
        url (str): url for page
    """
    global all_html
    res = requests.get(url)
    print(res.status_code, res.url,len(all_html))
    if res.url != base_url[:len(base_url)-1]:
        scrape(res)


    
    
def scrape(html_text):
    """function to to extract data from html page

    Args:
        html_text (requests.models.Response): result http request
    """
    try:
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
        print("time finish  "+html_text.url+" --- %s seconds ---" % (time.time() - start_time))
        append_dict_as_row(name_file, car_row, d_lable)
    except:
        print("error_scrape -> " + html_text.url)
    

if __name__ == '__main__':
    # 432098->680193
    generate_urls(590093,600093)
    with Pool(10) as p:
        results=p.map(give_html, all_urls)

    # results=pp(results)
#    results=list(filter(None, results))
#
#    with Pool(10) as p:
#        data=p.map(scrape, results)
    
    print("time request--- %s seconds ---" % (time.time() - start_time))
    
