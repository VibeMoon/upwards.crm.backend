import uuid
import base64
import os
from django.core.files.base import ContentFile


class UserService:

    @staticmethod
    def decode_file(data):
        if isinstance(data, dict):
            data = data["file"]

        if data.startswith('data:'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            return ContentFile(base64.b64decode(imgstr), name=filename)
        else:
            with open(data, 'rb') as f:
                file_content = f.read()
            return ContentFile(file_content, name=os.path.basename(data))
