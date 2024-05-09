from game import event
import random
from game.combat import Combat
from game.combat import Panda
from game.display import announce
import game.config as config

class WildPanda (event.Event):
    '''
    A combat encounter with a wild Panda
    When the event is drawn, creates a combat encounter with a single wiold panda, kicks control over to the combat code to resolve the fight.
    The panda is "edible", which is modeled by increasing the ship's food by 5 per panda appearing and adding an apropriate message to the result.
        Since food is good, the event only has a 50% chance to add itself to the result.
    '''

    def __init__ (self):
        self.name = " Panda attack"

    def process (self, world):
        result = {}
        result["message"] = "the panda was defeated! ...Those look pretty tasty!"
        monsters = []
        n_appearing = 1
        n = 1
        while n <= n_appearing:
            monsters.append(Panda("Wild Panda "+str(n)))
            n += 1
        announce ("The crew is attacked by a wild Panda!")
        Combat(monsters).combat()
        if random.randrange(2) == 0:
            result["newevents"] = [ self ]
        else:
            result["newevents"] = [ ]
        config.the_player.ship.food += n_appearing*5

        return result