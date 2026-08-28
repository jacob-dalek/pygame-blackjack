from blackjack import Entity

SUITS = ['C', 'D', 'H', 'S']
FACE_VALUES = ['Q','J','K','A']
VALUES = [2,3,4,5,6,7,8,9,10]

WIDTH = 640
HEIGHT = 320

BLACKJACK = 21


# def card_logic(value, entity: Entity):        
#         if value not in FACE_VALUES:
#             return value
#         if value == 'A':
#             entity.ace_count += 1
#             return 11
        
#         else:
#             return 10

# def ace_logic(entity: Entity):
#     while (entity.ace_count > 0 and entity.value > 21):
#         entity.ace_count -= 1
#         entity.value -= 10