from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient, APITestCase

client = APIClient()


class TweetsTests(APITestCase):
    def test_success_call_without_limit(self):
        url = '/hashtags/lovepakistan'
        response = self.client.get(url)
        assert response.status_code == 200
        print(len(response.data))
        assert len(response.data) == 30

    def test_success_call_with_limit(self):
        url = '/hashtags/lovepakistan?limit=10'
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 10

    def test_invalid_hashtag(self):
        url = '/hashtags/iksbuwtsdkags'
        response = self.client.get(url)
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_success_call_with_max_limit(self):
        url = '/hashtags/lovepakistan?limit=51'
        response = self.client.get(url)
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_success_call_with_min_limit(self):
        url = '/hashtags/lovepakistan?limit=0'
        response = self.client.get(url)
        assert response.status_code == HTTP_204_NO_CONTENT

    def test_negative_integer_limit(self):
        url = '/hashtags/lovepakistan?limit=-1'
        response = self.client.get(url)
        assert response.status_code == HTTP_400_BAD_REQUEST
