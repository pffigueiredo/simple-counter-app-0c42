import pytest
from app.counter_service import get_counter, increment_counter, reset_counter
from app.database import reset_db


@pytest.fixture()
def new_db():
    reset_db()
    yield
    reset_db()


def test_get_counter_creates_new_when_none_exists(new_db):
    """Test that get_counter creates a new counter with value 0 when none exists"""
    counter = get_counter()
    assert counter.value == 0
    assert counter.id is not None


def test_get_counter_returns_existing_counter(new_db):
    """Test that get_counter returns existing counter"""
    # Create initial counter
    first_counter = get_counter()
    first_counter_id = first_counter.id

    # Get counter again
    second_counter = get_counter()

    assert second_counter.id == first_counter_id
    assert second_counter.value == 0


def test_increment_counter_creates_new_with_value_1(new_db):
    """Test that increment_counter creates new counter with value 1 when none exists"""
    counter = increment_counter()
    assert counter.value == 1
    assert counter.id is not None


def test_increment_counter_increments_existing_counter(new_db):
    """Test that increment_counter increments existing counter value"""
    # Create initial counter
    initial_counter = get_counter()
    assert initial_counter.value == 0

    # Increment counter
    incremented_counter = increment_counter()
    assert incremented_counter.value == 1

    # Increment again
    incremented_again = increment_counter()
    assert incremented_again.value == 2


def test_increment_counter_multiple_times(new_db):
    """Test incrementing counter multiple times"""
    for expected_value in range(1, 6):
        counter = increment_counter()
        assert counter.value == expected_value


def test_reset_counter_creates_new_with_value_0(new_db):
    """Test that reset_counter creates new counter with value 0 when none exists"""
    counter = reset_counter()
    assert counter.value == 0
    assert counter.id is not None


def test_reset_counter_resets_existing_counter(new_db):
    """Test that reset_counter resets existing counter to 0"""
    # Increment counter to non-zero value
    increment_counter()
    increment_counter()
    incremented_counter = increment_counter()
    assert incremented_counter.value == 3

    # Reset counter
    reset_counter_result = reset_counter()
    assert reset_counter_result.value == 0

    # Verify counter is still reset
    current_counter = get_counter()
    assert current_counter.value == 0


def test_counter_persistence_after_operations(new_db):
    """Test that counter value persists after various operations"""
    # Initial state
    counter = get_counter()
    assert counter.value == 0

    # Increment and verify persistence
    increment_counter()
    counter = get_counter()
    assert counter.value == 1

    # Increment more and verify
    increment_counter()
    increment_counter()
    counter = get_counter()
    assert counter.value == 3

    # Reset and verify
    reset_counter()
    counter = get_counter()
    assert counter.value == 0


def test_counter_updated_at_changes_on_increment(new_db):
    """Test that updated_at timestamp changes when counter is incremented"""
    # Create initial counter
    initial_counter = get_counter()
    initial_updated_at = initial_counter.updated_at

    # Increment counter
    incremented_counter = increment_counter()

    # Check that updated_at has changed
    assert incremented_counter.updated_at > initial_updated_at


def test_counter_updated_at_changes_on_reset(new_db):
    """Test that updated_at timestamp changes when counter is reset"""
    # Create and increment counter
    increment_counter()
    incremented_counter = get_counter()
    incremented_updated_at = incremented_counter.updated_at

    # Reset counter
    reset_counter_result = reset_counter()

    # Check that updated_at has changed
    assert reset_counter_result.updated_at > incremented_updated_at


def test_counter_id_remains_same_across_operations(new_db):
    """Test that counter ID remains the same across different operations"""
    # Create initial counter
    initial_counter = get_counter()
    initial_id = initial_counter.id

    # Increment counter
    incremented_counter = increment_counter()
    assert incremented_counter.id == initial_id

    # Reset counter
    reset_counter_result = reset_counter()
    assert reset_counter_result.id == initial_id

    # Get counter again
    final_counter = get_counter()
    assert final_counter.id == initial_id
