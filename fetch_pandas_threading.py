"""
Python program to fetch multiple semester result and print average SGPA.
Based on the initial fetch.py program to fetch single semester results and on the improved fetch_pandas.py program

TODO: Print status of PASS/FAIL in the final resulting table

Program By : V DHEERAJ SHENOY
"""

import pandas as pd
import numpy as np
from tabulate import tabulate
import threading
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
LINK : The Jain University result web link with value kept black with {}

Add the month-year string to variables, e.g: link1, link2, link3.... etc. and then add to the links array
"""

USN_pattern = "22MSRPH0"
FROM = 1
TO = 5
LINK = "http://results.jainuniversity.ac.in/webResult.aspx?id=CENTER+FOR+POST+GRADUATE+STUDIES&value={}"

link1 = LINK.format("DEC-2022")
link2 = LINK.format("MAY-2023")
links = [link1, link2]

TIME_TO_WAIT = 30
opts = Options()
opts.add_argument("--headless")

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

# DataFrame that holds the record of each student
ranklist = pd.DataFrame(columns=["Name", "SGPA"])

# Class for result fetching (based on fetch_pandas.py)
class RankListThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        driver = webdriver.Firefox(options=opts)
        #print("Loading Headless Browser")
        driver.get(self.url)
        tmpString = ""
        textField = WebElement
        #print("Fetching Results...")
        for i in range(FROM, TO + 1):
            printProgressBar(i, TO + 1 - FROM)
            try:
                textField = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtStudentCode"]')))
            finally:
                if  i < 10:
                    tmpString = "0" + str(i)
                else:
                    tmpString = str(i)

                rollno = USN_pattern + tmpString
                #print("Fetching ", rollno)
                # progress bar
                textField.send_keys(rollno)
                textField.send_keys(Keys.RETURN)
                try:
                    name = WebDriverWait(driver, TIME_TO_WAIT).until(EC.presence_of_element_located((By.ID, "lblStuName")))
                    sgpa = WebDriverWait(driver, TIME_TO_WAIT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="lblSGPA"]')))
                    sgpa = driver.find_element(By.XPATH, '//*[@id="lblSGPA"]').get_attribute("innerHTML")
                    ranklist.loc[len(ranklist)] = [name.text, float(sgpa),]
                except AlertException:
                    #ranklist.loc[len(ranklist)] = [name.text, float(sgpa), self.status]
                    continue
                # try:
                #     if sgpa == "0.00":
                #         self.status = "Fail"
                #     else:
                #         self.status = "Pass"
                #     ranklist.loc[len(ranklist)] = [name.text, float(sgpa), self.status]
                except AttributeError:
                    continue
                nextBtn = driver.find_element(By.ID, "btnnextResult")
                nextBtn.click()

        driver.close()

# Function to sort according to the SGPA and group by the names based on mean of the SGPA
def arrangeDataFrame(n):
    sortedList = ranklist.groupby(["Name"]).mean().reset_index()
    sortedList = sortedList.sort_values("SGPA", ascending = False, ignore_index = True) # sorting the list w.r.t SGPA
    sortedList.index = np.arange(1, len(sortedList) + 1) # changing index to start from 1 instead of the default from 0
    print("\n\nAverage SGPA of {} semester(s)\n".format(n))
    print(tabulate(sortedList, headers='keys', tablefmt='psql'))

# Array holding the thread process
threads = []

# Main function that is the driver of the threading program
def main_func():
    printProgressBar(1, TO + 1 - FROM)
    for l in links:
        r = RankListThread(l)
        r.start()
        threads.append(r)

    for t in threads:
        t.join()

    arrangeDataFrame(len(links))

# Main part of the program
if __name__ == "__main__":
    main_func()
