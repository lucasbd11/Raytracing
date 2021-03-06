
import sys, os
sys.path.append('/Users/Lucas/Desktop/Dev/raytracing')

import random
from vecteurs import vecteur
from image import image
from couleurs import couleur
from rayons import rayon
import objet
import math



def point_sphere_aleatoire(centre):
    r = random.uniform(0,1)
    phi = random.uniform(0,2*math.pi)
    theta = phi = random.uniform(0,math.pi)
    x = math.cos(phi)*math.sin(theta)*r+centre.x
    y = math.sin(phi)*math.sin(theta)*r+centre.y
    z = math.cos(theta)*r+centre.z
    
    return vecteur(x,y,z)




def couleur_rayon_old(ray,scene,CAMERA,level=10,TRACER = "OFF"):
    
        if level <= 0:
            if TRACER == "ON":
                print("level 0")
            return couleur(0,0,0)

        objet_scene = objet.test_intersection(ray,scene,CAMERA)
        

        
        if objet_scene[0]:

            t = objet_scene[2]

            if objet_scene[3] == "DANS":
                centre_sphere = ray.ndirection_decale*t+objet_scene[1].normale(ray,CAMERA)
            
            elif objet_scene[3] == "HORS":
                centre_sphere = ray.ndirection_decale*t-objet_scene[1].normale(ray,CAMERA)
                try:
                    centre_sphere = ray.ndirection_decale*t-objet_scene[1].normale(ray,CAMERA)
                except:
                    print(ray,objet_scene)
                    raise TypeError
            
            else:
                print(objet_scene)
                raise TypeError("Ni dedans ni dehors d'un objet")
            
            point_random = point_sphere_aleatoire(centre_sphere)
            
            p = ray.ndirection_decale*t
            new_ray = rayon((p.x,p.y,p.z),point_random-p)
            
            
            
            if level == 10:
                return ((0.5*couleur_rayon_old(new_ray,scene,CAMERA,level-1)+0.5*objet_scene[1].couleur_inter(ray))+couleur(0,0,0))/2
            else:
                
                return ((0.5*couleur_rayon_old(new_ray,scene,CAMERA,level-1))+couleur(0,0,0))/2
        
        else:

            couleur_haut = couleur(0.7,0.7,1)
            couleur_bas = couleur(1,1,1)
            y = ray.direction.y
            y = (y+1)*0.5
            if level != 10:
                return couleur(1,1,1)
            
            return couleur_haut*y+(1-y)*couleur_bas

def couleur_rayon(ray,scene):
        
        objet_scene = objet.test_intersection(ray,scene)
        
        if objet_scene[0]:

            t = objet_scene[2]
            objet_origine = objet_scene[1]
            
            if objet_scene[3] == "DANS":
                
                
                
                return couleur(0,1,0)

            elif objet_scene[3] == "HORS":
                
                if objet_scene[1].texture.type_obj == "mat":
                    val_lumiere = objet.test_lumiere(ray,scene,objet_origine,t)
                    couleur_objet = objet_origine.couleur_inter(ray,scene)*val_lumiere
                    
                    
                elif objet_scene[1].texture.type_obj == "métal":
                    val_lumiere = objet.test_lumiere(ray,scene,objet_origine,t)
                    couleur_objet = objet_origine.couleur_inter(ray,scene)*val_lumiere*0.92
                elif objet_scene[1].texture.type_obj == "verre":
                    couleur_objet = objet_origine.couleur_inter(ray,scene)
                
                    
                return couleur_objet
            
            else:
                print(objet_scene)
                raise TypeError("Ni dedans ni dehors d'un objet")
            
        
        
        else:
            
            couleur_haut = couleur(0.7,0.7,1)
            couleur_bas = couleur(1,1,1)
            y = ray.direction.y
            y = (y+1)*0.5
            #return couleur(0,0,0)
            return couleur_haut*y+(1-y)*couleur_bas            
            
            



def create_rayon(CAMERA,ECRAN_BAS_GAUCHE,ECRAN_HORIZONTAL,ECRAN_VERTICAl,LARGEUR,HAUTEUR,NB_RAYON,DISTANCE_CAM_ECRAN):
    
    cam_vect = vecteur(CAMERA[0],CAMERA[1],CAMERA[2])
    normale_ecran = -1*(ECRAN_HORIZONTAL.prod_vectorielle(ECRAN_VERTICAl)).normaliser()
    
    
    bas_gauche_ecran = -1*ECRAN_HORIZONTAL/2+(-1*ECRAN_VERTICAl/2)+normale_ecran*DISTANCE_CAM_ECRAN+cam_vect
    
    progression = 0 
    for y0 in range(0,HAUTEUR,1):
        

        y = (ECRAN_VERTICAl/HAUTEUR)*y0
        if y0%(HAUTEUR/20) == 0:
            print(y0*100/HAUTEUR)
        
        for x0 in range(0,LARGEUR,1):

            x = (ECRAN_HORIZONTAL/LARGEUR)*x0
            
            
            list_rayons = []
            for i in range(NB_RAYON):
                dx = (ECRAN_HORIZONTAL/LARGEUR)*random.uniform(0,1)
                dy = (ECRAN_VERTICAl/HAUTEUR)*random.uniform(0,1)

                if NB_RAYON == 1:
                    dx = dy = vecteur(0,0,0)
                list_rayons += [rayon(CAMERA,bas_gauche_ecran+x+y+dx+dy)]

            

            yield x0,y0,list_rayons
global im

def main():
    LARGEUR = 1000
    HAUTEUR = 500
    CAMERA = (0,3,0)
    DISTANCE_CAM_ECRAN = 1
    ECRAN_HORIZONTAL = vecteur(4,0,0)
    ECRAN_VERTICAl = vecteur(0,2,-1)
    
    
    ECRAN_BAS_GAUCHE = (-2,-1,-1)

    GAMMA = 2
    NB_RAYON = 10
    
    global im
    im = image(LARGEUR,HAUTEUR)
    
    
    # boule = objet.sphere(0,0.5,-2,0.2,\
    #                                 objet.materiel(couleur_obj = couleur(0,0.5,0.7),type_obj = "mat"))
    # 
    # boule4 = objet.sphere(-2,0,-5,1,\
    #                                 objet.materiel(couleur_obj = couleur(0.4,0.2,0.4),type_obj = "mat"))
    # 
    # boule5 = objet.sphere(-0.3,-1,-1.5,0.2,\
    #                                 objet.materiel(couleur_obj = couleur(1,0.8,0.1),type_obj = "mat"))
    # 
    # boule2 = objet.sphere(1.5,0,-3.5,1,\
    #                                 objet.materiel(couleur_obj = couleur(0.86,0.49,0.14),type_obj = "métal",indice_reflexion = 0.2))
    # 
    # 
    # boule3 = objet.sphere(0.1,-0.2,-2,0.4,\
    #                                 objet.materiel(couleur_obj = couleur(0.82,0.98,0.98),type_obj = "métal"))

    boule = objet.sphere(2,2,-6,1,\
                                    objet.materiel(type_obj = "verre",indice_refraction = 1.7))
    

    
    boule3 = objet.sphere(0,0,-15,1,\
                                    objet.materiel(couleur_obj = couleur(0.4,0.2,0.4),type_obj = "mat"))

   
    boule4 = objet.sphere(0.2,-0.5,-8,0.5,\
                                    objet.materiel(couleur_obj = couleur(0.86,0.49,0.14),type_obj = "métal",indice_reflexion = 0.2))
    
    boule5 = objet.sphere(2.5,-0.5,-3,0.5,\
                                    objet.materiel(couleur_obj = couleur(0.86,0.49,0.14),type_obj = "métal",indice_reflexion = 0))
 
    
    sol = objet.surface("y",-1,objet.materiel(couleur_obj = couleur(1,0,0),type_obj = "mat", texture_img = "texture/dirt.ppm", texture_img_rapport = 1))

    lum = objet.lumiere(0,1000,-4,"Global")

    #scene = [boule,sol,boule2,lum,boule3,boule4,boule5]
    scene = [boule,sol,lum,boule3,boule4,boule5]
    
    
    
    
    for x,y,list_ray in create_rayon(CAMERA,ECRAN_BAS_GAUCHE,ECRAN_HORIZONTAL,ECRAN_VERTICAl,LARGEUR,HAUTEUR,NB_RAYON,DISTANCE_CAM_ECRAN):
        list_couleurs = []
        for i in range(NB_RAYON):

            list_couleurs += [couleur_rayon(list_ray[i],scene)]
            
            list_couleurs[-1].r = list_couleurs[-1].r**(1/GAMMA)
            list_couleurs[-1].g = list_couleurs[-1].g**(1/GAMMA)
            list_couleurs[-1].b = list_couleurs[-1].b**(1/GAMMA)

        
        cf = couleur(0,0,0)
        for i in list_couleurs:
            cf = cf + i
        cf = cf/NB_RAYON
        

        im.mettre_couleur(x,y,cf)
    
    
    
    







    with open("tests/test42.ppm","w") as file:
        im.write_img(file)
    
    
    








if __name__ == "__main__":
    main()