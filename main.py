import re
from bs4 import BeautifulSoup
import requests
import mysql.connector

count = 0 
# count is used for counting pages and printing number of the current page;
pages = 10
carNumbers = 10
carsInfoList = []
carCountForErr = 0
# carCountForErr is to count all of the cars in all of pages;

print("Please wait...")
print("Data is gathering...")

for pageN in range(pages):
    carsInfo = requests.get('https://www.truecar.com/used-cars-for-sale/listings/?page={}&sort[]=best_match'.format(pageN+1), timeout = 120)

    soup = BeautifulSoup(carsInfo.text, 'html.parser')
    carYear = soup.find_all( 'span', attrs = {"class":"vehicle-card-year"})
    carName = soup.find_all('span' , attrs = {"class":"vehicle-header-make-model text-truncate"})
    carsPrice  = soup.find_all('div', attrs = { "data-test":"vehicleListingPriceAmount"})
    carsMileage = soup.find_all('div' , attrs = {"data-test":"vehicleMileage"})
    count +=1
    
    for i in range(carNumbers):
        # We have to change type and format of carYear, price and mile by regex;
        # mile = 12,345345 miles , price = $12,536 . The comma and the dollar sign plus every letter should be removed.

        priceMile = ""
        priceMile = carsPrice[i].text + "    "+ carsMileage[i].text
        createNewFormat = list(map(str, re.findall(r'(\d+,\d+)',priceMile)))
        # Because some car information are not efficient we use try except
        try:
            new_regex_price = createNewFormat[0]
            new_regex_mile = createNewFormat[1]
            carCountForErr +=1
        except:
            continue
        # print(createNewFormat)
        
        new_regex_price = int(re.sub(r'\,', '', new_regex_price))
        new_regex_mile = int(re.sub(r'\,', '', new_regex_mile))
        carsInfoList.append([carName[i].text , int(carYear[i].text), new_regex_mile, new_regex_price]) 
        # print(carName[i].text , int(carYear[i].text), new_regex_price, new_regex_mile)
    print("page {} data is saving...".format(count))


print(carsInfoList)
print(len(carsInfoList))

cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='mldb')

cursor = cnx.cursor()
# carlist is our table

for i in range(len(carsInfoList)):
    query = "insert into carinfo values('%s', '%i', '%i', '%i')"%(carsInfoList[i][0], carsInfoList[i][1], carsInfoList[i][2], carsInfoList[i][3])
    cursor.execute(query)
    cnx.commit()

print("Information successfully added to ml DB.")
# print(count)
cnx.close()