from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import requests

depart_city = "TPE" #出發地
arrive_city = "KIX" #目的地
depart_time = "2024-07-01" #去程時間 XXXX(西元年)/XX(月)/XX(日)
arrive_time = "2024-07-04" #返程時間 XXXX(西元年)/XX(月)/XX(日)  若為單程則此欄為""
cabinclass = "" #艙等 經濟艙:""/特選經濟艙:"premium"/商務艙:"business"/頭等艙:"first"
directflight = False #是否僅限直飛航班 若是->True  若否->False
#===============旅客數量===============#
numOfAdult = 1 #成人數量
numOfStudent = 0 #18歲以上學生數量
numOfTeenager = 0 #青少年(12-17歲)數量
numOfChild = 0 #兒童(2-11)數量
numOfBaby1S = 0 #2歲以下佔坐兒童數量
numOfBaby1L = 0 #2歲以下不佔坐兒童數量
#=====================================#
if numOfAdult == 0:
    adult = ""
else:
    adult = str(numOfAdult) + "adults"
if numOfStudent == 0:
    student = ""
else:
    student = str(numOfStudent) + "students"
if numOfTeenager > 0 or numOfChild > 0 or numOfBaby1S >0 or numOfBaby1L > 0:
    children = "children" + "-17"*numOfTeenager + "-11"*numOfChild + "-1S"*numOfBaby1S + "-1L"*numOfBaby1L
else:
    children = ""
#=====================================#
if cabinclass == "premium":
    classtype = "特選經濟艙"
elif cabinclass == "business":
    classtype = "商務艙"
elif cabinclass == "first":
    classtype = "頭等艙"
else:
    classtype = "經濟艙"
#=====================================#
if directflight == True:
    fdDir = "fs=fdDir=true;stops=~0"
else:
    fdDir = ""
#=====================================#
search_Info = f'''目前查詢條件\n出發地:{depart_city}\n目的地:{arrive_city}\n出發日期:{depart_time}\n抵達日期:{arrive_time}
艙等:{classtype}\n旅客人數\n成人:{str(numOfAdult)}人\n學生:{str(numOfStudent)}人\n青少年:{str(numOfTeenager)}人\n兒童:{str(numOfChild)}人
2歲以下佔坐嬰兒:{str(numOfBaby1S)}人\n2歲以下不佔坐嬰兒:{str(numOfBaby1L)}人'''

#若人數設定中students非0，則會多顯示需驗證學生身分內容，XPATH需重新定位
if numOfStudent >= 1:
    cheapestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[1]'
    bestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[2]'
    fastFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[3]'
    flightInfo_XPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div'
else:
    cheapestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[1]/div[1]'
    bestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[1]/div[2]'
    fastFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[1]/div[3]'
    flightInfo_XPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div'

#URL Setting
url = f"https://www.tw.kayak.com/flights/{depart_city}-{arrive_city}/{depart_time}/{arrive_time}/{cabinclass}/{adult}/{student}/{children}?{fdDir}"
url_Price = url + "&sort=price_a"
url_Best = url + "&sort=bestflight_a"
url_Duration = url + "&sort=duration_a"
browser = webdriver.Chrome()
browser.get(url)
sleep(10)

def get_Reco_Flight(): #獲取最便宜/超值/最快三項簡易資訊
    print("推薦航班資訊")
    print("==========================")
    result_Reco = browser.find_elements(By.CLASS_NAME,"Hv20-option")
    for z in result_Reco:
        print(z.text)
    reco_Result_Message = "推薦航班資訊\n==== ==== ====\n" + "\n".join(a.text for a in result_Reco)
    return reco_Result_Message

def get_Cheapest_Flight():
    print("最優惠航班資訊")
    print("============")
    cheapest_Result_Summary = browser.find_element(By.XPATH,cheapestFlightSummary_XPATH) #cheapest_result_box_summary
    cheapest_Result_Summary.click() #click cheapest_result_box
    sleep(3)
    result_Cheapest = browser.find_elements(By.XPATH,flightInfo_XPATH) #get cheapest flight info
    for j in result_Cheapest:
        print(j.text)
    cheapest_Result_Message = "最優惠航班資訊\n==== ==== ====\n" + j.text + "詳細資訊請點擊下方連結\n" + url_Price
    return cheapest_Result_Message

def get_Best_Flight():
    print("超值航班資訊")
    print("===========")
    best_Result_Summary = browser.find_element(By.XPATH,bestFlightSummary_XPATH) #best_result_box_summary
    best_Result_Summary.click() #click best_result_box
    sleep(3)
    result_Best = browser.find_elements(By.XPATH,flightInfo_XPATH) #get best flight info
    for i in result_Best:
        print(i.text)
    best_Result_Message = "超值航班資訊\n==== ==== ====\n" + i.text + "詳細資訊請點擊下方連結\n" + url_Best
    return best_Result_Message

def get_Fast_Flight():
    print("最快航班資訊")
    print("===========")
    fast_Result_Summary = browser.find_element(By.XPATH,fastFlightSummary_XPATH) #fast_result_box_summary
    fast_Result_Summary.click() #click fast_result_box
    sleep(3)
    result_Fast = browser.find_elements(By.XPATH,flightInfo_XPATH) #get fast flight info
    for k in result_Fast:
        print(k.text)
    fast_Result_Message = "最快航班資訊\n==== ==== ====\n" + k.text + "詳細資訊請點擊下方連結\n" + url_Duration
    return fast_Result_Message

#LineNotify
def lineNotify(token, msg):
    headers = {
        "Authorization" : "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    payload = {'message' : msg}
    r = requests.post("https://notify-api.line.me/api/notify",headers = headers, params = payload)
    print(r.status_code)
    return r.status_code #return 200->success

def main():
    reco_Flight_Result = get_Reco_Flight()
    cheapest_Flight_Result = get_Cheapest_Flight()
    best_Flight_Result = get_Best_Flight()
    fast_Flight_Result = get_Fast_Flight()
    lineNotify(token, search_Info) #Send current setting Info
    sleep(2)
    lineNotify(token, reco_Flight_Result) #Send Recommendation Info  #TODO 是否保留?
    sleep(2)
    lineNotify(token, cheapest_Flight_Result) #Send Cheapest Flight Info
    sleep(2)
    lineNotify(token, best_Flight_Result) #Send Best Flight Info
    sleep(2)
    lineNotify(token, fast_Flight_Result) #Send Fast Flight Info
    sleep(2)

token = "XXX" #Fill in your Token
main()