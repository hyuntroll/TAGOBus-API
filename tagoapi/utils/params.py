from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tagoapi import TAGOAuth

def build_params(
        auth: "TAGOAuth",  
        numOfRows: int = 10, 
        pageNo: int = 1,
        **kwargs: dict
    ) -> dict:

    return {
        "serviceKey": auth.getServiceKey(),
        "numOfRows": numOfRows,
        "pageNo": pageNo,
        "_type": "json",
        **{key: value for key, value in kwargs.items() if value}
        }