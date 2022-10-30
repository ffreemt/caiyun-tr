# caiyun-tr
[![pytest](https://github.com/ffreemt/caiyun-tr/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/caiyun-tr/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/caiyun_tr.svg)](https://badge.fury.io/py/caiyun_tr)

caiyun-tr

## Install it

```shell
pip install caiyun-tr --upgrade

# pip install git+https://github.com/ffreemt/caiyun-tr
# poetry add git+https://github.com/ffreemt/caiyun-tr
# git clone https://github.com/ffreemt/caiyun-tr && cd caiyun-tr
```

## Use it
```python
from caiyun_tr import caiyun_tr

print(caiyun_tr("test this"))
# 试试这个

# only certain pairs are valid, en/ja is not valid
print(caiyun_tr("test this", from_lang="en", to_lang="ja"))
# Exception: Unsupported trans_type (language pair)

# zh/ja is valid
print(caiyun_tr("test this", from_lang="zh", to_lang="ja"))
# テストして

print(caiyun_tr("テストして", 'ja', "zh"))
# 测试一下
```

Only certain from_lang/to_lang pairs are supported by the website. There is nothing we can do about it.

If the caiyun website changes, this package will likely no longer work. If you feedback, the dev will try to fix it -- there is no guarantee thou. 