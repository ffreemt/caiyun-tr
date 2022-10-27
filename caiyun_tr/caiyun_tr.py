"""Define caiyun_tr."""
from base64 import b64decode
from codecs import encode
from hashlib import md5

import httpx
from logzero import logger

url_jwt = "https://api.interpreter.caiyunai.com/v1/user/jwt/generate"
url = "https://api.interpreter.caiyunai.com/v1/translator"

headers = {
    "X-Authorization": "token:qgemv4jr1y38jyq6vhvi",
    "Content-Type": "application/json;charset=UTF-8",
    "app-name": "app",
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


def fetch_jwt():
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
        logger.errot(exc)
        raise

    return jwt, browser_id


def caiyun_tr(
    # text: str, jwt: str, brower_id: str, from_lang: str = "en", to_lang: str = "zh"
    text: str,
    from_lang: str = "en",
    to_lang: str = "zh",
) -> str:
    """Define caiyun_tr."""
    try:
        jwt, brower_id = fetch_jwt()
    except Exception as exc:
        logger.error(exc)
        raise

    lpair = f"{from_lang}2{to_lang}"
    headers1 = dict(**headers, **{"T-Authorization": jwt})
    data = {
        "source": text.splitlines(),
        "trans_type": lpair,
        "request_id": "web_fanyi",
        "media": "text",
        "os_type": "web",
        "dict": False,
        "cached": True,
        "replaced": True,
        "browser_id": brower_id,
    }

    try:
        resp = httpx.post(url, json=data, headers=headers1)
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error(exc)
        if "not implemented" in str(exc).lower():
            logger.info(
                "Supported languages: zh en, zh ja, en zh, ja zh. Check params supplied "
            )
    except Exception as exc:
        logger.error(exc)
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

    target = jdata.get("target", "")
    if not target:
        logger.warning(" Nothing expected returned, something has gone wrong... ")
        return ""

    lines = []
    for trtext in target:
        # decrypt
        try:
            _ = b64decode(rot13(trtext)).decode("utf-8")
            lines.append(_)
        except Exception as exc:
            logger.error(exc)
            raise

    return "\n".join(lines)
