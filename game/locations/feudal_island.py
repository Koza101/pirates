
from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items

class FeudalIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "feudal island"
        self.symbol = 'F'   #This is relevant for developement, need to figure out what
        self.visitable = True
        self.starting_location = Rock_Face(self)
        self.locations = {}
        self.locations["Rock Face"] = self.starting_location
        self.locations["Abandoned Temple"] = AbandonedTemple(self)
        self.locations["Stone Cave"] = StoneCave(self)
        self.locations["Bamboo Forrest"] = BambooForrest(self)
        self.locations["Decrepit Village"] = DecrepitVillage(self)
        

    def enter (self, ship):
        print ("arrived at a rocky island")

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
        announce ("arrive at the Rock Face. Your ship is at anchor while the waves slam it relentlessly against the sheer rocks.")

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

        self.event_chance = 0

    def enter (self):
        description = "You come across an abandoned temple constructed of stone and bamboo"
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
            


#New locations added after this line:

class BambooForrest (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Bamboo Forrest"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        
        self.event_chance = 0

    def enter (self):

        description = "You stumble into a dense forrest composed entirely of bamboo"
        announce (description)



    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Abandoned Temple"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Decrepit Village"]
        elif (verb == "South"):
            config.the_player.next_loc = self.main_location.locations["Rock Face"]
                    

class StoneCave (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Stone Cave"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 0

    def enter (self):
        
        description = "You find a cave carved out of the stone that makes up the island"
        announce (description)


    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Abandoned Temple"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Decrepit Village"]
        elif (verb == "South"):
            config.the_player.next_loc = self.main_location.locations["Rock Face"]
                    

class DecrepitVillage (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Decrepit Village"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 0

    def enter (self):

        description = "You stumble into a village. It has obviously been long abandoned"
        announce (description)



    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Abandoned Temple"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["Stone Cave"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Bamboo Forrest"]