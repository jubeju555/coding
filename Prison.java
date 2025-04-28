import java.util.Scanner;
    //lab name
    //synopsis of the lab 
    // your name 
    // must have peoples names who was near
public class Prison{
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter client's first name: ");
        String firstName = scanner.next();

        System.out.print("Enter client's last name: ");
        String lastName = scanner.next();

        System.out.print("Enter client's age: ");
        int age = scanner.nextInt();

        System.out.print("Enter client's prison sentence in months: ");
        double prisonSentenceMonths = scanner.nextDouble();

        double prisonSentenceYears = prisonSentenceMonths / 12;

        // Corrected output formatting
        System.out.printf("%s, %s, currently %d years old, will be %.2f years old when released from prison.%n",
                lastName, firstName, age, age + prisonSentenceYears);

        scanner.close();
    }
}
