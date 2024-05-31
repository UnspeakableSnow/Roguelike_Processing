'''#最終課題（個人作品）
add_library('minim')
import csv
from random import randint
mode=[0,0,""]
textXYS=[100,0,0]
def say():
    global mode,textXYS,timen
    textSize(50)
    fill(255)
    textlen=(len(mode[2])+60-timen)/10
    if textXYS[1]==0:
        textAlign(LEFT)
        text(mode[2].decode('utf-8')[0:textlen],50,textXYS[0])
def setup():
    global l,x,y,me,ue,sita,mawari,hane,time,csv_data,timen,minim,people,hurin,semi
    timen=1
    size(1400,1000)
    filename="datas.csv"
    time=0
    l=[0]
    x=[0]
    y=[0]
    lines = loadStrings(filename)
    for i in range(1,len(lines)):
        fl=lines[i].split(',')[1]
        if fl!='':
            l.append(float(fl))
        else:
            l.append(l[i-1])
    for i in range(1,len(lines)):
        fl=lines[i].split(',')[2]
        if fl!='':
            x.append(float(fl))
        else:
            x.append(x[i-1])
    for i in range(1,len(lines)):
        fl=lines[i].split(',')[3]
        if fl!='':
            y.append(float(fl))
        else:
            y.append(y[i-1])
    me = loadImage("me.png")
    ue = loadImage("ue.png")
    sita = loadImage("sita.png")
    mawari = loadImage("mawari.png")
    hane = loadImage("hane.png")
    minim = Minim(this)
    people=minim.loadFile(u'高校の教室.mp3')
    hurin=minim.loadFile(u'風鈴1.mp3')
    semi=[]
    semi.append(minim.loadFile(u'アブラゼミの鳴き声1.mp3'))
    semi.append(minim.loadFile(u'ツクツクボウシの鳴き声1.mp3'))
    semi.append(minim.loadFile(u'ニイニイゼミの鳴き声.mp3'))
    semi.append(minim.loadFile(u'ヒグラシの鳴き声.mp3'))
    semi.append(minim.loadFile(u'ミンミンゼミの鳴き声.mp3'))
    people.play()
    hurin.play()
    semi[0].play()
    semi[1].play()
    semi[2].play()
    semi[3].play()
    semi[4].play()
    people.loop()
    hurin.loop()
    semi[0].loop()
    semi[1].loop()
    semi[2].loop()
    semi[3].loop()
    semi[4].loop()
    noStroke()
    font=createFont("HGS創英角ﾎﾟｯﾌﾟ体",50)
    textFont(font)
    csv_data = []
    with open('say.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            csv_data.append(row)
def draw():
    global l,x,y,me,ue,sita,mawari,hane,time,csv_data,timen,mode
    time+=1
    if time==len(l):
        time=0
    colorMode(HSB)
    for i in range(500):
        pad=height/500
        fill((i+time*10)%255,255,126)
        rect(0,pad*i,width,pad*(i+1))
    colorMode(RGB)
    X=(x[time]*30+width/7)*2/3
    Y=(y[time]*30+height/2)*2/3
    image(me,(mouseX-width/2)/4+X+50,(mouseY-200-height/2)/4+Y,width*2/3,height*2/3)
    image(ue,X,Y,width*2/3,(height-l[time]*2+500)*2/3)
    image(sita,X,Y,width*2/3,(height+l[time]*2-500)*2/3)
    image(mawari,X,Y,width*2/3,height*2/3)
    image(hane,X+sin(time)*300-1000,Y-300,width*2.3-sin(time)*600,height)
    #text(timen,width/2,100)
    timen-=1
    if timen==0:
        mode[1]+=1
        if len(csv_data[mode[0]])/2<=mode[1]:
            mode[0]=randint(0,len(csv_data)-1)
            mode[1]=0
        mode[2]=csv_data[mode[0]][mode[1]]
        timen=len(mode[2])+60
    say()'''
