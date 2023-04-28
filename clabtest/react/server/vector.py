class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __len__(self) -> int:
        return((self.x**2 + self.y**2)**0.5)

    def get_weighted_magnitude(self):
        # more distance is bad therefore
        # since we prefer to do more horizontal
        # movement and less vertical, give the
        # horizontal component less value 
        # and the vertical component more 
        # value. Then when checking the magnitudes
        # of 2 vectors against each other, a vector that
        # requires big vertical jumps will be considered 
        # as having more distance.
        # these coefficients for the components are decided
        # randomly, and will be continuously tuned to see
        # what works best. There isn't really a science to this
        # so I have to take the gradient descent route and hope
        # I just find a good combo eventually
        weighted_horizontal_component = 0.7 * self.x
        weighted_vertical_component = 1.1 * self.y
        return(((weighted_horizontal_component**2) + (weighted_vertical_component**2))**0.5)
