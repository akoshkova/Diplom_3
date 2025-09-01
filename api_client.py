import requests


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    self.session = requests.Session()

    def create_user(self, user_data):
        return self.session.post(f"{self.base_url}/api/auth/register", json=user_data)

    def delete_user(self, access_token):
        return self.session.delete(
            f"{self.base_url}/api/auth/user",
            headers={'Authorization': f'Bearer {access_token}'}
        )
