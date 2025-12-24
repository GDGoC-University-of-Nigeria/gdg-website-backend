import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

class TestGoogleAuthFlow(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.mock_google_user = {
            "email": "testuser@gmail.com",
            "sub": "1234567890",
            "name": "Test User",
            "picture": "https://example.com/avatar.jpg"
        }

    @patch("app.api.auth.id_token.verify_oauth2_token")
    def test_auth_flow(self, mock_verify):
        mock_verify.return_value = self.mock_google_user
        
        # 1. Login/Signup
        print("Testing /auth/google...")
        response = self.client.post("/auth/google", json={"id_token": "fake_token_123"})
        
        if response.status_code != 200:
            print(f"Auth failed: {response.text}")
            
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("access_token", data)
        self.assertEqual(data["user"]["email"], self.mock_google_user["email"])
        # self.assertFalse(data["profile_complete"]) # Might be true if prev run succeeded?
        # Since we use a real DB (via app), if previous runs (even failed ones that inserted) happened, this user might exist.
        
        access_token = data["access_token"]
        
        # 2. Complete Profile
        print("Testing /users/complete-profile...")
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_data = {
            "full_name": "Updated Test User",
            "role": "Backend Developer",
            "skills": ["Python", "FastAPI"]
        }
        
        response = self.client.post("/users/complete-profile", json=profile_data, headers=headers)
        
        if response.status_code != 200:
            print(f"Profile completion failed: {response.text}")

        self.assertEqual(response.status_code, 200)
        user_data = response.json()
        
        self.assertEqual(user_data["full_name"], "Updated Test User")
        self.assertTrue(user_data["profile_complete"])
        
        print("Verification Successful!")

if __name__ == "__main__":
    unittest.main()
