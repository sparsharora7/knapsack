class TreeNode:
    def __init__(self, leaf=True):
        self.keys = []
        self.values = []
        self.children = []
        self.leaf = leaf

class BPlusTree:
    def __init__(self, degree):
        self.root = TreeNode()
        self.degree = degree

    def search(self, key):
        return self.search_recursive(self.root, key)

    def search_recursive(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
        elif node.leaf:
            return None
        else:
            return self.search_recursive(node.children[i], key)

    def insert(self, key, value):
        if key in self.root.keys:
            print("Item already exists in inventory")
            return

        if len(self.root.keys) == 2 * self.degree - 1:
            new_root = TreeNode(leaf=False)
            new_root.children.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root
            self.insert_non_full(self.root, key, value)
        else:
            self.insert_non_full(self.root, key, value)

    def insert_non_full(self, node, key, value):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                node.values[i+1] = node.values[i]
                i -= 1
            node.keys[i+1] = key
            node.values[i+1] = value
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.degree - 1:
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self.insert_non_full(node.children[i], key, value)

    def split_child(self, parent, index):
        degree = self.degree
        child = parent.children[index]
        new_child = TreeNode(leaf=child.leaf)
        parent.keys.insert(index, child.keys[degree - 1])
        parent.values.insert(index, child.values[degree - 1])
        parent.children.insert(index + 1, new_child)
        new_child.keys = child.keys[degree:]
        new_child.values = child.values[degree:]
        child.keys = child.keys[:degree - 1]
        child.values = child.values[:degree - 1]
        if not child.leaf:
            new_child.children = child.children[degree:]
            child.children = child.children[:degree]


class GroceryStore:
    def __init__(self):
        self.inventory = BPlusTree(degree=3)

    def add_item_to_inventory(self, item_id, item_name, item_price):
        self.inventory.insert(item_id, (item_name, item_price))

    def search_item_in_inventory(self, item_id):
        return self.inventory.search(item_id)

    def display_inventory(self):
        print("Inventory:")
        print("Item ID | Item Name | Price")
        for key in self.inventory.root.keys:
            item_name, item_price = self.inventory.search(key)
            print(f"{key} | {item_name} | {item_price}")

# Example usage:
store = GroceryStore()
store.add_item_to_inventory(1, "Apple", 1.5)
store.add_item_to_inventory(2, "Banana", 0.75)
store.add_item_to_inventory(3, "Orange", 1.25)

store.display_inventory()
