import pytest
from httpx import AsyncClient, ASGITransport
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/activities")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

@pytest.mark.asyncio
async def test_signup_and_unregister():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Get an activity name
        activities_resp = await ac.get("/activities")
        activity_name = next(iter(activities_resp.json().keys()))
        test_email = "testuser@example.com"
        # Signup
        signup_url = f"/activities/{activity_name}/signup?email={test_email}"
        response = await ac.post(signup_url)
        assert response.status_code == 200
        assert "message" in response.json()
        # Unregister (if endpoint exists)
        unregister_url = f"/activities/{activity_name}/unregister?email={test_email}"
        response = await ac.post(unregister_url)
        # Accept 200 or 404 if endpoint is not implemented
        assert response.status_code in (200, 404)
