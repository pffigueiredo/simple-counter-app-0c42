import pytest
from nicegui.testing import User
from app.database import reset_db


@pytest.fixture()
def new_db():
    reset_db()
    yield
    reset_db()


async def test_counter_page_displays_initial_value(user: User, new_db) -> None:
    """Test that counter page displays initial value of 0"""
    await user.open("/counter")

    # Check that page loads with counter value 0
    await user.should_see("Counter App")
    await user.should_see("0")  # Initial counter value


async def test_counter_increment_button_works(user: User, new_db) -> None:
    """Test that increment button increases counter value"""
    await user.open("/counter")

    # Initial value should be 0
    await user.should_see("0")

    # Click increment button
    user.find("Increment").click()

    # Should see value 1
    await user.should_see("1")

    # Click increment button again
    user.find("Increment").click()

    # Should see value 2
    await user.should_see("2")


async def test_counter_reset_button_works(user: User, new_db) -> None:
    """Test that reset button resets counter to 0"""
    await user.open("/counter")

    # Increment counter a few times
    user.find("Increment").click()
    user.find("Increment").click()
    user.find("Increment").click()

    # Should see value 3
    await user.should_see("3")

    # Click reset button
    user.find("Reset").click()

    # Should see value 0
    await user.should_see("0")


async def test_counter_persistence_across_page_loads(user: User, new_db) -> None:
    """Test that counter value persists when page is reloaded"""
    await user.open("/counter")

    # Increment counter
    user.find("Increment").click()
    user.find("Increment").click()

    # Should see value 2
    await user.should_see("2")

    # Reload page
    await user.open("/counter")

    # Should still see value 2
    await user.should_see("2")


async def test_home_page_navigation_to_counter(user: User, new_db) -> None:
    """Test navigation from home page to counter page"""
    await user.open("/")

    # Should see welcome message
    await user.should_see("Welcome to Counter App")

    # Click button to open counter
    user.find("Open Counter").click()

    # Should navigate to counter page
    await user.should_see("Counter App")
    await user.should_see("0")  # Initial counter value


async def test_counter_page_has_proper_ui_elements(user: User, new_db) -> None:
    """Test that counter page has all expected UI elements"""
    await user.open("/counter")

    # Check for main elements
    await user.should_see("Counter App")
    await user.should_see("0")  # Counter value
    await user.should_see("Increment")
    await user.should_see("Reset")
    await user.should_see("The counter value is automatically saved to the database")


async def test_multiple_increments_and_reset_cycle(user: User, new_db) -> None:
    """Test multiple increment and reset operations"""
    await user.open("/counter")

    # Test multiple increments
    for i in range(1, 6):
        user.find("Increment").click()
        await user.should_see(str(i))

    # Reset
    user.find("Reset").click()
    await user.should_see("0")

    # Increment again after reset
    user.find("Increment").click()
    await user.should_see("1")
