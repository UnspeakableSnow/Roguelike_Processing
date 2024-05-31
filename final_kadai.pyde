add_library('minim')
import csv
import time
import random
import os
import gc

def setup():
    global mapraw,mmap,entitys,itemss,npcs,mode,logn,filename,bgC,minim,atmus,talkmus,getm,equm,drpm
    fullScreen(P2D)
    frameRate(60)
    background(0,0,100)
    font=createFont("HGS創英角ﾎﾟｯﾌﾟ体",50)
    textFont(font)
    minim = Minim(this)
    plstmus=minim.loadFile(u'決定ボタンを押す8.mp3')
    atmus=minim.loadFile(u'刀で斬る2.mp3')
    talkmus=minim.loadFile(u'メッセージ表示音1.mp3')
    getm=minim.loadFile(u'宝箱を開ける.mp3')
    equm=minim.loadFile(u'剣を抜く.mp3')
    drpm=minim.loadFile(u'剣を落とす.mp3')
    plstmus.play(0)
    mapraw=[]
    mmap=[]
    filename=""
    #filename="map1.csv"#デバッグ用
    entitys=[] #0:pl 1:bos 2-:ene
    itemss=[]
    npcs=[]
    mode=0 #0:タイトル＆ファイルネーム問答　1:メイン　2:クリア表示
    logn=[]
    bgC=[0,0,100]
class entity():
    def __init__(self,id):
        self.yx=[int(mapraw[mapraw[0][0]+1+id][0]),int(mapraw[mapraw[0][0]+1+id][1])]
        self.HP=int(mapraw[mapraw[0][0]+1+id][2])
        self.AP=int(mapraw[mapraw[0][0]+1+id][3])
        self.name=mapraw[mapraw[0][0]+1+id][4]
        self.img=loadImage(filename+"/"+mapraw[mapraw[0][0]+1+id][5])
        self.equipment=-1
        #print(self.name) #デバッグ
class item():
    def __init__(self,id):
        self.yx=[int(mapraw[mapraw[0][0]+3+enenum+id][0]),int(mapraw[mapraw[0][0]+3+enenum+id][1])]
        self.addAP=int(mapraw[mapraw[0][0]+3+enenum+id][2])
        self.name=mapraw[mapraw[0][0]+3+enenum+id][3]
        self.img=loadImage(filename+"/"+mapraw[mapraw[0][0]+3+enenum+id][4])
class npc():
    def __init__(self,id):
        self.yx=[int(mapraw[mapraw[0][0]+3+enenum+itemnum+id][0]),int(mapraw[mapraw[0][0]+3+enenum+itemnum+id][1])]
        self.serif=mapraw[mapraw[0][0]+3+enenum+itemnum+id][2]
        self.name=mapraw[mapraw[0][0]+3+enenum+itemnum+id][3]
        self.img=loadImage(filename+"/"+mapraw[mapraw[0][0]+3+enenum+itemnum+id][4])
def loger(new="#"):
    if new!="#":
        logn.append(new)
    fill(textC[0],textC[1],textC[2])
    textSize(20)
    textAlign(LEFT)
    if len(logn)<(height/20+1):
        for i in range(len(logn)):
            text(logn[len(logn)-i-1].decode('utf-8'),20,height-60-30*i)
    else:
        for i in range((height/20+1)):
            text(logn[len(logn)-i-1].decode('utf-8'),20,height-60-30*i)
def loadmap():
    global enenum,itemnum,npcnum,clearMes,startMes,gameoverMes,blockSize,BrcImg,bgC,textC,player#,bgP
    mapfile=filename+"/map.csv"
    f = open(mapfile, "r")
    reader = csv.reader(f)
    for row in reader:
        mapraw.append(row)
    f.close()
    mapraw[0][0]=int(mapraw[0][0]) #high
    mapraw[0][1]=int(mapraw[0][1]) #weight
    enenum=int(mapraw[0][2])
    itemnum=int(mapraw[0][3])
    npcnum=int(mapraw[0][4])
    startMes=mapraw[0][5]
    clearMes=mapraw[0][6]
    gameoverMes=mapraw[0][7]
    BrcImg=loadImage(filename+"/"+mapraw[0][8])
    bgC=[int(mapraw[0][9]),int(mapraw[0][10]),int(mapraw[0][11])]
    textC=[int(mapraw[0][12]),int(mapraw[0][13]),int(mapraw[0][14])]
    player=minim.loadFile(filename+"/"+mapraw[0][15])
    player.play(0)
    player.loop()
    player.setGain(-8)
    #bgP=loadImage(filename.decode('utf-8')+u"/"+mapraw[0][16].decode('utf-8'))
    if height/mapraw[0][0]<(width-400)/(mapraw[0][1]*10):
        blockSize=height/mapraw[0][0]
    else:
        blockSize=(width-400)/(mapraw[0][1]*10)
    #print(mapraw)　#デバッグ
    for i in range(mapraw[0][0]):
        mmap.append([])
        for j in range(mapraw[0][1]):
            mapraw[i+1][j]=int(mapraw[i+1][j])
            #print(mapraw[i+1][j]) #デバッグ
            for c in range(10):
                if mapraw[i+1][j]%2==0:
                    mmap[i].append(" ")
                else:
                    mmap[i].append("#")
                mapraw[i+1][j]=int(mapraw[i+1][j]/2)
    for i in range(2+enenum):
        entitys.append(entity(i))
    for i in range(itemnum):
        itemss.append(item(i))
    for i in range(npcnum):
        npcs.append(npc(i))
def printmap():
    #image(bgP,0,0,width,height)
    background(bgC[0],bgC[1],bgC[2])
    fill(0,0)
    for y in range(mapraw[0][0]):
        for x in range(mapraw[0][1]*10):
            if mmap[y][x]=="#":
                stroke(0)
                image(BrcImg,blockSize*x+400,blockSize*y,blockSize,blockSize)
    for i in range(npcnum):
        stroke(255)
        rect(blockSize*npcs[i].yx[1]+400,blockSize*npcs[i].yx[0],blockSize,blockSize)
        image(npcs[i].img,blockSize*npcs[i].yx[1]+400,blockSize*npcs[i].yx[0],blockSize,blockSize)
    for i in range(itemnum):
        stroke(200,200,0)
        rect(blockSize*itemss[i].yx[1]+400,blockSize*itemss[i].yx[0],blockSize,blockSize)
        image(itemss[i].img,blockSize*itemss[i].yx[1]+400,blockSize*itemss[i].yx[0],blockSize,blockSize)
    for i in range(enenum):
        stroke(0,150,0)
        rect(blockSize*entitys[i+2].yx[1]+400,blockSize*entitys[i+2].yx[0],blockSize,blockSize)
        image(entitys[i+2].img,blockSize*entitys[i+2].yx[1]+400,blockSize*entitys[i+2].yx[0],blockSize,blockSize)
    stroke(180,0,0)
    rect(blockSize*entitys[1].yx[1]+400,blockSize*entitys[1].yx[0],blockSize,blockSize)
    image(entitys[1].img,blockSize*entitys[1].yx[1]+400,blockSize*entitys[1].yx[0],blockSize,blockSize)
    stroke(200,0,200)
    rect(blockSize*entitys[0].yx[1]+400,blockSize*entitys[0].yx[0],blockSize,blockSize)
    image(entitys[0].img,blockSize*entitys[0].yx[1]+400,blockSize*entitys[0].yx[0],blockSize,blockSize)
    loger()
    fill(textC[0]+100%255,textC[1],textC[2])
    textSize(30)
    textAlign(RIGHT)
    if entitys[0].equipment!=-1:
        text((entitys[0].name+"(プレイヤー)[HP:"+str(entitys[0].HP)+" 攻撃力:"+str(entitys[0].AP)+" 装備品:"+itemss[entitys[0].equipment].name+"(追加攻撃力:"+str(itemss[entitys[0].equipment].addAP)+")]").decode('utf-8'),width-20,height-20)
    else:
        text((entitys[0].name+"(プレイヤー)[HP:"+str(entitys[0].HP)+" 攻撃力:"+str(entitys[0].AP)+" 装備品:なし)]").decode('utf-8'),width-20,height-20)
def move(changey,changex):
    entitys[0].yx[0]+=changey
    entitys[0].yx[1]+=changex
    #printmap()#過負荷につき
    time.sleep(0.2)
    if(mmap[entitys[0].yx[0]][entitys[0].yx[1]]=="#"):
        loger(new="目の前は壁だった！")
        entitys[0].yx[0]-=changey
        entitys[0].yx[1]-=changex
    if(entitys[0].yx==entitys[1].yx):
        chacha=entitys[1].HP
        if entitys[0].equipment!=-1:
            entitys[1].HP-=(entitys[0].AP+itemss[entitys[0].equipment].addAP)
        else:
            entitys[1].HP-=entitys[0].AP
        atmus.play(0)
        loger(new=entitys[1].name+"　に攻撃した！ "+entitys[1].name+" の残りHP："+str(chacha)+" -> "+str(entitys[1].HP))
        if entitys[1].HP<=0:
            loger(new=entitys[1].name+" を倒した！")
            entitys[1].yx=[-1,-1]
            global mode
            mode=2
        else:
            entitys[0].yx[0]-=changey
            entitys[0].yx[1]-=changex
    if entitys[1].yx!=[-1,-1]:
        movebos()
    for i in range(enenum):
        if(entitys[0].yx==entitys[i+2].yx):
            chacha=entitys[i+2].HP
            if entitys[0].equipment!=-1:
                entitys[i+2].HP-=(entitys[0].AP+itemss[entitys[0].equipment].addAP)
            else:
                entitys[i+2].HP-=entitys[0].AP
            atmus.play(0)
            loger(new=entitys[i+2].name+"　に攻撃した！ "+entitys[i+2].name+" の残りHP："+str(chacha)+" -> "+str(entitys[i+2].HP))
            if entitys[i+2].HP<=0:
                loger(new=entitys[i+2].name+" を倒した！")
                entitys[i+2].yx=[-1,-1]
            else:
                entitys[0].yx[0]-=changey
                entitys[0].yx[1]-=changex
        if entitys[i+2].yx!=[-1,-1]:
            moveene(i)
    for i in range(itemnum):
        if(entitys[0].yx==itemss[i].yx):
            getm.play(0)
            loger(new=itemss[i].name+"(追加攻撃力:"+str(itemss[i].addAP)+") を拾った！ 装備しますか?[Y/n]")
            global qi
            qi=i
            mode=3
    for i in range(npcnum):
        if(entitys[0].yx==npcs[i].yx):
            loger(new=npcs[i].name+" に話しかけた！")
            entitys[0].yx[0]-=changey
            entitys[0].yx[1]-=changex
            talkmus.play(0)
            loger(new=npcs[i].name+": "+npcs[i].serif)
def moveene(id):
    if (entitys[id+2].yx[0]==entitys[0].yx[0] and (entitys[id+2].yx[1]-1==entitys[0].yx[1] or entitys[id+2].yx[1]+1==entitys[0].yx[1])) or (entitys[id+2].yx[1]==entitys[0].yx[1] and (entitys[id+2].yx[0]-1==entitys[0].yx[0] or entitys[id+2].yx[0]+1==entitys[0].yx[0])):
        kyashu=entitys[0].HP
        entitys[0].HP-=entitys[id+2].AP
        loger(new=entitys[id+2].name+"　に攻撃された！ 残りHP："+str(kyashu)+" -> "+str(entitys[0].HP))
        atmus.play(0)
    else:
        houkou=random.randint(0,3)
        if(houkou==0):
            movee=[-1,0]
        elif(houkou==1):
            movee=[0,-1]
        elif(houkou==2):
            movee=[1,0]
        else:
            movee=[0,1]
        entitys[id+2].yx[0]+=movee[0]
        entitys[id+2].yx[1]+=movee[1]
        if mmap[entitys[id+2].yx[0]][entitys[id+2].yx[1]]=="#" or entitys[id+2].yx==entitys[1].yx:
            #時間とリソースがあるなら判定追加
            entitys[id+2].yx[0]-=movee[0]
            entitys[id+2].yx[1]-=movee[1]
def movebos():
    global entitys
    if (entitys[1].yx[0]==entitys[0].yx[0] and (entitys[1].yx[1]-1==entitys[0].yx[1] or entitys[1].yx[1]+1==entitys[0].yx[1])) or (entitys[1].yx[1]==entitys[0].yx[1] and (entitys[1].yx[0]-1==entitys[0].yx[0] or entitys[1].yx[0]+1==entitys[0].yx[0])):
        kyashu=entitys[0].HP
        entitys[0].HP-=entitys[1].AP
        atmus.play(0)
        loger(new=entitys[1].name+"　に攻撃された！ 残りHP："+str(kyashu)+" -> "+str(entitys[0].HP))
def draw():
    global filename,mode,key,bgC
    if mode==0 or mode==1 or mode==3:
        background(bgC[0],bgC[1],bgC[2])
    if mode==0:
        waitTime=0
        if keyPressed==True and key!=ENTER:
            filename=filename+key
            waitTime=0.2
        fill(255)
        textAlign(CENTER)
        textSize(50)
        text(u"フォルダ名:"+filename.decode('utf-8'),width/2+100,height/2+100)
        if key==ENTER:
            loadmap()
            printmap()
            loger(new="マップ読み込み完了")
            global startMes,mapraw
            loger(new="♪"+mapraw[0][15])
            loger(new=startMes)
            loger(new="移動:wasd　終了:esc")
            mode=1
        time.sleep(waitTime)
    if mode==1:
        global mapraw,clearMes,gameoverMes,enenum,minim,player,equm,drpm
        printmap()
        if keyPressed==True:
            if key=="w":
                move(-1,0)
                time.sleep(0.2)
            if key=="a":
                move(0,-1)
                time.sleep(0.2)
            if key=="s":
                move(1,0)
                time.sleep(0.2)
            if key=="d":
                move(0,1)
                time.sleep(0.2)
            if entitys[1].HP<=0:
                mode=2
                player.pause()
                playera=minim.loadFile(filename.decode('utf-8')+u"/"+mapraw[0][16].decode('utf-8'))
                playera.play(0)
                loger(new="GameClear!: "+clearMes)
                printmap()
                global mapraw,mmap,itemss,npcs,logn,filename,minim,atmus,talkmus,getm,equm,drpm
                del mapraw,mmap,itemss,npcs,logn,filename,minim,atmus,talkmus,getm,equm,drpm
                gc.collect()
            if entitys[0].HP<=0:
                mode=-1
                player.pause()
                playera=minim.loadFile(filename.decode('utf-8')+u"/"+mapraw[0][17].decode('utf-8'))
                playera.play(0)
                loger(new="GAME OVER: "+gameoverMes)
                printmap()
                #print(entitys[0].yx) #デバッグ
                global mapraw,mmap,itemss,npcs,logn,filename,minim,atmus,talkmus,getm,equm,drpm
                del mapraw,mmap,itemss,npcs,logn,filename,minim,atmus,talkmus,getm,equm,drpm
                gc.collect()
    if mode==2 or mode==-1:
        pass
    if mode==3:
        printmap()
        if key=="Y" or key=="y":
            if entitys[0].equipment!=-1:
                cache=itemss[entitys[0].equipment].addAP
            else:
                cache=0
            entitys[0].equipment=qi
            equm.play(0)
            loger(new="装備ダメージ変化！　"+str(cache)+"->"+str(itemss[entitys[0].equipment].addAP))
            mode=1
            itemss[qi].yx=[-1,-1]
        elif key=="N" or key=="n":
            drpm.play(0)
            loger(new="処分しました")
            mode=1
            itemss[qi].yx=[-1,-1]
