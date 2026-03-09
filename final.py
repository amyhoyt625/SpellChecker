# Amy Hoyt
# Prof. Fanaei
# EECE 2140
# Final Project, Prompt 3: Spell Checker


# Logic of the Application

#SpellChecker class for the different correction functions
class SpellChecker:
    def __init__(self, dictionary_file, text_file):
        """Initialize the SpellChecker with dictionary and text files."""
        self.dictionary = self.load_dictionary(dictionary_file)
        self.text = self.load_text(text_file)

    def load_dictionary(self, filename):
        '''Loads the dictionary from a text file'''
        # Opens the file in read mode 
        with open(filename, 'r') as file:
            # Converts words to lower case and removes white space 
            return set(word.strip().lower() for word in file)

    def load_text(self, filename):
        '''Loads the text file to be checked'''
        # Opens the file in read mode 
        with open(filename, 'r') as file:
            # Converts words to lower case and removes white space
            return [word.strip().lower() for word in file.read().split()]

    def single_transpositions(self, word):
        '''Generates and filters single transpositions (letter switches) of adjacent letters in a word'''
        # Initializes a list of valid transpositions
        transpositions = []
        # Loops through all letters within the word (-1 to accommodate for i + 1)
        for i in range(len(word) - 1):
            # Makes word into a list
            swapped = list(word)
            # Switches the letters within the list
            swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
            # Creates the new word from the swapped list
            new_word = ''.join(swapped)
            # Adds to transpositions only if it's in the dictionary
            if new_word in self.dictionary:
                transpositions.append(new_word)
        return transpositions

    def double_letters(self, word):
        '''Generates and filters replacements for double letters'''
        # Initializes a list of valid words
        doubles = []
        # Loops through all letters in the word (-1 to accommodate for i + 1)
        for i in range(len(word) - 1):
            # Checks if the letter at position i and i + 1 are the same
            if word[i] == word[i + 1]:
                # Creates the new word with one of the duplicate letters removed
                new_word = word[:i] + word[i + 1:]
                # Adds to doubles only if it's in the dictionary
                if new_word in self.dictionary:
                    doubles.append(new_word)
        return doubles

    def character_replacements(self, word):
        '''Replaces each character in the word with every other character in the alphabet'''
        # Initializes a list of words
        replacements = []
        # Makes alphabet variable
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        # Loops through all letters within a word
        for i in range(len(word)):
            # Loops through all characters within the alphabet
            for char in alphabet:
                # Checks if the ith element of the word is the same as the current char in the alphabet
                if word[i] != char:
                    # If not the same create the new word with the char added in 
                    new_word = word[:i] + char + word[i + 1:]
                    # If the new word is in the dictionary it is appended to replacements  
                    if new_word in self.dictionary:
                        replacements.append(new_word)
        return replacements

    def missing_letters(self, word):
        '''Inserts each letter of the alphabet at every position in the word'''
        # Initializes a list of words
        missing = []
        # Makes alphabet variable
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        # Loops through all letters within a word, (+1 to consider inserting at the end of the word)
        for i in range(len(word) + 1): 
            # Loops through all characters within the alphabet
            for char in alphabet:
                # Create the new word with the char added in 
                new_word = word[:i] + char + word[i:]
                # If the new word is in the dictionary it is appended to missing
                if new_word in self.dictionary:
                    missing.append(new_word)
        return missing

    def suggest_corrections(self, word):
        '''Suggests corrections for a given misspelled word'''
        # Initializes a set of words
        corrections = set()
        # Use each of the functions above to make corrections by
        # checking the misspelled word's corrections to the dictionary
        corrections.update(self.single_transpositions(word))
        corrections.update(self.double_letters(word))
        corrections.update(self.character_replacements(word))
        corrections.update(self.missing_letters(word)) 
        return corrections

    def spell_check(self, text):
        '''Checks each word in the text file against the dictionary'''
        # Loops through all the words in the given file 
        for word in text:
            # Checks if word isn't in the dictionary (aka misspelled)
            if word not in self.dictionary:
                # Uses suggestions function to find corrections for the misspelled word
                suggestions = self.suggest_corrections(word)
                # Checks if there is a suggestion for the misspelled word
                if suggestions:
                    print(f"Misspelled word: {word}. Did you mean: {', '.join(suggestions)}?")
                else:
                    print(f"Misspelled word: {word}. No suggestions available.")

# Example files to be used
# Create a "dictionary.txt" file with correctly spelled words  
with open('dictionary.txt', mode='w') as words_file: 
    words_file.writelines(['apple\n', 'default\n', 'engineer\n', 'example\n', 'gold\n', 'deer\n', 'dear\n'])

# Create a "words_example1.txt" file with correctly and incorrectly spelled words
with open('words_example1.txt', mode='w') as words_file: 
    words_file.writelines(['engineer\n', 'enginneer\n','xample\n', 'example\n', 'aple\n', 'depr\n' , 'gipd\n', 'djkbvjia\n'])

# Create a "words_example2.txt" file with correctly and incorrectly spelled words
with open('words_example2.txt', mode='w') as words_file: 
    words_file.writelines(['default\n','edfault\n', 'dfeault\n', 'deafult\n', 'defalut\n', 'defautl\n'])

# User interface
def main():
    '''main fucntion for user input and execution'''
    # Prompt the user for file names
    dictionary_file = input("Enter the name of the dictionary file (with .txt): ").strip()
    text_file = input("Enter the name of the text file to check (with .txt): ").strip()

    # Load the dictionary and text
    try:
        spell_checker = SpellChecker(dictionary_file, text_file)
        print("Starting spell check...")
        spell_checker.spell_check(spell_checker.text)
    except FileNotFoundError as e:
        print(f"Error: {e}. Please make sure the file exists and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Main function for user interface
# Ensures that the main function main() runs only when the script is executed directly 
if __name__ == "__main__":
    main()


