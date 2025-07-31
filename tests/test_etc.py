from tagoapi import *
from pprint import pprint
from dotenv import load_dotenv
import os


# def get_inher():
#     auth = TAGOAuth(serviceKey='1234')
#     busRoute = BusRoute(auth)
#     return busRoute.test(), busRoute.test_url()

# def test_inher():
#     assert(get_inher(), ('1234', "http://apis.data.go.kr/1613000"))


# if __name__ == "__main__":
#     test_lst = [
#         {'routeid': 'DGB2000002000', 'routeno': '순환2', 'routetp': '순환버스', 'endnode': None, 'startnode': None, 'endvehicletime': 2236, 'startvehicletime': 530},
#         {'routeid': 'DGB2000002100', 'routeno': '순환2-1', 'routetp': '순환버스', 'endnode': None, 'startnode': None, 'endvehicletime': 2230, 'startvehicletime': 530},
#         {'routeid': 'DGB2000003000', 'routeno': '순환3', 'routetp': '순환버스', 'endnode': None, 'startnode': None, 'endvehicletime': 2221, 'startvehicletime': 530},
#         {'routeid': 'DGB2000003100', 'routeno': '순환3-1', 'routetp': '순환버스', 'endnode': None, 'startnode': None, 'endvehicletime': 2220, 'startvehicletime': 530}
#     ]
    
#     lst = Route.from_list(test_lst)

#     print( Vehicle(route=lst[0]).to_dict())

#     print(TAGOClient(TAGOAuth('45'))._get1("34", new=None, ka=4, jkadf=34))
#     print(strip_meta(
#         {"response": {
#             "body": {
#                 "items": {
#                     "item": [
#                         {"a":1}, {"b":2}
#                     ]
#                 }
#             }
#         }}
#     ))


test = {
    "response": {
        "header": {
            "resultCode": "00",
            "resultMsg": "NORMAL SERVICE."
        },
        "body": {
            "items": {
                "item": [
                    {
                        "citycode": 12,
                        "cityname": "세종특별시"
                    },
                    {
                        "citycode": 21,
                        "cityname": "부산광역시"
                    },
                    {
                        "citycode": 22,
                        "cityname": "대구광역시"
                    },
                    {
                        "citycode": 23,
                        "cityname": "인천광역시"
                    },
                    {
                        "citycode": 24,
                        "cityname": "광주광역시"
                    },
                    {
                        "citycode": 25,
                        "cityname": "대전광역시/계룡시"
                    },
                    {
                        "citycode": 26,
                        "cityname": "울산광역시"
                    },
                    {
                        "citycode": 39,
                        "cityname": "제주도"
                    },
                    {
                        "citycode": 31010,
                        "cityname": "수원시"
                    },
                    {
                        "citycode": 31020,
                        "cityname": "성남시"
                    },
                    {
                        "citycode": 31030,
                        "cityname": "의정부시"
                    },
                    {
                        "citycode": 31040,
                        "cityname": "안양시"
                    },
                    {
                        "citycode": 31050,
                        "cityname": "부천시"
                    },
                    {
                        "citycode": 31060,
                        "cityname": "광명시"
                    },
                    {
                        "citycode": 31070,
                        "cityname": "평택시"
                    },
                    {
                        "citycode": 31080,
                        "cityname": "동두천시"
                    },
                    {
                        "citycode": 31090,
                        "cityname": "안산시"
                    },
                    {
                        "citycode": 31100,
                        "cityname": "고양시"
                    },
                    {
                        "citycode": 31110,
                        "cityname": "과천시"
                    },
                    {
                        "citycode": 31120,
                        "cityname": "구리시"
                    },
                    {
                        "citycode": 31130,
                        "cityname": "남양주시"
                    },
                    {
                        "citycode": 31140,
                        "cityname": "오산시"
                    },
                    {
                        "citycode": 31150,
                        "cityname": "시흥시"
                    },
                    {
                        "citycode": 31160,
                        "cityname": "군포시"
                    },
                    {
                        "citycode": 31170,
                        "cityname": "의왕시"
                    },
                    {
                        "citycode": 31180,
                        "cityname": "하남시"
                    },
                    {
                        "citycode": 31190,
                        "cityname": "용인시"
                    },
                    {
                        "citycode": 31200,
                        "cityname": "파주시"
                    },
                    {
                        "citycode": 31210,
                        "cityname": "이천시"
                    },
                    {
                        "citycode": 31220,
                        "cityname": "안성시"
                    },
                    {
                        "citycode": 31230,
                        "cityname": "김포시"
                    },
                    {
                        "citycode": 31240,
                        "cityname": "화성시"
                    },
                    {
                        "citycode": 31250,
                        "cityname": "광주시"
                    },
                    {
                        "citycode": 31260,
                        "cityname": "양주시"
                    },
                    {
                        "citycode": 31270,
                        "cityname": "포천시"
                    },
                    {
                        "citycode": 31320,
                        "cityname": "여주시"
                    },
                    {
                        "citycode": 31350,
                        "cityname": "연천군"
                    },
                    {
                        "citycode": 31370,
                        "cityname": "가평군"
                    },
                    {
                        "citycode": 31380,
                        "cityname": "양평군"
                    },
                    {
                        "citycode": 32010,
                        "cityname": "춘천시"
                    },
                    {
                        "citycode": 32020,
                        "cityname": "원주시/횡성군"
                    },
                    {
                        "citycode": 32050,
                        "cityname": "태백시"
                    },
                    {
                        "citycode": 32310,
                        "cityname": "홍천군"
                    },
                    {
                        "citycode": 32360,
                        "cityname": "철원군"
                    },
                    {
                        "citycode": 32410,
                        "cityname": "양양군"
                    },
                    {
                        "citycode": 33010,
                        "cityname": "청주시"
                    },
                    {
                        "citycode": 33020,
                        "cityname": "충주시"
                    },
                    {
                        "citycode": 33030,
                        "cityname": "제천시"
                    },
                    {
                        "citycode": 33320,
                        "cityname": "보은군"
                    },
                    {
                        "citycode": 33330,
                        "cityname": "옥천군"
                    },
                    {
                        "citycode": 33340,
                        "cityname": "영동군"
                    },
                    {
                        "citycode": 33350,
                        "cityname": "진천군"
                    },
                    {
                        "citycode": 33360,
                        "cityname": "괴산군"
                    },
                    {
                        "citycode": 33370,
                        "cityname": "음성군"
                    },
                    {
                        "citycode": 33380,
                        "cityname": "단양군"
                    },
                    {
                        "citycode": 34010,
                        "cityname": "천안시"
                    },
                    {
                        "citycode": 34020,
                        "cityname": "공주시"
                    },
                    {
                        "citycode": 34040,
                        "cityname": "아산시"
                    },
                    {
                        "citycode": 34050,
                        "cityname": "서산시"
                    },
                    {
                        "citycode": 34060,
                        "cityname": "논산시"
                    },
                    {
                        "citycode": 34070,
                        "cityname": "계룡시"
                    },
                    {
                        "citycode": 34330,
                        "cityname": "부여군"
                    },
                    {
                        "citycode": 34390,
                        "cityname": "당진시"
                    },
                    {
                        "citycode": 35010,
                        "cityname": "전주시"
                    },
                    {
                        "citycode": 35020,
                        "cityname": "군산시"
                    },
                    {
                        "citycode": 35040,
                        "cityname": "정읍시"
                    },
                    {
                        "citycode": 35050,
                        "cityname": "남원시"
                    },
                    {
                        "citycode": 35060,
                        "cityname": "김제시"
                    },
                    {
                        "citycode": 35320,
                        "cityname": "진안군"
                    },
                    {
                        "citycode": 35330,
                        "cityname": "무주군"
                    },
                    {
                        "citycode": 35340,
                        "cityname": "장수군"
                    },
                    {
                        "citycode": 35350,
                        "cityname": "임실군"
                    },
                    {
                        "citycode": 35360,
                        "cityname": "순창군"
                    },
                    {
                        "citycode": 35370,
                        "cityname": "고창군"
                    },
                    {
                        "citycode": 35380,
                        "cityname": "부안군"
                    },
                    {
                        "citycode": 36010,
                        "cityname": "목포시"
                    },
                    {
                        "citycode": 36020,
                        "cityname": "여수시"
                    },
                    {
                        "citycode": 36030,
                        "cityname": "순천시"
                    },
                    {
                        "citycode": 36040,
                        "cityname": "나주시"
                    },
                    {
                        "citycode": 36060,
                        "cityname": "광양시"
                    },
                    {
                        "citycode": 36320,
                        "cityname": "곡성군"
                    },
                    {
                        "citycode": 36330,
                        "cityname": "구례군"
                    },
                    {
                        "citycode": 36350,
                        "cityname": "고흥군"
                    },
                    {
                        "citycode": 36380,
                        "cityname": "장흥군"
                    },
                    {
                        "citycode": 36400,
                        "cityname": "해남군"
                    },
                    {
                        "citycode": 36410,
                        "cityname": "영암군"
                    },
                    {
                        "citycode": 36420,
                        "cityname": "무안군"
                    },
                    {
                        "citycode": 36430,
                        "cityname": "함평군"
                    },
                    {
                        "citycode": 36450,
                        "cityname": "장성군"
                    },
                    {
                        "citycode": 36460,
                        "cityname": "완도군"
                    },
                    {
                        "citycode": 36470,
                        "cityname": "진도군"
                    },
                    {
                        "citycode": 36480,
                        "cityname": "신안군"
                    },
                    {
                        "citycode": 37010,
                        "cityname": "포항시"
                    },
                    {
                        "citycode": 37020,
                        "cityname": "경주시"
                    },
                    {
                        "citycode": 37030,
                        "cityname": "김천시"
                    },
                    {
                        "citycode": 37040,
                        "cityname": "안동시"
                    },
                    {
                        "citycode": 37050,
                        "cityname": "구미시"
                    },
                    {
                        "citycode": 37060,
                        "cityname": "영주시"
                    },
                    {
                        "citycode": 37070,
                        "cityname": "영천시"
                    },
                    {
                        "citycode": 37080,
                        "cityname": "상주시"
                    },
                    {
                        "citycode": 37090,
                        "cityname": "문경시"
                    },
                    {
                        "citycode": 37100,
                        "cityname": "경산시"
                    },
                    {
                        "citycode": 37320,
                        "cityname": "의성군"
                    },
                    {
                        "citycode": 37330,
                        "cityname": "청송군"
                    },
                    {
                        "citycode": 37340,
                        "cityname": "영양군"
                    },
                    {
                        "citycode": 37350,
                        "cityname": "영덕군"
                    },
                    {
                        "citycode": 37360,
                        "cityname": "청도군"
                    },
                    {
                        "citycode": 37370,
                        "cityname": "고령군"
                    },
                    {
                        "citycode": 37380,
                        "cityname": "성주군"
                    },
                    {
                        "citycode": 37390,
                        "cityname": "칠곡군"
                    },
                    {
                        "citycode": 37400,
                        "cityname": "예천군"
                    },
                    {
                        "citycode": 37410,
                        "cityname": "봉화군"
                    },
                    {
                        "citycode": 37420,
                        "cityname": "울진군"
                    },
                    {
                        "citycode": 37430,
                        "cityname": "울릉군"
                    },
                    {
                        "citycode": 38010,
                        "cityname": "창원시"
                    },
                    {
                        "citycode": 38030,
                        "cityname": "진주시"
                    },
                    {
                        "citycode": 38050,
                        "cityname": "통영시"
                    },
                    {
                        "citycode": 38060,
                        "cityname": "사천시"
                    },
                    {
                        "citycode": 38070,
                        "cityname": "김해시"
                    },
                    {
                        "citycode": 38080,
                        "cityname": "밀양시"
                    },
                    {
                        "citycode": 38090,
                        "cityname": "거제시"
                    },
                    {
                        "citycode": 38100,
                        "cityname": "양산시"
                    },
                    {
                        "citycode": 38310,
                        "cityname": "의령군"
                    },
                    {
                        "citycode": 38320,
                        "cityname": "함안군"
                    },
                    {
                        "citycode": 38330,
                        "cityname": "창녕군"
                    },
                    {
                        "citycode": 38340,
                        "cityname": "고성군"
                    },
                    {
                        "citycode": 38350,
                        "cityname": "남해군"
                    },
                    {
                        "citycode": 38360,
                        "cityname": "하동군"
                    },
                    {
                        "citycode": 38370,
                        "cityname": "산청군"
                    },
                    {
                        "citycode": 38380,
                        "cityname": "함양군"
                    },
                    {
                        "citycode": 38390,
                        "cityname": "거창군"
                    },
                    {
                        "citycode": 38400,
                        "cityname": "합천군"
                    }
                ]
            }
        }
    }
}.get("response").get("body").get("items").get("item")


load_dotenv()
api_key = os.getenv('TAGO_API_KEY')
client = TAGOClient( auth=TAGOAuth(api_key) )

for i in test:
    try:
        shit = client.get_route_by_no(i["citycode"], "1")[0].to_dict()
    except:
        print(i["citycode"])
    print(shit["routeId"][0:3])

# print([i.to_dict() for i in client.get_route_by_no(12, "1")])

# print(test)

