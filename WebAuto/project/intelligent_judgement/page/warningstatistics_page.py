from WebAuto.project.intelligent_judgement.page.login_page import LoginPage

class WarningStatisticsPage(LoginPage):
    page_title = ("css", "p.count_map_title")
    user_name=("css", "div.user > span")

    caselist_button=("css","p span.to_list")


    time_frame=("css","input.ant-calendar-input")
    start_time_button = ("xpath", "//div[@id='count_content']/div/div/p/span[2]/span/span/input")
    end_time_button = ("xpath", "//div[@id='count_content']/div/div/p/span[2]/span[3]/span/input")

    casecause_frame=("css","span.ant-select-selection__rendered")
    casecause_list=("css","li.ant-select-dropdown-menu-item")

    __one_level=("css","li.count_level1 > b")
    __two_level=("css","li.count_level2 > b")
    __three_level=("css","li.count_level3 > b")

    logout_link = ("link", "u'退出'")

    def logout(self):
        self.click(*self.logout_link)

    def title(self):
        return self.find_element(*self.page_title).text

    def userName(self):
        return self.find_element(*self.user_name).text

    def jump_warn_to_list(self):
        self.click(*self.caselist_button)
        print('预警统计页面跳转案件列表页面')
        self.sleep(11)


    def time_filter(self,start_time, end_time):

        print("SubTest:时间筛选：" + start_time + '至' + end_time)

        #开始时间设置
        self.click(*self.start_time_button)
        self.clear(*self.time_frame)
        self.type(start_time,*self.time_frame)
        self.actionChain().context_click(self.find_element(*self.page_title)).perform()

        self.sleep(1)

        # 结束时间设置
        self.click(*self.end_time_button)
        self.clear(*self.time_frame)
        self.type(end_time, *self.time_frame)
        self.actionChain().context_click(self.find_element(*self.page_title)).perform()


        # self.sleep(3)
        # js='document.getElementsByClassName("ant-calendar-picker-input ant-input ant-input-lg").value=2016-12-25'
        # self.execute_script(js)
        # self.sleep(5)
        #
        # js="document.getElementsByClassName('ant-calendar-picker-input ant-input ant-input-lg')[1].value="+end_time
        # self.execute_script(js)
        # self.sleep(5)

        self.getscreen("偏离度预警案件分布-时间筛选 " + start_time + ':' + end_time)

        print("EndTest:时间筛选结束" )


    def warning_present(self):
        one_level_num = self.text(*self.__one_level)
        two_level_num = self.text(*self.__two_level)
        three_level_num = self.text(*self.__three_level)

        print(
            "偏离度预警案件分布模块状态：1级预警-{0}，二级预警-{1}，三级预警-{2}".format(one_level_num, two_level_num, three_level_num))

        return (one_level_num,two_level_num,three_level_num)

    def warning_jump(self,level):

        levels = {1:self.__one_level, 2: self.__two_level, 3: self.__three_level}
        level_num = self.text(*levels[level])

        print("{0}级预警数值{1}，点击进入该预警入口".format(level,level_num))

        if level_num=='0':
            print(
                "No need to click：{0}级预警入口为0".format(level))
            return False
        else:
            self.click(*levels[level])
            return level_num


    def casecausefliter(self,case_cause):
        print('=====SubTest:案由筛选:{0}======'.format(case_cause))

        self.click(*self.casecause_frame)
        self.sleep(1)
        lilist = self.find_elements(*self.casecause_list)

        for li in lilist:
            if case_cause == li.text:
                self.sleep(1)
                li.click()
                self.getscreen("案由筛选{0}".format(case_cause))
                break

        print('=====EndSubTest:案由筛选======')



























