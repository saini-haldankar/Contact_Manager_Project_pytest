import pytest

from app.database import initialize_database

from app.contacts import (
    create_contact,
    get_all_contacts,
    search_by_name,
    search_by_email,
    search_by_phone,
    update_contact,
    delete_contact,
)


@pytest.fixture
def db(tmp_path):
    db_path = tmp_path / "test_contacts.db"
    db_name = str(db_path)

    initialize_database(db_name)

    return db_name


def test_create_contact(db):
    contact_id = create_contact(
        "John Doe",
        "9876543210",
        "john@gmail.com",
        db
    )

    assert contact_id == 1

    contacts = get_all_contacts(db)

    assert len(contacts) == 1
    assert contacts[0]["name"] == "John Doe"
    assert contacts[0]["phone"] == "9876543210"
    assert contacts[0]["email"] == "john@gmail.com"


def test_search_by_name(db):
    create_contact(
        "John Doe",
        "9876543210",
        "john@gmail.com",
        db
    )

    create_contact(
        "Alice Smith",
        "9123456780",
        "alice@gmail.com",
        db
    )

    results = search_by_name("John", db)

    assert len(results) == 1
    assert results[0]["name"] == "John Doe"


def test_search_by_email(db):
    create_contact(
        "John Doe",
        "9876543210",
        "john@gmail.com",
        db
    )

    results = search_by_email(
        "john@gmail.com",
        db
    )

    assert len(results) == 1
    assert results[0]["name"] == "John Doe"


def test_search_by_phone(db):
    create_contact(
        "John Doe",
        "9876543210",
        "john@gmail.com",
        db
    )

    results = search_by_phone(
        "9876",
        db
    )

    assert len(results) == 1
    assert results[0]["name"] == "John Doe"


def test_update_contact(db):
    contact_id = create_contact(
        "John Doe",
        "9876543210",
        "john@gmail.com",
        db
    )

    updated = update_contact(
        contact_id,
        "John Smith",
        "9999999999",
        "johnsmith@gmail.com",
        db
    )

    assert updated is True

    contacts = get_all_contacts(db)

    assert contacts[0]["name"] == "John Smith"
    assert contacts[0]["phone"] == "9999999999"
    assert contacts[0]["email"] == "johnsmith@gmail.com"


def test_delete_contact(db):
    contact_id = create_contact(
        "John Doe",
        "9876543210",
        "john@gmail.com",
        db
    )

    deleted = delete_contact(
        contact_id,
        db
    )

    assert deleted is True

    contacts = get_all_contacts(db)

    assert len(contacts) == 0


def test_duplicate_phone_is_rejected(db):
    create_contact(
        "John Doe",
        "9876543210",
        "john@gmail.com",
        db
    )

    with pytest.raises(ValueError):
        create_contact(
            "Alice Smith",
            "9876543210",
            "alice@gmail.com",
            db
        )


def test_duplicate_email_is_rejected(db):
    create_contact(
        "John Doe",
        "9876543210",
        "john@gmail.com",
        db
    )

    with pytest.raises(ValueError):
        create_contact(
            "Alice Smith",
            "9123456780",
            "john@gmail.com",
            db
        )


def test_empty_name_is_rejected(db):
    with pytest.raises(ValueError):
        create_contact(
            "",
            "9876543210",
            "john@gmail.com",
            db
        )


def test_empty_phone_is_rejected(db):
    with pytest.raises(ValueError):
        create_contact(
            "John Doe",
            "",
            "john@gmail.com",
            db
        )


def test_empty_email_is_rejected(db):
    with pytest.raises(ValueError):
        create_contact(
            "John Doe",
            "9876543210",
            "",
            db
        )


def test_invalid_phone_rejected(db):
    with pytest.raises(
        ValueError,
        match="only digits"
    ):
        create_contact(
            "John Doe",
            "abc123",
            "john@gmail.com",
            db
        )


def test_short_phone_rejected(db):
    with pytest.raises(
        ValueError,
        match="at least 10 digits"
    ):
        create_contact(
            "John Doe",
            "12345",
            "john@gmail.com",
            db
        )


def test_invalid_email_rejected(db):
    with pytest.raises(
        ValueError,
        match="Invalid email"
    ):
        create_contact(
            "John Doe",
            "9876543210",
            "invalid-email",
            db
        )
