import os
import uuid
from django.core.files.storage import Storage
from google.cloud import storage
from django.conf import settings
from django.core.files.base import ContentFile


class FirebaseStorage(Storage):
    def __init__(self):
        self.client = storage.Client.from_service_account_json(
            os.path.join(settings.BASE_DIR,
                         'firebase-credentials.json')
        )
        self.bucket = self.client.get_bucket('twitter-clone-6df96.appspot.com')

    def _generate_unique_name(self, name):
        extension = os.path.splitext(name)[1]
        return f'{uuid.uuid4().hex}{extension}'

    def _open(self, name, mode='rb'):
        blob = self.bucket.blob(name)
        content = blob.download_as_bytes()
        return ContentFile(content)

    def _save(self, name, content):
        unique_name = self._generate_unique_name(name)
        blob = self.bucket.blob(unique_name)
        blob.upload_from_string(content.read(), content.content_type)
        return unique_name

    def exists(self, name):
        blob = self.bucket.blob(name)
        return blob.exists()

    def url(self, name):
        blob = self.bucket.blob(name)
        return blob.public_url

    def delete(self, name):
        blob = self.bucket.blob(name)
        blob.delete()

    def size(self, name):
        blob = self.bucket.blob(name)
        return blob.size
