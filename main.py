import csv
import json

import requests


def isContinue():
    print("是否继续？")
    return input().lower() == 'y'


auth = input("请输入ULearning API Token，位于请求头位置：")
res = []
# data = setting.js
while True:
    try:
        questionID = int(input("请输入QuestionID："))
        url = f"https://utestapi.ulearning.cn/exams/user/study/getExamReport?examId={questionID}"
        payload = {}
        headers = {
            'Authorization': f'{auth}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
        if data['code'] == 1:
            data = data['result']
            title = data['examTitle']
            for i in data['part']:
                types = i['partname']
                for s in i['children']:
                    question = s['title']
                    correctAnswer = s['correctAnswerAndReplay']['correctAnswer']
                    choices = s['item']
                    ans = []
                    for j in correctAnswer:
                        print(j)
                        if len(j) == 1:
                            ans.append(f'{j} 、{choices[ord(j) - ord("A")]["title"]}；')
                        else:
                            ans.append(f"{'正确' if j == 'true' else '错误'}")
                    res.append([question, "".join(ans), types, title])
    except:
        print("error!")
    if not isContinue():
        break

print(res)
writer = csv.writer(open("result.csv", encoding="utf-8", mode='w+'))
writer.writerows(res)
