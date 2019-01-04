import os
import shutil


class HandleOperation:
    def obtain_project_info(self, project):
        project_info = JsonHandle(project_info_path).jData[project]
        launch_info = {}
        launch_info["driver"] = project_info["test_driver"]
        launch_info["driver_types"] = project_info["driver_types"]

        launch_info["test_version"] = project_info["test_version"]
        version_info = project_info[launch_info["test_version"]]
        launch_info["url"] = version_info[project_info["test_url"]]

        account_info = {}
        account_info["username"] = version_info["username"]
        account_info["password"] = version_info["password"]
        return (launch_info, account_info)

    def read(self,dicfile):
        import os
        import win32com.client
        content_list = []
        for filename, filepath in dicfile.items():
            # 读取文本的内容，包括txt、doc
            if ".txt" in filepath or ".Txt" in filepath:
                try:
                    # utf-8
                    with open(filepath) as f:
                        read_file_content = f.read()
                except:
                    # gbk
                    with open(filepath, "rb") as f:
                        read_file_content = f.read().decode("utf-8", "ignore")
            else:
                # .doc
                filepath_new = filepath.replace(".doc", ".txt")
                wordApp = win32com.client.Dispatch('Word.Application')
                doc = wordApp.Documents.Open(filepath)
                # 以txt格式存储
                doc.SaveAs(filepath_new, 4)
                doc.Close()
                wordApp.Quit()
                with open(filepath_new) as f:
                    read_file_content = f.read()
                os.remove(filepath_new)
            content_list.append((filename, filepath, read_file_content))
        return content_list

    def achive_file(self,filepath, type_dic=True):
        import os
        dicfile = {}
        listfile = []
        if type_dic == False:
            if os.path.isfile(filepath):
                filename = filepath.split("\\")[-1]
                listfile.append({filename: filepath})
            else:
                for root, dir, filenames in os.walk(filepath):
                    for f in filenames:
                        listfile.append({f: os.path.join(root, f)})
            return listfile
        else:
            if os.path.isfile(filepath):
                filename = filepath.split("\\")[-1]
                # filename=os.path.basename(filepath)
                dicfile[filename] = filepath
            else:
                for root, dir, filenames in os.walk(filepath):
                    for f in filenames:
                        dicfile[f] = os.path.join(root, f)
            return dicfile

    def cutout_content(self,file_content, position):
        import re
        result_content = ""
        if position == "查明部分":
            try:
                match = re.search(
                    r"(经.*?查明|本院查明)[,，:：]((.|\r\n|\n)*(?=(\n|\r\n)*认定上述事实)|(.|\r\n|\n)*(?=(\n|\r\n)*上述事实)|(.|\r\n|\n)*(?=(\n|\r\n)*以上事实))",
                    file_content)
                if match:
                    result_content = match.group(2)
            except:
                result_content = ""

        elif position == "指控部分":
            try:
                # pattern=re.compile(r'.+指控[,，:：]?((.|\r\n|\n)*(?=(\n|\r\n)*认定上述事实)|(.|\r\n|\n)*(?=(\n|\r\n)*上述事实)|(.|\r\n|\n)*(?=(\n|\r\n)*以上事实))')
                # result_content = pattern.search(file_content)
                match = re.search(
                    r".+指控[,，:：]?((.|\r\n|\n)*(?=(\n|\r\n)*认定上述事实)|(.|\r\n|\n)*(?=(\n|\r\n)*上述事实)|(.|\r\n|\n)*(?=(\n|\r\n)*以上事实))",
                    file_content)
                if match:
                    result_content = match.group(1)
            except:
                result_content = ""
        return result_content

    def move_file(self,filepath, orgdir, desdir):
        path_new = filepath.replace(orgdir, desdir)
        pathdir_new = os.path.dirname(path_new)
        if os.path.exists(pathdir_new):
            pass
        else:
            os.makedirs(pathdir_new)
        shutil.move(filepath, pathdir_new)

    def copy_file(self,filepath, orgdir, desdir):
        path_new = filepath.replace(orgdir, desdir)
        pathdir_new = os.path.dirname(path_new)
        if os.path.exists(pathdir_new):
            pass
        else:
            os.makedirs(pathdir_new)
        shutil.copy(filepath, pathdir_new)

    def timeData_handle(self,**kwargs):
        """
        时间参数处理
        :param kwargs:
        :return:
        """
        result_data={}
        if kwargs.get("end_time") and kwargs.get("start_time"):
            end_time = kwargs["end_time"]
            start_time = kwargs["start_time"]
        elif kwargs.get("end_time"):
            end_time = kwargs["end_time"]
            y, m, d = time.strptime(end_time, "%Y-%m-%d")[0:3]
            start_time = (datetime.datetime(y, m, d) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        elif kwargs.get("start_time"):
            start_time = kwargs["start_time"]
            end_time = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            end_time = datetime.datetime.now().strftime("%Y-%m-%d")
            start_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        result_data["start_time"]=start_time
        result_data["end_time"] = end_time
        return result_data




if __name__ == '__main__':
    file_list=HandleOperation().achive_file("F:\\AutoTest\\data\\data_from\\file",False)
    choice=random_choice_list(file_list)()
    for i in range(5):
        file=next(choice)
        filename=list(file.keys())[0]
        filepath=file[filename]
        print(filename+"  "+filepath)
    # print(DATA_FROM_PATH)
    # print(achive_file(DATA_FROM_PATH))


    file_content_all=open("F:\\test_project\\Auto_test\\Data\\file\\交通肇事罪\\起诉书（庄某某交通肇事案）(公开版)---沪松检诉刑诉〔2017〕566号.txt").read()
    Investgation=HandleOperation().cutout_content(file_content_all,"查明部分")
    print(Investgation)