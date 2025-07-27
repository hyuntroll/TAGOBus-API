import requests
import xmltodict
from requests.exceptions import (
    ConnectionError, Timeout, HTTPError, RequestException, JSONDecodeError
)


def http_get(endpoint: str, params: dict) -> dict:
    try:
        response = requests.get(endpoint, params=params, timeout=(3, 10))
        response.raise_for_status()

        return response.json()
    except ConnectionError:
        raise RuntimeError("서버에 연결할 수 없습니다. 인터넷 연결이나 도메인을 확인해주세요.")
    except Timeout:
        raise RuntimeError("요청 시간이 초가되었습니다.")
    except HTTPError as e:
        raise RuntimeError(f"HTTP 오류 발생: {e.response.status_code}")
    except JSONDecodeError as e:
        try:
            return xmltodict.parse(response.text).get("OpenAPI_ServiceResponse", {}).get("cmmMsgHeader", {})
        except Exception as e:
            raise ValueError("응답을 JSON으로 디코딩 할 수 없습니다.")
    

    except RequestException as e:
        raise RuntimeError(f"요청 중 알 수 없는 오류 발생: {e}")