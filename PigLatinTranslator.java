// Pig latin translator 
// Create a program that changes your words from english and turns them into pig latin 
// judah benjamin
// kirtan (help me fix the ordering of how the sentences)

import java.util.Scanner;

public class PigLatinTranslator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String input;
// whats printer out when you compile the code
        System.out.println("Enter a sentence ('quit' to quit):");

        do {
            input = scanner.nextLine();

            // Check if the user wants to quit
            if (!input.equals("quit")) {
                // Translate the input sentence and print the result
                String translatedSentence = translateSentence(input);
                System.out.println(translatedSentence);
            }

        } while (!input.equals("quit"));

        scanner.close();
    }

    // Translate a single word to Pig Latin
    static String translateWord(String word) {
        // Convert the word to lowercase for consistent processing
        word = word.toLowerCase();

        // Create a StringBuilder to efficiently build the translated word
        StringBuilder translatedWord = new StringBuilder();

        if (isVowel(word.charAt(0)) || findFirstVowelIndex(word) == -1) {
            // If the word starts with a vowel, simply add "yay" to the end
            translatedWord.append(word).append("yay");
        } else {
            // If the word starts with a consonant, find the index of the first vowel
            int firstVowelIndex = findFirstVowelIndex(word);
            
            // Rearrange the word accordingly and add "ay" at the end
            translatedWord.append(word.substring(firstVowelIndex))
                .append(word.substring(0, firstVowelIndex))
                .append("ay");
        }

        // Convert the translated word from StringBuilder to String
        return translatedWord.toString();
    }

    // Checks if a character is a vowel
    static boolean isVowel(char letter) {
        // Define an array of lowercase vowels
        char[] vowels = {'a', 'e', 'i', 'o', 'u', 'y'};
        
        // Check if the letter is a vowel
        for (char vowel : vowels) {
            if (letter == vowel) {
                return true;
            }
        }
        return false;
    }

    // Finds the index of the first vowel in a word
    static int findFirstVowelIndex(String word) {
        for (int i = 0; i < word.length(); i++) {
            if (isVowel(word.charAt(i))) {
                return i;
            }
        }
        // Return -1 to indicate that no vowel was found
        return -1;
    }

    // Translate an entire sentence to Pig Latin
    static String translateSentence(String sentence) {
        // Split the sentence into individual words
        String[] words = sentence.split(" ");
        
        // Create a StringBuilder to efficiently build the translated sentence
        StringBuilder translatedSentence = new StringBuilder();

        for (String word : words) {
            // Translate each word and append it to the sentence
            translatedSentence.append(translateWord(word)).append(" ");
        }

        // Convert the translated sentence from StringBuilder to String and trim any extra spaces
        return translatedSentence.toString().trim();
    }
}
