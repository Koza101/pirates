
from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
import random
from game import event

class FeudalIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "feudal island"
        self.symbol = 'F'   #How island is represented on map
        self.visitable = True
        self.starting_location = Rock_Face(self)
        self.locations = {}
        self.locations["Rock Face"] = self.starting_location
        self.locations["Abandoned Temple"] = AbandonedTemple(self)
        self.locations["Temple Interior"] = TempleInterior(self)
        self.locations["Stone Cave"] = StoneCave(self)
        self.locations["Stone Cave Interior"] = StoneCaveInterior(self)
        self.locations["Bamboo Forrest"] = BambooForrest(self)
        self.locations["Decrepit Village"] = DecrepitVillage(self)
        

    def enter (self, ship):
        print ("You sail upon a rocky island.\nDo you want to go ashore?")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Rock_Face (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Rock Face"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.append (bugs.Bugs())
        self.events.append(falling_rocks.FallingRocks())

    def enter (self):
        announce ("Arrived at the Rock Face. Your ship is at anchor while the waves slam it relentlessly against the sheer rocks.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Abandoned Temple"]
        elif (verb == "east" or verb == "west"):
            announce ("Your only option is to head north onto the face, thankfully there is a passage reachable from the deck of your ship")


class AbandonedTemple (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Abandoned Temple"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['explore'] = self
        self.verbs['exit'] = self
        self.templedoor = False
        #Specify the chance of an event happening, number represents a percentage
        self.event_chance = 0
        #Add events that may be encountered
        

    def enter (self):
        description = "You come across an abandoned temple constructed of stone and bamboo.\nYou could explore it for treasure."
        announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["Rock Face"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Decrepit Village"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["Stone Cave"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Bamboo Forrest"]
        elif (verb == "explore"):
            #Tried adding a while loop here for after the temple has already been explored. Game would freeze when implemented.
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations["Temple Interior"]

class TempleInterior(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Temple Interior"
        self.verbs['exit'] = self
        self.verbs['leave'] = self
        self.verbs['yes'] = self
        self.verbs['no'] = self
        self.verbs['approach'] = self
        self.verbs['enter'] = self

        self.event_chance = 0
        self.events.append(arrow_trap.ArrowTrap())  # added into init file for events

        # Initialize blackjack related attributes
        self.deck = self.create_deck()
        self.templedoor = False  #Tried making explore option unavailable after exploring the first time

    def enter(self):
        description = "You enter into the temple exploring its narrow hallways and corridors.\nYour crew comes across a cloaked man sitting in front of two grand doors. Do you want to approach?"
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb in ["exit", "leave"]:
            config.the_player.next_loc = self.main_location.locations["Abandoned Temple"]
            config.the_player.go = True
        elif (verb == "yes" or verb == "play again"):
            self.HandleTemple()
        elif (verb == "no"):
            print("You choose to leave the man alone.")

    def HandleTemple(self):
        print("As you approach the cloaked man he lays out a set of cards. Two face up for you and each member of your crew. He has a card face up and face down for himself.")
        print("You recognize the orientation of the cards. It's blackjack.\n")
        choice = input("Do you wish to play? [yes/no] ")
        if choice.lower() == "yes":
            self.HandleGame()
        else:
            print("You leave the cloaked man. He silently picks up the deck as you move away.")

    def create_deck(self):
        card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        return [(card, category) for category in card_categories for card in cards_list]
    
    def card_value(self, card):
        if card[0] in ['Jack', 'Queen', 'King']:
            return 10
        elif card[0] == 'Ace':
            return 11
        else:
            return int(card[0])
        
    def deal_initial_cards(self):
        return [self.deck.pop(), self.deck.pop()]
    
    def calculate_score(self, cards):
        return sum(self.card_value(card) for card in cards)

    def HandleGame(self):
        while True:
            random.shuffle(self.deck)
            player_cards = self.deal_initial_cards()
            dealer_cards = self.deal_initial_cards()

            while True:
                player_score = self.calculate_score(player_cards)
                print("Your cards: {}, score: {}".format(player_cards, player_score))
                if player_score > 21:
                    print("Bust! You lose.")
                    break
                choice = input("would you like another card? [hit/stand] ").lower()
                if choice == "hit" or choice == "yes":
                    player_cards.append(self.deck.pop())
                    print("You motion to hit.")
                else:
                    print("You motion to stand.")
                    break

            if player_score > 21:
                if not self.ask_play_again("Busted! Do you wish to try again? [yes/no]"):
                    break
            else:
                while self.calculate_score(dealer_cards) < 17:
                    dealer_cards.append(self.deck.pop())
                dealer_score = self.calculate_score(dealer_cards)
                print("Dealer's cards: {}, score: {}".format(dealer_cards, dealer_score))

                if dealer_score > 21 or player_score > dealer_score:
                    print("You win! You turn your attention to the doors which are beginning to move. You glance back at where the man was sitting, but he has seemingly disappeared into thin air!")
                    self.templedoor = True
                    self.TempleDoor()
                    break
                elif dealer_score == player_score:
                    if not self.ask_play_again("It's a tie! Do you wish to try again? [yes/no] "):
                        break
                else:
                    if not self.ask_play_again("Dealer wins! Do you wish to try again? [yes/no] "):
                        break

    def ask_play_again(self, message):
        while True:
            choice = input(message).lower()
            if choice == "yes":
                return True  # Continue the game
            elif choice == "no":
                print("You decide to step away from the game.")
                return False  # Exit the game loop
            else:
                print("Invalid choice. Please answer 'yes' or 'no'.")

    def TempleDoor(self):
        print("You approach the now open doors to discover a Katana on display. It seems to belong to that of a great shogun warrior.")
        print("You take the sword from it's pedistal. It is a pristine and magnificent weapon. There must be more left behind on this island.")

        config.the_player.add_to_inventory([Katana()])


class Katana(Item):
    #A better cutlass
    def __init__(self):
        super().__init__("Katana", 500)
        self.damage = (20, 100) #First value verb, second value verb2
        self.skill = "swords"
        self.verb = "stab"
        self.verb2 = "slash"
   
        






        #Need to add option to enter?
        
        # if verb == "take":
        #     if self.item_in_temple == None and self.item_in_clothes == None:
        #         announce ("You don't see anything to take.")
        #     elif len(cmd_list) > 1:
        #         at_least_one = False #Track if you pick up an item, print message if not.
        #         item = self.item_in_temple
        #         if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
        #             announce ("You take the "+item.name+" from the temple.")
        #             config.the_player.add_to_inventory([item])
        #             self.item_in_temple = None
        #             config.the_player.go = True  #Manually setting go to True to make time pass
        #             at_least_one = True
        #         item = self.item_in_clothes
        ##         if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
        ##             announce ("You pick up the "+item.name+" out of the pile of clothes. ...It looks like someone was eaten here.")
        ##             config.the_player.add_to_inventory([item])
        ##             self.item_in_clothes = None
        ##             config.the_player.go = True
        ##             at_least_one = True
        ##         if at_least_one == False:
        ##             announce ("You don't see one of those around.")
        



#New locations added after this line:

class BambooForrest (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Bamboo Forrest"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['take'] = self
        
        self.event_chance = 0
        self.item_in_tree = Tanto()
        self.item_in_clothes = None

    def enter (self):

        edibles = False
        for e in self.events:
            if isinstance(e, Panda.WildPanda):
                edibles = True
        #The description has a base description, followed by variable components.
        description = "You stumble into a dense forrest composed entirely of bamboo.\n You notice multiple overgrown paths through the stalks."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_tree != None:
            description = description + " You see a " + self.item_in_tree.name + " stuck in a stalk of bamboo "
            announce (description)



        #Prompt to explore or go somewhere else??


    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["Abandoned Temple"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Decrepit Village"]
        elif (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["Rock Face"]
        #Need option to explore
        if (verb == "take"):
            if self.item_in_tree == None and self.item_in_clothes == None:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "item"):
                    announce ("You take the "+item.name+" from the tree.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True  #Manually setting go to True to make time pass
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the "+item.name+" out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")
                    

class Tanto(Item):
    def __init__(self):
        super().__init__("tanto knife", 400)
        self.damage = (10, 40)
        self.skill = "swords"
        self.verb = "swipe"
        self.verb2 = "stab"




class StoneCave (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Stone Cave Entrance"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['enter'] = self
        self.verbs['west'] = self
        self.verbs['exit'] = self
        self.event_chance = 0

    def enter (self):
        
        description = "You find a cave carved out of the stone that makes up the island.\nIt appears to be signifigant with stone statues guarding the entrance.\nDo you wish to enter or move on?"
        announce (description)


    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Abandoned Temple"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Decrepit Village"]
        elif (verb == "South"):
            config.the_player.next_loc = self.main_location.locations["Rock Face"]
        #need option to enter cave
        elif (verb == "enter"):
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations["Stone Cave Interior"]
            

class StoneCaveInterior(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Stone Cave Interior"
        self.verbs['exit'] = self
        self.verbs['leave'] = self
        
        self.event_chance = 100
        self.events.append(arrow_trap.ArrowTrap()) #added into init file for events
        
    def enter(self):
        description = "You enter into the stone cave. You notice ancient scripts carved into the stone walls."
        announce(description)
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "exit" or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations["Stone Cave"]
            config.the_player.go = True
            
        
        
            
    #def HandleTemple(self):
        

class DecrepitVillage (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Decrepit Village"
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['investigate'] = self

        self.item_in_house = CeremonialTea()

        self.event_chance = 0

    def enter (self):

        
        #The description has a base description, followed by variable components.
        description = "You come across a small village long in ruin.\n There is one building left standing."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_house != None:
            description = description + " You see a glimmer from within the building. Would you like to investigate? "
            announce (description)

        #Prompt to explore or go somewhere else??

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["Abandoned Temple"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["Stone Cave"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Bamboo Forrest"]
        if (verb == "investigate"):
            announce("You find a lavishly decorated pot among what appears to be a tea set.\nWithin the pot, you discover tea leaves. They seem to be well preserved.")
            item = self.item_in_house
            announce ("You take the "+item.name+" from the pot.")
            config.the_player.add_to_inventory([item])
            self.item_in_house = None
            at_least_one = False
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations["Decrepit Village"]
            if self.item_in_house == None:
                announce ("You don't see anything else to take.")
        

class CeremonialTea(Item):
    def __init__(self):
        super().__init__("ceremonial tea", 50)
