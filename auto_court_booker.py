"""
自動預借球場
"""
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from time import sleep

def auto_book_court(url, headless):
	"""
	# [以下 url 是已經選定好 (1)區域 和 (2)球種 後的單一固定網址]
	# P.S. 該網頁只能預訂當前月份
	# 中正 - 羽球
	# http://booking.tpsc.sporetrofit.com/Location/Reserve?LID=JJSC&CategoryId=Badminton
	# 中正 - 撞球
	# http://booking.tpsc.sporetrofit.com/Location/Reserve?LID=JJSC&CategoryId=Billiard
	"""
	
	"""
	a_xpath = "//*[contains(text(), '開放預約')]/../.."
	a_tag_names = [tag.tag_name for tag in driver.find_elements_by_xpath(a_xpath)]
	print(*(a_tag_name for a_tag_name in a_tag_names))
	"""
	
	"""
	[以下 url 是已經選定好 (1)區域 (2)球種 (3) 日期 後的單一固定網址]
	# 3.18
	http://booking.tpsc.sporetrofit.com/Location/BookingList?LID=JJSC&CategoryId=Badminton&UseDate=2021-03-18

	# 3.19
	http://booking.tpsc.sporetrofit.com/Location/BookingList?LID=JJSC&CategoryId=Badminton&UseDate=2021-03-19
	"""
	if headless == True:
		_options = Options()
		_options.add_argument("--headless")
		driver = wd.Chrome("./chromedriver.exe", options=_options)
	else:
		driver = wd.Chrome("./chromedriver.exe")
	
	driver.implicitly_wait(10)
	driver.get(url)
	
	# 可被預約的 "地區, 場地/位置, 使用日期, 使用時間" 的 xpaths (=> 每一筆資料)
	bookable_pattern = "//td[@style='text-align:center;display:none;' and @title='預約']/../"
	ids = [1, 3, 4, 7]
	bookable_patterns = [f"{bookable_pattern}td[{i}]" for i in ids]
	bookable_id_patterns = "//td[@style='text-align:center;display:none;' and @title='預約']/../td[1]/.."
	booking_info = list()
	
	# 依類型(欄位)逐次爬取可預約的各資料
	for pattern in bookable_patterns:
		#print(pattern)
		col_data = driver.find_elements_by_xpath(pattern)
		l = len(col_data)
		if len(booking_info) == 0:
			for _ in range(l):
				booking_info.append([])
		for i in range(l):
			booking_info[i].append(col_data[i].text)
	
	IDs = driver.find_elements_by_xpath(bookable_id_patterns)
	for i, ID in enumerate(IDs):
		booking_info[i].insert(0, ID.get_attribute("id"))
	
	#print(booking_info)
	# result:
	"""
	[['中正', '7F羽球A', '2021-03-19', '06:00 - 07:00'], 
	 ['中正', '7F羽球B', '2021-03-19', '06:00 - 07:00'], 
	 ['中正', '7F羽球C', '2021-03-19', '06:00 - 07:00'], 
	 ['中正', '7F羽球B', '2021-03-19', '07:00 - 08:00'], 
	 ['中正', '7F羽球C', '2021-03-19', '07:00 - 08:00'], 
	 ['中正', '7F羽球B', '2021-03-19', '08:00 - 09:00']]
	"""
	
	#文字選擇提示
	print(f"共有 {l} 個時段可預借，資料如下:")
	print("編號	地區	場地/位置	使用日期	使用時間")
	for record in booking_info:
		print('	'.join(record))
	ans = input("請輸入要預借時段的 ID (如: 1,3,4): ")
	choices = ans.replace(' ', '').split(",")
	for i, choicedID in enumerate(choices):
		#choice = int(choice)
		#print(choice)
		
		# 依使用者選擇的時段續借
		ID_xpath = f"//table//tr[@id={choicedID}]//input[@type='button']" 
		booking_btn = driver.find_element_by_xpath(ID_xpath)
		print(f"正在按下ID為{choicedID}的預約按鈕")
		print("詳細資訊:")
		print("編號	地區	場地/位置	使用日期	使用時間")
		print('	'.join(booking_info[i]))
		print("[測試] 等待 0.5 秒")
		sleep(0.5)
		print("[狀態]「預約」按鈕已經按下")
		booking_btn.click()
		
		print("[測試] 等待 0.5 秒")
		print("[狀態] 因為未登入帳號等因素，系統不讓預約")
		print("[狀態] 正在關閉彈出式視窗")
		sleep(0.5)
		driver.find_element_by_xpath("//input[@id='popup_ok']").click()
		
if __name__ == "__main__":
	# 選定好 (1)區域 (2)球種 的網址:
	# url = "http://booking.tpsc.sporetrofit.com/Location/Reserve?LID=JJSC&CategoryId=Badminton"  
	
	# 選定好 (1)區域 (2)球種 (3) 日期 的網址:
	url = "http://booking.tpsc.sporetrofit.com/Location/BookingList?LID=JJSC&CategoryId=Badminton&UseDate=2021-03-19"
	
	headless = False
	auto_book_court(url, headless)
	
	