#-*- coding utf-8 -*-
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from WebAuto.common.browser import Browser
from WebAuto.common.data_handle import picture_path


class Page(Browser):
    """selenium 二次封装"""

    def __init__(self,page=None):
        if page:
            self.driver=page.driver
        else:
            # Browser.__init__(self)
            super(Page,self).__init__()


    def execute_script(self,js):
        print(js)
        return self.driver.execute_script(script=js)

    def getscreen(self,screen_name):
        now_time=time.strftime("%Y-%m-%d %H-%M-%S",time.localtime())
        name={"True":picture_path+now_time +screen_name + ".png","False":picture_path+screen_name + ".png"}
        try:
            self.driver.get_screenshot_as_file(name["True"])
        except Exception as e:
            print("截图异常",format(e))

    def handle_element(self,loc):
        type=loc[0]
        if type=="id":
            type=By.ID
        elif type=="xpath":
            type = By.XPATH
        elif type=="link":
            type = By.LINK_TEXT
        elif type=="plink":
            type = By.PARTIAL_LINK_TEXT
        elif type=="name":
            type = By.NAME
        elif type=="tag":
            type = By.TAG_NAME
        elif type=="class":
            type = By.CLASS_NAME
        elif type=="css":
            type=By.CSS_SELECTOR

        return (type,loc[1])

    def is_enabled(self,*loc):
        return self.find_element(*loc).is_enabled()

    def is_displayed(self,*loc):
        return self.find_element(*loc).is_displayed()

    def find_element(self,*args):
        args = self.handle_element(args)
        self.wait_until(args)
        return self.driver.find_element(*args)

    def find_elements(self,*args):
        args = self.handle_element(args)
        return self.driver.find_elements(*args)

    def wait_until(self,loc,method="presence",timeout=10,poll_frequency=0.02):
        wait=WebDriverWait(self.driver, timeout, poll_frequency)
        if method=="presence":
            wait.until(EC.presence_of_element_located(loc))
        elif method=="clickable":
            wait.until(EC.element_to_be_clickable(loc))
        elif method=="not_load":
            wait.until_not(EC.visibility_of_element_located((By.CSS_SELECTOR,"loading")))


    def click(self,*args):
        try:
            self.find_element(*args).click()
        except Exception:
            try:
                self.find_element(*(By.CSS_SELECTOR, "loading"))
                self.wait_until(args, "not_load")
            except Exception:
                time.sleep(2)
            finally:
                self.find_element(*args).click()



    def clear(self,*args):
        self.find_element(*args).clear()

    def text(self,*args):
        return self.find_element(*args).text

    def is_element_present(self, *args):
        try:
            self.driver.find_element(*args)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True


    def is_element_exsit(self, *args):
        try:
            self.find_element(*args)
            return True
        except Exception as e:
            return False

    def actionChain(self):
        return ActionChains(self.driver)

    def forword(self):
        self.driver.forward()
        print("Click forward on current page.")

    def back(self):
        self.driver.back()
        print("Click back on current page.")

    def type(self, content, *args):
        self.find_element(*args).send_keys(content)

    def getCookies(self):
        return self.driver.get_cookies()

    def addCookie(self,cookie):
        return self.driver.add_cookie(cookie)

    def refresh(self):
        self.driver.refresh()


    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def sleep(self,second=6):
        time.sleep(second)


