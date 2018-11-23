import os
import win32com.client

def read(dicfile):
    content_list=[]
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
        content_list.append((filename,filepath,read_file_content))
    return content_list
