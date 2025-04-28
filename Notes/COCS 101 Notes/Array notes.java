// Arrays in Java: A Comprehensive Guide

/**
 * This class demonstrates arrays in Java, including creation, access, iteration,
 * and common operations.
 */
public class ArrayExamples {

    public static void main(String[] args) {

        // --------------------------------------------------------------------
        // Creating arrays with size and data type specification
        // --------------------------------------------------------------------

        int[] numbers = new int[5]; // Array of 5 integers
        String[] cities = new String[3]; // Array of 3 strings
        double[] sunshineHours = {7.5, 6.5, 6.05}; // Array initialized with values

        // --------------------------------------------------------------------
        // Accessing elements using index (remember indexing starts from 0)
        // --------------------------------------------------------------------

        double secondCitySunshine = sunshineHours[1]; // Accessing second element

        // --------------------------------------------------------------------
        // Modifying elements
        // --------------------------------------------------------------------

        numbers[2] = 100; // Setting the value at index 2 to 100

        // --------------------------------------------------------------------
        // Iterating through an array using a for loop
        // --------------------------------------------------------------------

        for (int i = 0; i < numbers.length; i++) {
            System.out.println(numbers[i]);
        }

        // --------------------------------------------------------------------
        // Enhanced for loop (for-each loop)
        // --------------------------------------------------------------------

        for (double hour : sunshineHours) {
            System.out.println(hour);
        }

        // --------------------------------------------------------------------
        // Array length
        // --------------------------------------------------------------------

        int cityCount = cities.length; // Get the number of elements in the cities array

        // --------------------------------------------------------------------
        // Parallel Arrays (arrays holding related data)
        // --------------------------------------------------------------------

        String[] parallelCities = {"San Juan", "Accra", "Sao Paulo"};
        int[] parallelPopulation = {335468, 2557000, 12330000};
        double[] parallelSunshineHours = {7.5, 6.5, 6.05};

        // --------------------------------------------------------------------
        // Accessing corresponding elements from parallel arrays
        // --------------------------------------------------------------------

        for (int i = 0; i < parallelCities.length; i++) {
            System.out.println(parallelCities[i] + "'s population is " + parallelPopulation[i] + ".");
            System.out.println("The least amount of sunshine " + parallelCities[i] + " gets is " + parallelSunshineHours[i] + " hours a day.");
        }

        // --------------------------------------------------------------------
        // ArrayIndexOutOfBoundsException (avoiding out-of-bounds access)
        // --------------------------------------------------------------------

        // This would throw an exception (index 3 is out of bounds)
        // String invalidCity = cities[3];
    }
}
