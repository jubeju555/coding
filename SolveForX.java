// solve for x
// a progrma that give you multiple questions and makes you solve for x and gives you a score based on your answers 
// judah benjamin
import java.util.Scanner;
import java.util.Random;

public class SolveForX {
    // Constants
    static final int MAX_SIZE = 10;
    static final int MIN_COEFF = 0;
    static final int MAX_COEFF = 5;
    static final int MIN_VAL = -100000;
    static final int MAX_VAL = 100000;
    static final int MIN_EQ = -100000;
    static final int MAX_EQ = 100000;
    static final double MY_EPSILON = 0.01;

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        // Get the seed from the user
        System.out.print("Enter seed: ");
        int seed = input.nextInt();
        new Random(seed);

        // Get the number of problems from the user
        int numProblems;
        do {
            System.out.print("How many problems do you want? ");
            numProblems = input.nextInt();
        } while (numProblems < 1 || numProblems > MAX_SIZE);

        // Get coefficients and values from the user
        int minCoeff, maxCoeff, minVal, maxVal, minEq, maxEq;
        do {
            System.out.print("Enter minimum coefficient: ");
            minCoeff = input.nextInt();
        } while (minCoeff < MIN_COEFF || minCoeff > MAX_COEFF);
        do {
            System.out.print("Enter maximum coefficient: ");
            maxCoeff = input.nextInt();
        } while (maxCoeff < minCoeff || maxCoeff > MAX_COEFF);
        do {
            System.out.print("Enter minimum value: ");
            minVal = input.nextInt();
        } while (minVal < MIN_VAL || minVal > MAX_VAL);
        do {
            System.out.print("Enter maximum value: ");
            maxVal = input.nextInt();
        } while (maxVal < minVal || maxVal > MAX_VAL);
        do {
            System.out.print("Enter minimum equals: ");
            minEq = input.nextInt();
        } while (minEq < MIN_EQ || minEq > MAX_EQ);
        do {
            System.out.print("Enter maximum equals: ");
            maxEq = input.nextInt();
        } while (maxEq < minEq || maxEq > MAX_EQ);

        // Generate random arrays
        int[] coefficients = generateRandomArray(numProblems, minCoeff, maxCoeff);
        int[] values = generateRandomArray(numProblems, minVal, maxVal);
        int[] operations = generateRandomArray(numProblems, 0, 1);
        int[] equals = generateRandomArray(numProblems, minEq, maxEq);

        // Generate answers
        double[] answers = generateAnswers(coefficients, values, operations, equals);

        // Initialize statistics
        int numCorrect = 0;
        int numIncorrect = 0;

        // Ask and check the user's answers
        for (int i = 0; i < numProblems; i++) {
            System.out.printf("%dx %s %d = %d%n", coefficients[i], (operations[i] == 0 ? "+" : "-"), values[i], equals[i]);
            System.out.print("What is x? ");
            
            if (input.hasNextDouble()) {
                double userAnswer = input.nextDouble();
                if (compareAnswer(userAnswer, answers[i])) {
                    System.out.printf("x = %.3f     CORRECT%n", userAnswer);
                    numCorrect++;
                } else {
                    System.out.printf("x = %.3f     INCORRECT%n", userAnswer);
                    numIncorrect++;
                }
            } else {
                System.out.println("Invalid answer.");
                input.next(); // Consume the invalid input
            }
        }

        // Print statistics
        System.out.printf("Num correct   = %d%n", numCorrect);
        System.out.printf("Num incorrect = %d%n", numIncorrect);
        double score = (double) numCorrect / numProblems * 100;
        System.out.printf("Your score    = %.0f%%%n", score);

        input.close();
    }

    // Helper method to generate random array
    static int[] generateRandomArray(int size, int minValue, int maxValue) {
        int[] array = new int[size];
        Random random = new Random();

        for (int i = 0; i < size; i++) {
            array[i] = random.nextInt(maxValue - minValue + 1) + minValue;
        }

        return array;
    }

    // Helper method to generate answers
    static double[] generateAnswers(int[] coeffs, int[] values, int[] signs, int[] equals) {
        double[] answers = new double[coeffs.length];

        for (int i = 0; i < coeffs.length; i++) {
            answers[i] = generateAnswer(coeffs[i], values[i], signs[i], equals[i]);
        }

        return answers;
    }

    // Helper method to generate a single answer
    static double generateAnswer(int coeff, int value, int sign, int equal) {
        return (sign == 0) ? (equal - value) / (double) coeff : (equal + value) / (double) coeff;
    }

    // Helper method to compare answers
    static boolean compareAnswer(double left, double right) {
        return Math.abs(left - right) <= MY_EPSILON;
    }
}
