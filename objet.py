from vecteurs import vecteur
from couleurs import couleur
import copy
import math
import matplotlib.pyplot as plt
import numpy as np
from rayons import rayon



class materiel:
    def __init__(self,couleur_obj,type_obj):
        """matériaux possibles: verre ; mat ; métal"""
        
        if not(type_obj in ["verre","mat","métal"]):
            raise TypeError("matériel non connu")
        
        self.couleur_obj = couleur_obj
        self.type_obj = type_obj


class sphere:
    
    def __init__(self,x,y,z,rayon,texture):
        self.position = vecteur(x,y,z)
        self.rayon = rayon
        
        self.texture = texture
    
    def intersection(self,rayon):
        a = rayon.ndirection_decale.prod_scalaire(rayon.ndirection_decale)
        #b = 2*rayon.ndirection.prod_scalaire(rayon.origine-self.position) on pose b = 2d on a donc une équation simplifiée
        d = rayon.ndirection_decale.prod_scalaire(rayon.origine-self.position)
        c = (rayon.origine-self.position).prod_scalaire(rayon.origine-self.position)-self.rayon**2
        
        discriminant = d**2-a*c

        if discriminant >= 0:
            t1 = (-d-math.sqrt(discriminant))/a
            t2 = (-d+math.sqrt(discriminant))/a
            
            if t1 >= 0:
                if abs(t1)>1e3:

                    return False,None,None
                return True,t1,"HORS"
            
            elif t2 >=0:
                if abs(t2)>1e3 or abs(t2)<0.01:

                    return False,None,None
                return True,t2,"DANS"
            
            else:
                return False,None
        else:
            return False,None
    
    
    def normale(self,ray):

        p = ray.origine + ray.ndirection_decale*self.intersection(ray)[1]
        normale = (p-self.position).normaliser()
        return normale
    
    def couleur_inter(self,ray,scene):
        couleur_coef = abs(ray.ndirection_decale.prod_scalaire(self.normale(ray)))
        if self.texture.type_obj == "mat":
            couleur_base = self.texture.couleur_obj         
            return (couleur_base+couleur_base*couleur_coef*2)/3
        
        if self.texture.type_obj == "métal":
            point_contact = ray.origine+ray.ndirection_decale*test_intersection(ray,scene)[2]
            
            normale_obj = self.normale(ray)
            ray.origine = point_contact
            ray.ndirection_decale = ray.ndirection_decale+2*normale_obj
            
            inter = test_intersection(ray,scene)
            
            if inter[0]:
                val_lum = test_lumiere(ray,scene,inter[1],inter[2])
                return (inter[1].couleur_inter(ray,scene)*val_lum+self.texture.couleur_obj*couleur_coef*2)/3
            else:
                return (couleur(0.7,0.7,1)+self.texture.couleur_obj)/2
            
    
    
    def debug_graf(self,rayon,type="DEUX"):
        distance = []
        t = list(np.linspace(-20,20,2000))
        
        for i in t:
            point = rayon.origine+i*rayon.ndirection
            d_temps = math.sqrt((point.x-self.position.x)**2 + (point.y-self.position.y)**2 + (point.z-self.position.z)**2)
            distance += [d_temps-self.rayon]
            #distance += [d_temps]
        
        
        a = rayon.ndirection.prod_scalaire(rayon.ndirection)
        d = rayon.ndirection.prod_scalaire(rayon.origine-self.position)
        
        
        b = 2*rayon.ndirection.prod_scalaire(rayon.origine-self.position) #on pose b = 2d on a donc une équation simplifiée
        c = (rayon.origine-self.position).prod_scalaire(rayon.origine-self.position)-self.rayon**2
        
        discriminant = d**2-a*c

        if discriminant >= 0:
            t1 = (-d-math.sqrt(discriminant))/a
            t2 = (-d+math.sqrt(discriminant))/a
            plt.scatter(t1,0)
            plt.scatter(t2,0)
        
        
        x = np.linspace(-20,20,2000)
        y = a*x**2+b*x+c
        
        if type == "Deux":
            plt.plot(x,y,color="Red")
            plt.plot(t,distance,color="Blue")
        if type == "Bleu":
            plt.plot(t,distance,color="Blue")
        if type == "Rouge":
            plt.plot(x,y,color="Red")          
        plt.show()
    
    
class surface:
    def __init__(self,type,val,texture):
        self.type = type
        self.val = val
        self.texture = texture
    
    def intersection(self,ray):
        
        def test_position(ray):
                position = ray.ndirection_decale.prod_scalaire(self.normale(ray))
                if position < 0:
                    return "HORS"
                else:
                    return "DANS"
        
        if self.type == "x" and ray.ndirection_decale.x != 0:
            t = (self.val-ray.origine.x)/ray.ndirection_decale.x
            
            if abs(t)>1e3 or t<0.01:
                return False,None,None

            if t >= 0:
                return True,t,test_position(ray)

        
        if self.type == "y" and ray.ndirection_decale.y != 0:
            
            t = (self.val-ray.origine.y)/ray.ndirection_decale.y
            
            if abs(t)>1e3 or t<0.01:
                
                return False,None,None
            
            if t >= 0:
                return True,t,test_position(ray)

        
        if self.type == "z" and ray.ndirection_decale.z != 0:
            
            t = (self.val-ray.origine.z)/ray.ndirection_decale.z
            
            if abs(t)>1e3 or t<0.01:
                return False,None,None
            
            if t >= 0:
                return True,t,test_position(ray)
        
        return False,None,None

    def normale(self,ray):
        if self.type == "x":
            return vecteur(1,0,0)
        if self.type == "y":
            return vecteur(0,1,0)
        if self.type == "z":
            return vecteur(0,0,1)
    
    def couleur_inter(self,ray,scene):
        
        t = self.intersection(ray)[1]
        
        if (ray.ndirection_decale.x*t%1 <=0.5) ^ (ray.ndirection_decale.z*t%1 <=0.5):
            r = 0.8
            g = 0.8
            b = 0
        else:
            r = 0
            g = 0.8
            b = 0.8
    
       
        

        
        return couleur(r,g,b)




class lumiere:
    def __init__(self,x,y,z,intensite):
        self.position = vecteur(x,y,z)
        self.intensite = intensite
    
    def illumine(self,ray,scene):
        
        inter = test_intersection(ray,scene)
        
        if inter[0]:
            return 0.2
        else:
            return self.intensite
    
    def intersection(self,ray):
        return False,None,None



def test_lumiere(ray,scene,objet_origine,t):
    
    list_val = []
    for objet in scene:
        if type(objet) == lumiere:
            rayon_lum = rayon((ray.ndirection_decale.x*t+ray.origine.x,ray.ndirection_decale.y*t+ray.origine.y,ray.ndirection_decale.z*t+ray.origine.z),objet.position)
            val = objet.illumine(rayon_lum,scene)
            if val != "Global":
                val = abs(val*ray.ndirection_decale.prod_scalaire(objet_origine.normale(ray)))
            elif val == "Global":
                val = 1
            list_val += [val]
        
    return max(list_val)
        
            
            



def test_intersection(ray,scene):
    scene_obj = copy.copy(scene)
    list_t = [None for i in scene]
    list_posi = [None for i in scene]
    inter = False

    
    for objet_scene_index in range(len(scene_obj)):
        intersect = scene_obj[objet_scene_index].intersection(ray)
        

        if intersect[0]:
            inter = True

            list_t[objet_scene_index] = intersect[1]
            list_posi[objet_scene_index] = intersect[2]
    
    if not(inter):
        return False,None
    
    while None in list_t:
        index = list_t.index(None)
        scene_obj.pop(index)
        list_t.pop(index)
        list_posi.pop(index)
        
    return True,scene_obj[list_t.index(min(list_t))],min(list_t),list_posi[list_t.index(min(list_t))]
    

























    









