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
    def __init__(self, size=10):
        self.size = size
        self.data = [None] * size

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
        node = self.data[idx]

        if node is None:
            self.data[idx] = Node(key, contact)
            return

        # Traverse chain to update if key exists, otherwise append
        prev = None
        curr = node
        while curr:
            if curr.key == key:
                curr.value = contact
                return
            prev = curr
            curr = curr.next

        prev.next = Node(key, contact)

    def search(self, key):
        """Return the Contact with matching name, or None if not found."""
        idx = self.hash_function(key)
        curr = self.data[idx]
        while curr:
            if curr.key == key:
                return curr.value
            curr = curr.next
        return None

    def print_table(self):
        """Print the structure of the hash table."""
        for i, node in enumerate(self.data):
            entries = []
            curr = node
            while curr:
                # Safely access name/number attributes if present
                name = getattr(curr.value, "name", None) or curr.key
                number = getattr(curr.value, "number", None)
                if number is not None:
                    entries.append(f"{name}:{number}")
                else:
                    entries.append(str(name))
                curr = curr.next
            chain = " -> ".join(entries) if entries else "None"
            print(f"[{i}]: {chain}")
\