class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''

    def __init__(self, name: str, number: str) -> None:
        self.name = str(name)
        self.number = str(number)

    def __str__(self) -> str:
        return f"{self.name}: {self.number}"


class Node:
    '''
    Node class to represent a single entry in the hash table.
    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The value (Contact object) associated with the key.
        next (Node): Pointer to the next node in case of a collision.
    '''

    def __init__(self, key: str, value: Contact) -> None:
        self.key = key
        self.value = value
        self.next = None  # linked-list pointer


class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts.
    Attributes:
        size (int): The size of the hash table.
        data (list): The underlying array to store linked lists for collision handling.
    Methods:
        hash_function(key): Converts a string key into an array index.
        insert(key, value): Inserts a new contact into the hash table.
        search(key): Searches for a contact by name.
        print_table(): Prints the structure of the hash table.
    '''

    def __init__(self, size: int = 10) -> None:
        if size <= 0:
            raise ValueError("HashTable size must be positive.")
        self.size = size
        self.data = [None] * size  # array of Node heads (or None)

    def hash_function(self, key: str) -> int:
        """Simple, deterministic hash: sum of character codes mod table size."""
        # This choice makes "Amy" and "May" collide (both sum to 295), which is useful for testing.
        return sum(ord(c) for c in str(key)) % self.size

    def insert(self, name: str, number: str) -> None:
        """
        Insert or update a contact.
        - If 'name' already exists, update its number.
        - Otherwise, prepend a new Node at this bucket's linked list.
        """
        idx = self.hash_function(name)
        head = self.data[idx]

        # Update if exists
        curr = head
        while curr is not None:
            if curr.key == name:
                curr.value.number = number  # update existing
                return
            curr = curr.next

        # Not found: create and prepend new node
        new_contact = Contact(name, number)
        new_node = Node(name, new_contact)
        new_node.next = head
        self.data[idx] = new_node

    def search(self, name: str):
        """
        Return the Contact with matching name, or None if not found.
        """
        idx = self.hash_function(name)
        curr = self.data[idx]
        while curr is not None:
            if curr.key == name:
                return curr.value
            curr = curr.next
        return None

    def print_table(self) -> None:
        """
        Print each index and the chain of contacts stored there in the format:
        Index i: Empty
        or
        Index i: - Name: Number - Name2: Number2
        """
        for i in range(self.size):
            node = self.data[i]
            if node is None:
                print(f"Index {i}: Empty")
                continue

            # Build the chain string
            parts = []
            curr = node
            while curr is not None:
                parts.append(f"- {curr.value}")  # Contact.__str__ formats "Name: Number"
                curr = curr.next
            print(f"Index {i}: {' '.join(parts)}")


# -----------------------------
# Basic tests / demonstration
# -----------------------------
if __name__ == "__main__":
    # Contact and Node quick sanity checks
    contact_1 = Contact("Riley", "123-456-7890")
    print(contact_1)  # Riley: 123-456-7890

    node_1 = Node(contact_1.name, contact_1)
    print(node_1.key)    # Riley
    print(node_1.value)  # Riley: 123-456-7890
    print(node_1.next)   # None

    # HashTable tests (your placements may vary depending on hash function)
    table = HashTable(10)
    table.print_table()
    '''
    Expected shape (exact indices may differ by hash_function):
    Index 0: Empty
    Index 1: Empty
    Index 2: Empty
    Index 3: Empty
    Index 4: Empty
    Index 5: Empty
    Index 6: Empty
    Index 7: Empty
    Index 8: Empty
    Index 9: Empty
    '''

    # Add some values
    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")
    print("\nAfter inserting John and Rebecca:")
    table.print_table()

    # Search for a value
    contact = table.search("John")
    print("\nSearch result:", contact)  # e.g., John: 909-876-1234

    # Edge Case #1 - Hash collisions (Amy and May collide under this hash)
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")
    print("\nAfter inserting Amy and May (collision test):")
    table.print_table()

    # Edge Case #2 - Duplicate Keys (update number)
    table.insert("Rebecca", "999-444-9999")
    print("\nAfter updating Rebecca:")
    table.print_table()

    # Edge Case #3 - Searching for a value not in the table
    print("\nSearch for Chris (not present):", table.search("Chris"))  # None


# --------------------------
# Design Memo (paste-ready)
# --------------------------
"""
Design Memo  

A hash table is ideal for fast lookups because it maps keys (contact names) to array
indices in essentially O(1) average time. By computing a small integer index from a
string key via a deterministic hash function, we jump directly to the relevant bucket
instead of scanning an entire list. This is especially beneficial as the contact list
grows, where linear search would become increasingly slow.

We handle collisions with separate chaining: each array slot stores the head of a
linked list of Nodes. If multiple names hash to the same index (e.g., “Amy” and “May”
with the simple ordinal-sum hash), we traverse the small linked list at that bucket.
Insertion places a new node at the head unless the key already exists, in which case
we update the existing contacts number. Search walks the chain to find a matching
key. This approach keeps the implementation simple and maintains good performance
when the table size is chosen sensibly relative to expected entries.

An engineer might choose a hash table over a list when frequent insert/search by key
is required and order does not matter. Compared to a tree (like a balanced BST), a
hash table typically has better constant-factor performance for exact-key operations
and simpler code, at the cost of not providing sorted order or efficient range queries.
Trees are better when you need ordering or prefix/range lookups. Lists are appropriate
for tiny datasets or when you primarily append and iterate. For a contact manager
indexed by exact name, a hash table strikes the right balance of simplicity and speed.
"""

