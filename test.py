import requests
import json

#from simplejson import JSONDecodeError
#import psycopg2
#import os
#from dotenv import load_dotenv
#load_dotenv()
url = 'https://pxnet2.stat.fi:443/PXWeb/api/v1/en/Postinumeroalueittainen_avoin_tieto/2021/paavo_pxt_12f1.px'
post_code = ["00130","02380","16710","41930","54800"]
values="hr_ktu"
query={
      "query": [
        {
          "code": "Postinumeroalue",
          "selection": {
            "filter": "item",
            "values": post_code

          }
        },
        {
          "code": "Tiedot",
          "selection": {
            "filter": "item",
            "values": [
              values
            ]
          }
        }
      ],
      "response": {
        "format": "json-stat2"
      }
    }

try :
  response = requests.post(url, json=query)
  content = response.json()
except json.decoder.JSONDecodeError as e:
  print("there is an error with url")
except Exception as e:
  print("something else wrong with the code",e)

else:
  
  print(content)
