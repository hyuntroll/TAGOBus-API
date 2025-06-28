from tagoapi import modelA


def test_test_hello():
    # 해당 함수의 반환값이 맞는지 확인
    assert modelA("Python") == "Hello, Python!"
    assert modelA() == "Hello, World!"