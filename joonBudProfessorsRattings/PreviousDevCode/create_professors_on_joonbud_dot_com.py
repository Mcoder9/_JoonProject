# NOTE : don't forget to click checkbox ADD TO PATH when installing python
# install python 3
# install firefox
# now you need to install python packages
# open your python editor and install from there OR
# open cmd type following commands, each will install one package
# pip install selenium
# pip install colorama
# pip install pandas
# pip install numpy
# put all files in same folder
# file are user_accounts.txt ,  main .py files ,  geckodriver ,  data file csv
# thats it you can run the program
# NOTE : program creates one more file log for teacher creation
# be sure to copy this file along with all others when you move the project to some other location


# NOTE : running in headless may not work for certain sites
# You can run the program in headless mode
# browser window will not show up
# you need to un comment (remove #) from line 41 (#options.add_argument('-headless'))
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import pandas as pd
import sys
import time
import os
import colorama
colorama.init(autoreset = True)
import numpy as np
import random
import sys
import traceback
import warnings
warnings.simplefilter("ignore")
import json
################################### SETTINGS ################################################
options = Options()
options.add_argument("window-size=1280,800")
#options.add_argument('-headless')
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = False


platform = sys.platform
if "win32" not in platform:
	PATH_STYLE = "/"
else:
	PATH_STYLE = "\\"


sys.path.append(os.path.dirname(os.path.abspath(".")))

#################################################################### GLOBAL VARIABLES #################################################################################
ADD_PROFESSOR_URL = "http://joonbud.com/professors/categories/saddleback-college.2/add"
USERNAME = "abdev"
PASSWORD = "abdevfiverr"
DATA_FILE_PATH = "." + PATH_STYLE + "rmp_get_output_2022-09-23.csv"
PROFESSOR_CREATION_LOG_FILE_PATH = "." + PATH_STYLE + "professor_creation_log.json"
USER_ACCOUNTS_FILE_PATH = "." + PATH_STYLE + "user_accounts.txt"


# if user accounts file does not exist then quite the program
if not os.path.exists(USER_ACCOUNTS_FILE_PATH):
	print(colorama.Fore.RED + "user_accounts.txt file is required to write reviews, aborting program!")
	sys.exit(0)
else:
	f = open(USER_ACCOUNTS_FILE_PATH, "r")
	user_accounts = [l.strip("\n") for l in f.readlines()]
	f.close()




# read professor_creation_log.json
if os.path.exists(PROFESSOR_CREATION_LOG_FILE_PATH):
	f = open(PROFESSOR_CREATION_LOG_FILE_PATH, "r")
	PROFESSOR_CREATION_LOG = json.load(f)
	f.close()
else:
	# previous log does not exist
	PROFESSOR_CREATION_LOG = []


##################################################################### FUNCTIONS ###########################################################################################
def login(username, password):
	# enter login email
	browser.find_element(by="xpath", value="//input[@name='login']").send_keys(username)
	# enter login password
	browser.find_element(by="xpath", value="//input[@name='password']").send_keys(password)
	# click on submit
	browser.find_element(by="xpath", value="//button[@type='submit']").click()



def logout():
	while True:
		try:
			browser.find_element(by="xpath", value="//a[@href='/account/']").click()
			break
		except:
			continue
	print("Waiting until log out button appears")
	while True:
		try:
			browser.find_element(by="xpath", value="//div[@data-href='/account/visitor-menu']//a[contains(text(), 'Log out')]").click()
			break
		except:
			try:
				browser.find_element(by="xpath", value="//a[@href='/account/']").click()
				time.sleep(2)
			except:
				continue
		



def read_csv():
	data = pd.read_csv(DATA_FILE_PATH)
	return data


def save_json(file_path, data):
	f = open(file_path, "w")
	json.dump(data, f)
	f.close()



#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx#

# read data file
DATA = read_csv()

############################################################################## FIRST PART PROFESSOR CREATION ##################################################################
browser = webdriver.Firefox(options=options, desired_capabilities=cap)
try:
	browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
except:
	print(colorma.Fore.LIGHYELLOW_EX + "Warning : Failed to set navigator")


browser.get(ADD_PROFESSOR_URL)





teacher_class_data = pd.DataFrame().assign(A = DATA["Teacher Name"], B = DATA["Department + Class"]).drop_duplicates()

#ORIGINAL_PROFESSOR_COUNTER = 9
#CURRENT_PROFESSOR_COUNTER = ORIGINAL_PROFESSOR_COUNTER + CURRENT_PROFESSOR
for i in range(0, len(teacher_class_data)):
	login(USERNAME, PASSWORD)
	############################################################# create teacher ###########################################################################
	row = teacher_class_data.iloc[i]
	teacher, class_name = row["A"], row["B"]
	# add if already not added
	if [teacher, class_name] not in PROFESSOR_CREATION_LOG:
		browser.get(ADD_PROFESSOR_URL)
		# choose prefix
		browser.find_element(by="xpath", value="//a[@class='menuTrigger menuTrigger--prefix']").click()
		browser.find_element(by="xpath", value="//div[@class='menu-row']//a[contains(text(), 'Saddleback College Rate My Professors')]").click()
		time.sleep(1)
		browser.find_element(by="xpath", value="//input[@name='title']").send_keys(teacher)
		browser.find_element(by="xpath", value="//input[@name='tag_line']").send_keys(class_name)
		browser.find_element(by="xpath", value="//div[@contenteditable='true']").send_keys("-")
		browser.find_element(by="xpath", value="//div[@class='formSubmitRow-controls']//button[@type='submit']").click()
		# save this to professor_creation_log.json
		PROFESSOR_CREATION_LOG.append([teacher, class_name])
		# ensure no duplicates are included
		PROFESSOR_CREATION_LOG = list(set([str(l) for l in PROFESSOR_CREATION_LOG]))
		PROFESSOR_CREATION_LOG = [eval(name) for name in PROFESSOR_CREATION_LOG]
		# save
		save_json(PROFESSOR_CREATION_LOG_FILE_PATH, PROFESSOR_CREATION_LOG)
	else:
		print(colorama.Fore.YELLOW + "Teacher already created")
	# log out
	logout()
	#################################################################### SECOND PART ADDING REVIEWS ###################################################################
	# find all records in DATA for teacher and class combinations
	RECORDS = DATA[np.equal.outer(DATA.to_numpy(copy=False),  [teacher, class_name]).any(axis=1).all(axis=1)].drop_duplicates()
	try:
		accounts = {l.split(":")[0] : l.split(":")[1] for l in user_accounts[:len(RECORDS)]}
	except:
		print(colorama.Fore.RED + "Not suffient user accounts")
		print(colorama.Fore.RED + "Current teacher has " , len(RECORDS) , " reviews to write")
		print(colorama.Fore.RED + "Accounts available " , len(user_accounts))
		print(colorama.Fore.RED + "Add more accounts in " , USER_ACCOUNTS_FILE_PATH, "Aborting program!")
		sys.exit(0)
	for c, username in zip(range(0, len(RECORDS)), accounts):
		login(username, accounts[username])
		record = RECORDS.iloc[c]
		# get last name in teacher name
		#first_name = teacher.split(" ")[-1]
		# go to search page
		browser.get("http://joonbud.com/professors/categories/saddleback-college.2/")
		# click on search
		# using first search bar
		#browser.find_element(by="xpath", value="//input[@aria-label='Search']").send_keys(teacher)
		#browser.find_element(by="xpath", value="//input[@aria-label='Search']").send_keys(Keys.ENTER)
		#print("Waiting for results")
		#while True:
		#	try:
		#		browser.find_element(by="xpath", value="//h3[@class='contentRow-title']//a[contains(@href, 'professor')]").click()
		#		break
		#	except:
		#		continue
		# using quick search
		while True:
				try:
					browser.find_element(by="id", value="quickSearchTitle").send_keys(teacher)
					time.sleep(1)
					break
				except Exception as e:
					print(e)
		browser.find_element(by="id", value="quickSearchTitle").send_keys(Keys.ENTER)
		print("Waiting for results")
		while True:
			try:
				# this record will be present because it is created already
				browser.find_element(by="xpath", value="//td[@class='dataList-cell dataList-cell--link']").click()
				break
			except:
				continue
		# click on Rate This Professor
		browser.find_element(by="xpath", value="//span[contains(text(), 'Rate This Professor')]").click()
		print("Waiting for review writing window")
		while True:
			try:
				overlay = browser.find_element(by="xpath", value="//div[@class='overlay']")
				break
			except:
				continue
		rating = record["Rating"]
		review = record["Comment"]
		overlay.find_element(by="xpath", value="//a[@data-rating-value='" + str(rating) + "']").click()
		# write review
		overlay.find_element(by="xpath", value="//textarea[@name='message']").send_keys(review)
		browser.find_element(by="xpath", value="//span[contains(text(), 'Submit rating')]").click()
		print("################ REVIEW WRITING #####################")
		print(colorama.Fore.GREEN + "For current professor")
		print(colorama.Fore.GREEN + "Reviews written " , c + 1)
		remaining_reviews = len(RECORDS) - c - 1
		print(colorama.Fore.LIGHTGREEN_EX + colorama.Style.BRIGHT + "Remaining Reviews" , remaining_reviews)
		print(colorama.Fore.GREEN + "Total Reviews" , len(RECORDS))
		logout()
	print("################ PROFESSOR STATS ####################")
	print(colorama.Fore.GREEN + "Completed " , i + 1)
	print(colorama.Fore.LIGHTGREEN_EX + colorama.Style.BRIGHT + "Remaining " , len(teacher_class_data) - i - 1)
	print(colorama.Fore.GREEN + "Total professors" , len(teacher_class_data))
	print(colorama.Fore.GREEN + "PROFESSOR CREATION")



#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx#