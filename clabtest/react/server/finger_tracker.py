class Hand:
    def __init__(self):
        self.fingers = {
                        "index" : None,
                        "middle" : None,
                        "ring" : None,
                        "pinky" : None
                        }

    def get_available_fingers(self):
        return([finger 
                if self.fingers[finger] == None 
                for finger in self.fingers.keys()])


    def get_range(self):
        """
        Returns a list of what positions can be played based on where the hand is located. 
        Particularly, this focuses on the position of the index finger.
        """
        available_fingers = self.get_available_fingers()
        # when the index finger currently placed down
        # then your lower bound is 0 as you can just slide your entire
        # hand down
        # and your upper bound is determined by your pinky, which i will say
        # can extend up to 4 frets beyond your current position
        if "index" not in available_fingers:
            lower_bound = 0
            upper_bound = self.fingers["index"].fret + 4
            return([lower_bound, upper_bound])
        


            
            

