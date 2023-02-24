from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from chat.models import Message

class FileUploadTest(TestCase):
    def setUp(self):
        self.msg = Message.objects.create(message="Test Message",room_id=1,sender_id=1,receiver_id=2)
        self.url = reverse('file_upload')
    
    def test_file_upload_view(self):
        file = SimpleUploadedFile("test_file.txt", b"test file contents")
        data = {
            'files': file,
            'message_id': self.msg.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.msg.file, file)
        self.assertContains(response, "File Successfully added!")