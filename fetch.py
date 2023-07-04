from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException as AlertException
import numpy as np
from tabulate import tabulate
from numba import njit

class Student:
    def __init__(self, rollno, name, sgpa, status = "Pass"):
        self.rollno = rollno
        self.name = name
        self.sgpa = sgpa
        self.status = status

    def __str__(self):
        return "ROLL NO: {}\nNAME: {}\nSGPA: {}\nSTATUS: {}".format(self.rollno, self.name, self.sgpa, self.status)

def fetchResults(FROM, TO):
    opts = Options()
    opts.add_argument("--headless")

    link = "http://results.jainuniversity.ac.in/webResult.aspx?id=CENTER+FOR+POST+GRADUATE+STUDIES&value=MAY-2023"
    a = ""
    name = ""
    sgpa = ""
    textField = ""
    studentArray = []

    print("Loading Headless Browser")
    driver = webdriver.Firefox(options=opts)
    driver.get(link)
    print("Fetching Results...")

#    studArray = np.empty(shape = (TO + 1, 1), dtype=Student)

    for i in range(FROM, TO + 1):
        try:
            textField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtStudentCode"]')))
        finally:
            if i < 10:
                a = "0" + str(i)
            else:
                a = str(i)
            rollno = "22MSRPH0" + a
            print("Fetching ", rollno)
            textField.send_keys(rollno)
            textField.send_keys(Keys.RETURN)
        
        try:
            name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "lblStuName")))
            sgpa = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lblSGPA"]')))
            sgpa = driver.find_element(By.XPATH, '//*[@id="lblSGPA"]').get_attribute("innerHTML")
        except AlertException:
            studentArray.append(Student(rollno, "", "", "Witheld"))
            #studArray[i] = Student(rollno, "", "", "Witheld")
            continue
        try:
            if sgpa == "0.00":
                studentArray.append(Student(rollno, name.text, sgpa, "Fail"))
                #studArray[i] = Student(rollno, name.text, sgpa, "Fail")
            else:
                studentArray.append(Student(rollno, name.text, sgpa))
                #studArray[i] = Student(rollno, name.text, sgpa)
        except AttributeError:
            continue
        nextBtn = driver.find_element(By.ID, "btnnextResult")
        nextBtn.click()

    driver.close()
    return studentArray


def getRankList(array):
    sortedArray = sorted(array, key=lambda x: x.sgpa, reverse=True)
    tableHeaders = ["Rank", "Roll No", "Name", "SGPA", "Status"]
    rows = []
    
    for i in range(len(sortedArray)):
        rows.append([i + 1, sortedArray[i].rollno, sortedArray[i].name, sortedArray[i].sgpa, sortedArray[i].status])

    print(tabulate(rows, tableHeaders))

arr = fetchResults(1, 23)
getRankList(arr)
