import java.util.logging.Logger;
    //lab name
    //synopsis of the lab 
    // your name 
    // must have peoples names who was near
public class FactorialCalculator {
    private static final Logger logger = Logger.getLogger(FactorialCalculator.class.getName());

    public static void main(String[] args) {
        int number = 5; // Change this to the number you want to calculate the factorial of
        long factorial = calculateFactorial(number);
        logger.info("The factorial of " + number + " is: " + factorial);
    }

    public static long calculateFactorial(int n) {
        if (n == 0 || n == 1) {
            return 1;
        } else {
            return n * calculateFactorial(n - 1);
        }
    }
}
