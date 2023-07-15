"""
Python program to fetch single semester result
Based on the initial fetch.py program to fetch single semester results + using PANDAS library and has the added feature of grouping names of the students who score the same SGPA
Program By : V DHEERAJ SHENOY
"""

import pandas as pd
import numpy as np
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException as AlertException

"""
USN_pattern : The pattern of the USN for your program
FROM : USN starting number
TO : USN Ending number
"""

USN_pattern = "22MSRPH0"
FROM = 1
TO = 22
LINK = "http://results.jainuniversity.ac.in/webResult.aspx?id=CENTER+FOR+POST+GRADUATE+STUDIES&value=MAY-2023"
TIME_TO_WAIT = 30

# Print iterations progress

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def fetchResults(FROM, TO):
    opts = Options()
    opts.add_argument("--headless")
    tmpString = ""
    textField = WebElement

    ranklist = pd.DataFrame(columns=["Name", "SGPA"])
    driver = webdriver.Firefox(options=opts)
    printProgressBar(FROM, TO + 1 - FROM)

    driver.get(LINK)
    for i in range(FROM, TO + 1):
        printProgressBar(i, TO + 1 - FROM)
        try:
            textField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtStudentCode"]')))
        finally:
            if i < 10:
                tmpString = "0" + str(i)
            else:
                tmpString = str(i)

            rollno = USN_pattern + tmpString
            textField.send_keys(rollno)
            textField.send_keys(Keys.RETURN)
        try:
            name = WebDriverWait(driver, TIME_TO_WAIT).until(EC.presence_of_element_located((By.ID, "lblStuName")))
            sgpa = WebDriverWait(driver, TIME_TO_WAIT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lblSGPA"]')))
            sgpa = driver.find_element(By.XPATH, '//*[@id="lblSGPA"]').get_attribute("innerHTML")
            ranklist.loc[len(ranklist)] = [name.text, float(sgpa)]
        except AlertException:
            continue
        nextBtn = driver.find_element(By.ID, "btnnextResult")
        nextBtn.click()

    driver.close()

    pd.options.display.max_colwidth = None

    sortedList = ranklist.sort_values("SGPA", ascending = False, ignore_index = True) # sorting the list w.r.t SGPA
    sortedList = sortedList.rename_axis(index = "Rank") # adding title to the index column of the DataFrame

    #sortedList = sortedList.groupby(["Name"]).mean()
    sortedList = sortedList.groupby(["SGPA"])["Name"].apply(', '.join).reset_index()
    sortedList = ranklist.sort_values("SGPA", ascending = False) # sorting the list w.r.t SGPA
    sortedList.index = np.arange(1, len(sortedList) + 1) # changing index to start from 1 instead of the default from 0
    print(tabulate(sortedList, headers='keys', tablefmt='psql'))

if __name__ == "__main__":
    fetchResults(FROM, TO)
