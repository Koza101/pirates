#Falling rock event to take place at rock face of onin island, no effect on crew. Exists for dramatic effect.

from game import event

class FallingRocks (event.Event):
    '''Some padding for ship-board events. Does nothing but print a message about nothing happening, then adds itself to the new events result'''

    def __init__ (self):
        self.name = " Some rocks have fallen from above"

    def process (self, world):
        result = {}
        result["message"] = "Some rocks are falling from above the cliff face\nThankfully they pose no threat"
        result["newevents"] = [ self ]
        return result
