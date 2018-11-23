from AppAuto.common.app import App
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from time import sleep
from selenium.webdriver.common.by import By


class Page(App):
    """selenium 二次封装"""

    def __init__(self,page=None):
        if page:
            self.driver=page.driver
        else:
            # Browser.__init__(self)
            super(Page,self).__init__()

    def handle_element(self,*loc):
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
        else:
            print("Invalid location method")
        return (type,loc[1])

    def find_element(self,*loc):
        '''封装单个元素定位方法'''
        loc=self.handle_element(*loc)
        try:
            self.wait_until(loc)
        except Exception as e:
            print("{0}：超时未找到".format(loc))
        return self.driver.find_element(*loc)

    def find_elements(self,*loc):
        '''封装一组元素定位方法'''
        loc = self.handle_element(*loc)
        return self.driver.find_elements(*loc)

    def text(self,*loc):
        return self.find_element(*loc).text

    def input(self,*loc,input_value):
        self.find_element(*loc).send_keys(input_value)

    def click(self,*loc):
        self.find_element(*loc).click()

    def tap(self,x=100,y=200,duration=500):
        # self.driver.tap([(x,y)],duration)
        try:
            self.driver.tap([(100,200)], duration)
        except Exception as e:
            print(e)

    def long_press(self,*loc,long_duration):
        TouchAction(self.driver).long_press(self.find_element(*loc)).wait(long_duration).perform()

    def larger(self):
        window_size = self.driver.get_window_size()
        height = window_size["height"]
        width = window_size["width"]
        x11=width*0.45
        x12=width*0.25
        x21=width*0.55
        x22=width*0.75
        y=height*0.5
        touch_action1=TouchAction(self.driver).press(x=x11,y=y).wait(50).move_to(x=x12,y=y).release()
        touch_action2= TouchAction(self.driver).press(x=x21, y=y).wait(50).move_to(x=x22, y=y).release()
        zoom_action=MultiAction(self.driver)
        zoom_action.add(touch_action1,touch_action2)
        zoom_action.perform()

    def smaller(self):
        window_size = self.driver.get_window_size()
        height = window_size["height"]
        width = window_size["width"]
        x12=width*0.45
        x11=width*0.25
        x22=width*0.55
        x21=width*0.75
        y=height*0.5
        touch_action1=TouchAction(self.driver).press(x=x11,y=y).wait(50).move_to(x=x12,y=y).release()
        touch_action2= TouchAction(self.driver).press(x=x21, y=y).wait(50).move_to(x=x22, y=y).release()
        zoom_action = MultiAction(self.driver)
        zoom_action.add(touch_action1,touch_action2)
        zoom_action.perform()

    def swipe_up(self,up_width_ratio=0.5,up_height_ratio=(3/4,1/4)):
        window_size = self.driver.get_window_size()
        height = window_size["height"]
        width = window_size["width"]
        self.driver.swipe(width*up_width_ratio,height*up_height_ratio[0],width/2,height*up_height_ratio[1],200)

    def swipe_down(self,down_width_ratio=0.5,down_height_ratio=(1/4,3/4)):
        window_size = self.driver.get_window_size()
        height = window_size["height"]
        width = window_size["width"]
        self.driver.swipe(width*down_width_ratio,height*down_height_ratio[0],width/2,height*down_height_ratio[1],200)

    def swipe_right(self,right_height_ratio=0.5,right_width_ratio=(3/4,1/4)):
        window_size = self.driver.get_window_size()
        height = window_size["height"]
        width = window_size["width"]
        self.driver.swipe(width*right_width_ratio[0],height*right_height_ratio,width*right_width_ratio[1],height*right_height_ratio,200)

    def swipe_left(self,right_height_ratio=0.5,right_width_ratio=(1/4,3/4)):
        window_size = self.driver.get_window_size()
        height = window_size["height"]
        width = window_size["width"]
        self.driver.swipe(width*right_width_ratio[0],height*right_height_ratio,width*right_width_ratio[1],height*right_height_ratio,200)

    def sleep(self,time=10):
        sleep(time)

    def is_display(self, *loc):
        return self.find_element(*loc).is_displayed()

    def is_enabled(self, *loc):
        return self.find_element(*loc).is_enabled()

    def is_visibility(self, loc):
        return EC.visibility_of_element_located(loc)

    def is_clicked(self, loc):
        return EC.element_to_be_clickable(loc)

    def is_text(self, loc, text):
        return EC.text_to_be_present_in_element(loc, text)

    def is_presence(self, loc):
        return EC.presence_of_element_located(loc)

    def wait_until(self,loc,func=is_presence,timeout=10,poll_frequency=0.02):
        WebDriverWait(self.driver,timeout,poll_frequency).until(func(self,loc))
