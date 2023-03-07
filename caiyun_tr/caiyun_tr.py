"""Define caiyun_tr."""
# pylint: disable=invalid-name, too-many-branches, too-many-statements
from base64 import b64decode
from codecs import encode
from hashlib import md5
from random import randint
from typing import Optional

import httpx
from logzero import logger

url_jwt = "https://api.interpreter.caiyunai.com/v1/user/jwt/generate"
url = "https://api.interpreter.caiyunai.com/v1/translator"
url = "https://interpreter.cyapi.cn/v1/translator"

# browser_id = md5(b"").hexdigest()
# jwt_dict = {}  # for reuse, sort of global jwt
headers = {
    "X-Authorization": "token:qgemv4jr1y38jyq6vhvi",
    "Content-Type": "application/json;charset=UTF-8",
    "app-name": "app",
}
# fd4
# "X-Authorization", "token:qgemv4jr1y38jyq6vhvi"

headers = {
    'Content-Type': 'application/json',
    'x-authorization': 'token ssdj273ksdiwi923bsd9',
    'user-agent': 'caiyunInterpreter/5 CFNetwork/1404.0.5 Darwin/22.3.0'
}


def caiyun_decode(sent):
    """Decode.

    s = rot13(s)
    s2 = base64.b64decode(s).decode('utf-8')
    return s2
    """
    return b64decode(rot13(sent)).decode("utf-8")


def rot13(message: str) -> str:
    """Rotate 13."""
    return encode(message, "rot13")


def fetch_jwt() -> str:
    """Fetch jwt."""
    browser_id = md5(b"").hexdigest()

    data = {"browser_id": browser_id}
    try:
        res = httpx.post(url_jwt, json=data, headers=headers)
        res.raise_for_status()
    except Exception as exc:
        logger.error(exc)
        raise

    # r = requests.post(url, data=json.dumps(data), headers=headers)

    try:
        jwt = res.json()["jwt"]
    except Exception as exc:
        logger.error(exc)
        raise

    return jwt


def caiyun_tr(
    # text: str, jwt: str, brower_id: str, from_lang: str = "en", to_lang: str = "zh"
    text: str,
    from_lang: str = "en",
    to_lang: str = "zh",
    # jwt: Optional[str] = None,
) -> str:
    """Define caiyun_tr.

    Args:
        text: to be translated
        from_lang: source language
        to_lang: destination language
        # jwt: fetch new jwt if None, use it if provided.

    Returns:
        translation text, para info preserved
    """
    # global jwt_dict  # pylint: disable=global-statement

    # first run: fetch_jwt
    # if not jwt_dict: jwt_dict.update(**{"jwt": fetch_jwt()})

    # default to global jwt
    # if jwt is None: jwt = jwt_dict.get("jwt")

    lpair = f"{from_lang}2{to_lang}"
    # headers1 = dict(**headers, **{"T-Authorization": jwt})
    _ = """
    data = {
        "source": text.splitlines(),
        "trans_type": lpair,
        "request_id": "web_fanyi",
        "media": "text",
        "os_type": "web",
        "dict": False,
        "cached": True,
        "replaced": True,
        "browser_id": browser_id,
    }
    # """

    data = {
        "source": text.splitlines(),
        "trans_type": lpair,
        "request_id": "web_fanyi",
        "media": "text",
        # "os_type": "web",
        "dict": False,
        "cached": True,
        "replaced": True,
        "detect": True,
        "os_type": "ios",
        "device_id": "F1F902F7-1780-4C88-848D-71F35D88A602",
    }
    # data["source"] = text
    data["request_id"] = randint(1, 1000)

    _ = """  # Token expired
    {'http_code': 200,
    'message': 'Token expired',
    'err_code': None,
    'details': None,
    'auth_code': -3}
    """
    # update jwt when expired
    # for _ in range(2):
    try:
        # resp = httpx.post(url, json=data, headers=headers1)
        resp = httpx.post(url, json=data, headers=headers)
        # resp.raise_for_status()
    except httpx.HTTPStatusError as exc:  # cant seem to catch httpx.HTTPStatusError
        logger.error(exc)
        if "not implemented" in str(exc).lower():
            logger.warning(
                "Supported languages: zh en, zh ja, en zh, ja zh. Check params supplied "
            )
        raise
    except Exception as exc:
        logger.error(exc)
        if "not implemented" in str(exc).lower():
            logger.warning(
                "Supported languages: zh en, zh ja, en zh, ja zh. Check params supplied "
            )
        raise

    try:
        jdata = resp.json()
    except Exception as exc:
        logger.error(
            "respo.json() exception: %s, something from the caiyun site has probably changed, contact dev for a possible fix.",
            exc,
        )
        logger.error("resp.text: %s", resp.text)
        raise

    # pair not supported
    if "Unsupported" in jdata.get("message", ""):
        logger.error(" language pair not supported, check params supplied")
        raise Exception("Unsupported trans_type (language pair)")

    target = jdata.get("target", "")
    if not target:
        logger.warning(" Nothing expected returned, something has gone wrong... ")
        return ""

    lines = []
    for trtext in target:
        # decrypt
        try:
            # _ = b64decode(rot13(trtext)).decode("utf-8")
            lines.append(trtext)
        except Exception as exc:
            logger.error(exc)
            raise

    return "\n".join(lines)


_ = '''
import urllib

try:
req = urllib.request.Request("https://lingocloud.caiyunapp.com/v1/translator")

req.add_header("Connection", "keep-alive")
req.add_header("sec-ch-ua", "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"")
req.add_header("version", "1.8.0")
req.add_header("DNT", "1")
req.add_header("os-version", "")
req.add_header("sec-ch-ua-mobile", "?0")
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
req.add_header("app-name", "xy")
req.add_header("Content-Type", "application/json;charset=UTF-8")
req.add_header("Accept", "application/json, text/plain, */*")
req.add_header("device-id", "")
req.add_header("os-type", "web")
req.add_header("X-Authorization", "token:qgemv4jr1y38jyq6vhvi")
req.add_header("T-Authorization", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJicm93c2VyX2lkIjoiNWRkYjE5Y2Y3Yzg1MTExZDVjNGIyNGMxY2UyYjRmMjQiLCJpcF9hZGRyZXNzIjoiMjE5Ljc2LjI1LjEyNSIsInRva2VuIjoicWdlbXY0anIxeTM4anlxNnZodmkiLCJ2ZXJzaW9uIjoxLCJleHAiOjE2NzgxNzI1NTd9.PmqL-0dM5aB0af1WvDsMTI9glY4oRjqByn7Dh4aWyMI")
req.add_header("sec-ch-ua-platform", "\"Windows\"")
req.add_header("Origin", "https://fanyi.caiyunapp.com")
req.add_header("Sec-Fetch-Site", "same-site")
req.add_header("Sec-Fetch-Mode", "cors")
req.add_header("Sec-Fetch-Dest", "empty")
req.add_header("Referer", "https://fanyi.caiyunapp.com/")
req.add_header("Accept-Encoding", "gzip, deflate, br")
req.add_header("Accept-Language", "en,zh;q=0.9,de;q=0.8")

body = """{\"source\":\"多测试测试一下\",\"trans_type\":\"zh2en\",\"request_id\":\"web_fanyi\",\"media\":\"text\",\"os_type\":\"web\",\"dict\":true,\"cached\":true,\"replaced\":true,\"browser_id\":\"5ddb19cf7c85111d5c4b24c1ce2b4f24\"}""".encode()

r = urllib.request.urlopen(req, body)

r_read = r.read()

text_tr = caiyun_decode(json.loads(r_read.decode()).get('target'))
# '''
