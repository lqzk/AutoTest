import shutil
import os


def move_file(filepath,orgdir,desdir):
    path_new=filepath.replace(orgdir,desdir)
    pathdir_new=os.path.dirname(path_new)
    if os.path.exists(pathdir_new):
        pass
    else:
        os.makedirs(pathdir_new)
    shutil.move(filepath,pathdir_new)


def copy_file(filepath,orgdir,desdir):
    path_new=filepath.replace(orgdir,desdir)
    pathdir_new=os.path.dirname(path_new)
    if os.path.exists(pathdir_new):
        pass
    else:
        os.makedirs(pathdir_new)
    shutil.copy(filepath,pathdir_new)

# if __name__ == "__main__":
#     # unittest.main()
#     pathdir = "F:\\test_project\\file\\诈骗\\起诉书（周某某诈骗案）---沪浦检刑诉〔2017〕257号.txt"
#     # content=open(pathdir).read()
#     # Defendant_to_end=re.search(r"((经(依法)?审[查理]查明)|(本院查明))[:：，,]?((.|\n|\r\n)*?)上述事实",content).group(5)
#     # print(Defendant_to_end)
#     move_file(pathdir, 'file', 'tested_file')
