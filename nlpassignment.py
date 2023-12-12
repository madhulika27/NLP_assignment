import random
import nltk
nltk.download('brown')
from nltk.corpus import brown

def scramble_word(word):
    letters = list(word.lower())
    random.shuffle(letters)
    scrambled = ''.join(letters)
    while scrambled == word.lower():
        random.shuffle(letters)
        scrambled = ''.join(letters)
    return scrambled

def word_scrambler_game():
    num_letters = int(input("Enter the initial length of words you want to guess: "))
    score = 0
    length_changed = False
    prev_score_for_change = 0

    while True:
        if score - prev_score_for_change >= 15 and not length_changed:
            new_length = int(input("Wow, you are too good at this! Want to have a go at some bigger words? Enter the new length of words: "))
            if new_length > num_letters:
                num_letters = new_length
                length_changed = True
                prev_score_for_change = score

        if score - prev_score_for_change >= 15 and (length_changed or input("Do you want to increment the word size? (y/n): ").lower() == 'y'):
            new_length = int(input("Wow, you are too good at this! Want to have a go at some bigger words? Enter the new length of words: "))
            if new_length > num_letters:
                num_letters = new_length
                length_changed = True
                prev_score_for_change = score

        words = brown.words()
        possible_words = [word for word in words if len(word) == num_letters and word.islower()]
        word_freq = nltk.FreqDist(possible_words)
        total_words = len(possible_words)

        random_word = random.choice(possible_words)
        scrambled = scramble_word(random_word)

        print(f"Scrambled word: {scrambled}")

        attempts = 0
        correct = False

        example_sent_1 = None
        example_sent_2 = None

        while attempts < 3:
            user_guess = input("Enter your guess (or '0' to quit): ").lower()

            if user_guess == '0':
                print(f"Your final score is: {score}")
                return

            if user_guess == random_word:
                score += max(0, 3 - attempts)
                print(f"Correct guess! You get {max(0, 3 - attempts)} points.")
                correct = True
                break
            else:
                if attempts == 0:
                    print("Incorrect guess! Here's a sentence where the word is used:")
                    sentences = brown.sents(categories='news')
                    for sent in sentences:
                        if random_word in sent and (not example_sent_1 or random_word not in example_sent_1):
                            example_sent_1 = ' '.join(sent)
                            print(example_sent_1.replace(random_word, '*' * len(random_word)))
                            break
                elif attempts == 1:
                    print("Incorrect guess again! Here's another example sentence:")
                    for sent in sentences:
                        if random_word in sent and (not example_sent_2 or random_word not in example_sent_2) and random_word not in example_sent_1:
                            example_sent_2 = ' '.join(sent)
                            print(example_sent_2.replace(random_word, '*' * len(random_word)))
                            break

                print("Try again.")
                attempts += 1

        if not correct:
            print(f"Sorry, you didn't guess the word. The correct answer was: {random_word}")
            score -= 1  
            if score < 0:
                score = 0

# Start the game
word_scrambler_game()
