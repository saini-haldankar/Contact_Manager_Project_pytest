"""Contact management module.

Provides functions for creating, retrieving, searching,
updating, and deleting contacts using an SQLite database.
"""

import re
import sqlite3

from app.database import get_connection


def validate_email(email):
    """Validate an email address.

    :param email: Email address to validate.
    :raises ValueError: If the email address is invalid.
    """

    # Define a basic email validation pattern.
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    # Check whether the email matches the pattern.
    if not re.match(pattern, email):
        raise ValueError("Invalid email address.")


def validate_phone(phone):
    """Validate a phone number.

    The phone number must contain only digits and
    must contain at least 10 digits.

    :param phone: Phone number to validate.
    :raises ValueError: If the phone number is invalid.
    """

    # Check that the phone number contains only digits.
    if not phone.isdigit():
        raise ValueError("Phone number must contain only digits.")

    # Check that the phone number has at least 10 digits.
    if len(phone) < 10:
        raise ValueError("Phone number must contain at least 10 digits.")


def create_contact(name, phone, email, db_name="contacts.db"):
    """Create a new contact.

    Validates the contact information and stores the contact
    in the SQLite database.

    :param name: Name of the contact.
    :param phone: Phone number of the contact.
    :param email: Email address of the contact.
    :param db_name: Name of the SQLite database.
    :return: ID of the newly created contact.
    :raises ValueError: If any field is empty or invalid, or if
        the phone number or email already exists.
    """

    # Remove unnecessary spaces from the input values.
    name = name.strip()
    phone = phone.strip()
    email = email.strip()

    # Check that the name is not empty.
    if not name:
        raise ValueError("Name cannot be empty.")

    # Check that the phone number is not empty.
    if not phone:
        raise ValueError("Phone cannot be empty.")

    # Check that the email address is not empty.
    if not email:
        raise ValueError("Email cannot be empty.")

    # Validate the phone number and email address.
    validate_phone(phone)
    validate_email(email)

    # Open a connection to the database.
    connection = get_connection(db_name)

    try:
        # Insert the new contact into the database.
        cursor = connection.execute(
            """
            INSERT INTO contacts (name, phone, email)
            VALUES (?, ?, ?)
            """,
            (name, phone, email)
        )

        # Save the changes to the database.
        connection.commit()

        # Return the ID of the newly created contact.
        return cursor.lastrowid

    except sqlite3.IntegrityError:
        # Handle duplicate phone numbers or email addresses.
        raise ValueError(
            "Phone number or email already exists."
        )

    finally:
        # Always close the database connection.
        connection.close()


def get_all_contacts(db_name="contacts.db"):
    """Retrieve all contacts from the database.

    Contacts are returned in ascending order by their ID.

    :param db_name: Name of the SQLite database.
    :return: List of contacts represented as dictionaries.
    """

    # Open a connection to the database.
    connection = get_connection(db_name)

    # Retrieve all contacts ordered by ID.
    contacts = connection.execute(
        """
        SELECT id, name, phone, email
        FROM contacts
        ORDER BY id
        """
    ).fetchall()

    # Close the database connection.
    connection.close()

    # Convert database rows into dictionaries.
    return [dict(contact) for contact in contacts]


def search_by_name(name, db_name="contacts.db"):
    """Search for contacts by name.

    The search supports partial name matching.

    :param name: Name or partial name to search for.
    :param db_name: Name of the SQLite database.
    :return: List of matching contacts represented as dictionaries.
    """

    # Open a connection to the database.
    connection = get_connection(db_name)

    # Search for contacts whose name contains the given text.
    contacts = connection.execute(
        """
        SELECT id, name, phone, email
        FROM contacts
        WHERE name LIKE ?
        ORDER BY name
        """,
        (f"%{name}%",)
    ).fetchall()

    # Close the database connection.
    connection.close()

    # Convert database rows into dictionaries.
    return [dict(contact) for contact in contacts]


def search_by_email(email, db_name="contacts.db"):
    """Search for contacts by email address.

    The search supports partial email matching.

    :param email: Email address or partial email address to search for.
    :param db_name: Name of the SQLite database.
    :return: List of matching contacts represented as dictionaries.
    """

    # Open a connection to the database.
    connection = get_connection(db_name)

    # Search for contacts whose email contains the given text.
    contacts = connection.execute(
        """
        SELECT id, name, phone, email
        FROM contacts
        WHERE email LIKE ?
        ORDER BY email
        """,
        (f"%{email}%",)
    ).fetchall()

    # Close the database connection.
    connection.close()

    # Convert database rows into dictionaries.
    return [dict(contact) for contact in contacts]


def search_by_phone(phone, db_name="contacts.db"):
    """Search for contacts by phone number.

    The search supports partial phone number matching.

    :param phone: Phone number or partial phone number to search for.
    :param db_name: Name of the SQLite database.
    :return: List of matching contacts represented as dictionaries.
    """

    # Open a connection to the database.
    connection = get_connection(db_name)

    # Search for contacts whose phone number contains the given text.
    contacts = connection.execute(
        """
        SELECT id, name, phone, email
        FROM contacts
        WHERE phone LIKE ?
        ORDER BY phone
        """,
        (f"%{phone}%",)
    ).fetchall()

    # Close the database connection.
    connection.close()

    # Convert database rows into dictionaries.
    return [dict(contact) for contact in contacts]


def update_contact(
    contact_id,
    name,
    phone,
    email,
    db_name="contacts.db"
):
    """Update an existing contact.

    Validates the new contact information before updating
    the database record.

    :param contact_id: ID of the contact to update.
    :param name: New name of the contact.
    :param phone: New phone number of the contact.
    :param email: New email address of the contact.
    :param db_name: Name of the SQLite database.
    :return: True if the contact was updated, otherwise False.
    :raises ValueError: If any field is empty or invalid, or if
        the phone number or email already exists.
    """

    # Remove unnecessary spaces from the input values.
    name = name.strip()
    phone = phone.strip()
    email = email.strip()

    # Check that the name is not empty.
    if not name:
        raise ValueError("Name cannot be empty.")

    # Check that the phone number is not empty.
    if not phone:
        raise ValueError("Phone cannot be empty.")

    # Check that the email address is not empty.
    if not email:
        raise ValueError("Email cannot be empty.")

    # Validate the phone number and email address.
    validate_phone(phone)
    validate_email(email)

    # Open a connection to the database.
    connection = get_connection(db_name)

    try:
        # Update the contact with the new information.
        cursor = connection.execute(
            """
            UPDATE contacts
            SET name = ?, phone = ?, email = ?
            WHERE id = ?
            """,
            (name, phone, email, contact_id)
        )

        # Save the changes to the database.
        connection.commit()

        # Return whether a contact was successfully updated.
        return cursor.rowcount > 0

    except sqlite3.IntegrityError:
        # Handle duplicate phone numbers or email addresses.
        raise ValueError(
            "Phone number or email already exists."
        )

    finally:
        # Always close the database connection.
        connection.close()


def delete_contact(contact_id, db_name="contacts.db"):
    """Delete a contact from the database.

    :param contact_id: ID of the contact to delete.
    :param db_name: Name of the SQLite database.
    :return: True if the contact was deleted, otherwise False.
    """

    # Open a connection to the database.
    connection = get_connection(db_name)

    # Delete the contact with the specified ID.
    cursor = connection.execute(
        """
        DELETE FROM contacts
        WHERE id = ?
        """,
        (contact_id,)
    )

    # Save the deletion.
    connection.commit()

    # Close the database connection.
    connection.close()

    # Return whether a contact was successfully deleted.
    return cursor.rowcount > 0
