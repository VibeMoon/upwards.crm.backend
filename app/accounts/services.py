import uuid
import base64
import os
from django.core.files.base import ContentFile


class UserService:
    @staticmethod
    def decode_file(data):
        if not data:
            raise ValueError("Empty file data")
        if data.startswith('data:'):
            if ';base64,' not in data:
                raise ValueError("Invalid base64 format")

            header, imgstr = data.split(';base64,')
            if not imgstr:
                raise ValueError("Empty base64 data")

            ext = header.split('/')[-1] if '/' in header else 'png'
            filename = f"{uuid.uuid4()}.{ext}"
            try:
                decoded_data = base64.b64decode(imgstr)
                return ContentFile(decoded_data, name=filename)
            except Exception as e:
                raise ValueError(f"Invalid base64 data: {str(e)}")

        raise ValueError("Unsupported file format")
