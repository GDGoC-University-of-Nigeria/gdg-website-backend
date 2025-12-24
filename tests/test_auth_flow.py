
import pytest
from unittest.mock import patch
from httpx import AsyncClient, ASGITransport
from app.main import app

import uuid

# Mock Google Auth response
random_id = str(uuid.uuid4())[:8]
mock_google_user = {
    "email": f"testuser_{random_id}@gmail.com",
    "sub": "1234567890",
    "name": "Test User",
    "picture": "https://example.com/avatar.jpg"
}

@pytest.fixture
def mock_verify_token():
    with patch("app.api.auth.id_token.verify_oauth2_token") as mock:
        mock.return_value = mock_google_user
        yield mock

@pytest.mark.asyncio
async def test_google_auth_flow(mock_verify_token):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Login/Signup with Google
        response = await client.post("/auth/google", json={"id_token": "fake_token_123"})
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert data["user"]["email"] == mock_google_user["email"]
        assert data["profile_complete"] is False
        
        access_token = data["access_token"]
        
        # 2. Complete Profile
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_data = {
            "full_name": "Updated Test User",
            "role": "Backend Developer",
            "skills": ["Python", "FastAPI"]
        }
        
        response = await client.post("/users/complete-profile", json=profile_data, headers=headers)
        assert response.status_code == 200
        user_data = response.json()
        
        assert user_data["full_name"] == "Updated Test User"
        assert user_data["role"] == "Backend Developer"
        assert "Python" in user_data["skills"]
        assert user_data["profile_complete"] is True
        
        # 3. Verify Login again (Should show profile complete)
        response = await client.post("/auth/google", json={"id_token": "fake_token_123"})
        assert response.status_code == 200
        data = response.json()
        assert data["profile_complete"] is True
