from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
import os, time, browser_cookie3, re, sys
from bs4 import BeautifulSoup

port_arg = sys.argv[1]
bet_name = sys.argv[2]
#amount = '0.1'#sys.argv[3]

# setting proxy
proxy_ip_port = f"127.0.0.1:{port_arg}"
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxy_ip_port
proxy.ssl_proxy = proxy_ip_port

capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)

chrome_profile = "C:/Users/Ruel/AppData/Local/Google/Chrome/User Data/Default"
cookies = browser_cookie3.chrome(cookie_file=chrome_profile+'/Network/Cookies', domain_name='.betclic.fr')

keys = []
values = []
for c in cookies:
	c = str(c).split(' ')
	c = c[1].split('=')
	keys.append(c[0])
	values.append(c[1])

options = webdriver.ChromeOptions()
options.add_argument("--headless")

options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe" # Select a path where chrome.exe is located
driver = webdriver.Chrome("C:/chromedriver.exe", chrome_options=options, desired_capabilities=capabilities) # Select a path where chromedriver.exe is located

print('+++++PROXY connection detials'+port_arg)
driver.get('https://www.betclic.fr') # Fetching page

time.sleep(3)

# setting cookies
for i in range(len(keys)):
	driver.add_cookie({"name":keys[i],"domain":".betclic.fr","value":values[i]})


driver.implicitly_wait(20)
clicked = False

def page_action(driver, bet_name):
	global clicked
	with open(f'file_com/latest_amount.txt', 'r') as f:
		ready = float(f.readline()) + 0.1
		amount = str(ready)
	with open(f'file_com/latest_amount.txt', 'w') as f:
		f.write(amount)

	driver.get('https://www.betclic.fr/live') # Fetching page
	print('[+] Opening the bet')
	if clicked == False:
		driver.find_element('xpath', f"//div[@title='{bet_name}']").click()
		clicked = True
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

	input_box = driver.find_element('xpath', "//input[@name='stakeField']")
	input_box.send_keys(amount) # Entering amount
	input_box.send_keys(Keys.RETURN)
	return

try:
	page_action(driver, bet_name)
except:
	pass

page_reload = False
ready = 'NULL'
while True:
	with open(f'file_com/ready {port_arg}.txt', 'r') as f:
		if f.readline() == 'Ready':
			page_reload = True

	with open(f'file_com/ready {port_arg}.txt', 'r') as f:
		ready = f.readline()

	try:
		if (ready == 'Not Ready' and page_reload == True) or 'betclic.fr/live' not in driver.current_url:
			driver.implicitly_wait(20)
			page_action(driver, bet_name)
			page_reload = False
	except:
		pass

	#driver.implicitly_wait(1.5)
	with open(f'file_com/release.txt', 'r') as f:
		if f.readline() != 'NULL':
			driver.quit() # Closing driver instance
			exit() # Exiting program
	try:
		driver.implicitly_wait(1)
		driver.find_element('xpath', "//button[@id='bet'][@class='button is-primary btn isPrimary']").click()
	except:
		pass
