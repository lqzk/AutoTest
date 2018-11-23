from WebAuto.project.intelligent_judgement.page.caselist_page import CaselistPage
import re


class CaseStudyPage(CaselistPage):
    list_button=("xpath",".//div[1]/div/div[1]/div/p/span[1]/a")

    casestudy_title=("css","b.title")
    case_tags=("css","ul.case_tags")

    current_sentence=("xpath","//div[@id='top_content']/div/div[2]/div/table/tbody/tr/td/i/span[2]")
    current_fine=("xpath","//div[@id='top_content']/div/div[2]/div/table/tbody/tr[2]/td/i/span[3]")
    current_probation=("xpath","//div[@id='top_content']/div/div[2]/div/table/tbody/tr[3]/td/i/span[2]")
    deviation = ("xpath","//div[@id='top_content']/div/div/div[2]/div/p/span[2]")

    case_push=("xpath","//div[@id='bottom_content']/div[2]/ul/li[1]")
    case_list=("css","div.case")

    law_application_button=("xpath","//div[@id='bottom_content']/div[2]/ul/li[2]")
    criminal_law_button=("xpath","//div[@id='bottom_content']/div[2]/div/div/ul/li[1]")
    criminal_law=("css","div.item")
    law_explain_button=("xpath","//div[@id='bottom_content']/div[2]/div/div/ul/li[2]")
    law_explain=("css","div.item")
    city_regulation_button = ("xpath", "//div[@id='bottom_content']/div[2]/div/div/ul/li[3]")
    city_regulation = ("css", ".law_pane>div")
    understand_application_button={"jsgy":("xpath", "//div[@id='bottom_content']/div[2]/div/div/ul/li[3]"),
                                   "shjcy":("xpath", "//div[@id='bottom_content']/div[2]/div/div/ul/li[4]")}
    understand_application = ("css", ".law_pane>div")
    punish_guidance_button={"jsgy":("xpath", "//div[@id='bottom_content']/div[2]/div/div/ul/li[4]"),
                            "shjcy":("xpath", "//div[@id='bottom_content']/div[2]/div/div/ul/li[5]")}
    punish_guidance=("css","div.law_pane_sentencing")
    declare_sentence=("xpath","//div[@id='bottom_content']/div[2]/div/div/div/div/div[3]/p/i/span")

    law_message_button=("xpath","//div[@id='bottom_content']/div[2]/ul/li[3]")
    law_message=("css","div.faxin")
    public_sentiment_button=("xpath","//div[@id='bottom_content']/div[2]/ul/li[4]")
    punish_map_button=("xpath","//div[@id='bottom_content']/div[2]/ul/li[5]")


    def jump_study_to_list(self):
        self.find_element(*self.list_button).click()
        print('个案研究页面跳转案件列表页面')
        self.sleep(11)

    def info(self,version="jsgy",title=""):

        result_info={}

        case_tags_info=self.text(*self.case_tags)
        result_info["标签信息"]=case_tags_info
        print("标签信息：\n" + case_tags_info)
        casestudy_title_info=self.text(*self.casestudy_title)

        result_info["标题"] = casestudy_title_info
        print("标题：" + casestudy_title_info)

        casecause_info=""
        try:
            casecause_info = re.compile(r'.+罪').search(casestudy_title_info).group(0)
        except Exception :
            pass
        finally:
            result_info["罪名"] = casecause_info

        print("罪名：" + casecause_info)

        current_sentence_info = self.text(*self.current_sentence)
        current_fine_info =  self.text(*self.current_fine)
        current_probation_info =  self.text(*self.current_probation)
        result_info["当前判罚"] = str("{0}\n{1}\n{2}".format(current_sentence_info,current_fine_info,current_probation_info))
        if current_sentence_info != "-- --" and current_probation_info != "-- --" and current_probation_info < current_sentence_info:
            print("当前判罚存在问题" )
        print("当前判罚为：{0},{1},{2}" .format(current_sentence_info , current_fine_info , current_probation_info))

        deviation_info=self.text(*self.deviation)
        result_info["偏离度"] =deviation_info
        if deviation_info!='-- --'and len(deviation_info)>1:
            if float(deviation_info) > 0.5:
                print("偏离度不合理：" + deviation_info)
            else:
                print("偏离度正常：" + deviation_info)

        self.click(*self.case_push)
        case_list_info=self.find_elements(*self.case_list)
        self.getscreen("案例推送_{0}".format(title))
        if case_list_info:
            print("有案例推送")
            case_exsit = "有"
        else:
            print("无案例推送")
            case_exsit = "无"
        result_info["案例推送"] = case_exsit

        #法律适用
        self.click(*self.law_application_button)


        self.click(*self.criminal_law_button)
        criminal_law_info=self.find_elements(*self.criminal_law)
        self.getscreen("刑法规定__{0}".format(title))
        if criminal_law_info:
            print("有刑法规定")
            criminal_law_exsit = "有"
        else:
            print("无刑法规定")
            criminal_law_exsit = "无"
        result_info["刑法规定"] = criminal_law_exsit

        self.click(*self.law_explain_button)
        law_explain_info = self.find_elements(*self.law_explain)
        self.getscreen("司法解释_{0}".format(title))
        if law_explain_info:
            print("有司法解释")
            law_explain_exsit = "有"
        else:
            print("无司法解释")
            law_explain_exsit = "无"
        result_info["司法解释"] = law_explain_exsit


        if version == "shjcy":
            self.click(*self.city_regulation_button)
            city_regulation_info = self.find_elements(*self.city_regulation)
            self.getscreen("本市规定_" + title)
            if city_regulation_info:
                print("有本市规定")
                city_regulation_exsit = "有"
            else:
                print("无本市规定")
                city_regulation_exsit = "无"
            result_info["本市规定"] = city_regulation_exsit

        self.click(*self.understand_application_button[version])
        understand_application_info = self.find_elements(*self.understand_application)
        self.getscreen("理解与适用_".format(title))
        if understand_application_info:
            print("有理解与适用")
            understand_application_exsit = "有"
        else:
            print("无理解与适用")
            understand_application_exsit = "无"
        result_info["理解与适用"] = understand_application_exsit


        self.click(*self.punish_guidance_button[version])
        punish_guidance_info = self.find_elements(*self.punish_guidance)
        self.getscreen("量刑指导意见_".format(title))
        if punish_guidance_info:
            declare_sentence_info=self.text(*self.declare_sentence)
            print("有量刑指导意见,宣告刑期：" + declare_sentence_info+"个月")
            punish_guidance_exsit = declare_sentence_info+"个月"
        else:
            print("无量刑指导意见")
            punish_guidance_exsit = "无"
        result_info["量刑指导意见"] = punish_guidance_exsit

        self.click(*self.law_message_button)
        law_message_info = self.find_elements(*self.law_message)
        self.getscreen("法信推送_{0}".format(title))
        if law_message_info:
            print("有法信推送")
            law_message_exsit = "有"
        else:
            print("无法信推送")
            law_message_exsit = "无"
        result_info["法信推送"] = law_message_exsit


        # 舆情推送
        self.click(*self.public_sentiment_button)

        # 量刑地图模块
        self.click(*self.punish_map_button)
        self.getscreen("量刑地图_{0}".format(title))

        return result_info





























