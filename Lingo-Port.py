import pygame
import sys
import random
import pickle
from buttonClass import *

def loadWordlist(filename='words.txt'):
    retval =[]
    with open(filename,'r') as f:
        for line in f:
            retval.append(line.strip())

    return retval


def loadDictionary(filename='dictionary.txt'):
    #use text file so we can make edits to dictionary
    with open("dictionary.txt",'r') as f:
        return f.read().splitlines()


pygame.init()

# Constants

WORDS = random.shuffle(loadWordlist())
DICTIONARY = loadDictionary()

#WIDTH, HEIGHT = 633, 900

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.image.load("assets/Starting Tiles.png")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(317, 300))
ICON = pygame.image.load("assets/Icon.png")

pygame.display.set_caption("LINGO!")
pygame.display.set_icon(ICON)

#GREEN = "#6aaa64"
#YELLOW = "#c9b458"
#GREY = "#787c7e"
#OUTLINE = "#d3d6da"
#FILLED_OUTLINE = "#878a8c"

#CORRECT_WORD = 'tests'
#CORRECT_WORD = random.choice(WORDS)
CORRECT_WORD = WORDS.pop() #pop words off to prevent repeat words
CORRECT_GUESSES = [False,False,False,False,False] # Used to track which bonus letter to give
ALPHABET = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
AVAILABLE_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)

SCREEN.fill("white")
SCREEN.blit(BACKGROUND, BACKGROUND_RECT)


pygame.display.update()

LETTER_X_SPACING = 85
LETTER_Y_SPACING = 12
LETTER_SIZE = 75

# Global variables

guesses_count = 0

# guesses is a 2D list that will store guesses. A guess will be a list of letters.
# The list will be iterated through and each letter in each guess will be drawn on the screen.
guesses = [[] for i in range(6)]
current_guess = []
current_guess_string = ""
current_letter_bg_x = 110

# Indicators is a list storing all the Indicator object. An indicator is that button thing with all the letters you see.
indicators = []

game_result = ""



class Letter:
    def __init__(self, text, bg_position):
        # Initializes all the variables, including text, color, position, size, etc.
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, LETTER_SIZE, LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x+36, self.bg_position[1]+34)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(SCREEN, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(SCREEN, FILLED_OUTLINE, self.bg_rect, 3)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        SCREEN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def moveup_row(self):
        if self.bg_y < 100:
            self.delete()
        else:
            self.bg_y -= 100
            self.bg_position = self.bg_x,self.bg_y
            self.bg_rect = (self.bg_position[0], self.bg_y, LETTER_SIZE, LETTER_SIZE)
            self.text_position = (self.bg_x+36, self.bg_position[1]+34)
            self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
            self.text_rect = self.text_surface.get_rect(center=self.text_position)
            self.draw()

    def delete(self):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(SCREEN, "white", self.bg_rect)
        pygame.draw.rect(SCREEN, OUTLINE, self.bg_rect, 3)
        pygame.display.update()


def check_guess(guess_to_check):
    # Goes through each letter and checks if it should be green, yellow, or grey.
    global DICTIONARY, current_guess, current_guess_string, guesses_count, current_letter_bg_x, game_result,CORRECT_GUESSES,guesses
    game_decided = False
    if current_guess_string.lower() in DICTIONARY:
        LEFT_OVER = [i for i in CORRECT_WORD] # convert string to a list of characters to allow for deletion
        for i in range(5):
            #check for green letters
            lowercase_letter = guess_to_check[i].text.lower()

            if lowercase_letter in CORRECT_WORD:
                if lowercase_letter == CORRECT_WORD[i]:
                    CORRECT_GUESSES[i] = True #Used to keep track of bonus letters
                    LEFT_OVER[i] = ''
                    guess_to_check[i].bg_color = GREEN
                    guess_to_check[i].text_color = "white"
                    if not game_decided:
                        game_result = "W"
        for i in range(5):
            if guess_to_check[i].bg_color != GREEN:
                lowercase_letter = guess_to_check[i].text.lower()
                try:
                    index = LEFT_OVER.index(lowercase_letter)
                except ValueError:
                    index = -1
                if index >= 0:
                    # letter exists in the word but in wrong place
                    LEFT_OVER[index] = ''
                    print(LEFT_OVER)

                    guess_to_check[i].bg_color = YELLOW
                    # for indicator in indicators:
                    #     if indicator.text == lowercase_letter.upper():
                    #         indicator.bg_color = YELLOW
                    #         indicator.draw()
                    guess_to_check[i].text_color = "white"
                    game_result = ""
                    game_decided = True
                else:
                    game_result = ""
                    game_decided = True
                
        
            guess_to_check[i].draw()
            pygame.display.update()

    else:
        for i in range(5):
            guess_to_check[i].bg_color = RED
            guess_to_check[i].text_color = "white"
            guess_to_check[i].draw()
            pygame.display.update()


    guesses_count += 1
    current_guess = []
    current_guess_string = ""
    current_letter_bg_x = 110
    if guesses_count == 6 and game_result == "":
        SCREEN.fill("white")
        SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
        for button in buttons:
            button.draw(SCREEN)

        guesses_count -=1
        for guess in guesses:
            for letter in guess:
                letter.moveup_row()

def play_again():
    # Puts the play again text on the screen.
    pygame.draw.rect(SCREEN, "white", (10, 600, 1000, 600))
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
    play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 700))
    word_was_text = play_again_font.render(f"The word was {CORRECT_WORD}!", True, "black")
    word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 650))
    SCREEN.blit(word_was_text, word_was_rect)
    SCREEN.blit(play_again_text, play_again_rect)
    pygame.display.update()

def button_hint(params):
    next_letter = 0
    if CORRECT_GUESSES.count(False) > 1:    
        # don't give clue if only 1 letter is unknown
        for i in range(5):
            if CORRECT_GUESSES[i] == False:
                next_letter = i
                break
        new_letter = Letter(CORRECT_WORD[next_letter].upper(), (current_letter_bg_x+next_letter*LETTER_X_SPACING, guesses_count*100+LETTER_Y_SPACING))
        new_letter.draw()
        CORRECT_GUESSES[next_letter] = True


def button_reset(params):
    global game_result
    game_result = "L"

def reset():
    # Resets all global variables to their default states.
    global guesses_count, CORRECT_WORD, guesses, current_guess, current_guess_string, game_result,CORRECT_GUESSES
    SCREEN.fill("white")
    SCREEN.blit(BACKGROUND, BACKGROUND_RECT)
    guesses_count = 0
    #CORRECT_WORD = random.choice(WORDS)
    CORRECT_WORD = WORDS.pop() #pop words off to prevent repeat words
    #CORRECT_WORD = 'TESTS'
    guesses = [[] for i in range(6)]
    current_guess = []
    current_guess_string = ""
    game_result = ""
    CORRECT_GUESSES = [False,False,False,False,False]
    for button in buttons:
        button.draw(SCREEN)
    pygame.display.update()
    button_hint(None)


def create_new_letter(key_pressed):
    # Creates a new letter and adds it to the guess.
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, guesses_count*100+LETTER_Y_SPACING))
    current_letter_bg_x += LETTER_X_SPACING
    guesses[guesses_count].append(new_letter)
    current_guess.append(new_letter)
    for guess in guesses:
        for letter in guess:
            letter.draw()

def delete_letter():
    # Deletes the last letter from the guess.
    global current_guess_string, current_letter_bg_x
    guesses[guesses_count][-1].delete()
    guesses[guesses_count].pop()
    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_letter_bg_x -= LETTER_X_SPACING


    
buttons = []
buttons.append(Button(40,740,100,40,text="Hint",color=CYAN,highlightcolor=NEONPINK,function=button_hint))
buttons.append(Button(180,740,100,40,text="Give Up",color=ORANGE,highlightcolor=NEONPINK,function=button_reset))

for button in buttons:
    button.draw(SCREEN)
button_hint(None)
pygame.display.update()

while True:
    if game_result != "":
        play_again()
    for button in buttons:
        button.update(pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_result != "":
                    reset()
                else:
                    if len(current_guess_string) == 5:
                        check_guess(current_guess)
                        # draw the all the letters that are already correct
                        for i in range(5):
                            if CORRECT_GUESSES[i] == True:
                                new_letter = Letter(CORRECT_WORD[i].upper(), (current_letter_bg_x+i*LETTER_X_SPACING, guesses_count*100+LETTER_Y_SPACING))
                                new_letter.draw()

        
            elif event.key == pygame.K_BACKSPACE:
                if len(current_guess_string) > 0:
                    delete_letter()
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                    if len(current_guess_string) < 5:
                        create_new_letter(key_pressed)
        elif event.type  == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            for button in buttons:
                if button.pressed(mousePos):
                    button.function(button.params)
            pygame.display.update()
