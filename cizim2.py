from pol3 import Bulanik
from tkinter import *

class Cizim(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()

        self.canvas_width = 1000
        self.canvas_height = 650
        
        self.hesap = Bulanik()

        self.ara_not = 35
        self.genel_not = 78
        

        self.alanlariYap()
        self.xcarpan = 8
        self.ycarpan = 1.8
        self.sira = ['zayif','orta','iyi','pekiyi']
        self.basarisira = ['F','C','B','A']
        self.renkler = ['red','orange','lime green','maroon']

        #self.y_originler = (220, 470, 720)
        self.y_originler = (190, 410, 630)
        self.x_origin = 100
        self.grafikler = ['Ara Sınav', 'Genel Sınav', 'Başarı']

        self.sil_cizgi = []
        
        for grfk in range(3):
            x0 = self.x_origin
            y0 = self.y_originler[grfk]
            bilgi = self.grafikler[grfk]
         
            for i in range(len(self.sira)):
                if bilgi == 'Ara Sınav':
                    mesaj = self.sira[i]
                    noktalar = self.hesap.ara_sinav[mesaj]
                    
                elif bilgi == 'Genel Sınav':
                    mesaj = self.sira[i]
                    noktalar = self.hesap.genel_sinav[mesaj]
                else:
                    mesaj = self.basarisira[i]
                    noktalar = self.hesap.basari[mesaj]
                renk = self.renkler[i]
                
                self.poligonCiz(noktalar, renk, mesaj, x0, y0)

            self.eksenleriCiz(x0,y0,bilgi)


    def sonucCiz(self):
        for i in self.sil_cizgi:
            self.w.delete(i)

        #Ara sınavı çiz
        y0 = self.y_originler[0]
        notu = self.ara_not
        sonuc = self.hesap.ara
        self.sinavCiz(y0, notu)
        self.kesisimCiz(y0, notu, sonuc)
        
        #Genel sınavı çiz
        y0 = self.y_originler[1]
        notu = self.genel_not
        sonuc = self.hesap.genel
        self.sinavCiz(y0, notu)
        self.kesisimCiz(y0, notu, sonuc)
        
        #Hesaplanan Puanı çiz
        y0 = self.y_originler[2]
        notu = int(round(self.hesap.puan,0))
        sonuc = self.hesap.genel
        self.sinavCiz(y0, notu)
        
        #Uzman'ı göster
        self.bilgi.config(text='Uzman:  ' + str(self.hesap.uzman)+
                          '\t PUAN: '+str(self.hesap.puan))
        # Başarı çiz
        basari = self.hesap.basari_list
        for b in basari:
            
            harf, alan, xmerkez, ymerkez, y, xler = b
            xa, xb = xler
            str_alan = 'Alan: %.2f' % alan

            renk = self.renkler[self.basarisira.index(harf)]

            x0 = self.x_origin 
            y0 = self.y_originler[2]

            x1 = x0 + xa * self.xcarpan
            y1 = y0 - y * self.ycarpan*100
            x2 = x0 + xb * self.xcarpan
            l1 = self.w.create_line(x1, y1, x2, y1, fill = renk)
            self.sil_cizgi.append(l1)
            xorta = (x1 + x2)/2
            t1 = self.w.create_text(xorta, y1-8, text=str(y), fill = renk)
            t2 = self.w.create_text(xorta, y1+8, text=str_alan, fill = renk)
            self.sil_cizgi.append(t1)
            self.sil_cizgi.append(t2)
            # Ağırlık merkezlerini koy
            x1 = x0 + xmerkez * self.xcarpan
            y1 = y0 - ymerkez * self.ycarpan * 100
            p = self.w.create_oval(x1-3, y1-3, x1+3, y1+3, fill = renk)
            self.sil_cizgi.append(p)
            #p_text = '(%.2f,%.2f)' % (xmerkez, ymerkez)
            p_text = '%.2f' % xmerkez
            pt = self.w.create_text(x1, y1+8, text=p_text, fill = 'black')
            self.sil_cizgi.append(pt)
            
    def sinavCiz(self, y0, notu):
        x0 = self.x_origin
        y0 = y0

        x = x0 + notu * self.xcarpan
        n1 = self.w.create_line(x, y0, x, y0-200, fill = 'blue')
        self.sil_cizgi.append(n1)
        t = self.w.create_text(x+8, y0-180, text=str(notu), fill='blue')
        self.sil_cizgi.append(t)
        
    def kesisimCiz(self, y0, notu, sonuc):
        x0 = self.x_origin
        y0 = y0

        x = x0 + notu * self.xcarpan
        kesisimler = sonuc
        for k, v in kesisimler.items():
            sira = self.sira.index(k)
            renk = self.renkler[sira]
            y = y0 - v*self.ycarpan*100
            n2 = self.w.create_line(x,y, x0, y, fill = renk)
            self.sil_cizgi.append(n2)
            t = self.w.create_text(x0+20, y-5, text=str(v), fill=renk)
            self.sil_cizgi.append(t)
            
    def hesapla(self):
            
        self.ara_not    = int(self.ent_ara_not.get())
        self.genel_not  = int(self.ent_genel_not.get())
        self.hesap.hesabaBasla(self.ara_not, self.genel_not)

        self.sonucCiz()
      
    def mesajYeriBul(self,noktalar):
        #y'si minimum, x'i maksimum olan nokta bulunacak.
        l=sorted(noktalar, key=lambda nokta:(nokta[1], -nokta[0]))
        return l[0]
    
    def poligonCevir(self, noktalar, x0, y0):
        rt = []
        for x, y in noktalar:
            xyeni = x0 + x*self.xcarpan
            yyeni = y0 - y*self.ycarpan*100
            rt.append((xyeni, yyeni))
        return rt

    def poligonCiz(self, noktalar, renk, mesaj, x0, y0):
        noktalar = self.poligonCevir(noktalar, x0, y0)
        self.w.create_polygon(noktalar, fill='', width = 2, outline=renk)
        mesajyeri = self.mesajYeriBul(noktalar)
        self.w.create_text(mesajyeri[0]+20, mesajyeri[1]-4, text=mesaj)
        
    def eksenleriCiz(self, x0, y0, bilgi):
        xmax, ymax = 800, 180
        
        fg = 'blue'
        kalinlik = 3
        line_prop = dict(fill=fg, width=kalinlik,
                         arrow='last',arrowshape='16 16 3')
        
        self.w.create_line(x0,y0, x0+xmax+20, y0, **line_prop)  #x-ekseni
        self.w.create_line(x0,y0, x0, y0-ymax-20, **line_prop)  #y-ekseni
        for x in range(10,101,10):
            xp = x0+x*self.xcarpan
            self.w.create_line(xp, y0+3, xp, y0-3)
            self.w.create_text(xp, y0+10, text=str(x))
        
        
        for y in range(10,101,10):
            yp = y0 - y*self.ycarpan
            self.w.create_line(x0-3,yp, x0+3, yp)
            self.w.create_text(x0-20, yp, text=str(y/100))

        self.w.create_text(35, y0-100, text= bilgi)
        
        
    def alanlariYap(self):
        
        self.master.title( "Bulanık Mantık Algoritması" )

        #Tuşlar için frame
        frmTus = Frame(self, width = 250,
                       height = self.canvas_height, bd=3,
                       relief = RAISED)
        frmTus.pack(side=LEFT, expand=YES, fill = BOTH)
        
        row = 1
        # Notlar için Entry oluştur
        lab = Label(frmTus, text='Ara Sınav Notu', width=15)
        ent1 = Entry(frmTus, justify=CENTER, bd=3, width=15)
        ent1.insert(0, self.ara_not)
        lab.grid(row=row, sticky=W, padx=15)
        ent1.grid(row = row+1, sticky=W, padx=15)
        self.ent_ara_not = ent1

        row += 2
        lab = Label(frmTus, text='Genel Sınav Notu', width=15)
        ent2 = Entry(frmTus, justify=CENTER, bd=3, width=15)
        ent2.insert(0, self.genel_not)
        lab.grid(row=row, sticky=W, padx=15)
        ent2.grid(row = row+1, sticky=W, padx=15)
        self.ent_genel_not = ent2
       
        
        row += 3
        #Butonlar
        tus_bilgi = (
                     ('Hesapla', self.hesapla,'normal'),
                     ('Çıkış', self.quit,'normal'),
                      )

        self.tuslar = {}
        for text, metot, durum in tus_bilgi:
            b = Button(frmTus, text = text, command = metot, state=durum, width=15)
            b.grid(row =row,sticky=W, padx=15, pady=5)
            row += 1
            self.tuslar[text] = b
 
        
        # Bilgi label'i
        l = Label(self, text='Bilgi: ', fg='red', bd=4, relief=RAISED)
        l.pack(side=TOP, fill=X)
        self.bilgi = l

        #Canvas
        self.w = Canvas(self, width = self.canvas_width,
                        height = self.canvas_height)
        self.w.pack(expand=YES, fill = BOTH)



if __name__ == '__main__':

    czm = Cizim()
    czm.mainloop()
