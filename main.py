
import sys, os
sys.path.append('/Users/Lucas/Desktop/Dev/raytracing')

import random
from vecteurs import vecteur
from image import image
from couleurs import couleur
from rayons import rayon
import objet
import math

#1/0

def point_sphere_aleatoire(centre):
    r = random.uniform(0,1)
    phi = random.uniform(0,2*math.pi)
    theta = phi = random.uniform(0,math.pi)
    x = math.cos(phi)*math.sin(theta)*r+centre.x
    y = math.sin(phi)*math.sin(theta)*r+centre.y
    z = math.cos(theta)*r+centre.z
    
    return vecteur(x,y,z)




def couleur_rayon(ray,scene,CAMERA,level=10):
    
        if level <= 0:
            #print("ok")
            return couleur(0,0,0)

        objet_scene = objet.test_intersection(ray,scene,CAMERA)
        

        
        if objet_scene[0]:

            t = objet_scene[2]

            if objet_scene[3] == "DANS":
                centre_sphere = ray.ndirection*t+objet_scene[1].normale(ray,CAMERA)
            
            elif objet_scene[3] == "HORS":
                centre_sphere = ray.ndirection*t-objet_scene[1].normale(ray,CAMERA)
                try:
                    centre_sphere = ray.ndirection*t-objet_scene[1].normale(ray,CAMERA)
                except:
                    print(ray,objet_scene)
                    raise TypeError
            
            else:
                print(objet_scene)
                raise TypeError("Ni dedans ni dehors d'un objet")
            
            point_random = point_sphere_aleatoire(centre_sphere)
            
            p = ray.ndirection*t
            new_ray = rayon((p.x,p.y,p.z),point_random-p)
            
            if random.randint(0,1) == 1:
                return couleur(0,0,0)
            
            if level == 10:
                return 0.5*couleur_rayon(new_ray,scene,CAMERA,level-1)+0.5*objet_scene[1].couleur_inter(ray)
            else:
                return 0.5*couleur_rayon(new_ray,scene,CAMERA,level-1)
        
        else:
            # if level == 10:
            #     print("ok")
            couleur_haut = couleur(0.7,0.7,1)
            couleur_bas = couleur(1,1,1)
            y = ray.direction.y
            y = (y+1)*0.5
            return couleur_haut*y+(1-y)*couleur_bas



def create_rayon(CAMERA,ECRAN_BAS_GAUCHE,ECRAN_HORIZONTAL,ECRAN_VERTICAl,LARGEUR,HAUTEUR,NB_RAYON):
    
    progression = 0 
    for y0 in range(0,HAUTEUR,1):
        
        y = (y0/HAUTEUR)*ECRAN_VERTICAl

        if y0%(HAUTEUR/20) == 0:
            print(y0*100/HAUTEUR)
        
        for x0 in range(0,LARGEUR,1):
            x = (x0/LARGEUR)*ECRAN_HORIZONTAL
            
            list_rayons = []
            for i in range(NB_RAYON):
                dx = random.uniform(0,ECRAN_HORIZONTAL/LARGEUR)
                dy = random.uniform(0,+ECRAN_VERTICAl/HAUTEUR)
                list_rayons += [rayon(CAMERA,vecteur(x+ECRAN_BAS_GAUCHE[0]+dx,y+ECRAN_BAS_GAUCHE[1]+dy,ECRAN_BAS_GAUCHE[2]))]
            

            yield x0,y0,list_rayons
global im

def main():
    LARGEUR = 200
    HAUTEUR = 100
    CAMERA = (0,0,0)
    ECRAN_BAS_GAUCHE = (-2,-1,-1)
    ECRAN_HORIZONTAL = 4
    ECRAN_VERTICAl = 2
    GAMMA = 2
    NB_RAYON = 30
    
    global im
    im = image(LARGEUR,HAUTEUR)
    
    boule = objet.sphere(0,0,-3,1)
    boule2 = objet.sphere(0,1.5,-3,0.6)
    boule3 = objet.sphere(1.5,0,-2,0.1)
    sol = objet.surface("y",-1)
    
    scene = [sol,boule,boule2,boule3]
    
    for x,y,list_ray in create_rayon(CAMERA,ECRAN_BAS_GAUCHE,ECRAN_HORIZONTAL,ECRAN_VERTICAl,LARGEUR,HAUTEUR,NB_RAYON):
        list_couleurs = []
        for i in range(NB_RAYON):
            list_couleurs += [couleur_rayon(list_ray[i],scene,CAMERA)]
            list_couleurs[-1].r = list_couleurs[-1].r**(1/GAMMA)
            list_couleurs[-1].g = list_couleurs[-1].g**(1/GAMMA)
            list_couleurs[-1].b = list_couleurs[-1].b**(1/GAMMA)
        
        cf = couleur(0,0,0)
        for i in list_couleurs:
            cf = cf + i
        cf = cf/NB_RAYON
        

        im.mettre_couleur(x,y,cf)
    
    
    
    







    with open("tests/test15.ppm","w") as file:
        im.write_img(file)
    
    
    








if __name__ == "__main__":
    main()