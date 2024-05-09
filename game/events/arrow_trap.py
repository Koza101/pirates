#Booby Trap event to happen in Abandoned Temple Location

from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random


class ArrowTrap (Context, event.Event):
    
    def __init__(self):
        super().__init__()
        self.name = "arrow trap"
        self.traps = 1
        self.verbs['disarm'] = self
        self.verbs['go anyway'] = self
        self.verbs['turn back'] = self
        self.result = {}
        self.go = False
        

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "disarm"):
            self.go = True
            r = random.randint(1,10)
            if (r < 6):
                self.result["message"] = "You successfully disarmed the trap"
                if (self.traps > 1):
                    self.traps = self.traps - 1
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.isLucky() == True):
                    self.result["message"] = "Luckily, the trap wasn't functional"
                else:
                    self.result["message"] = c.get_name() + " took an arrow to the knee!"
                    if (c.inflict_damage (self.traps, "The arrow proved fatal")):
                        self.result["message"] = ".." + c.get_name + "Took a fatal arrow to the knee!"
                        
        elif (verb == "go anyway"):
            self.go = True
            r = random.randint(1,10)
            if (r > 5):
                self.result["message"] = "Thankfully, the trap is so old it no longer functions"
                if (self.traps >= 1):
                    self.traps = self.traps - 1
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.islucky() == True):
                    self.result["message"] = c.get_name() + "Activated the trap but luckily avoided being struck by an arrow."
                else: 
                    self.result["message"] = c.get_name() + " took an arrow to the knee!"
                    if (c.inflict_damage (self.traps, "The arrow proved fatal")):
                        self.result["message"] = ".." + c.get_name + "Took a fatal arrow to the knee!"
                    
        elif (verb == "turn back"):
            self.go = False
            
    def process (self, world):
        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"
        
        while (self.go == False):
            print (str (self.traps) + "You have discovered a trap, what do you want to do?")
            Player.get_interaction ([self])
        
        return self.result