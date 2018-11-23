import os
from WebAuto.project.intelligent_judgement.common.generator import random_choice_list

def achive_file(filepath,type_dic=True):
    dicfile = {}
    listfile=[]
    if type_dic==False:
        if os.path.isfile(filepath):
            filename = filepath.split("\\")[-1]
            listfile.append({filename:filepath})
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




if __name__ == '__main__':
    file_list=achive_file("F:\\AutoTest\\data\\data_from\\file",False)
    choice=random_choice_list(file_list)()
    for i in range(5):
        file=next(choice)
        filename=list(file.keys())[0]
        filepath=file[filename]
        print(filename+"  "+filepath)
    # print(DATA_FROM_PATH)
    # print(achive_file(DATA_FROM_PATH))
