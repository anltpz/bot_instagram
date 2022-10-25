
from lib2to3.pgen2 import driver
from re import S
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
import getpass


users = set()
following_list = set()
#dictionary
class BasePage:
    
    user_name=(By.XPATH,"//header/section/div[1]")


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
        self.login_button = (By.XPATH,"//div[contains(text(),'Log in')]")

    def login(self,username,password):
        sleep(2)
        self.send_keys(self.username,username)
        self.send_keys(self.password,password)
        self.click(self.login_button)

class HomePage(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
        self.profile = (By.XPATH,"//div[@class='profile']")
        self.save_your_login_info = (By.XPATH,"//div[@class='_ac8f']") 
        self.turn_on_notifications = (By.XPATH,"""//div[@class="_a9-z"]/button[2]""")
        
    def click_save_your_login_info(self):
        self.wait_for_clickable(self.save_your_login_info).click()

    def click_turn_on_notifications(self):
        self.wait_for_clickable(self.turn_on_notifications).click()

class AccountPage(BasePage):

    def __init__(self,driver):
        super().__init__(driver)
        sleep(3)
        self.profile = (By.CLASS_NAME,"""_aarf _aak0""")
        self.profile_status=(By.XPATH,"//section/ul/li")  

       
       
        self.dialog = (By.CSS_SELECTOR,"div[role=dialog")
        self.get_following_list = (By.XPATH,"//div[@class=\"_ab8w  _ab94 _ab99 _ab9f _ab9k _ab9p _abcm\"]/span/a")
        self.get_followers_list = (By.XPATH,"//div[@class=\"_ab8w  _ab94 _ab99 _ab9f _ab9k _ab9p _abcm\"]/span/a")

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

                
    

    
       
    def get_following_count(self):
        AccountPage.scroll_down(self)
        following = self.find_elements(self.get_following_list)
        sayac =0
        for i in following:
            i = i.text.replace("\nVerified","")
            self.followingList.add(i)
            sayac+=1
        
        print("following sayisi: ",sayac)
        
        print(self.followingList)

   
    def  get_followers_count(self):
        AccountPage.scroll_down(self)
        followers = self.find_elements(self.get_followers_list)
        sayac =0
        for i in followers:
            i = i.text.replace("\nVerified","")
            self.followersList.add(i)
            sayac+=1
        print("Followers sayisi: ",sayac)
        print(self.followersList)
    
    def get_dont_follow_me(self):
        for  i  in self.followingList:
            if i not in self.followersList:
                print("Dont follow me: ",i)

            
        
    
    
    def get_info_following_list(self):
        
        following_liste=[]
        try:
            for i in self.followingList:
             self.driver.get("https://www.instagram.com/{}".format(i)) 

             sleep(3)
             username= self.find_element(self.user_name)
             name_user=username.text.split("\n")
             objec={}
             name={}
             status_info = self.find_elements(self.profile_status)
             for i in status_info:
                 liss=i.text.split(" ")
                 objec[liss[1]]=liss[0]
                 name={
                        name_user[0]:objec
                 }
             following_liste.append(name)
             print(name)
            
        except  NoSuchElementException:
             print("Hesap private")
        finally:
            json.dump(following_liste,open("info.json","w"))
            print("Bitti")

   
    def  get_info_followers_list(self):
        
        followers_list=[]
        try:
            for i in self.followingList:
             self.driver.get("https://www.instagram.com/{}".format(i)) 

             sleep(3)
             username= self.find_element(self.user_name)
             name_user=username.text.split("\n")
             objec={}
             name={}
             status_info = self.find_elements(self.profile_status)
             for i in status_info:
                 liss=i.text.split(" ")
                 objec[liss[1]]=liss[0]
                 name={
                        name_user[0]:objec
                 }
             followers_list.append(name)
             print(name)
            
        except  NoSuchElementException:
             print("Hesap private")
        finally:
            json.dump(followers_list,open("followers.json","w"))
            print("Bitti")

     
print("Program başladı")   

kullanici_adi = input("Kullanici adi giriniz : ")
sifre =getpass.getpass("Sifre giriniz:")
testdriver = webdriver.Chrome(ChromeDriverManager().install())
login = Login(testdriver)
accountPage=AccountPage(testdriver)
homePage=HomePage(testdriver)

login.login(kullanici_adi,sifre)
sleep(3)
homePage.click_save_your_login_info()
homePage.click_turn_on_notifications()
def  json_followers_data(account_name):
    testdriver.get("https://www.instagram.com/{}/followers".format(account_name))
    sleep(3)
    accountPage.get_following_count()
    sleep(3)
    accountPage.get_info_followers_list()
    

def  json_following_data():
    accountPage.get_info_following_list()
    sleep(3)
def  dont_follow_me_list():

    testdriver.get("https://www.instagram.com/anltpzz/following/")
    sleep(3)
    accountPage.get_following_count()

    # accountPage.get_info_following_list()
    testdriver.get("https://www.instagram.com/anltpzz/followers/")
    sleep(3)
    accountPage.get_info_followers_list()

json_followers_data("anltpzz")
dont_follow_me_list()









