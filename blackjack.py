import pygame
import random
import os

WIDTH = 640
HEIGHT = 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def load_image(self):
        card = f"{os.getcwd()}/cards/{self.value}-{self.suit}.png" 
        image = pygame.image.load(card)
        image = pygame.transform.scale(image,(180,180))
        screen.blit(image,(0,HEIGHT-180))

    def __str__(self):
        return f"{self.value} {self.suit}"

def init_deck(deck: list[Card]):
        suits = ['C', 'D', 'H', 'S']
        values = [2,3,4,5,6,7,8,9,10,'J', 'K', 'Q', 'A'] # pythons weird typecasting
        for suit in suits:
            for value in values:
                deck.append(Card(value, suit))
        random.shuffle(deck)


class Blackjack:

    @staticmethod
    def run(): 
        clock = pygame.time.Clock()  # Initialize the clock object
        deck: list[Card] = []
        init_deck(deck)
        pygame.init()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0,255,0))

            deck[0].load_image()

            pygame.display.flip()
            pygame.display.update()

if __name__ == "__main__":
    Blackjack.run()