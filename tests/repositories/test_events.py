"""
Unit tests for event repository functions.

These tests verify the behavior of repository functions in isolation,
focusing on database operations and data transformations.
"""
import pytest
from datetime import date, time
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.events import (
    create_event,
    get_event_by_id,
    get_all_events,
    update_event,
    delete_event,
)
from app.schemas.event import EventCreate, EventUpdate
from app.models.event import Event
from app.models.user import User


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_event_success(test_db: AsyncSession, admin_user: User):
    """Test successful event creation."""
    # Arrange
    event_data = EventCreate(
        title="Test Event",
        description="Test Description",
        date=date(2026, 2, 15),
        start_time=time(14, 0),
        end_time=time(16, 0),
        image_url="https://example.com/image.jpg",
        location="Test Location",
    )
    
    # Act
    event = await create_event(test_db, event_data, admin_user.id)
    
    # Assert
    assert event.id is not None
    assert event.title == "Test Event"
    assert event.description == "Test Description"
    assert event.creator_id == admin_user.id
    assert event.speakers == []  # No speakers initially


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_event_by_id_success(test_db: AsyncSession, admin_user: User):
    """Test retrieving an event by ID."""
    # Arrange - Create an event first
    event_data = EventCreate(
        title="Test Event",
        description="Test Description",
        date=date(2026, 2, 15),
        start_time=time(14, 0),
        end_time=time(16, 0),
    )
    created_event = await create_event(test_db, event_data, admin_user.id)
    
    # Act
    retrieved_event = await get_event_by_id(test_db, created_event.id)
    
    # Assert
    assert retrieved_event is not None
    assert retrieved_event.id == created_event.id
    assert retrieved_event.title == "Test Event"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_event_by_id_not_found(test_db: AsyncSession):
    """Test retrieving a non-existent event returns None."""
    # Arrange
    non_existent_id = uuid4()
    
    # Act
    event = await get_event_by_id(test_db, non_existent_id)
    
    # Assert
    assert event is None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_all_events(test_db: AsyncSession, admin_user: User):
    """Test retrieving all events."""
    # Arrange - Create multiple events
    event_data_1 = EventCreate(
        title="Event 1",
        date=date(2026, 2, 15),
        start_time=time(14, 0),
        end_time=time(16, 0),
    )
    event_data_2 = EventCreate(
        title="Event 2",
        date=date(2026, 3, 20),
        start_time=time(10, 0),
        end_time=time(12, 0),
    )
    
    await create_event(test_db, event_data_1, admin_user.id)
    await create_event(test_db, event_data_2, admin_user.id)
    
    # Act
    events = await get_all_events(test_db)
    
    # Assert
    assert len(events) == 2
    assert events[0].title in ["Event 1", "Event 2"]
    assert events[1].title in ["Event 1", "Event 2"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_event_success(test_db: AsyncSession, admin_user: User):
    """Test updating an event."""
    # Arrange - Create an event first
    event_data = EventCreate(
        title="Original Title",
        description="Original Description",
        date=date(2026, 2, 15),
        start_time=time(14, 0),
        end_time=time(16, 0),
    )
    event = await create_event(test_db, event_data, admin_user.id)
    
    # Act - Update the event
    update_data = EventUpdate(
        title="Updated Title",
        description="Updated Description",
    )
    updated_event = await update_event(test_db, event, update_data)
    
    # Assert
    assert updated_event.title == "Updated Title"
    assert updated_event.description == "Updated Description"
    assert updated_event.date == date(2026, 2, 15)  # Unchanged


@pytest.mark.unit
@pytest.mark.asyncio
async def test_update_event_skip_none_values(test_db: AsyncSession, admin_user: User):
    """Test that None values are skipped during update."""
    # Arrange - Create an event
    event_data = EventCreate(
        title="Original Title",
        description="Original Description",
        date=date(2026, 2, 15),
        start_time=time(14, 0),
        end_time=time(16, 0),
    )
    event = await create_event(test_db, event_data, admin_user.id)
    
    # Act - Update with None values
    update_data = EventUpdate(
        title="Updated Title",
        description=None,  # Should be skipped
        date=None,  # Should be skipped
    )
    updated_event = await update_event(test_db, event, update_data)
    
    # Assert
    assert updated_event.title == "Updated Title"
    assert updated_event.description == "Original Description"  # Unchanged
    assert updated_event.date == date(2026, 2, 15)  # Unchanged


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delete_event_success(test_db: AsyncSession, admin_user: User):
    """Test deleting an event."""
    # Arrange - Create an event
    event_data = EventCreate(
        title="Event to Delete",
        date=date(2026, 2, 15),
        start_time=time(14, 0),
        end_time=time(16, 0),
    )
    event = await create_event(test_db, event_data, admin_user.id)
    event_id = event.id
    
    # Act - Delete the event
    await delete_event(test_db, event)
    
    # Assert - Event should no longer exist
    deleted_event = await get_event_by_id(test_db, event_id)
    assert deleted_event is None
