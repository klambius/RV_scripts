# -*- coding: utf-8 -*-

import requests
import json
from uuid import uuid4
import string
import random
import base64
import urllib3
import time

crypto_tail44 = '\u001D91FFD0\u001D92fFgWxK0YxoHt5EB2J1+Keut9iQMm4lQFZMdgsFM97Hg='
gtn = '04604060998657'
url = "https://10.77.124.52:8443/v1/requests"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic dXNlcjI6cXdFMTIzeHg='
}

def generate_random_sn(length: int = 13):
    letters = string.hexdigits
    rand_sn = ''.join(random.choice(letters) for _ in range(length))
    return rand_sn

def generate_base64_km(gt: str, tail: str):
    dm = '01' + gt + '21' + generate_random_sn() + tail
    return base64.b64encode(dm.encode('utf-8')).decode('utf-8')

urllib3.disable_warnings()

status_code = 201
number = 0
uri_list = [str(uuid4()) for _ in range(3)]
print(len(uri_list))
start_post_time = time.time()

while status_code == 201 and number < 3:
    documentID = uri_list[number]
    number += 1

    # Генерация случайного количества марок
    marks_count = random.randint(1000, 2000)
    marks = {"{}".format(i): {"mark": generate_base64_km(gtn, crypto_tail44)} for i in range(1, marks_count + 1)}

    payload = json.dumps({
      "rvRequestId": documentID,
      "request": {
        "type": "registerMarksByRequisites",
        "documentOut": {
          "type": 0,
          "code": "0504204",
          "codeName": "Требование накладная",
          "date": "2022-07-05T23:32:28Z",
          "series": "123456N",
          "number": number
        },
        "marks": marks
      }
    })

    post_response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    status_code = post_response.status_code
    print(number, documentID, status_code)

execution_post_time = time.time() - start_post_time

status_code = 200
number = 0
start_get_time = time.time()
payload = {}

while status_code == 200 and number < 3:
    documentID = uri_list[number]
    number += 1
    get_url = url + '/' + documentID
    get_response = requests.request("GET", get_url, headers=headers, data=payload, verify=False)
    status_code = get_response.status_code
    print(number, documentID, status_code, str(get_response.content))

execution_get_time = time.time() - start_get_time
print('Номер последнего документа: ' + str(number) + '\n' +
      'ID последнего сохраненного в БД документа: ' + documentID + '\n' +
      'Status последнего GET запроса: ' + str(status_code) + '\n' +
      'Время отправки 10000 заданий в секундах: ' + str(execution_post_time) + '\n' +
      'Время выполнения GET-запросов в секундах: ' + str(execution_get_time))
print(str(get_response.content))
