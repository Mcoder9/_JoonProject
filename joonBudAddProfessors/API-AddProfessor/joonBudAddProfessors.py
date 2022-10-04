import csv,json
import subprocess,os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class JoonBudBot:
    def __init__(self, username, password,addUrl):
        self.username = username
        self.password = password
        self.addUrl = addUrl

    def browser(self):
        # subprocess.Popen(["start","msedge","--remote-debugging-port=8989","--user-data-dir=" + os.getcwd() + "/edgeProfile",],shell=True)
        options = Options()
        options.add_argument("--start-maximized")
        # options.add_experimental_option("debuggerAddress", "localhost:8989")
        # service = Service(executable_path='msedgedriver.exe')
        service = Service(executable_path=EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=service,options=options)
        self.driver.implicitly_wait(3)

    def login(self):
        self.driver.get('http://joonbud.com')
        self.driver.find_element(By.XPATH, '//input[@name="login"]').send_keys(self.username)
        pswBox = self.driver.find_element(By.XPATH, '//input[@name="password"]')
        pswBox.send_keys(self.password)
        pswBox.send_keys(Keys.ENTER)
        sleep(4)
    
    def addProfessors(self,row):
        title,class_ = row[0],row[1]
        self.driver.get(self.addUrl)
        'Select prefix'
        self.driver.find_element(By.CSS_SELECTOR, '.inputGroup-text a.menuTrigger--prefix').click()
        self.driver.find_element(By.CSS_SELECTOR, 'a.menuPrefix.label').click()
        self.driver.find_element(By.XPATH, '//input[@name="title"]').send_keys(title)
        self.driver.find_element(By.XPATH, '//input[@name="tag_line"]').send_keys(class_)
        self.driver.find_element(By.CSS_SELECTOR, 'div.fr-wrapper p').send_keys('-')
        'Save Button'
        self.driver.find_element(By.CSS_SELECTOR, '.formSubmitRow-controls>button').click()
    
    def updateTrackLogger(self,row):
        with open('TrackLogg.csv', 'a',encoding='utf-8',newline='') as file:
            csv.writer(file).writerow(row)
    
    def readTrackLog(self):
        with open('TrackLogg.csv') as trackLoggFile:
            trackRows = list(csv.reader(trackLoggFile))
            return trackRows


    def run(self):
        self.browser()
        self.login()
        trackRows = self.readTrackLog()
        with open('InputData.csv') as inputDataFile:
            inputRows = list(csv.reader(inputDataFile))
            for row in inputRows:
                if row not in trackRows:
                    print(f'Row::{row}')
                    self.addProfessors(row)
                    self.updateTrackLogger(row)
                    trackRows = self.readTrackLog()
                    print(f'Added::{row}')
                    sleep(4)
                else:
                    print(f'skipped::{row}')




if __name__ == '__main__':
    config = json.load(open('config.json'))
    username = config['username']
    password = config['password']
    addUrl = config['addUrl']
    bot = JoonBudBot(username, password, addUrl)
    bot.run()



    