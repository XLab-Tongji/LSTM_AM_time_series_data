import requests
import json

url = "http://47.101.219.119:7001/api/universal/Monitoring/MonDataEqu_shushui/where?prj=shushui&" \
      "dataset=3835049491879165952&order=ID&increase=false"


payload = json.dumps({
  "where": "(([t]>'2021/3/16 07:00:00') and ([t]<'2021/3/16 07:30:20') and ([wm]>0))"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
