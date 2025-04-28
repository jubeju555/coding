// Creating Arrays
int[] numbers = new int[5]; // Creates an array of integers with a length of 5
String[] names = {"Alice", "Bob", "Charlie"}; // Creates an array of strings and initializes it with values

// Setting Elements
numbers[0] = 10; // Sets the first element of the 'numbers' array to 10
numbers[1] = 20; // Sets the second element of the 'numbers' array to 20

// Getting Elements
int firstNumber = numbers[0]; // Retrieves the first element of the 'numbers' array


// Make an Empty Array
int[] emptyArray = new int[0]; // Creates an empty integer array

// Indexing Into an Array
int thirdNumber = numbers[2]; // Retrieves the third element of the 'numbers' array

// Accessing the Array
int[] numbersArray = {1, 2, 3, 4, 5}; // Creates and initializes an array of integers

// Determining Array Size
int size = numbersArray.length; // Retrieves the length or size of the 'numbersArray'

// Iterating over an Array - For Loop
for (int i = 0; i < numbersArray.length; i++) { // Loops through each element of the array using a for loop
    System.out.println(numbersArray[i]); // Prints each element of the array
}

// Enhanced for Loop
for (int number : numbersArray) { // Enhanced for loop for iterating over each element of the array
    System.out.println(number); // Prints each element of the array
}

// ArrayList vs Array
// ArrayList
ArrayList<String> namesList = new ArrayList<>(); // Creates a new ArrayList of strings
namesList.add("Alice"); // Adds "Alice" to the ArrayList
namesList.add("Bob"); // Adds "Bob" to the ArrayList
namesList.add("Charlie"); // Adds "Charlie" to the ArrayList

// Array
String[] namesArray = {"Alice", "Bob", "Charlie"}; // Creates and initializes an array of strings

// Initializing an ArrayList
ArrayList<Integer> numbersList = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5)); // Creates and initializes an ArrayList of integers

// Adding Elements to an ArrayList
ArrayList<String> namesList = new ArrayList<>(); // Creates a new ArrayList of strings
namesList.add("Alice"); // Adds "Alice" to the ArrayList
namesList.add("Bob"); // Adds "Bob" to the ArrayList

// Getting Elements in an ArrayList
String firstName = namesList.get(0); // Retrieves the first element of the 'namesList' ArrayList

// Setting Elements in an ArrayList
namesList.set(1, "David"); // Replaces the element at index 1 in the 'namesList' ArrayList with "David"

// Removing Elements from an ArrayList
namesList.remove("Bob"); // Removes "Bob" from the 'namesList' ArrayList
