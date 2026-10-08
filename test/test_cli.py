from app.database import initialize_database
from app.contacts import create_contact, get_all_contacts

from app.cli import (
    create_contact_cli,
    delete_contact_cli,
    search_contact_cli,
    update_contact_cli,
)


def test_create_contact_cli(tmp_path, monkeypatch, capsys):
    db_path = tmp_path / "test_contacts.db"
    db_name = str(db_path)

    initialize_database(db_name)

    inputs = iter([
        "Alice Smith",
        "9876543210",
        "alice@gmail.com",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    from app import cli

    original_create_contact = cli.create_contact

    def create_test_contact(name, phone, email):
        return original_create_contact(
            name,
            phone,
            email,
            db_name
        )

    monkeypatch.setattr(
        cli,
        "create_contact",
        create_test_contact
    )

    create_contact_cli()

    output = capsys.readouterr().out

    assert "Contact created successfully!" in output
    assert "Contact ID: 1" in output


def test_delete_contact_cli(tmp_path, monkeypatch, capsys):
    db_path = tmp_path / "test_contacts.db"
    db_name = str(db_path)

    initialize_database(db_name)

    contact_id = create_contact(
        "John Doe",
        "9876543210",
        "john@gmail.com",
        db_name
    )

    from app import cli

    original_delete_contact = cli.delete_contact

    def delete_test_contact(contact_id):
        return original_delete_contact(
            contact_id,
            db_name
        )

    monkeypatch.setattr(
        cli,
        "delete_contact",
        delete_test_contact
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: str(contact_id)
    )

    delete_contact_cli()

    output = capsys.readouterr().out

    assert "Contact deleted successfully!" in output

    contacts = get_all_contacts(db_name)

    assert len(contacts) == 0


def test_search_by_name_cli(tmp_path, monkeypatch, capsys):
    db_path = tmp_path / "test_contacts.db"
    db_name = str(db_path)

    initialize_database(db_name)

    create_contact(
        "Alice Smith",
        "9876543210",
        "alice@gmail.com",
        db_name
    )

    from app import cli

    original_search = cli.search_by_name

    def search_test(value):
        return original_search(value, db_name)

    monkeypatch.setattr(
        cli,
        "search_by_name",
        search_test
    )

    inputs = iter([
        "1",
        "Alice"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    search_contact_cli()

    output = capsys.readouterr().out

    assert "Alice Smith" in output
    assert "9876543210" in output
    assert "alice@gmail.com" in output


def test_search_by_email_cli(tmp_path, monkeypatch, capsys):
    db_path = tmp_path / "test_contacts.db"
    db_name = str(db_path)

    initialize_database(db_name)

    create_contact(
        "Alice Smith",
        "9876543210",
        "alice@gmail.com",
        db_name
    )

    from app import cli

    original_search = cli.search_by_email

    def search_test(value):
        return original_search(value, db_name)

    monkeypatch.setattr(
        cli,
        "search_by_email",
        search_test
    )

    inputs = iter([
        "2",
        "alice@gmail.com"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    search_contact_cli()

    output = capsys.readouterr().out

    assert "Alice Smith" in output
    assert "alice@gmail.com" in output


def test_search_by_phone_cli(tmp_path, monkeypatch, capsys):
    db_path = tmp_path / "test_contacts.db"
    db_name = str(db_path)

    initialize_database(db_name)

    create_contact(
        "Alice Smith",
        "9876543210",
        "alice@gmail.com",
        db_name
    )

    from app import cli

    original_search = cli.search_by_phone

    def search_test(value):
        return original_search(value, db_name)

    monkeypatch.setattr(
        cli,
        "search_by_phone",
        search_test
    )

    inputs = iter([
        "3",
        "9876"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    search_contact_cli()

    output = capsys.readouterr().out

    assert "Alice Smith" in output
    assert "9876543210" in output


def test_update_contact_cli(tmp_path, monkeypatch, capsys):
    db_path = tmp_path / "test_contacts.db"
    db_name = str(db_path)

    initialize_database(db_name)

    contact_id = create_contact(
        "John Doe",
        "9876543210",
        "john@gmail.com",
        db_name
    )

    from app import cli

    original_update = cli.update_contact

    def update_test_contact(
        contact_id,
        name,
        phone,
        email
    ):
        return original_update(
            contact_id,
            name,
            phone,
            email,
            db_name
        )

    monkeypatch.setattr(
        cli,
        "update_contact",
        update_test_contact
    )

    inputs = iter([
        str(contact_id),
        "John Smith",
        "9999999999",
        "johnsmith@gmail.com",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    update_contact_cli()

    output = capsys.readouterr().out

    assert "Contact updated successfully!" in output

    contacts = get_all_contacts(db_name)

    assert contacts[0]["name"] == "John Smith"
    assert contacts[0]["phone"] == "9999999999"
    assert contacts[0]["email"] == "johnsmith@gmail.com"
