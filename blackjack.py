import pygame
import random
import os
from package.constants import * # constant dependency package. although polutting file namespace with constant values may cause issues...

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()  # Initialize the clock object

# class Engine:
#     def __init__(self, width, height, caption="Blackjack"):
#         self.resolution = width, height
#         self.caption = caption
#         self.screen = pygame.display.set_mode(self.resolution)


#     def run(self, running=False, fps=10):
#         pygame.display.set_caption("Blackjack")
#         clock = pygame.time.Clock()  # Initialize the clock object

#         while running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False

#         pygame.display.flip()

#         self.screen.fill((0,255,0))

        
#         clock.tick(fps)
#         pygame.display.update()



class Card:
    def __init__(self, value, suit, size):
        self.value = value
        self.suit = suit
        self.size = size 

    def get_image_url(self):
        card = f"{os.getcwd()}/cards/{self.value}-{self.suit}.png" 
        return card

    def __repr__(self): # not __str__ weird dundee methods 
        return f"{self.value} {self.suit}"

class Card_GUI:
    def __init__(self, entity, card_size=90, card_x=0, card_y=HEIGHT):
        self.entity: Entity = entity
        self.card_size = card_size
        self.card_x = card_x 
        self.card_y = card_y
        self.coordinate = (self.card_size, self.card_size)

    def get_card(self, card: Card):
        image = pygame.image.load(card.get_image_url())
        image = pygame.transform.scale(image, self.coordinate) # looks dodgy
        return image

    def display_hand(self):
        card_pos_x = 0
        self.card_y -=self.card_size
        for url in [card.get_image_url() for card in self.entity.hand]:
            if (self.card_x > WIDTH-60): # will need alternative resolution logic
                self.card_x = 0
                self.card_y -= self.card_size

            image = pygame.image.load(url)
            image = pygame.transform.scale(image, self.coordinate) # looks dodgy
            screen.blit(image, (self.card_x, self.card_y))
            card_pos_x += self.card_size

class Entity:
    def __init__(self, name=""):
        self.value = 0
        self.name = name
        self.hand = []
        self.ace_count = 0

    def card_logic(self, card):        
        if card.value == 'A':
            self.ace_count += 1
            return 11
        if card.value not in FACE_VALUES:
            return card.value
        else:
            return 10

    def ace_logic(self):
        while (self.ace_count > 0 and self.value > 21):
            self.ace_count -= 1
            self.value -= 10

    def output_hand(self, card_gui: Card_GUI): # defualt arg not great there is a better way of handling data surely
        card_gui.display_hand()

    def hand_sum(self):
        if not self.hand and len(self.hand) < 1:
            return self.value
        sum = 0
        for card in self.hand: # will need to debug
            sum += self.card_logic(card)
        self.value = sum

        self.ace_logic()

        return self.value


class Dealer(Entity):
    def __init__(self, name=""):
        super().__init__(name)
        self.card_gui = Card_GUI(self, card_x=200, card_y=100) # magic numbers

    def conceal_cards(self): # mediocre naming 
            card_pos_x = 0
            for index, card in enumerate(self.hand):
                if (self.card_gui.card_x > WIDTH-60): # will need alternative resolution logic
                    self.card_gui.card_x = 0
                    self.card_gui.card_y -= self.card_gui.card_size
    
                image = self.card_gui.get_card(card)
    
                if (index > 0):
                    image = pygame.image.load(CARD_BACK)
                    image = pygame.transform.scale(image, self.card_gui.coordinate) 
                    screen.blit(image, (card_pos_x, self.card_gui.card_y))
    
                screen.blit(image, (card_pos_x, self.card_gui.card_y))

                card_pos_x += self.card_gui.card_size


    def give_card(self, entity: Entity, deck: list[Card]):
        if entity.hand_sum() >= BLACKJACK:
            return

        entity.hand.append(deck.pop(0))

    def reveal_card(self):
        self.hand[0]

    def output_hand(self):
        self.card_gui.display_hand()

    def logic(self, deck: list[Card], player: Entity):
        if (self.value == 17):
            return self.value
        if (self.value < 16 and player.value > 18 and player.value < 21 ):
            self.hand.append(deck.pop(0))

        while (self.value != BLACKJACK and player.value == BLACKJACK):
            if not deck:
                return
             # drains the deck not to sure why needs to ne debugged
            self.hand.append(deck.pop(0))
               
    def deal_cards(self, entity: Entity, deck: list[Card]):
        for _ in range(2):
            self.give_card(self, deck)
            self.give_card(entity, deck)



class Blackjack:
    def __init__(self, player: Entity, dealer: Dealer):
        self.player = player
        self.dealer = dealer

    def user_input(self, deck):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.dealer.give_card(self.player, deck)

        if keys[pygame.K_n]:
            return

        
            

    def win_logic(self):
        player_score = self.player.value
        dealer_score = self.player.value

        # not a fan of the chaining but if it works so be it
        if player_score > dealer_score and player_score < BLACKJACK: 
            print(f"{self.player.name} wins!")
        if dealer_score > player_score and dealer_score < BLACKJACK: 
            print("dealers wins!")
        if player_score == BLACKJACK: 
            print(f"{self.player.name} Blackjack!")
        if dealer_score == BLACKJACK: 
            print(f"dealer Blackjack!")
        if player_score == dealer_score: 
            print("Draw")
        else:
            print("what even is this branch?")

    @staticmethod
    def init_deck(deck: list[Card]):
        for suit in SUITS:
            for value in FACE_VALUES + VALUES:
                deck.append(Card(value, suit, 90))
        random.shuffle(deck)

    
    
    def run(self): 
        deck: list[Card] = []
        Blackjack.init_deck(deck)
        running = True
        self.dealer.deal_cards(self.player, deck)


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.player.hand_sum()
            self.dealer.hand_sum() # need a dnry here

            screen.fill((50,225,10))

            self.user_input(deck)

            # self.dealer.output_card(Card_GUI(self.dealer, card_x=200, card_y=100)) # this needs to be worked on holy


            # print(self.player.hand_sum()) 

            self.dealer.logic(deck, self.player)

            self.dealer.conceal_cards()

            # self.dealer.output_hand()



            # self.win_logic() 


            self.player.output_hand(Card_GUI(self.player)) # this needs to be worked on holy
            # self.dealer.output_card(Card_GUI(self.dealer), card_x=200, card_y=100) # this needs to be worked on holy
            # self.dealer.output_hand(self.dealer.card_gui)
            
            pygame.display.flip()
            clock.tick(5.0)
            pygame.display.update()

            # self.player.output_card(Card_GUI(self.player)) # this needs to be worked on holy
            
            

if __name__ == "__main__":
    blackjack = Blackjack(Entity("Jacob"), Dealer("John"))
    blackjack.run()