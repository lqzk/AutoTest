import re

def cutout_content(file_content,position):
    result_content=""
    if position=="查明部分":
        try:
            match = re.search(r"(经.*?查明|本院查明)[,，:：]((.|\r\n|\n)*(?=(\n|\r\n)*认定上述事实)|(.|\r\n|\n)*(?=(\n|\r\n)*上述事实)|(.|\r\n|\n)*(?=(\n|\r\n)*以上事实))",file_content)
            if match:
                result_content = match.group(2)
        except:
            result_content = ""

    elif position=="指控部分":
        try:
            # pattern=re.compile(r'.+指控[,，:：]?((.|\r\n|\n)*(?=(\n|\r\n)*认定上述事实)|(.|\r\n|\n)*(?=(\n|\r\n)*上述事实)|(.|\r\n|\n)*(?=(\n|\r\n)*以上事实))')
            # result_content = pattern.search(file_content)
            match = re.search(r".+指控[,，:：]?((.|\r\n|\n)*(?=(\n|\r\n)*认定上述事实)|(.|\r\n|\n)*(?=(\n|\r\n)*上述事实)|(.|\r\n|\n)*(?=(\n|\r\n)*以上事实))",file_content)
            if match:
                result_content = match.group(1)
        except:
            result_content = ""
    return result_content


if __name__ == '__main__':
    file_content_all=open("F:\\test_project\\Auto_test\\Data\\file\\交通肇事罪\\起诉书（庄某某交通肇事案）(公开版)---沪松检诉刑诉〔2017〕566号.txt").read()
    Investgation=cutout_content(file_content_all,"查明部分")
    print(Investgation)