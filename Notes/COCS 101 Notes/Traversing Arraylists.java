// Traversing ArrayLists in Java

// **What is Traversing?**
// Visiting each element in an ArrayList one by one (access or modify data).

// **Basic Traversal Methods**

// **1. Enhanced for loop (simplest):**
// Iterates through each element and assigns it to a temporary variable.

ArrayList<String> fruits = new ArrayList<>();
fruits.add("apple");
fruits.add("banana");
fruits.add("cherry");

for (String fruit : fruits) {
    System.out.println(fruit);
}

// **2. Standard for loop (more control):**
// Uses an index to access elements by position (get(i)).

for (int i = 0; i < fruits.size(); i++) {
    String fruit = fruits.get(i);
    System.out.println(fruit);
}

// **Removing Elements During Traversal**

// **Caution!** Removing elements with a for loop can cause errors (index shifting).
// **Use iterators for safe removal.**

Iterator<String> it = fruits.iterator();
while (it.hasNext()) {
    String fruit = it.next();
    if (fruit.equals("banana")) {
        it.remove();  // Safe removal with iterators
    }
}

// **Common Traversal Errors**

// **1. ConcurrentModificationException:** Don't modify size (add/remove) while iterating with a for loop (use iterators).
// **2. IndexOutOfBoundException:** Ensure loop index stays within 0 to size-1 range.

// **Tip:** Choose the traversal method based on your needs.
// Enhanced for loop - simpler for accessing elements.
// Standard for loop - more control for specific operations.
