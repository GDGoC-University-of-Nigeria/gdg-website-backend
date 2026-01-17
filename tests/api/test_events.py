"""
Integration tests for event API endpoints.

These tests verify the end-to-end behavior of the events API,
including authentication, authorization, validation, and database interactions.
"""
import pytest
from httpx import AsyncClient
from datetime import date

from app.models.user import User


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_event_as_admin(
    test_client: AsyncClient,
    admin_headers: dict,
    sample_event_data: dict,
):
    """Test that an admin can create an event."""
    # Act
    response = await test_client.post(
        "/events/",
        json=sample_event_data,
        headers=admin_headers,
    )
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_event_data["title"]
    assert data["description"] == sample_event_data["description"]
    assert "id" in data
    assert "created_at" in data
    assert data["speakers"] == []


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_event_unauthorized(
    test_client: AsyncClient,
    sample_event_data: dict,
):
    """Test that creating an event without authentication fails."""
    # Act
    response = await test_client.post(
        "/events/",
        json=sample_event_data,
    )
    
    # Assert
    assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_event_as_non_admin(
    test_client: AsyncClient,
    regular_user_headers: dict,
    sample_event_data: dict,
):
    """Test that a non-admin user cannot create an event."""
    # Act
    response = await test_client.post(
        "/events/",
        json=sample_event_data,
        headers=regular_user_headers,
    )
    
    # Assert
    assert response.status_code == 403


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_event_missing_required_fields(
    test_client: AsyncClient,
    admin_headers: dict,
):
    """Test that creating an event with missing required fields fails."""
    # Arrange - Missing date and times
    invalid_data = {
        "title": "Test Event",
        "description": "Test Description",
    }
    
    # Act
    response = await test_client.post(
        "/events/",
        json=invalid_data,
        headers=admin_headers,
    )
    
    # Assert
    assert response.status_code == 422


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_all_events(
    test_client: AsyncClient,
    admin_headers: dict,
    sample_event_data: dict,
):
    """Test retrieving all events."""
    # Arrange - Create an event first
    await test_client.post(
        "/events/",
        json=sample_event_data,
        headers=admin_headers,
    )
    
    # Act
    response = await test_client.get("/events/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["title"] == sample_event_data["title"]
    assert "speakers" in data[0]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_event_by_id(
    test_client: AsyncClient,
    admin_headers: dict,
    sample_event_data: dict,
):
    """Test retrieving a specific event by ID."""
    # Arrange - Create an event first
    create_response = await test_client.post(
        "/events/",
        json=sample_event_data,
        headers=admin_headers,
    )
    event_id = create_response.json()["id"]
    
    # Act
    response = await test_client.get(f"/events/{event_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == event_id
    assert data["title"] == sample_event_data["title"]
    assert "speakers" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_event_by_id_not_found(test_client: AsyncClient):
    """Test retrieving a non-existent event returns 404."""
    # Arrange
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    
    # Act
    response = await test_client.get(f"/events/{non_existent_id}")
    
    # Assert
    assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_event_as_admin(
    test_client: AsyncClient,
    admin_headers: dict,
    sample_event_data: dict,
    sample_event_update_data: dict,
):
    """Test that an admin can update an event."""
    # Arrange - Create an event first
    create_response = await test_client.post(
        "/events/",
        json=sample_event_data,
        headers=admin_headers,
    )
    event_id = create_response.json()["id"]
    
    # Act
    response = await test_client.put(
        f"/events/{event_id}",
        json=sample_event_update_data,
        headers=admin_headers,
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == sample_event_update_data["title"]
    assert data["description"] == sample_event_update_data["description"]
    assert data["date"] == sample_event_data["date"]  # Unchanged


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_event_with_null_date(
    test_client: AsyncClient,
    admin_headers: dict,
    sample_event_data: dict,
):
    """Test that updating an event with null date doesn't change the date."""
    # Arrange - Create an event first
    create_response = await test_client.post(
        "/events/",
        json=sample_event_data,
        headers=admin_headers,
    )
    event_id = create_response.json()["id"]
    original_date = create_response.json()["date"]
    
    # Act - Update with null date
    update_data = {
        "title": "Updated Title",
        "date": None,
    }
    response = await test_client.put(
        f"/events/{event_id}",
        json=update_data,
        headers=admin_headers,
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["date"] == original_date  # Date should remain unchanged


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_event_unauthorized(
    test_client: AsyncClient,
    admin_headers: dict,
    sample_event_data: dict,
):
    """Test that updating an event without authentication fails."""
    # Arrange - Create an event first
    create_response = await test_client.post(
        "/events/",
        json=sample_event_data,
        headers=admin_headers,
    )
    event_id = create_response.json()["id"]
    
    # Act
    response = await test_client.put(
        f"/events/{event_id}",
        json={"title": "Updated Title"},
    )
    
    # Assert
    assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_event_as_admin(
    test_client: AsyncClient,
    admin_headers: dict,
    sample_event_data: dict,
):
    """Test that an admin can delete an event."""
    # Arrange - Create an event first
    create_response = await test_client.post(
        "/events/",
        json=sample_event_data,
        headers=admin_headers,
    )
    event_id = create_response.json()["id"]
    
    # Act
    response = await test_client.delete(
        f"/events/{event_id}",
        headers=admin_headers,
    )
    
    # Assert
    assert response.status_code == 204
    
    # Verify event is deleted
    get_response = await test_client.get(f"/events/{event_id}")
    assert get_response.status_code == 404


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_event_not_found(
    test_client: AsyncClient,
    admin_headers: dict,
):
    """Test deleting a non-existent event returns 404."""
    # Arrange
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    
    # Act
    response = await test_client.delete(
        f"/events/{non_existent_id}",
        headers=admin_headers,
    )
    
    # Assert
    assert response.status_code == 404


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_event_unauthorized(
    test_client: AsyncClient,
    admin_headers: dict,
    sample_event_data: dict,
):
    """Test that deleting an event without authentication fails."""
    # Arrange - Create an event first
    create_response = await test_client.post(
        "/events/",
        json=sample_event_data,
        headers=admin_headers,
    )
    event_id = create_response.json()["id"]
    
    # Act
    response = await test_client.delete(f"/events/{event_id}")
    
    # Assert
    assert response.status_code == 401
