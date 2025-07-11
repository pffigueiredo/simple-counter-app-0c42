from datetime import datetime
from app.database import get_session
from app.models import Counter


def get_counter() -> Counter:
    """Get the current counter value from database. Creates a new counter if none exists."""
    with get_session() as session:
        counter = session.query(Counter).first()
        if counter is None:
            counter = Counter(value=0)
            session.add(counter)
            session.commit()
            session.refresh(counter)
        return counter


def increment_counter() -> Counter:
    """Increment the counter value by 1 and return the updated counter."""
    with get_session() as session:
        counter = session.query(Counter).first()
        if counter is None:
            counter = Counter(value=1)
            session.add(counter)
        else:
            counter.value += 1
            counter.updated_at = datetime.utcnow()

        session.commit()
        session.refresh(counter)
        return counter


def reset_counter() -> Counter:
    """Reset the counter value to 0 and return the updated counter."""
    with get_session() as session:
        counter = session.query(Counter).first()
        if counter is None:
            counter = Counter(value=0)
            session.add(counter)
        else:
            counter.value = 0
            counter.updated_at = datetime.utcnow()

        session.commit()
        session.refresh(counter)
        return counter
