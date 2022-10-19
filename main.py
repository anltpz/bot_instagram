
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
#action chains
from selenium.webdriver.common.action_chains import ActionChains
#keys 
import json
from user_info import USERNAME, PASSWORD


users = set()
following_list = set()
#dictionary
class BasePage:
    total_followers = (By.XPATH,"//header/section/ul/li[2]/a/div/span")
    total_post = (By.XPATH,"//header/section/ul/li[1]/div/span")
    total_following = (By.XPATH,"//header/section/ul/li[3]/a/div/span")

    private_total_post = (By.XPATH,"//ul[@class=\"x78zum5 x1q0g3np xieb3on\"/li[1]//span")
    private_total_followers = (By.XPATH,"//ul[@class=\"x78zum5 x1q0g3np xieb3on\"]/li[2]//span")
    private_total_following = (By.XPATH,"//ul[@class=\"x78zum5 x1q0g3np xieb3on\"]/li[3]//span")

  

    def __init__(self,driver=webdriver):
        self.driver =driver
        self.followersList=set()
        self.followingList=set()
        self.private_account = False


    def find_element(self,locator):
        return self.driver.find_element(*locator)

    def find_elements(self,locator):
        return self.driver.find_elements(*locator)

    def click(self,locator):
        self.find_element(locator).click()

    def send_keys(self,locator,text):
        self.find_element(locator).send_keys(text)

    def get_text(self,locator):
        return self.find_element(locator).text

    def get_texts(self,locator):
        return [element.text for element in self.find_elements(locator)]

    def wait_for_clickable(self,locator):
        return WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(locator))

    def wait_for_visible(self,locator):
        return WebDriverWait(self.driver,10).until(EC.visibility_of_element_located(locator))

    def wait_for_invisibility(self,locator):
        return WebDriverWait(self.driver,10).until(EC.invisibility_of_element_located(locator))

   

    
class Login(BasePage):

    def __init__(self,driver,url="https://www.instagram.com/"):
        super().__init__(driver)
        self.driver.get(url)
        self.username = (By.XPATH,"//input[@name='username']")
        self.password = (By.XPATH,"//input[@name='password']")
        self.login_button = (By.XPATH,"//div[contains(text(),'Log In')]")

    def login(self,username,password):
        sleep(2)
        self.send_keys(self.username,username)
        self.send_keys(self.password,password)
        self.click(self.login_button)

class HomePage(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
        self.profile = (By.XPATH,"//div[@class='profile']")

    

class AccountPage(BasePage):

    def __init__(self,driver):
        super().__init__(driver)
        sleep(3)
        self.profile = (By.CLASS_NAME,"""_aarf _aak0""")
        self.save_your_login_info = (By.XPATH,"//div[@class='_ac8f']") 
        self.turn_on_notifications = (By.XPATH,"""//div[@class="_a9-z"]/button[2]""")
        self.get_followers_list = (By.XPATH,"//div[@class=\"_ab8w  _ab94 _ab99 _ab9f _ab9k _ab9p _abcm\"]/span/a")
       
        self.dialog = (By.CSS_SELECTOR,"div[role=dialog")
        self.get_following_list = (By.XPATH,"//div[@class=\"_ab8w  _ab94 _ab99 _ab9f _ab9k _ab9p _abcm\"]/span/a")

    def scroll_down(self):
        js_code="""
        sayfa = document.querySelector("._aano");
        sayfa.scrollTo(0,sayfa.scrollHeight);
        var sayfaSonu = sayfa.scrollHeight;
        return sayfaSonu;
        """
        sayfaSonu=self.driver.execute_script(js_code)
        while True:
            son =sayfaSonu
            sleep(3)
            sayfaSonu=self.driver.execute_script(js_code)
            if son == sayfaSonu:
                break

                
    def click_save_your_login_info(self):
        self.wait_for_clickable(self.save_your_login_info).click()

    def click_turn_on_notifications(self):
        self.wait_for_clickable(self.turn_on_notifications).click()

    def get_followers(self):
       AccountPage.scroll_down(self)
       follower=  self.find_elements(self.get_followers_list)
       sayac =0
       for i in follower:
           self.followersList.add(i.text)
           sayac+=1
           print("followers sayısı: ",sayac)
       print(self.followersList)
       
       
    def get_following(self):
        AccountPage.scroll_down(self)
        following = self.find_elements(self.get_following_list)
        sayac =0
        for i in following:
            i = i.text.replace("\nVerified","")
            self.followingList.add(i)
            sayac+=1
        print("following sayisi: ",sayac)
        print(self.followingList)

    

    def get_info_following_info(self):
        
        liste=[]
        try:
            for i in self.followingList:
             self.driver.get("https://www.instagram.com/{}".format(i)) 
             sleep(3)
             total_followers= self.find_element(AccountPage.total_followers).text
             total_following = self.find_element(AccountPage.total_following).text
             total_post = self.find_element(AccountPage.total_post).text
             print("Followers: ",total_followers)
             print("Following: ",total_following)
             print("Post: ",total_post)
             print("**********************")
             obj = {
                    "name":i,
                    "Followers": total_followers,
                    "Following": total_following,
                    "Post": total_post
                 }
                
             liste.append(obj)
            # dict[i] =f"data: Followers:{total_followers}",f"Following:{total_following}",f"Post:{total_post}"
            
        except  NoSuchElementException:
             print("Hesap private")
        finally:
            json.dump(liste,open("info.json","w"))
            print("Bitti")


            
        
print("Program başladı")   

kullanici_adi = input("Kullanici adi giriniz : ")
sifre = input("Sifre giriniz : ")

testdriver = webdriver.Chrome(ChromeDriverManager().install())
login = Login(testdriver)
accountPage=AccountPage(testdriver)
#aanltpuz
login.login(kullanici_adi,sifre)
accountPage.click_save_your_login_info()
accountPage.click_turn_on_notifications()
sleep(2)
# testdriver.get("https://www.instagram.com/leomessi/followers/")

# sleep(10)
# accountPage.get_followers()
# sleep(10)
testdriver.get("https://www.instagram.com/anltpzz/following/")
sleep(3)
accountPage.get_following()
sleep(3)
accountPage.get_info_following_info()










