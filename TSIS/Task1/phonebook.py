import json
from connect import get_connection


# ---------------- FETCH ----------------
def fetch(query, params=None):
    conn = get_connection()
    if not conn:
        return []

    cur = conn.cursor()
    cur.execute(query, params or ())
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


# ---------------- RUN ----------------
def run(query, params=None):
    conn = get_connection()
    if not conn:
        return

    cur = conn.cursor()
    cur.execute(query, params or ())
    conn.commit()
    cur.close()
    conn.close()


# ---------------- ADD CONTACT ----------------
def add_contact(name, email, birthday, group_name, phone, ptype):
    conn = get_connection()
    cur = conn.cursor()

    group_name = group_name.strip().capitalize()

    cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
    group = cur.fetchone()

    if group is None:
        cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (group_name,))
        group_id = cur.fetchone()[0]
    else:
        group_id = group[0]

    cur.execute("""
        INSERT INTO contacts(name,email,birthday,group_id)
        VALUES (%s,%s,%s,%s)
        RETURNING id
    """, (name, email, birthday, group_id))

    cid = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO phones(contact_id,phone,type)
        VALUES (%s,%s,%s)
    """, (cid, phone, ptype))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact added")


# ---------------- DELETE ----------------
def delete_contact(name):
    run("DELETE FROM contacts WHERE name=%s", (name,))
    print("Deleted")


# ---------------- VIEW ALL ----------------
def view_all():
    return fetch("""
        SELECT c.name, c.email, p.phone, p.type, g.name
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name
    """)


# ---------------- SEARCH ----------------
def search(q):
    return fetch("SELECT * FROM search_contacts(%s::text)", (q,))


# ---------------- GROUP ----------------
def by_group(g):
    return fetch("""
        SELECT c.name, c.email, p.phone, p.type, g.name
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
        JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
    """, (g,))


# ---------------- EMAIL ----------------
def email_search(e):
    return fetch("""
        SELECT c.name, c.email, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE c.email ILIKE %s
    """, (f"%{e}%",))


# ---------------- SORT ----------------
def sort_contacts(f):
    cols = {
        "name": "c.name",
        "birthday": "c.birthday",
        "date": "c.created_at"
    }

    col = cols.get(f, "c.name")

    return fetch(f"""
        SELECT c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {col}
    """)


# ---------------- PAGINATION ----------------
def paginate(page, size=5):
    off = (page - 1) * size

    return fetch("""
        SELECT c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name
        LIMIT %s OFFSET %s
    """, (size, off))


# ---------------- JSON EXPORT ----------------
def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id,name,email,birthday FROM contacts")
    data = cur.fetchall()

    result = []

    for c in data:
        cur.execute("SELECT phone,type FROM phones WHERE contact_id=%s", (c[0],))
        phones = cur.fetchall()

        result.append({
            "name": c[1],
            "email": c[2],
            "birthday": str(c[3]),
            "phones": [{"phone": p[0], "type": p[1]} for p in phones]
        })

    cur.close()
    conn.close()

    with open("contacts.json", "w") as f:
        json.dump(result, f, indent=4)

    print("Exported")


# ---------------- IMPORT JSON ----------------
def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    for c in data:
        exists = fetch("SELECT id FROM contacts WHERE name=%s", (c["name"],))

        if exists:
            choice = input(f"{c['name']} exists (skip/overwrite): ")
            if choice == "skip":
                continue
            run("DELETE FROM contacts WHERE name=%s", (c["name"],))

        add_contact(
            c["name"],
            c["email"],
            c["birthday"],
            "Other",
            c["phones"][0]["phone"],
            c["phones"][0]["type"]
        )


# ---------------- MENU ----------------
def menu():
    page = 1

    while True:
        print("""
1 Add
2 Search
3 Group
4 Email
5 Sort
6 View All
7 Pagination
8 Export JSON
9 Import JSON
10 Delete
11 Exit
""")

        cmd = input("> ")

        if cmd == "1":
            add_contact(
                input("Name: "),
                input("Email: "),
                input("Birthday (YYYY-MM-DD): "),
                input("Group: "),
                input("Phone: "),
                input("Type: ")
            )

        elif cmd == "2":
            print(search(input("Query: ")))

        elif cmd == "3":
            print(by_group(input("Group: ")))

        elif cmd == "4":
            print(email_search(input("Email: ")))

        elif cmd == "5":
            print(sort_contacts(input("name/birthday/date: ")))

        elif cmd == "6":
            print(view_all())

        elif cmd == "7":
            print(paginate(page))
            act = input("next/prev: ")
            if act == "next":
                page += 1
            elif act == "prev":
                page = max(1, page - 1)

        elif cmd == "8":
            export_json()

        elif cmd == "9":
            import_json()

        elif cmd == "10":
            delete_contact(input("Name: "))

        elif cmd == "11":
            break


if __name__ == "__main__":
    menu()