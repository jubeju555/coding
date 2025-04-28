public class ArrayTraversal {

// Traversing Arrays in Java

/**
 * This class demonstrates traversing arrays using for and while loops,
 * highlighting common pitfalls to avoid.
 */
    public static void main(String[] args) {

        // Sample array of orange orders
        int[] orangeOrders = {10, 3, 6, 4, 5, 1};

        // Accessing individual elements by index
        int firstOrder = orangeOrders[0]; // Accessing the first element (index 0)

        // Determining array size
        int arrayLength = orangeOrders.length; // Get the number of elements in the array

        // Iterating over an array using a for loop
        System.out.println("Iterating using for loop:");
        for (int i = 0; i < orangeOrders.length; i++) {
            System.out.println("Order at index " + i + ": " + orangeOrders[i]);
        }

        // Iterating over an array using a while loop
        System.out.println("\nIterating using while loop:");
        int index = 0;
        while (index < orangeOrders.length) {
            System.out.println("Order at index " + index + ": " + orangeOrders[index]);
            index++;
        }

        // Common pitfalls: ArrayIndexOutOfBoundsException
        // This would throw an error (index 6 is out of bounds)
        // System.out.println(orangeOrders[6]);

        // Finding a target value (exercise for the reader)
        // Implement logic to search for a specific order quantity in the array
    }
}
