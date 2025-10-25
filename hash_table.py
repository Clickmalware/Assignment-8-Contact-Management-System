class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''
    
    pass # Delete this line when implementing the class

class Node:
    """
    Node class to represent a single entry in the hash table linked list.
    Attributes:
        key (str): The key (contact name) used by the hash table.
        value (Contact): The Contact object associated with the key.
        next (Node): Pointer to the next node in the chain (default None).
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        

class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts using chaining.
    Each bucket is a Python list of (key, Contact) tuples to handle collisions.
    Attributes:
        size (int): The size of the hash table.
        data (list): The underlying array where each element is a list (chain).
    Methods:
        hash_function(key): Converts a string key into an array index.
        insert(key, value): Inserts a new contact into the hash table.
        search(key): Searches for a contact by name.
        print_table(): Prints the structure of the hash table.
    '''
    def __init__(self, size=10):
        self.size = size
        # Use lists for chains (simple and efficient in Python)
        self.data = [[] for _ in range(size)]

    def hash_function(self, key):
        """Simple hash: sum of ordinals mod table size."""
        if not isinstance(key, str):
            key = str(key)
        return sum(ord(c) for c in key) % self.size

    def insert(self, key, value):
        """
        Insert a contact. `value` can be a Contact instance or the contact's number (str).
        If the key already exists, update the contact's number.
        """
        # Normalize/create Contact instance in a way that works whether Contact.__init__ is defined or not.
        contact = None
        if isinstance(value, Contact):
            contact = value
            contact.name = key  # ensure name matches provided key
        else:
            try:
                # If Contact is implemented with __init__(name, number)
                contact = Contact(key, value)
            except TypeError:
                # Fallback for a bare class with no __init__
                contact = Contact()
                contact.name = key
                contact.number = value

        idx = self.hash_function(key)
        bucket = self.data[idx]

        # Update existing entry if key found
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, contact)
                return

        # Otherwise append new entry to the chain
        bucket.append((key, contact))

    def search(self, key):
        """Return the Contact with matching name, or None if not found."""
        idx = self.hash_function(key)
        bucket = self.data[idx]
        for k, contact in bucket:
            if k == key:
                return contact
        return None

    def print_table(self):
        """Print the structure of the hash table."""
        for i, bucket in enumerate(self.data):
            entries = []
            for k, contact in bucket:
                # Safely access name/number attributes if present
                name = getattr(contact, "name", None) or k
                number = getattr(contact, "number", None)
                if number is not None:
                    entries.append(f"{name}:{number}")
                else:
                    entries.append(str(name))
            chain = " -> ".join(entries) if entries else "None"
            print(f"[{i}]: {chain}")
