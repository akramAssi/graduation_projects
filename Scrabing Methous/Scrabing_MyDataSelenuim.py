from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import xlsxwriter



### https://shobiddak.com/cars/647396
browser = webdriver.Chrome(ChromeDriverManager().install())
# The first car was add to the Website is --> https://shobiddak.com/cars/432300   ------> 667367


# here we add a Coed for preparing an excel sheet


# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('MyData.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0

worksheet.write(row, 0, 'Car Name')
worksheet.write(row, 1, 'produce year')
worksheet.write(row, 2, 'Color')
worksheet.write(row, 3, 'fuel Type')
worksheet.write(row, 4, 'gear Type')
worksheet.write(row, 5, 'eng power')
worksheet.write(row, 6, 'distance')
worksheet.write(row, 7, 'oragin')
worksheet.write(row, 8, 'Ad data push')
worksheet.write(row, 9, 'price')

row = 1
col = 0


#




Link = "https://shobiddak.com/cars/"
CarNum = 432300




for iii in range(432300,432305):
    try:
        StrNumCar = str(iii)
        FinalLink = Link + StrNumCar
        browser.get(FinalLink)
        Color = browser.find_element_by_css_selector(".list_ads .list-row:nth-of-type(1) td:last-child")
        Fuel_type = browser.find_element_by_css_selector(".list_ads .list-row:nth-of-type(2) td:last-child")
        Gear_type = browser.find_element_by_css_selector(".list_ads .list-row:nth-of-type(5) td:last-child")
        engine_power = browser.find_element_by_css_selector(".list_ads .list-row:nth-of-type(7) td:last-child")
        distance = browser.find_element_by_css_selector(".list_ads .list-row:nth-of-type(8) td:last-child")
        priceCar = browser.find_element_by_class_name("post-price").text
        name = browser.find_element_by_class_name("section_title")
        Produce_Year = browser.find_element_by_class_name("section_title:last-child").text
        # here we add some thing
        car_license = browser.find_element_by_css_selector(".list_ads .list-row:nth-of-type(3) td:last-child")
        data_publish = browser.find_element_by_css_selector(".create_post .list-row:nth-of-type(2) td:last-child")
        ## To Split the Number from whole string (price)
        price = [int(i) for i in priceCar.split() if i.isdigit()]
        listToStrPrice = ' '.join([str(elem) for elem in price])
        # To Split the Number from whole string (Produce year)
        res = [int(i) for i in Produce_Year.split() if i.isdigit()]
        listToStrYear = ' '.join([str(elem) for elem in res])
        # print("The Information for these Car is : ")

        # print("Name of car is ---> ",name.get_attribute('innerHTML'))
        worksheet.write(row, col, name.get_attribute('innerHTML'))

        # print("The year of produce is --> ",listToStrYear)
        worksheet.write(row, col+1, listToStrYear)

        # print("its Color is --->",Color.get_attribute('innerHTML'))
        worksheet.write(row, col + 2, Color.get_attribute('innerHTML'))

        # print("Fuel type is --->",Fuel_type.get_attribute('innerHTML'))
        worksheet.write(row, col + 3, Fuel_type.get_attribute('innerHTML'))

        # print("Gear type is --->",Gear_type.get_attribute('innerHTML'))
        worksheet.write(row, col + 4, Gear_type.get_attribute('innerHTML'))

        # print("engine power is --->",engine_power.get_attribute('innerHTML'))
        worksheet.write(row, col + 5, engine_power.get_attribute('innerHTML'))

        # print("The amount of use the car in km--->",distance.get_attribute('innerHTML'))
        worksheet.write(row, col + 6, distance.get_attribute('innerHTML'))

        # print("The orgin of the car is --->" + car_license.get_attribute('innerHTML'))
        worksheet.write(row, col + 7, car_license.get_attribute('innerHTML'))

        # also here we add some thing

        # print("The data that the Ad was publish is ---> " + data_publish.get_attribute('innerHTML'))
        worksheet.write(row, col + 8, data_publish.get_attribute('innerHTML'))


        # print("The price for This car is -->",listToStrPrice)
        worksheet.write(row, col + 9, listToStrPrice)
        row += 1

        # print("------------------------------------")
        # browser.quit()
        # iii = iii + 1
    except:
        iii = iii + 1

workbook.close()
