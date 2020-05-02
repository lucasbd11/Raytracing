#from couleurs import couleur

class image:

    def __init__(self, largeur = 1, hauteur = 1):
        self.largeur = largeur
        self.hauteur = hauteur
        #self.pixels = [[couleur(0,0,0) for i in range(hauteur)] for i in range(largeur)]
        self.pixels = [[None for i in range(largeur)] for i in range(hauteur)]
    
    def mettre_couleur(self,x,y,couleur_valeur):
        self.pixels[-(y+1)][x] = couleur_valeur
    
    def write_img(self,file):
        
        def redim_valeur(x): 
            return round(max(min(x,1),0)*255)
        
        
        file.write("P3\n{} {}\n255\n".format(self.largeur,self.hauteur))
        
        
        
        for ligne in self.pixels:
            for pixel in ligne:
                try:
                    file.write("{}\n{}\n{}\n".format(redim_valeur(pixel.r),redim_valeur(pixel.g),redim_valeur(pixel.b)))
                except:
                    print(pixel)
                    print(ligne)
                    print(self.pixels.index(ligne))
                    file.write("{}\n{}\n{}\n".format(redim_valeur(pixel.r),redim_valeur(pixel.g),redim_valeur(pixel.b)))
                    raise "erreur"
            #file.write("\n")
    
        return file