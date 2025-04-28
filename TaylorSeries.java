// taylor series 
// estimating 𝑒^x by using the Taylor series expansion
// judah benjamin
// kirtan (told me how to formulate the quantitive portion of the code)
import java.util.Scanner;

public class TaylorSeries {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Prompt the user to enter the value of x
        System.out.print("Enter x: ");
        double x = scanner.nextDouble();

        int n;
        do {
            // Prompt the user to enter the number of iterations
            System.out.print("Enter number of iterations: ");
            n = scanner.nextInt();
        } while (n < 1 || n > 10000);

        // Calculate the result using the Taylor series method
        double taylorResult = taylor(x, n);

        // Calculate the result using the Math.exp method
        double expResult = Math.exp(x);

        // Calculate the error as a percentage
        double error = ((expResult - taylorResult) / expResult) * 100;

        // Display the results
        System.out.printf("TAYLOR: %.3f, EXP: %.3f, ERROR: %.0f%%.\n", taylorResult, expResult, error);

        scanner.close();
    }

    // Calculate the result using the Taylor series method
    static double taylor(double x, int n) {
        double result = 1;
        double z = 1;

        for (int i = 1; i <= n; i++) {
            z *= x / i;
            result += z;
        }

        return result;
    }
}