# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 12:56:58 2019

@author: Salim
"""

import random, pygame, sys
import pickle
import datetime
FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
HEAD=0
liste=[]

def Main():
    global fps,ekran,eat
    pygame.init()
    fps=pygame.time.Clock()
    eat=pygame.mixer.Sound("1.wav")
    ekran=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Yılan Oyunu")
    Giriş_Ekranı()
    while True:
        Oyun()
        OyunSonuEkranı()

def İskeyPress():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                pygame.quit()
            else:
                return event.key
    return None
def Oyun():
    global yuv_Kord,liste
    pygame.mixer.music.stop()
    startx=random.randint(5,CELLWIDTH)
    starty=random.randint(5,CELLHEIGHT)
    yıl_Kord=[{"x":startx,"y":starty},
              {"x":startx-1,"y":starty},
              {"x":startx-2,"y":starty}]
    yön=RIGHT
    elma=randompos()
    pos=randompos()
    skor=0
    liste=[]
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
        keys=pygame.key.get_pressed()
        if keys[ord("a")] and yön!=RIGHT:
            yön=LEFT
        elif keys[ord("d")] and yön!=LEFT:
            yön=RIGHT
        elif keys[ord("w")] and yön !=DOWN:
            yön=UP
        elif keys[ord("s")] and yön!=UP:
            yön=DOWN
        if yıl_Kord[HEAD]["x"]==elma["x"] and yıl_Kord[HEAD]["y"]==elma["y"]:
            elma=randompos()
            eat.play()
            liste=[]
            skor+=10
        else:
            del yıl_Kord[-1]
        if yıl_Kord[HEAD]["x"]==pos["x"] and yıl_Kord[HEAD]["y"]==pos["y"]:
            liste=[]
            skor+=20

        for body in yıl_Kord[1:]:
            if yıl_Kord[HEAD]["x"]==body["x"] and yıl_Kord[HEAD]["y"]==body["y"]:
                return
        if yıl_Kord[HEAD]["x"]==-1 or yıl_Kord[HEAD]["x"]==CELLWIDTH or yıl_Kord[HEAD]["y"]==-1 or yıl_Kord[HEAD]["y"]==CELLHEIGHT:
            return
        if yön==UP:
            newHead={"x":yıl_Kord[HEAD]["x"],"y":yıl_Kord[HEAD]["y"]-1}
        elif yön==DOWN:
            newHead={"x":yıl_Kord[HEAD]["x"],"y":yıl_Kord[HEAD]["y"]+1}
        elif yön==LEFT:
            newHead={"x":yıl_Kord[HEAD]["x"]-1,"y":yıl_Kord[HEAD]["y"]}
        elif yön==RIGHT:
            newHead={"x":yıl_Kord[HEAD]["x"]+1,"y":yıl_Kord[HEAD]["y"]}
        yıl_Kord.insert(0,newHead)
        ekran.fill(BGCOLOR)
        gridciz()
        Elmaçiz(elma)
        Büyük_Çiz(skor,pos)
        Yılanciz(yıl_Kord)
        Score(skor)
        veri=Yüksek_Skor()
        if skor>veri:
            Kaydet(skor)
        pygame.display.update()
        fps.tick(FPS)
def randompos():
    return {"x":random.randint(0,CELLWIDTH-1),
            "y":random.randint(0,CELLHEIGHT-1)}
def Büyük_Çiz(skor,pos):
    global liste
    if skor%50==0 and skor!=0:
        saniye=datetime.datetime.now().second
        if not saniye in liste:
            liste.append(saniye)
        if len(liste)<5:
                x=pos["x"]*CELLSIZE
                y=pos["y"]*CELLSIZE
                elmaKare=pygame.Rect(x,y,CELLSIZE,CELLSIZE)
                pygame.draw.rect(ekran,GREEN,elmaKare)
        else:
            return
            
        
def Elmaçiz(kord):
    x=kord["x"]*CELLSIZE
    y=kord["y"]*CELLSIZE
    elmaKare=pygame.Rect(x,y,CELLSIZE,CELLSIZE)
    pygame.draw.rect(ekran,RED,elmaKare)
    
def Yılanciz(kord):
    for i in kord:
        x=i["x"]*CELLSIZE
        y=i["y"]*CELLSIZE
        yılan=pygame.Rect(x,y,CELLSIZE,CELLSIZE)
        pygame.draw.rect(ekran,DARKGREEN,yılan)
        yılan2=pygame.Rect(x+4,y+4,CELLSIZE-8,CELLSIZE-8)
        pygame.draw.rect(ekran,GREEN,yılan2) 
def YazıEkle():
    font3=pygame.font.Font("freesansbold.ttf",20)
    yazı=font3.render("Başlamak için herhangi tuşa basınız",True,DARKGRAY)
    kare=yazı.get_rect()
    kare.center=(180,50)
    ekran.blit(yazı,kare)

def Giriş_Ekranı():
    pygame.mixer.music.load("2.wav")
    pygame.mixer.music.play(-1)
    font1=pygame.font.Font("freesansbold.ttf",100)
    render1=font1.render("Snake",True,WHITE,DARKGREEN)
    render2 = font1.render('Snake', True, GREEN)
    acı1=0
    acı2=0
    while True:
        ekran.fill(BGCOLOR)
        rotate1=pygame.transform.rotate(render1,acı1)
        rect1=rotate1.get_rect()
        rect1.center=(WINDOWWIDTH/2,WINDOWHEIGHT/2)
        ekran.blit(rotate1,rect1)
        
        rotate2 = pygame.transform.rotate(render2, acı2)
        Rect2 = rotate2.get_rect()
        Rect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        ekran.blit(rotate2, Rect2)
        YazıEkle()
        if İskeyPress():
            return
        pygame.display.update()
        fps.tick(FPS)
        acı1+=5
        acı2+=10
        
def gridciz():
    for x in range(0,WINDOWWIDTH,CELLSIZE):
        pygame.draw.line(ekran,DARKGRAY,(x,0),(x,WINDOWHEIGHT))
    for y in range(0,WINDOWHEIGHT,CELLSIZE):
        pygame.draw.line(ekran,DARKGRAY,(0,y),(WINDOWWIDTH,y))
def yuv_pos():
      liste=list(range(round(CELLSIZE/2),WINDOWWIDTH-round(CELLSIZE/2),CELLSIZE)) 
      sayı=random.randint(0,len(liste))
      liste2=list(range(round(CELLSIZE/2),WINDOWHEIGHT-round(CELLSIZE/2),CELLSIZE))
      x=liste[sayı]
      sayı2=random.randint(0,len(liste2)-1)
      y=liste2[sayı2]
      return x,y
def Yüksek_Skor():
    with open ("enyüksekskor.pickle","rb") as f:
        veri=pickle.load(f)
    font1=pygame.font.Font("freesansbold.ttf",20)
    yazı=font1.render("En Yüksek Skor:"+str(veri["v"]),True,WHITE)
    ekran.blit(yazı,(0,20))
    return int(veri["v"])
def Score(score):
    font1=pygame.font.Font("freesansbold.ttf",20)
    yazı=font1.render("Skor:"+str(score),True,WHITE)
    ekran.blit(yazı,(0,0))
def OyunSonuEkranı():
    while True:
        font =pygame.font.Font("freesansbold.ttf",150)
        game=font.render("GAME",True,WHITE)
        over=font.render("OVER",True,WHITE)
        ekran.blit(game,(70,70))
        ekran.blit(over,(70,200))
        YazıEkle()
        pygame.display.update()
        if İskeyPress():
            return
def Kaydet(skor):
    veri={"v":skor}
    with open("enyüksekskor.pickle","wb") as f:
        pickle.dump(veri,f)
    
if __name__=="__main__":
    Main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    








