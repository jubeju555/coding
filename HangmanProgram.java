import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class HangmanProgram {
    static final String[] pics = {
        "  +---+\n" +
        "  |   |\n" +
        "      |\n" +
        "      |\n" +
        "      |\n" +
        "      |\n" +
        "=========",

        "  +---+\n" +
        "  |   |\n" +
        "  O   |\n" +
        "      |\n" +
        "      |\n" +
        "      |\n" +
        "=========",

        "  +---+\n" +
        "  |   |\n" +
        "  O   |\n" +
        "  |   |\n" +
        "      |\n" +
        "      |\n" +
        "=========",

        "  +---+\n" +
        "  |   |\n" +
        "  O   |\n" +
        " /|   |\n" +
        "      |\n" +
        "      |\n" +
        "=========",

        "  +---+\n" +
        "  |   |\n" +
        "  O   |\n" +
        " /|\\  |\n" +
        "      |\n" +
        "      |\n" +
        "=========",

        "  +---+\n" +
        "  |   |\n" +
        "  O   |\n" +
        " /|\\  |\n" +
        " /    |\n" +
        "      |\n" +
        "=========",

        "  +---+\n" +
        "  |   |\n" +
        "  O   |\n" +
        " /|\\  |\n" +
        " / \\  |\n" +
        "      |\n" +
        "=========",
    };

    public static String[] getPics() {
        return pics;
    }

    final static String[] wordlist = {
        "elephant", "giraffe", "tiger", "lion", "monkey", "bear", "whale",
        "dolphin", "fish", "bird", "apple", "banana", "orange", "pear",
        "watermelon", "pizza", "cake", "cream", "cookie", "sandwich",
        "city", "country", "mountain", "ocean", "river", "lake", "forest",
        "desert", "beach", "park", "car", "house", "boat", "train", "plane",
        "book", "cellular", "laptop", "television", "clock", "man", "woman",
        "child", "boy", "girl", "doctor", "nurse", "teacher", "firefighter",
        "officer", "play", "read", "write", "sing", "dance", "swim", "sprint",
        "jump", "sports", "watch", "table", "chair", "bed", "couch", "lamp",
        "door", "window", "wall", "floor", "ceiling", "phone", "computer",
        "stereo", "alarm", "magazine", "newspaper", "pencil", "crayon", "paper",
        "cab", "semi", "railway", "hoverboard", "helicopter", "bike", "jetski", "skateboard",
        "rollerskates", "scooter", "puppy", "kitten", "horse", "bovine", "swine", "sheep",
        "rooster", "duck", "goose", "rabbit", "fusion", "moon", "star", "cloud",
        "rain", "snow", "wind", "thunder", "lightning", "rainbow", "happy",
        "exhausted", "angry", "excited", "scared", "surprised", "tired",
        "hungry", "thirsty", "bored"
    };

    private String chosenWord;
    private ArrayList<Character> guesses;
    private int wrongGuesses;

    public HangmanProgram(long seed) {
        Random rng = new Random(seed);
        int chosenWordIndex = rng.nextInt(wordlist.length);
        this.chosenWord = wordlist[chosenWordIndex];
        this.guesses = new ArrayList<>();
        this.wrongGuesses = 0;
    }

    public boolean won() {
        for (int i = 0; i < chosenWord.length(); i++) {
            if (!guesses.contains(chosenWord.charAt(i))) {
                return false;
            }
        }
        return true;
    }

    public boolean lost() {
        return wrongGuesses >= pics.length - 1;
    }

    public void printHangman() {
        System.out.println(pics[wrongGuesses]);
    }

    public void printLetters() {
        for (int i = 0; i < chosenWord.length(); i++) {
            char letter = chosenWord.charAt(i);
            if (guesses.contains(letter)) {
                System.out.print(letter + " ");
            } else {
                System.out.print("_ ");
            }
        }
        System.out.println();
    }

    public boolean guess(char letter) {
        if (guesses.contains(letter)) {
            System.out.println("You already guessed that letter!");
            return false;
        }

        guesses.add(letter);

        if (!chosenWord.contains(String.valueOf(letter))) {
            wrongGuesses++;
        }
 
        return true;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter seed: ");
        while (!scanner.hasNextLong()) {
            System.out.print("Invalid input. Enter a valid seed: ");
            scanner.next(); // consume the invalid input
        }
        long seed = scanner.nextLong();

        HangmanProgram hangman = new HangmanProgram(seed);

        while (!hangman.won() && !hangman.lost()) {
            System.out.println();
            hangman.printHangman();
            hangman.printLetters();

            System.out.print("Guess a letter: ");
            String input = scanner.next();

            if (input.length() != 1 || !Character.isLetter(input.charAt(0))) {
                System.out.println("Invalid input. Please enter a single letter.");
                continue;
            }

            char guess = Character.toLowerCase(input.charAt(0));

            hangman.guess(guess);
        }

        System.out.println();
        hangman.printHangman();
        hangman.printLetters();

        if (hangman.won()) {
            System.out.println("YOU GOT IT!");
        } else {
            System.out.println("Better luck next time!");
        }

        scanner.close();
    }
}