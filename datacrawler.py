from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import csv

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("http://127.0.0.1:5000")
driver.implicitly_wait(10)
driver.maximize_window()

# create an empty list for storing student data
templist = []
# declare page index starter
p=0

# find all pagination element
pages=driver.find_elements("xpath",'//div[@class="pagination"]/span')
while(p<(len(pages)-1)):
    # go into each page
    print('page '+str(p+1))
    # find all row element in the table.
    table_rows= driver.find_elements("xpath",'//ul[@id="students"]/table/tbody/tr')
    print('Found it!')
    # declare row index starter
    r = 1
    print(len(table_rows))
    while(r<=len(table_rows)):
        # go into each row.
        id_xpath = '//ul[@id="students"]/table/tbody/tr[' + str(r) + ']/td[1]'
        fname_xpath = '//ul[@id="students"]/table/tbody/tr[' + str(r) + ']/td[2]'
        lname_xpath = '//ul[@id="students"]/table/tbody/tr[' + str(r) + ']/td[3]'
        email_xpath = '//ul[@id="students"]/table/tbody/tr[' + str(r) + ']/td[4]'
        birthday_xpath = '//ul[@id="students"]/table/tbody/tr[' + str(r) + ']/td[5]'
        birthplace_xpath = '//ul[@id="students"]/table/tbody/tr[' + str(r) + ']/td[6]'
        point_xpath = '//ul[@id="students"]/table/tbody/tr[' + str(r) + ']/td[7]'
        maSV = driver.find_element("xpath", id_xpath).text
        Ho = driver.find_element("xpath", fname_xpath).text
        Ten = driver.find_element("xpath", lname_xpath).text
        email = driver.find_element("xpath", email_xpath).text
        ngaysinh = driver.find_element("xpath", birthday_xpath).text
        quequan = driver.find_element("xpath", birthplace_xpath).text
        diem = driver.find_element("xpath", point_xpath).text
        print(maSV)
        print(Ho)
        print(Ten)
        print(email)
        print(ngaysinh)
        print(quequan)
        print(diem)
        # create a dictionary as data.
        Table_dict = {
                        'MaSV': maSV,
                        'Ho': Ho,
                        'Ten': Ten,
                        'Email': email,
                        'NgaySinh': ngaysinh,
                        'Quequan': quequan,
                        'Diem': diem
                        }
        templist.append(Table_dict)
        # using pandas library func to load dictionary data into a data structure with rows and columns
        df = pd.DataFrame(templist)
        r+=1
    # after finishing on a page, go to the next page by clicking on Next button.
    driver.find_element("xpath",'//div[@class="pagination"]/span['+str(len(pages))+']').click()
    p+=1
    driver.implicitly_wait(10)

df.to_csv('table.csv')
driver.close()
print('Finish')
