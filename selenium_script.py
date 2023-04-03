from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
import os, time, browser_cookie3, re, sys, configparser
from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC

config = configparser.ConfigParser()

# Config variables
config.read('settings.ini')
CHROME_PATH = config['CHROME SETTINGS']['chrome_path']
CHROMEDRIVER_PATH = config['CHROME SETTINGS']['chromedriver_path']
CHROME_PROFILE = config['CHROME SETTINGS']['chrome_profile']

port_arg = sys.argv[1]
bet_xpath = sys.argv[2]
initial_amount = sys.argv[3]
link = sys.argv[4]

#port_arg = "8081"
#bet_xpath = "/html/body/app-desktop/div[1]/div/bcdk-content-scroller/div/sports-live-page/div/sports-live-event-bucket-list/bcdk-vertical-scroller/div/div[2]/div/div/sports-live-event-bucket[2]/div/div[2]/sports-events-event[1]/a/sports-events-event-markets-v2/sports-markets-default-v2/div/sports-selections-selection[2]/div/span[2]"
#initial_amount = "0.1"
#link = "https://www.betclic.fr/live"

# setting proxy
proxy_ip_port = f"127.0.0.1:{port_arg}"
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxy_ip_port
proxy.ssl_proxy = proxy_ip_port

capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)

#chrome_profile = "C:/Users/Ruel/AppData/Local/Google/Chrome/User Data/Default"
cookies = browser_cookie3.chrome(cookie_file=CHROME_PROFILE+'/Network/Cookies', domain_name='.betclic.fr')

keys = []
values = []
for c in cookies:
	c = str(c).split(' ')
	c = c[1].split('=')
	keys.append(c[0])
	values.append(c[1])

options = webdriver.ChromeOptions()
options.add_argument("--headless")

options.binary_location = CHROME_PATH # Select a path where chrome.exe is located
driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options, desired_capabilities=capabilities) # Select a path where chromedriver.exe is located

print('+++++PROXY connection detials'+port_arg)
driver.get('https://www.betclic.fr') # Fetching page
# setting cookies
for i in range(len(keys)):
	driver.add_cookie({"name":keys[i],"domain":".betclic.fr","value":values[i]})

time.sleep(3)

driver.implicitly_wait(20)
clicked = False

def page_action(driver, bet_xpath, link, initial_amount):
	global clicked
	# logic to increment/reset amount
	with open(f'file_com/amount_counter.txt', 'r') as f:
		counter = int(f.readline())
		if counter < 90:
			with open(f'file_com/latest_amount.txt', 'r') as f:
				ready = float(f.readline()) + 0.01
				ready = round(ready, 2)
				amount = str(ready)
			with open(f'file_com/latest_amount.txt', 'w') as f:
				f.write(amount)
			with open(f'file_com/amount_counter.txt', 'w') as f:
				f.write(str(counter+1))
		else:
			amount = initial_amount
			with open(f'file_com/latest_amount.txt', 'w') as f:
				f.write(amount)
			with open(f'file_com/amount_counter.txt', 'w') as f:
				f.write('0')

	driver.get('https://www.betclic.fr/live') # Fetching page
	driver.find_element(By.TAG_NAME, "html").send_keys(Keys.END)
	time.sleep(3)
	print('[+] Opening the bet')
	if clicked == False:
		driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, bet_xpath))))                
		page = driver.page_source

		# Getting odds
		attribute = re.findall(r'bettingslipBox_oddValue ng-trigger ng-trigger-selectionStateAnimation ng-tns-c[0-9]+-[0-9]+ ng-star-inserted', page)
		page = BeautifulSoup(page, 'lxml')
		odds = page.find('span', {'class': attribute})
		odds = odds.get_text().strip() # Odds in string value
		try:
			odds = odds.replace(",", ".")
		except:
			pass

		with open(f'file_com/initial_odd.txt', 'w') as f:
			f.write(odds)

		clicked = True 

	input_box = driver.find_element('xpath', "//input[@name='stakeField']")
	input_box.send_keys(amount) # Entering amount
	input_box.send_keys(Keys.RETURN) # Placing bet
	return

try:
	page_action(driver, bet_xpath, link, initial_amount)
except:
	raise

page_reload = False
ready = 'NULL'
while True:
	with open(f'file_com/running_status.txt', 'r') as f:
		status = f.readline()

	if 'start' in status:
		try:
			#if (ready == 'Not Ready' and page_reload == True) or 'betclic.fr/live' not in driver.current_url:
			if ('<span class="icons">Information</span>' in driver.page_source or '<span class="icons">Attention !</span>' in driver.page_source) or ('betclic.fr/live' not in driver.current_url or page_reload == True):
				driver.implicitly_wait(8)
				page_action(driver, bet_xpath, link, initial_amount)
				page_reload = False
			elif "Félicitations, ton pari est validé !" in driver.page_source:
				with open('file_com/results.txt', 'w') as q:
					q.write('Bet successful!')
				driver.implicitly_wait(8)
				page_action(driver, bet_xpath, link, initial_amount)
				page_reload = False
				#'<div data-qa="bet-confirmation-title"' in driver.page_source or 
			elif '<span class="icons">Cote suspendue' in driver.page_source:
				driver.implicitly_wait(8)
				page_action(driver, bet_xpath, link, initial_amount)
				page_reload = False
			else:
				try:
					driver.implicitly_wait(1)
					driver.find_element('xpath', "//button[@id='bet'][@class='button is-primary btn isPrimary']").click()
				except:
					pass

		except:
			page_reload = True

		# reloading if some special reload required
		with open('file_com/special_reload.txt', 'r') as q:
			if port_arg in q.readline():
				page_reload = True
			with open('file_com/special_reload.txt', 'w') as f:
				f.write('NULL')

	#driver.implicitly_wait(1.5)
	with open(f'file_com/exit.txt', 'r') as f:
		if 'true' in f.readline():
			driver.quit() # Closing driver instance
			exit() # Exiting program

