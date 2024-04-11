from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class Bugs (Context, event.Event):
    '''Encounter with an annoying cloud of bugs. Uses the parser to decide what to do about it.'''
    def __init__ (self):
        super().__init__()
        self.name = "Cloud of Bugs"
        self.bugs = 1
        self.verbs['swat'] = self
        self.verbs['ignore'] = self
        self.verbs['cover'] = self
        self.result = {}
        self.go = False

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "ignore"):
            self.go = True
            r = random.randint(1,10)
            if (r < 5):
                self.result["message"] = "the bugs flew away"
                if (self.bugs > 1):
                    self.bugs = self.bugs - 1
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.isLucky() == True):
                    self.result["message"] = "luckily, the bugs weren't interested."
                else:
                    self.result["message"] = c.get_name() + " is attacked by the bugs."
                    if (c.inflict_damage (self.bugs, "Bitten by the bugs")):
                        self.result["message"] = ".. " + c.get_name() + " was bitten by the bugs!"

        elif (verb == "swat"):
            self.bugs = self.bugs + 1
            self.result["newevents"].append (Bugs())
            self.result["message"] = "the bugs have been squashed"
            self.go = True
        elif (verb == "cover"):
            print ("the bugs can't bite you when covered up")
            self.go = False
        else:
            print ("You must do something about the bugs. we can swat, ignore, or cover")
            self.go = False



    def process (self, world):

        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        while (self.go == False):
            print (str (self.bugs) + " bugs have appeared what do you want to do?")
            Player.get_interaction ([self])

        return self.result
