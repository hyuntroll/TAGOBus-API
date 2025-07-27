import requests
import xmltodict


def http_get(endpoint: str, params: dict) -> dict:
    response = requests.get(endpoint, params=params, timeout=(3, 10))
    response.raise_for_status()
    try:
        return response.json()

    except requests.JSONDecodeError as e:
        try:
            return xmltodict.parse(response.text).get("OpenAPI_ServiceResponse", {}).get("cmmMsgHeader", {})
        except Exception as e:
            raise ValueError("응답을 JSON으로 디코딩 할 수 없습니다.")
        

    except requests.RequestException as e:
        raise ConnectionError(f"HTTP 요청 중 오류 발생: {e}")