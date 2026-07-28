"""수동 TAGO 호출 예제.

pytest 수집 시에는 실행되지 않으며, 직접 실행할 때만 네트워크를 사용한다.
"""


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    from src.tagoapi import TAGOClient

    load_dotenv()
    api_key = os.environ["TAGO_API_KEY"]

    with TAGOClient(api_key) as client:
        routes = client.get_route_by_no(routeNo="북구1", cityCode=22)
        print(routes)
