import requests

url="https://dispute.aegis-info.com/api/mediate/quick/saveCaseInfo"
url="http://dispute.aegis-info.com/api/mediate/quick/saveCaseInfo"
parm={"committeeId": "4401030010001", "disputeContent": "balabala", "disputeType": "01", "mediationDate": "2018-11-23"}
header={"Content-Type":"application/x-www-form-urlencoded"}
res=requests.post(url,data=parm,headers=header)
print(res.text)
