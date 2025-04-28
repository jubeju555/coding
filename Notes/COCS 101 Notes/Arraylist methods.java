// ArrayLists in Java

public class Main {

  public static void main(String[] args) {

    // Introduction to ArrayLists (like a resizable shopping list)
    System.out.println("ArrayLists");
    System.out.println("--------");
    System.out.println("// ArrayList is a resizable collection of elements.");
    System.out.println("// It's similar to an array, but more flexible because it can grow or shrink in size.");

    // Initializing ArrayLists without Types (useful when unsure about data types)
    System.out.println("\n// Initializing ArrayLists without Types");
    ArrayList fruits = new ArrayList(); // Create an empty ArrayList
    System.out.println("fruits: " + fruits); // Print the empty ArrayList

    // ArrayList vs Array (fixed size vs resizable)
    System.out.println("\n// ArrayList vs Array");
    System.out.println("// Arrays have a fixed size, while ArrayLists can grow or shrink in size.");

    // Initializing an ArrayList with elements (replace with your elements)
    System.out.println("\n// Initializing an ArrayList");
    ArrayList<String> fruitsList = new ArrayList<String>(); // Create an ArrayList of Strings
    fruitsList.add("apple");
    fruitsList.add("banana");
    fruitsList.add("cherry");
    System.out.println("fruitsList: " + fruitsList); // Print the ArrayList with fruits

    // Array vs. ArrayList Initialization (fixed data types vs mixed)
    System.out.println("\n// Array vs. ArrayList Initialization");

    // Array of integers (can only hold integers)
    int[] numbers = {1, 2, 3};
    System.out.println("numbers: " + java.util.Arrays.toString(numbers)); // Print the array of numbers

    // ArrayList can hold various data types (replace with your elements)
    ArrayList mixedData = new ArrayList();
    mixedData.add(10);
    mixedData.add("hello");
    mixedData.add(3.14);
    System.out.println("mixedData: " + mixedData); // Print the ArrayList with mixed data types

    // ArrayList Methods

    // Adding Elements
    System.out.println("\n// ArrayList Methods - Adding Elements");
    fruitsList.add("orange"); // Add "orange" to the end

    // Getting Elements
    System.out.println("\n// Getting Elements");
    String firstFruit = fruitsList.get(0); // Get the element at index 0 (usually the first)
    System.out.println("First fruit: " + firstFruit);

    // Setting Elements
    System.out.println("\n// Setting Elements");
    fruitsList.set(1, "mango"); // Replace element at index 1 with "mango"

    // Removing Elements
    System.out.println("\n// Removing Elements");
    fruitsList.remove(2); // Remove the element at index 2

    // ... Your code to use the modified fruitsList ...
  }
}
