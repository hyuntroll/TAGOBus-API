from typing import TYPE_CHECKING
from typing import TypeVar

U = TypeVar('U', dict[str], list)  # list, dict으로 반환할 때


if TYPE_CHECKING:
    from tagoapi import TAGOAuth

def build_params(
        auth: "TAGOAuth",
        numOfRows: int = 300,
        pageNo: int = 1,
        **kwargs: dict
    ) -> dict:

    return {
            "serviceKey": auth.serviceKey,
            "numOfRows": numOfRows,
            "pageNo": pageNo,
            "_type": "json",
            **{key: value for key, value in kwargs.items() if value}
        }

def parse_metadata(res: dict) -> U | None:
    striped = res.get("response", {}).get("body", {}).get("items", {})
    if isinstance(striped, dict):
        return striped.get("item", None)

    return None


def _check_bracket(data: str) -> list[str]:
    args = []
    current_match = None
    fa = ''
    for w in data:
        if current_match:
            fa += w

        if w == '<':
            current_match = True
        elif w == '>':
            if not current_match:
                return None  # 에러를 나타내든 뭐를 하든
            current_match = False
            args.append(fa[:-1].strip());
            fa = ''

    return args


class KeyExtract:  ## 이를 BaseModel에 바로/
    def __init__(self, raw_key):
        self.raw_key = raw_key

        self._args = _check_bracket(self.raw_key)

    @property
    def key_args(self):
        return self._args

    def generate_key(self, data: dict) -> str:
        generated_key = self.raw_key
        # if len(kwargs) > len(self._args):
        #     raise TypeError(f"generate_key() takes {len(self._args)} positional argument but {len(kwargs)} were given")

        # TODO: 이거 self._args말고 kwargs.keys해서 arg랑 대응 시켜서 없으면 raise 이런식으로 작성해도 좋을 듯
        for arg in self._args:
            k = data.get(arg.lower(), None)
            if not k:
                raise TypeError()
            generated_key = generated_key.replace(f"<{arg}>", k)

        return generated_key

    def __call__(self):
        pass
