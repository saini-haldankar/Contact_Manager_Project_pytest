from app.contacts import (
    create_contact,
    delete_contact,
    update_contact,
    get_all_contacts,
    search_by_name,
    search_by_email,
    search_by_phone,
)


def display_contacts(contacts):
    if not contacts:
        print("\nNo contacts found.")
        return

    print("\n========== CONTACTS ==========")

    for contact in contacts:
        print("ID    :", contact["id"])
        print("Name  :", contact["name"])
        print("Phone :", contact["phone"])
        print("Email :", contact["email"])
        print("------------------------------")


def create_contact_cli():
    print("\n===== CREATE CONTACT =====")

    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")

    try:
        contact_id = create_contact(name, phone, email)

        print("\nContact created successfully!")
        print("Contact ID:", contact_id)

    except ValueError as error:
        print("\nError:", error)


def delete_contact_cli():
    print("\n===== DELETE CONTACT =====")

    contact_id = input("Enter contact ID: ")

    try:
        contact_id = int(contact_id)

        deleted = delete_contact(contact_id)

        if deleted:
            print("\nContact deleted successfully!")
        else:
            print("\nContact not found.")

    except ValueError:
        print("\nPlease enter a valid ID.")


def update_contact_cli():
    print("\n===== UPDATE CONTACT =====")

    contact_id = input("Enter contact ID: ")

    try:
        contact_id = int(contact_id)

        name = input("New name: ")
        phone = input("New phone: ")
        email = input("New email: ")

        updated = update_contact(
            contact_id,
            name,
            phone,
            email
        )

        if updated:
            print("\nContact updated successfully!")
        else:
            print("\nContact not found.")

    except ValueError as error:
        print("\nError:", error)


def search_contact_cli():
    print("\n===== SEARCH CONTACT =====")
    print("1. Search by Name")
    print("2. Search by Email")
    print("3. Search by Phone")

    choice = input("Enter choice: ")

    if choice == "1":
        value = input("Enter name: ")
        contacts = search_by_name(value)

    elif choice == "2":
        value = input("Enter email: ")
        contacts = search_by_email(value)

    elif choice == "3":
        value = input("Enter phone: ")
        contacts = search_by_phone(value)

    else:
        print("\nInvalid choice.")
        return

    display_contacts(contacts)


def list_contacts_cli():
    print("\n===== ALL CONTACTS =====")

    contacts = get_all_contacts()

    display_contacts(contacts)


def run():
    while True:
        print("\n================================")
        print("        CONTACT MANAGER")
        print("================================")
        print("1. Create Contact")
        print("2. Delete Contact")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. List Contacts")
        print("6. Exit")
        print("================================")

        choice = input("Enter choice: ")

        if choice == "1":
            create_contact_cli()

        elif choice == "2":
            delete_contact_cli()

        elif choice == "3":
            search_contact_cli()

        elif choice == "4":
            update_contact_cli()

        elif choice == "5":
            list_contacts_cli()

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please try again.")
