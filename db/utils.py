from typing import Any, Union, Dict, List

import requests
from sqlalchemy import Dialect
from sqlalchemy_file import ImageField


def upload_file(img_bytes):
    url = 'https://telegra.ph/upload'
    response = requests.post(url, files={'file': img_bytes})
    if response.status_code == 200:
        return "https://telegra.ph" + response.json()[0]['src']
    print(f"Error uploading file: {response.status_code}")
    return


class CustomImageField(ImageField):
    def process_bind_param(self, value: Any, dialect: Dialect) -> Union[None, Dict[str, Any], List[Dict[str, Any]]]:
        data = {
            'file_name': upload_file(value.file)
        }
        value.update(data)
        return super().process_bind_param(value, dialect)
