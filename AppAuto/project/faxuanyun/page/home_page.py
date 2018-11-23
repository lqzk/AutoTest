from AppAuto.common.page import Page

class HomePage(Page):
    home_page_title=("id","n7")
    setting_button=("xpath","//android.view.View[@content-desc=\"设置\"]")
    nearby_activities = ("xpath", "//android.view.View[@content-desc=\"附近活动\"]")
    my_activity = ("xpath", "//android.view.View[@content-desc=\"我的活动\"]")
    daily_answer=("xpath","//android.view.View[@content-desc=\"每日答题\"]")
    mulitiplayer_war=("xpath","//android.view.View[@content-desc=\"多人团战\"]")
    ranking_list = ("xpath", "//android.view.View[@content-desc=\"排行榜\"]")




    def check_home_page(self):
        check_result=True
        elements=[self.nearby_activities,self.my_activity,self.daily_answer,self.mulitiplayer_war,self.ranking_list]
        for e in elements:
            check_result=check_result and self.is_display(*e)
        return check_result



    def get_title(self):
        return self.text(*self.home_page_title)