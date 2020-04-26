from vecteurs import vecteur

class rayon:
    
    def __init__(self,origine,direction):
       
        self.origine = vecteur(origine[0],origine[1],origine[2])
       
        self.ndirection = direction.normaliser()
        self.direction = direction

    
    
    def __str__(self):
        return f"rayon(ori: ({self.origine.x}, {self.origine.y}, {self.origine.z}),dire: ({self.ndirection.x}, {self.ndirection.y}, {self.ndirection.z}))"
        
    def __repr__(self):
        return f"rayon(ori: ({self.origine.x}, {self.origine.y}, {self.origine.z}),dire: ({self.ndirection.x}, {self.ndirection.y}, {self.ndirection.z}))"
    
    
    
    def __call__(self,t):
        return self.get_pos(t)
    
    def get_pos(self,t):
        return self.origine+t*self.ndirection
    
    