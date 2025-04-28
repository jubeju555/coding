//Income Tax Program
// create a program that calulates the amount of taxes you have to pay accordin to your salaery 
// judah benjamin
//kirtan(helped with final percentage output), 
//will gilice (helped with organization of order of if statements )
import java.util.Scanner;

public class IncomeTaxCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Prompt the user to enter their income.
        System.out.print("Enter total income: $");
        double income = scanner.nextDouble();
        double income2 = income; 
        double totalTax = 0.0; // Initialize the total tax to 0.

        // Calculate tax based on progressive tax brackets.
        if (income > 15000.00) {
            // 38.15% tax bracket.
            totalTax += (income - 15000.00) * 0.3815;
            income = 15000.00; // Set income to the next bracket.
        }
        if (income > 10000.00) {
            // 31.29% tax bracket.
            totalTax += (income - 10000.00) * 0.3129;
            income = 10000.00; // Set income to the next bracket.
        }
        if (income > 5000.00) {
            // 28.71% tax bracket.
            totalTax += (income - 5000.00) * 0.2871;
            income = 5000.00; // Set income to the next bracket.
        }
        if (income > 1000.00) {
            // 25.00% tax bracket.
            totalTax += (income - 1000.00) * 0.2500;
            income = 1000.00; // Set income to the next bracket.
        }

        // Calculate the percentage of income that was taxed.
        double taxedPercentage = (totalTax / income2) * 100.0;

        // Output the results with proper formatting.
        System.out.printf("Taxes owed = $%.2f%n", totalTax);
        System.out.printf( "%.2f%%%n",taxedPercentage );
       
        // Close the scanner.
        scanner.close(); 
    }
}
