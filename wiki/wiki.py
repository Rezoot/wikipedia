
import requests
from bs4 import BeautifulSoup as bs 
from tkinter import *
from time import sleep as spanko
from pyautogui import size
from threading import Thread
import os
from PIL import Image
#from time import sleep
#from urllib.request import urlopen
#from PIL import Image

#wielkosc monitora
screenWidth, screenHeight = size()
#wszystko w tekst bêdzie usuwane    
tab=[]
tabboczne=[]
#historia klikania
historia=[0]

#zwiazane z zdjeciami
ktory=0
obrazy=[]
luki=[]




#zmiana tytulu :V
def dzial():
        
    tyt.config(text=tytul)
    

    


#1cofanie, 0start, 2odnowa, 3reload
def back(opcja):
    if opcja==0:
        historia[2:].clear()
        aktualna(historia[1])
    elif opcja==2:
        historia.clear()
        historia.append(0)
        aktualna("https://pl.wikipedia.org/wiki/Specjalna:Losowa_strona")
    elif opcja==3:
        aktualna(historia[-1])
    else:
        a=historia[-2]
        if a==0:
            print("nah")
        else:
            historia.pop(-1)
            historia.pop(-1)
            aktualna(a)

def zdjecie_boczne(x,zdj,tex,kt):
   global ktory 
   req=requests.get(x)
   if req.status_code==200:
       obraz="obr"+str(kt)+".png"
       with open(obraz, 'wb') as f:
            f.write(req.content)
       
       obrazy.append(obraz)
       #proba za³adowania zdjecia
       try:
        luki[kt].config(file=obraz)
        but=Label(image=luki[kt])
        kotek1 = Image.open(obraz)
        w, h = kotek1.size
        zdj.config(height=h/15)
        
       except:#w przeciwnym razie poka¿ error
           but=Label(text="error formatu",bg="white")

           try:
               zdj.config(height=2)
           except:
               print("o chuj chodzi")
    


           #do naprawienia?? czasami za szybko dzia³a?
       try:
        zdj.window_create(END, window=but)
        zdj.insert(END,tex)
       except:
           print("o chuj chodzi")

   else:
       try:
        zdj.insert(END,"error: "+ str(req.status_code))
       except:
        print("o chuj chodzi")   
       ktory-=1 
   #print(tex)


#wy³uskanie tekstu
def znajdz(x):
    
    
    def tabelka(x,rodzaj):

        #tytul prawej tabelki wraz z kolorem
        def caption(x):
            
            bg2="white"
            fg2="black"
            try:
                stop=17
                for i in x["style"][17:]:
                    if i==";":
                        break 
                    stop+=1
                bg2=x["style"][17:stop]
                
                stop+=8
                stop2=stop
                for i in x["style"][stop:]:
                    if i==";":
                        break
                    stop2+=1
                fg2=x["style"][stop:stop2]
                if fg2[0]==":":
                    fg2=fg2[1:]
            except:
                pass
            
            tek=""

            
            for i in x.find_all("div"):
                if i.get("class") ==['iboxt-1'] or i.get("class") ==['iboxt-2'] or i.get("class") ==['iboxt-3']:
                    tek+=i.get_text()
                    tek+="\n"
                
            tek=tek[:-1]            
            
            tytboczny=Label(f2,font=("a",10),bg=bg2,text=tek,fg=fg2,width=24,height=2,justify='center')
            
            tytboczny.grid(row=1,column=0)
            tabboczne.append(tytboczny)
            tabboczne.append(1)#korekta tabelki

        #wydobycie zawartosci tabelki
        def wydobycie(x,rodzaj):
            col=[]
            ile=0

            def przerwa_w_tekscie(x):
                wysokosc=1
                zdanie=[]
                while True:
                    if len(x)>24*wysokosc:
                        wysokosc+=1
                    else:
                        break
                if wysokosc>1:
                    for i in x:
                        zdanie.append(i)
                    for i in zdanie[20:]:
                        #print(zdanie)
                        pass
                return x

            def zdjecie(link,ewtext,rodzaj):
                if rodzaj==1:
                    global ktory
                    colos=i.get("colspan")
                    rowos=i.get("rowspan")
                    zdj=Text(f2,width=24,pady=3)
                    zdj.grid(row=linia,column=c,columnspan=colos,rowspan=rowos)
                    tabboczne.append(zdj)
                    ktory+=1
                    foto=Thread(target=lambda:zdjecie_boczne(link,zdj,ewtext,ktory))
                    foto.start()

            #linki bocznej    
            def alink(c,ile,wysokosc):
                
                def zdobyc(i,tek):
                    for j in i:
                        
                        #print(j.name)
                        if  j.name==None:
                            if j=="\xa0":
                                tek+="\n"
                                
                            elif j!="\n":
                                tek+=j
                                
                        elif j.name=="a":
                            
                            a.insert(END,tek)
                            tek=''

                            link="https://pl.wikipedia.org"+j.get("href")
                            but=Button(a,text=j.get_text(),fg="blue",bd=0,bg="white",activebackground="white",command=lambda: aktualna(link))
                            a.window_create(END, window=but) 
                        else:
                           zdobyc(j,tek)
                           

                    
                a=Text(f2,width=24,pady=3)
                tek=''
                
                zdobyc(i,tek)
                
                #for j in i.get_text():
                #    if j=="\n":
                #       pass
                #   else:
                #        tek+=j
                #tek=przerwa_w_tekscie(tek)        
                #try:    
                #    link="https://pl.wikipedia.org"+i.find("a").get("href")
                #    but=Button(a,text=tek,fg="blue",bd=0,bg="white",activebackground="white",command=lambda: aktualna(link))
                #    a.window_create(END, window=but)
                #except:
                #    print(i.find("a").get("href"),"nie dziala")
                #    print(i.find("a"))
                #    a.insert(END,tek)

                while True:    
                    if len(tek)>24*wysokosc:
                        wysokosc+=1
                    else:    
                        break
                                    
                                
                                
                colos=i.get("colspan")
                rowos=i.get("rowspan")
                tabboczne.append(a)
                a.grid(row=linia,column=c,columnspan=colos,rowspan=rowos)
                ile+=1
                c+=1
                return c,ile,wysokosc

            def zwyktekst(c,ile,wysokosc):
                colos=i.get("colspan")
                rowos=i.get("rowspan")
                a=Text(f2,width=24,pady=3)
                            
                tek=''
                for j in i.get_text():
                    if j=="\n":
                        pass
                    elif j==chr(8226) and tek!='':
                        tek+="\n"
                        tek+=j
                    else:
                        tek+=j
                while True:    
                        if len(tek)>24*wysokosc:
                            wysokosc+=1
                        else:    
                            break
                                    


                a.insert(END,tek)
                tabboczne.append(a)
                            
                a.grid(row=linia,column=c,columnspan=colos,rowspan=rowos)
                c+=1
                ile+=1
                return c,ile,wysokosc



            global linia
            wysokosc=1
            if x.name==None:
                pass
            elif x.name=="tr":
                linia+=1
                


                #komórki dla bocznej tabelki  
                #przysz³y me obliczaæ d³ugoœæ tabelki. mo¿e zrobiæ ³adniejszy kod 
                if rodzaj==1:
                    c=0
                    for i in x:
                        col.append(i)
                    for i in col:
                        if i=="\n":
                            pass
                        elif i.find("a")!=None:


                            if i.find("a").find("img")!=None:#znowu cos zdjêcie ................
                                link="https:" + i.find("a").find("img").get("src")
                                ewtext=i.get_text()
                                zdjecie(link,ewtext,1)
                                ile+=1
                                c+=1
                                
                            #zwykly link
                            else:
                                c,ile,wysokosc=alink(c,ile,wysokosc)
                                
                        
                        elif i.find("img")!=None:
                                link="https:" + i.find("img").get("src")
                                i.get_text()
                                zdjecie(link,i,1)
                                c+=1
                                ile+=1
                                
                        #zwyk³y tekst w bocznej ramce
                        else:
                            c,ile,wysokosc=zwyktekst(c,ile,wysokosc)
                                     

                    tabboczne.append(ile)
                    for j in range(tabboczne[-1]):
                        tabboczne[-2-j].config(height=wysokosc)
                  

                #komórki dla innych tabelek
                else:
                    pass

            else:
                for i in x:
                    wydobycie(i,rodzaj)

        #poprawia wygl¹d bocznej, zmieniaj¹c rozmiar komórek.  ale mo¿e zamienie na ka¿d¹ tabelke     
        def poprawa_bocznej():
            liczby=[]
            for i in tabboczne:
                if type(i)==int:
                    liczby.append(i)
            maks=max(liczby)
            tabboczne[0].grid(columnspan=maks)
            for i in range(len(tabboczne)):#sprawdza ca³a tabelke
                if type(tabboczne[i])==int: #sprawdza czy liczba
                    if tabboczne[i]!=maks:#sprawdza czy jest najwieksza 
                        for j in range(tabboczne[i]):#sprawdza ile ich jest w rzêdzie 
                            obliczone=int(24*maks/tabboczne[i])#obliczona d³ugosc komórki
                            
                            tabboczne[i-j-1].config(width=obliczone)#zmiana szerokosci 
                            if tabboczne[i-j-1]!=tabboczne[0]:#sprawdza czy nie jest label
                                if obliczone/24==maks:#center
                                    tabboczne[i-j-1].tag_configure("center", justify='center')
                                    tabboczne[i-j-1].tag_add("center",1.0,END)
                                if len(tabboczne[i-j-1].get(1.0,END))<=24*obliczone:#sprawdza d³ugosc oraz ja zmienia
                                    tabboczne[i-j-1].config(height=1)
                                else:
                                    n=2
                                    while True:
                                        if len(tabboczne[i-j-1].get(1.0,END))>24*n:
                                            n+=1
                                        else:
                                            tabboczne[i-j-1].config(height=n)
                                            break

            tabboczne.append(0)
            


        if x.name==None:
            print(x)#pamietac o tym XDDDDDDDDDDDD
        elif x.name=="caption" and rodzaj==1:
            caption(x)

        elif x.name=="style":
            pass
        elif x.name=="tbody":
            wydobycie(x,rodzaj)
        else:
            for i in x:
                tabelka(i,rodzaj)

        #poprawi wyglad tabelki bocznej
        
        if rodzaj==1 and tabboczne!=[] and len(tabboczne)!=2 and tabboczne[-1]!=0:
            poprawa_bocznej()
            


       #spis treœci do zrobienia!!!!!!!!!!!!!!
    def h2(x,wielkosc):#podtytu³ i spis tresci
        tekst.insert(END,"\n")
        
        headline=x.find(class_="mw-headline")
        
        if headline!=None:
            headline=headline.get_text()
            Lobel=Label(tekst,text=headline,bg="white",fg="black",font=('Helvetica',wielkosc,"bold"))
            tekst.window_create(END, window=Lobel)
            
        else:
            x.get_text()#spis treœci
        tekst.insert(END,"\n")

    def a(x):#przycisk w tekscie
        but=Button(tekst,text=x.get_text(),fg="blue",bd=0,bg="white",activebackground="white",font=('Helvetica',10),command=lambda: aktualna("https://pl.wikipedia.org"+x.get("href")))
        tekst.window_create(END, window=but)

    def none(x):#wypisywanie czystego tekstu
        if x.get_text()!="\n":
            tekst.insert(END,x.get_text())

    def b(x):#pogrubione slowa
        Lobel=Label(tekst,text=x.get_text(),bg="white",font=('Helvetica',10,'bold'))
        tekst.window_create(END, window=Lobel)   

    #sprawdza czy tabelka jest boczna czy zawarta w tekscie
    if x.name=="table":
        try:
            if x['class']==['infobox']:
                boczna = Thread(target=lambda:tabelka(x,1))
                boczna.start()
                
            else:
                tabelka(x,0)
        except:
            tabelka(x,0)
    
    #button 
    elif x.name=="a":
        a(x)  
    elif x.name=="img":
        pass
        
    

    #none-wypisz 
    #h2, h3, h4 tytuly
    #b pogrubiony        
    elif x.name==None:
        none(x)
    elif x.name=="h2":
        h2(x,14)
    elif x.name=="h3":
        h2(x,12)
    elif x.name=="h4":
        h2(x,10)
    elif x.name=="b":
        b(x)   
    elif x.name=="style": #niepotrzebne pomin¹æ
        pass
    else:#zaglebianie sie w tekst
        for i in x:
            znajdz(i)
            
            
            
          
        
#l¹czenie oraz gridy
def aktualna(url):
    def des1():
        tekst.delete('1.0', END)
        for i in tab:
            i.destroy()
        tab.clear()
        for i in tabboczne:
            if type(i)!=int:
                i.destroy()
        tabboczne.clear()
        obrazy.clear()

    def slep():
        try:
            okno.geometry("%dx%d" % (szerokosc, wysokosc+1))
            spanko(1)
            okno.geometry("%dx%d" % (szerokosc, wysokosc))
        except:
            pass



    global linia,ktory,tytul
    linia=2
    ktory=0
    dziala=1
    tekst.config(state=NORMAL)
           
    #kasuje ca³y tekst przy ka¿dym odpaleniu 
    des1()
    
    sl=Thread(target=slep)
    sl.start()
    

    
    #w sumie to sprawdza czy strona istnieje
    while dziala!=0:
        try:
            download_html = requests.get(url)
            dziala=0
        except:
            if historia[-1]==0:
                url="https://pl.wikipedia.org/wiki/Specjalna:Losowa_strona"
            else:
                tekst.insert(1.0,"nie dziala  \n\n")
                url=historia[-1]

    print(url)
    if download_html.status_code==200:
        print("polaczone \n")
        zupa=bs(download_html.text,"html.parser")

        tytul=zupa.title.string[0:-32]
        historia.append(zupa.find("link",rel="canonical").get("href"))
        
    
        divy=zupa.find(id="bodyContent").find("div",class_="mw-parser-output")
        
        
      
        if divy!=None:
            for x in divy:
                 znajdz(x)
            razy=4.5
            if int(tekst.index(END)[:-2])*razy>tekst_height:
                tekst.config(height=int(tekst.index(END)[:-2])*razy)  
                okno.geometry("%dx%d" % (szerokosc, wysokosc+1))
    
                
            tekst.config(state=DISABLED)


            
        else:
            tekst.insert(END,"brak info")
        
            
        #zmienia tytul
        dzial()
       



        #testowe url





url="https://pl.wikipedia.org/wiki/Specjalna:Losowa_strona"
#url="https://pl.wikipedia.org/wiki/Autostrada_A6a_(Francja)"
#url="https://pl.wikipedia.org/wiki/987_p.n.e."
#url="https://pl.wikipedia.org/wiki/Love_is_Beautiful"
#url="https://pl.wikipedia.org/wiki/Puchar_%C5%9Awiata_w_skokach_narciarskich_w_Harrachovie"
#url="https://pl.wikipedia.org/wiki/Marcin_S%C3%B3jka"
#url="https://pl.wikipedia.org/wiki/Tu_bije_serce_Europy!_Wybieramy_hit_na_Eurowizj%C4%99!"
#url="https://pl.wikipedia.org/wiki/Ci%C4%85g_Fibonacciego"
#url="https://pl.wikipedia.org/wiki/Kategoria:Miasta_w_Danii"
#url="https://pl.wikipedia.orghttp://rmigovernment.org/about_your_government.jsp?docid=6"
#url="https://pl.wikipedia.org/wiki/Kiwiciowce"
#url="https://pl.wikipedia.org/wiki/Pa%C5%82ac_w_Bystrzycy_Dolnej"
#url="https://pl.wikipedia.org/wiki/Alessio_Sitti"
url="https://pl.wikipedia.org/wiki/Boucoiran-et-Nozi%C3%A8res"

#surowy wyglad
okno=Tk()
okno.configure(bg='white')

szerokosc=int(screenWidth/1.4)
wysokosc=int(screenHeight/1.3)
srodekx=int(screenWidth/10)
srodeky=int(screenHeight/10)
okno.geometry("%dx%d+%d+%d" % (szerokosc, wysokosc, srodekx, srodeky))


onf=Frame(okno,bg="white")
onf.pack(fill=BOTH,expand=1)


canv=Canvas(onf,bg="white")
canv.pack(side=LEFT,fill=BOTH,expand=1)

scrol=Scrollbar(onf,orient=VERTICAL,command=canv.yview)
scrol.pack(side=RIGHT,fill=Y)

canv.configure(yscrollcommand=scrol.set)
canv.bind('<Configure>',lambda e: canv.configure(scrollregion=canv.bbox("all")))


frampomo=Frame(canv,bg="white")




f=Frame(frampomo,bg="white")
f.pack(side=LEFT,padx=(20,0))


canvcreate=canv.create_window((0,0),window=frampomo,anchor="nw")


f2=Frame(frampomo,bg="white",relief=SOLID,bd=2)
f2.pack(side=TOP,padx=(20,0))



tyt=Label(f,text='',font=("comic sans",20),bg="white")
tekst_width=int(screenWidth/15)
tekst_height=int(screenHeight/22)
tekst=Text(f,bg="white",wrap=WORD,font=('Helvetica',10),height=tekst_height,width=tekst_width,bd=0)

miniframe=Frame(f2,bg="white")
miniframe.grid(row=0,column=0,columnspan=4)



#sekcja butonów

fontbut=("a",10,"bold")#font
szero=10 #szerokosc butona
bag="white" #kolor tylu
rel=GROOVE #rodzaj bordera
bed=3#wielkosc bordera

buto=Button(miniframe,text="od nowa",command=lambda:back(2),font=fontbut,width=szero,bg=bag,relief=rel,bd=bed)
buto2=Button(miniframe,text="back",font=fontbut,command=lambda:back(1),width=szero,bg=bag,relief=rel,bd=bed)
buto3=Button(miniframe,text="start",font=fontbut,command=lambda:back(0),width=szero,bg=bag,relief=rel,bd=bed)
buto4=Button(miniframe,text="R",font=fontbut,command=lambda:back(3),width=2,bg=bag,relief=rel,bd=bed)





buto.pack(side=LEFT,pady=2,padx=(0,10))
buto2.pack(side=LEFT,pady=2,padx=10)
buto3.pack(side=LEFT,pady=2,padx=(10,0))
buto4.pack(side=LEFT,pady=2,padx=(10,0))
tekst.grid(row=1,column=0,columnspan=10,rowspan=3000)
tyt.grid(row=0,column=0,columnspan=20)

for i in range(40):
    phi=PhotoImage()
    luki.append(phi)


aktualna(url)



okno.mainloop()

for i in range(41):
    linko="obr"+str(i)+".png"
    try:
        os.remove(linko)
    except:
        pass


print("zakonczona praca")




