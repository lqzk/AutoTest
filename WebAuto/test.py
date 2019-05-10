import re


def extract_date(string):
    year, month, day = 0, 0, 0
    if re.search(u"(\d*)年", string): year = int(re.search(u"(\d*)年", string).group(1))
    if not year==0:
        if re.search(u"年(\d*).*月", string): month = int(re.search(u"年(\d*).*月", string).group(1))
    else:
        if re.search(u"^(\d*).*月", string): month = int(re.search(u"^(\d*).*月", string).group(1))
    if re.search(u"(\d*)天", string): day = int(re.search(u"(\d*)天", string).group(1))
    return year, month, day

string='5个月15天'
print(extract_date(string))

