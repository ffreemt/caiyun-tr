"""Define caiyun_tr."""
# pylint: disable=invalid-name, too-many-branches, too-many-statements
from base64 import b64decode
from codecs import encode
from hashlib import md5
from typing import Optional

import httpx
from logzero import logger

url_jwt = "https://api.interpreter.caiyunai.com/v1/user/jwt/generate"
url = "https://api.interpreter.caiyunai.com/v1/translator"

browser_id = md5(b"").hexdigest()
jwt_dict = {}  # for reuse, sort of global jwt
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


def fetch_jwt() -> str:
    """Fetch jwt."""
    # browser_id = md5(b"").hexdigest()

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

    return jwt


def caiyun_tr(
    # text: str, jwt: str, brower_id: str, from_lang: str = "en", to_lang: str = "zh"
    text: str,
    from_lang: str = "en",
    to_lang: str = "zh",
    jwt: Optional[str] = None,
) -> str:
    """Define caiyun_tr.

    Args:
        text: to be translated
        from_lang: source language
        to_lang: destination language
        jwt: fetch new jwt if None, use it if provided.

    Returns:
        translation text, para info preserved
    """
    global jwt_dict  # pylint: disable=global-statement

    # first run: fetch_jwt
    if not jwt_dict.get("jwt"):
        jwt_dict = {"jwt": fetch_jwt()}
    if jwt is None:  # default to global jwt
        jwt = jwt_dict.get("jwt")

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
        "browser_id": browser_id,
    }

    _ = """  # Token expired
    {'http_code': 200,
    'message': 'Token expired',
    'err_code': None,
    'details': None,
    'auth_code': -3}
    """
    # update jwt when expired
    for _ in range(2):
        try:
            resp = httpx.post(url, json=data, headers=headers1)
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

        if "expired" in jdata.get(
            "message", ""
        ):  # update jwt/headers1 for next run and jwt_dict for possible next session
            logger.info("jwt expired, fetching a new jwt and try again")
            try:
                jwt = fetch_jwt()
            except Exception as exc:
                logger.error("Upable to fetch jwt: %s", exc)
                raise
            jwt_dict = {"jwt": jwt}
            headers1 = dict(**headers, **{"T-Authorization": jwt})
        else:
            # all is well, out of the loop
            break

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
            _ = b64decode(rot13(trtext)).decode("utf-8")
            lines.append(_)
        except Exception as exc:
            logger.error(exc)
            raise

    return "\n".join(lines)


_ = '''
def caiyun_fixed_jwt(text: str, jwt: Optional[str] = None, fron_lang: str = "zn", to_lang: str = "zh") -> str:
    """Translate via caiyun.

    """
    if jwt is None:
        jwt = fetch_jwt()
# '''
