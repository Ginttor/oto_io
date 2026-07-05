import random
import subprocess
import shutil
import json
import os
from datetime import datetime

##
def punt(a):#puntuar nota
    bnp=arch[a].split(":")
    bnpp=int(bnp[1]);bnpt=int(bnp[2])
    bnpp+=1
    if bnpp<bnpt:
        arch[a]=bnp[0]+":"+str(bnpp)+":"+bnp[2]+":"+bnp[3]+":"+bnp[4]
        print(arch[a])
    else:
        if bnp[3]=="":arch[a]="\n"
        elif bnpp<=bnpt:
            arch[a]=bnp[0]+":"+str(bnpp)+":"+bnp[2]+":"+bnp[3]+":"+bnp[4]
            print(arch[a])
    mm="\n".join(arch).replace("\n\n","\n")
    with open("arch.txt", "w",encoding='utf-8') as file:
        file.write(mm)
def vora():#borrar orario
    archh=[]
    for i in arch:
        if i.count("a:")>0:
            bnp=i.split(":")
            bnpp=int(bnp[1])
            bnpp+=1
            archh.append(bnp[0]+":0:"+bnp[2]+":"+bnp[3]+":"+bnp[4])
        elif i.count("o:")>0:
            print(i)
        else:archh.append(i)
    mm="\n".join(archh).replace("\n\n","\n")
    with open("arch.txt", "w",encoding='utf-8') as file:
        file.write(mm)
def orar():#orario
    xt=False;ahora = datetime.now()
    for i in arch:
        if i.count("o:")>0:xt=True;break
    if xt:
        oo=[]
        for i in arch :
            if i.count("o:"):oo.append(i)
        print(oo[ahora.weekday()+1])
        lt=oo[ahora.weekday()+1].split(":")[3].split(";")
        tm=oo[ahora.weekday()+1].split(":")[2].replace(".","").split("-")
        cdh=int(tm[0]);ltm=[cdh]
        for i in range(int(tm[1])-int(tm[0])):
            cdh+=1
            ltm.append(cdh)
        print(ltm);rrv=[]
        x=0;mm=">>> ("+oo[ahora.weekday()+1].split(":")[1]+ahora.strftime("-%H): ")+"ZZZ";oto="";oto2="";prg=[0,0]
        while x<len(ltm):
            ltn=lt[int(x/2)].replace("!","").split(",")
            if int(ahora.strftime("%H"))==ltm[x] or int(ahora.strftime("%H"))==ltm[x+1]:
                y=1;mm=""
                while y<len(ltn):
                    mm+="\n>>>("+oo[ahora.weekday()+1].split(":")[1]+"["+str(ltm[x])+"-"+str(ltm[x+1])+"])>>> <"+str(int(ltn[y]))+"> "+arch[int(ltn[y])]
                    rrv.append(int(ltn[y]))
                    y+=1
            else:
                y=1
                while y<len(ltn):
                    prg[0]+=int(arch[int(ltn[y])].split(":")[1])
                    prg[1]+=int(arch[int(ltn[y])].split(":")[2])
                    y+=1
                oto="\n"+oo[ahora.weekday()+1].split(":")[1]+": "+str(prg[0]/prg[1]*100)+"%\n"
                y=1
                while y<len(ltn):
                    oto2+=arch[int(ltn[y])]+"\n"
                    y+=1
            x+=2
        print(oto,oto2,mm)
        print("\n|[a]puntuar actividad\n+-------",rrv)
        com=input("->: ")
        if com=="a":
            for i in rrv:
                punt(i)
    else:
        arch.append("o:tt:"+str(ahora))
        tmo=0
        for i in orra:tmo+=i.count(".")
        x=0;oa1=[];oa2=[];oa3=[];cma=0
        while x<len(arch):
            if   arch[x].count("a:") and arch[x].split(":")[3]=="1":oa1.append(str(x));cma+=int(arch[x].split(":")[2])*int(arch[x].split(":")[3])
            elif arch[x].count("a:") and arch[x].split(":")[3]=="2":oa2.append(str(x));cma+=int(arch[x].split(":")[2])*int(arch[x].split(":")[3])
            elif arch[x].count("a:") and arch[x].split(":")[3]=="3":oa3.append(str(x));cma+=int(arch[x].split(":")[2])*int(arch[x].split(":")[3])
            x+=1
        print("!!--:",cma,tmo)
        oa=oa3+oa2+oa1
        z=0;oo=orra
        while z <len(oa):
            w=0;pss=0
            while w < int(arch[int(oa[z])].split(":")[2]):
                x=random.randint(0, 6)
                ec=oo[x].split(".:")
                lt=oo[x].split(":")[3].split(";")
                y=random.randint(0, len(lt)-1)
                cda=lt[y].count(".")-lt[y].count("!")
                if cda>=int(arch[int(oa[z])].split(":")[3]) and lt[y].count(","+oa[z])==0:
                    nn=""
                    if arch[int(oa[z])].split(":")[3]=="1":nn="!"
                    if arch[int(oa[z])].split(":")[3]=="2":nn="!!"
                    if arch[int(oa[z])].split(":")[3]=="3":nn="!!!"
                    lt[y]+=","+oa[z]+nn
                    oo[x]=ec[0]+".:"+";".join(lt)
                    w+=1
                pss+=1
                if pss>=168:w+=1
            z+=1
        for i in oo:
            arch.append(i)
        mm="\n".join(arch).replace("\n\n","\n")
        with open("arch.txt", "w",encoding='utf-8') as file:
            file.write(mm)
        orar()
def ress(d):#reseteo de archibo
    with open(d, "r",encoding='utf-8') as file:
        tlo=json.loads(file.read())
    x=0
    while x<len(tlo["LT"]):
        ot=tlo["LT"][x].split(":")
        tlo["LT"][x]=ot[0]+":0:"+ot[2]+":"+ot[3]
        x+=1
    with open(d, "w",encoding='utf-8') as file:
        file.write(str(tlo).replace("{","{\n").replace("}","}\n").replace("],","],\n").replace(": [",": [\n").replace("', '","', \n'").replace("'",'"'))
def banr(d):#baner de archibo
    global bnn
    bnn=random.randint(0, len(d)-1)
    bn=d[bnn]
    return str(bnn)+"> "+bn
def anpy(d):#prosesar archibbo
    with open(d, "r",encoding='utf-8') as file:
        tlo=json.loads(file.read())
    x=0;tt=[]#tt=tlo["LT"]
    re=[];rf=[]
    for e in tlo["EV"]["ap"]:
        for i in tlo["LT"]:
            if i.split(":")[0].count(e):re.append(i)
    for e in tlo["EV"]["rd"]:
        for i in re:
            if i.split(":")[2].count(e):rf.append(i)
    tlo["LT"]=rf
    while x<len(tlo["EV"]["kp"]):
        for i in tlo["LT"]:
            if i.split(":")[1]==str(x):tt.append(i)
        x+=1
    td=[0,0,0,0,0,0,0]
    ts=[0,0,0,0,0,0,0]
    for i in tt:
        x=0
        for e in tlo["EV"]["ap"]:
            if i.split(":")[0]==e:td[x]+=1
            if i.split(":")[0]==e:ts[x]+=int(i.split(":")[1])
            x+=1
    x=0;te=0
    while x<len(td):
        ts[x]=ts[x]/(len(tlo["EV"]["kp"])-1)
        te+=ts[x]
        x+=1
    x=0
    for i in tlo["EV"]["ap"]:
        mm=tlo["EV"]["ap"][i].split(":")[0]+":("+str(ts[x])+"/"+str(td[x])+"):"+tlo["EV"]["ap"][i].split(":")[2]
        print(mm)
        tlo["EV"]["ap"][i]=mm
        x+=1
    tlo["EV"]["tt"]="PROGRESS: "+"("+str(f"{(te/len(tt)*100):.2f}")+"% - "+str(len(tt))+")"
    print(tlo["EV"]["tt"])
    print("+-------------+")
    td=[0,0,0,0,0,0,0]
    ts=[0,0,0,0,0,0,0]
    tp=[0,0,0,0,0,0,0]
    y=0
    while y<len(tt):
        x=0
        #if tt[y].split(":")[2]==".":tt[y]=tt[y].replace(":.:",(":"+str(len(tlo["EV"]["rd"])-1)+":"))
        for e in tlo["EV"]["rd"]:
            if tt[y].split(":")[2]==e:td[x]+=1
            if tt[y].split(":")[2]==e and int(tt[y].split(":")[1])>0:ts[x]+=1
            if tt[y].split(":")[2]==e:tp[x]+=int(tt[y].split(":")[1])
            x+=1
        y+=1
    x=0
    while x<len(td):
        tp[x]=tp[x]/(len(tlo["EV"]["kp"])-1)
        x+=1
    x=0
    for i in tlo["EV"]["rd"]:
        rs=0.0
        if td[x]!=0:rs=tp[x]/td[x]
        mm=str(f"{(rs*100):.2f}")+"%-"+str(ts[x])+"/"+str(td[x])+")"
        tlo["EV"]["rd"][i]=mm+":"+tlo["EV"]["rd"][i].split(":")[1]
        print(tlo["EV"]["rd"][i])
        x+=1
    print("+-------------+")
    x=0
    for i in tlo["EV"]["rd"]:
        rs=0.0
        if td[x]!=0:rs=tp[x]/td[x]
        if rs!=1:
            print(tlo["EV"]["rd"][i],"->")
            for e in tt:
                if e.split(":")[2]==i:print("\t",e.replace((":"+e.split(":")[1]+":"+i),(":"+tlo["EV"]["kp"][int(e.split(":")[1])].split(":")[0]+":"+i)))
            break
        x+=1
    with open(d, "w",encoding='utf-8') as file:
        file.write(str(tlo).replace("{","{\n").replace("}","}\n").replace("],","],\n").replace(": [",": [\n").replace("', '","', \n'").replace("'",'"'))
arch=[];bnn=0;orra=[]
if  os.path.exists("boul"):
    ctt=os.listdir("boul")
else:
    os.mkdir("boul")
if  not os.path.exists("arch.txt"):
    with open("arch.txt", "w",encoding='utf-8') as file:
        file.write("")
if  not os.path.exists("orra.txt"):
    with open("orra.txt", "w",encoding='utf-8') as file:
        mm="""o:L:6-21.:...;...;...;...;...;...;...;...
o:M:6-21.:...;...;...;...;...;...;...;...
o:m:6-21.:...;...;...;...;...;...;...;...
o:J:6-21.:...;...;...;...;...;...;...;...
o:V:6-21.:...;...;...;...;...;...;...;...
o:S:6-21.:...;...;...;...;...;...;...;...
o:V:6-21.:...;...;...;...;...;...;...;..."""
        file.write(mm)
com=""
while com!="x":
    with open("arch.txt", "r",encoding='utf-8') as file:
        arch=file.read().split("\n")
    pan="""
[x]oto_io
+---<"""+banr(arch)+"""
|[s]:manejar segimientos
|[p]:manejar pendientes
|[o]:manejar orario
+--------
    """
    print(pan)
    com=input("->: ")
    if   com=="s":
        x=0
        while x<len(arch):
            if arch[x].count("s:")>0:print(x,"-",arch[x])
            x+=1
        pan="""
        |[i]:ingresar
        |[o]:reinisiar archibo
        |[#]:->
        """
        print(pan)
        com=input("->: ")
        try:
            if int(com)<len(arch):
                nrb="boul"+"/"+arch[int(com)].split(":")[2].split("/")[len(arch[int(com)].split(":")[2].split("/"))-1].replace("\n","")
                shutil.move(arch[int(com)].split(":")[2].replace("\n",""),nrb)
                anpy(nrb)
                shutil.move(nrb,arch[int(com)].split(":")[2].replace("\n",""))
                os.system("xdg-open "+arch[int(com)].split(":")[2].replace("\n",""))
        except ValueError:
            print("...")
        if   com=="i":
            com=input("ingresar ruta: ")
            if com.count("GD_")>0:
                cmm=input("ingresar comentario: ")
                with open("arch.txt", "a",encoding='utf-8') as file:
                    file.write("s:[ "+cmm+" ]:"+com+"\n")
            else:print("!!--no hay un nombre de formato compatible")
        elif com=="o":
            x=0
            while x<len(arch):
                print(x,"-",arch[x])
                x+=1
            com=input("cual: ")
            try:
                if int(com)<len(arch):
                    nrb="boul"+"/"+arch[int(com)].split(":")[2].split("/")[len(arch[int(com)].split(":")[2].split("/"))-1].replace("\n","")
                    shutil.move(arch[int(com)].split(":")[2].replace("\n",""),nrb)
                    ress(nrb)
                    anpy(nrb)
                    shutil.move(nrb,arch[int(com)].split(":")[2].replace("\n",""))
                    print("!!--:",arch[int(com)].split(":")[2].replace("\n",""))
                    os.system("xdg-open "+arch[int(com)].split(":")[2].replace("\n",""))
            except ValueError:
                print("...")
    elif com=="p":
        pan="""
        |[i]:ingresar
        |[p]:sumar punto
        """
        print(pan)
        com=input("->: ")
        if   com=="i":
            com=input("ingresar limite (x>0): ")
            try:
                if int(com):
                    cmm=input("ingresar comentario: ")
                    with open("arch.txt", "a",encoding='utf-8') as file:
                        file.write("p:0:"+com+":: "+cmm+"\n")
            except ValueError:print("!!--el limite que ingreso no es un numero")
        elif com=="p":
            if arch[bnn].count("p:")>0:
                punt(bnn)
    elif com=="o":
        with open("orra.txt", "r",encoding='utf-8') as file:
            orra=file.read().split("\n")
        pan="""
        |[o]:ver orario
        |[a]:actividades
        |[v]:vorrar orario

        """
        print(pan)
        com=input("->: ")
        if   com=="o":
            orar()
        elif com=="a":
            com=input("ingresar limite (x>0): ")
            cat=input("define en nivel de concentrasion(1)(2)(3): ")
            try:
                if int(com) and int(cat) and cat!="":
                    cmm=input("ingresar comentario: ")
                    with open("arch.txt", "a",encoding='utf-8') as file:
                        file.write("\na:0:"+com+":"+cat+": "+cmm+"\n")
            except ValueError:print("!!--el limite que ingreso no es un numero")
        elif com=="v":
            vora()

    print("+------------------------------------------------------------+\n")

