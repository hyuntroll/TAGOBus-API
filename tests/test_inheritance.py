from tagoapi import *

def get_inher():
    auth = TAGOAuth(serviceKey='1234')
    busRoute = BusRoute(auth)
    return busRoute.test(), busRoute.test_url()

def test_inher():
    assert(get_inher(), ('1234', "http://apis.data.go.kr/1613000"))


if __name__ == "__main__":
    print(get_inher())