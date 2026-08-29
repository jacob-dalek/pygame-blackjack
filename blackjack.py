import pygame
import random
import os
from package.constants import * # constant dependency package. although polutting file namespace with constant scores may cause issues...

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()  # Initialize the clock object

class Card:
    def __init__(self, score, suit, size):
        self.score = score
        self.suit = suit
        self.size = size 

    def get_image_url(self):
        card = f"{os.getcwd()}/cards/{self.score}-{self.suit}.png" 
        return card

    def __repr__(self): # not __str__ weird dundee methods 
        return f"{self.score} {self.suit}"

class Card_GUI:
    def __init__(self, card_size=90, card_x=0, card_y=200):
        self.card_size = card_size
        self.card_x = card_x 
        self.card_y = card_y
        self.card_scale = (90,90)

    def get_card(self, card: Card):
        image = pygame.image.load(card.get_image_url())
        image = pygame.transform.scale(image, self.card_scale) # looks dodgy
        return image

class Entity:
    def __init__(self):
        self.card_gui = Card_GUI()
        self.score = 0
        self.hand = []
        self.ace_count = 0

    def display_hand(self):
            card_pos_x = 0
            # self.card_y -=self.card_size
            for card in self.hand:
                if (self.card_gui.card_x > WIDTH-60): # will need alternative resolution logic
                    self.card_gui.card_x = 0
                    self.card_gui.card_y -= self.card_gui.card_size
    
                image = self.card_gui.get_card(card)
                
                screen.blit(image, (card_pos_x, self.card_gui.card_y))
    
                card_pos_x += self.card_gui.card_size

    def card_logic(self, card):        
        if card.score == 'A':
            self.ace_count += 1
            return 11
        if card.score not in FACE_VALUES:
            return card.score
        else:
            return 10

    def ace_logic(self):
        while (self.ace_count > 0 and self.score > 21):
            self.ace_count -= 1
            self.score -= 10

    # def output_hand(self, card_gui: Card_GUI): # defualt arg not great there is a better way of handling data surely
    #     card_gui.display_hand()

    def hand_sum(self):
        if not self.hand and len(self.hand) < 1:
            return self.score
        sum = 0
        for card in self.hand: # will need to debug
            sum += self.card_logic(card)
        self.score = sum

        self.ace_logic()

        return self.score


class Dealer(Entity):

    def __init__(self):
        super().__init__() 

        self.card_gui = Card_GUI(card_x=20, card_y=0) # magic numbers still dont understand the offset it starts from the top left 

    def conceal_cards(self): # mediocre naming 
            card_pos_x = 0
            for index, card in enumerate(self.hand):
                coordinate = (card_pos_x, self.card_gui.card_y)

                if (self.card_gui.card_x > WIDTH-60): # will need alternative resolution logic
                    self.card_gui.card_x = 0
                    self.card_gui.card_y -= self.card_gui.card_size
    
                image = self.card_gui.get_card(card)
    
                if (index > 0):
                    image = pygame.image.load(CARD_BACK)
                    image = pygame.transform.scale(image, self.card_gui.card_scale) 
                    screen.blit(image, coordinate)
    
                screen.blit(image, coordinate)

                card_pos_x += self.card_gui.card_size


    def give_card(self, entity: Entity, deck: list[Card]):
        if entity.hand_sum() >= BLACKJACK:
            return
        pygame.mixer.music.load(f"{CURR_DIR}/package/audio/card_hit.ogg") # this is not mine this is from FNV!!!
        entity.hand.append(deck.pop(0))
        pygame.mixer.music.play(0)

    def reveal_card(self):
        self.hand[0]

    def output_hand(self):
        self.card_gui.display_hand()

    def logic(self, deck: list[Card], player: Entity):
        if (self.score == 17):
            return self.score
        if (self.score < 16 and player.score > 18 and player.score < 21 ):
            # delay = pygame.time.delay(delay * 1000) # 1 second == 1000 milliseconds
            self.hand.append(deck.pop(0))

        while (self.score != BLACKJACK and player.score == BLACKJACK):
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

    # def user_input(self, deck):
    #     keys = pygame.key.get_pressed()
    #     hit = pygame.K_SPACE
    #     stand = pygame.K_n



    #     if hit and not self.is_bust(self.player): # hit
    #         self.dealer.give_card(self.player, deck)
            

    #     if stand: # stand
    #         self.dealer.display_hand()
    #         self.dealer.logic(deck, self.player)
    #         pygame.display.update()
    #         clock.tick(5.0)


    def is_draw(self) -> bool:
        return True if (self.player.score == self.dealer.score) else False
    def is_bust(self, entity: Entity) -> bool:
        return True if (entity.score > BLACKJACK) else False
    def is_blackjack(self, entity: Entity) -> bool:
        return True if(entity.score == BLACKJACK) else False 



    def win_logic(self):
        player_score = self.player.score
        dealer_score = self.player.score

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

        self.dealer.display_hand()


    @staticmethod
    def init_deck(deck: list[Card]):
        for suit in SUITS:
            for score in FACE_VALUES + VALUES:
                deck.append(Card(score, suit, 90))
        random.shuffle(deck)

    
    
    def run(self): 
        deck: list[Card] = []
        Blackjack.init_deck(deck)
        running = True

        self.dealer.deal_cards(self.player, deck)

        is_stand_flag = False
        while running:

            hit = pygame.K_SPACE
            stand = pygame.K_n

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == hit and not self.is_bust(self.player) and not is_stand_flag:
                        self.dealer.give_card(self.player, deck)
                        print("Hello world?")

                    if event.key == stand:
                        self.dealer.logic(deck, self.player)
                        pygame.display.update()
                        clock.tick(5.0)
                        is_stand_flag = True

            self.player.hand_sum()
            self.dealer.hand_sum() # need a dnry here

            screen.fill((50,225,10))

            self.dealer.conceal_cards()
            self.player.display_hand()


            if is_stand_flag:
                self.dealer.display_hand()
                pygame.display.update()
                clock.tick(5.0)
            else:
                pygame.display.update()
                clock.tick(5.0)



            # self.dealer.output_hand()

            # self.win_logic() 


            # self.dealer.output_card(Card_GUI(self.dealer), card_x=200, card_y=100) # this needs to be worked on holy
            # self.dealer.output_hand(self.dealer.card_gui)
            
            # pygame.display.flip()
        pygame.display.update()
        clock.tick(5.0)


            # self.player.output_card(Card_GUI(self.player)) # this needs to be worked on holy
            
            

if __name__ == "__main__":
    blackjack = Blackjack(Entity(), Dealer())
    blackjack.run()