import sys

class Dogru:
    def dogruDenklemi(self, a, b):
        ax, ay = a
        bx, by = b
        #y = mx + c
        try:
            m = (by-ay)/(bx-ax)
            c = ay - m*ax
            #print('m:',m,'c:',c)
            return (m, c)
        except ZeroDivisionError:
            # dikey doğru
            return None
            
        
    def y_bul(self, a, b, x):
        denklem = self.dogruDenklemi(a,b)
        if denklem:
            m, c = denklem
            y = m * x + c
            return round(y,4)
        else:
            return None

    def x_bul(self, a, b, y):
        denklem = self.dogruDenklemi(a,b)
        if denklem:
            m, c = denklem
            if m == 0:
                return None
            else:
                x = (y - c) / m
                return round(x,4)
        else:
            return a[0]
    

class Poligon:
    def __init__(self):
        self.dogru = Dogru()
        
    def noktalariAta(self, noktalar):
        self.noktalar = noktalar[:]
        # alan ve merkez hesabı için
        # poligonun ilk noktası sonda da bulunması gerekiyor.
        if self.noktalar[0] != self.noktalar[-1]:
            self.noktalar.append(self.noktalar[0])
                                 
                                 
    def alanBul(self):
        alan = 0.0
        for i in range(len(self.noktalar)-1):
            xi = self.noktalar[i][0]
            yi = self.noktalar[i][1]
            xiarti1 = self.noktalar[i+1][0]
            yiarti1 = self.noktalar[i+1][1]
            alan += xi * yiarti1 - xiarti1 * yi
            #print('alanBul:',i,xi,yi,xiarti1, yiarti1,alan)
        self.alan = alan/2
        return self.alan
    
    def merkezBul(self):
        alan = self.alanBul()
        xtop = 0.0
        ytop = 0.0
        for i in range(len(self.noktalar)-1):
            xi = self.noktalar[i][0]
            yi = self.noktalar[i][1]
            xiarti1 = self.noktalar[i+1][0]
            yiarti1 = self.noktalar[i+1][1]
            alttop = xi * yiarti1 - xiarti1 * yi
            xtop += (xi + xiarti1) * alttop
            ytop += (yi + yiarti1) * alttop

        self.xmerkez = xtop/(6 * alan)
        self.ymerkez = ytop/(6 * alan)
        return (self.xmerkez, self.ymerkez)

        

    def x_kesme(self, x):
        # x noktasından geçen doğrunun
        # poligonu kestiği noktaları bulur
        x0,y0 = self.noktalar[0]
        for xson, yson in self.noktalar[1:-1]:
            if x0 < x <= xson:
                y = self.dogru.y_bul((x0,y0),(xson,yson),x)
                #print('Y:',y)
                if y == None:
                    x0 = xson
                    y0 = yson
                    continue
                else:
                    return y
                    break
            else:
                x0 = xson
                y0 = yson
        else:
            #print('Kesmiyor')
            return None

    def y_kesme(self, y):
        # y=y doğrusunun 
        # poligonu kestiği noktaları bulur
       
        x0,y0 = self.noktalar[0]
        yeni_poligon = [(x0,y0)]
        for xson, yson in self.noktalar[1:-1]:
            x = self.dogru.x_bul((x0,y0),(xson,yson),y)
            #print('X:',x)
            
            if x == None:
                x0 = xson
                y0 = yson
                continue
            else:
                yeni_poligon.append((x,y))
                x0 = xson
                y0 = yson

        yeni_poligon.append(self.noktalar[-2])
        yeni_poligon.append(self.noktalar[0])

        # y'ye sahip x noktalarını bulalım.
        xler = sorted([nokta[0] for nokta in yeni_poligon if nokta[1] == y])
        #print('yeni_poligon:', yeni_poligon)
        self.noktalariAta(yeni_poligon)
        self.merkezBul()
        #print('Alan:%s, xmerkez:%s, ymerkez:%s' %
        #      (self.alan, self.xmerkez, self.ymerkez))
        return (self.alan, self.xmerkez, self.ymerkez, xler)                    

        
class Bulanik:
    def __init__(self):
        self.p = Poligon()
        
        self.ara_sinav = dict(
                zayif   = [(0,0),(0,1),(25,0)],
                orta    = [(0,0),(25,1),(50,0)],
                iyi     = [(25,0),(50,1),(100,0)],
                pekiyi  = [(50,0),(100,1),(100,0)]
                )

        self.genel_sinav = dict(
                zayif   = [(0,0),(0,1),(50,0)],
                orta    = [(0,0),(50,1),(75,0)],
                iyi     = [(50,0),(75,1),(100,0)],
                pekiyi  = [(75,0),(100,1),(100,0)]
                )

        self.basari = dict(
                F   = [(0,0),(0,1),(60,0)],
                C   = [(0,0),(60,1),(75,0)],
                B   = [(60,0),(75,1),(85,1),(100,0)],
                A   = [(75,0),(100,1),(100,0)]
                )


        self.uzman_gorus = {
            #('genel','ara'):Harf
            ('zayif','zayif')    :'F',
            ('zayif','orta')     :'F',
            ('zayif','iyi')      :'C',
            ('zayif','pekiyi')   :'C',
            ('orta','zayif')     :'C',
            ('orta','orta')      :'C',
            ('orta','iyi')       :'C',
            ('orta','pekiyi')    :'B',
            ('iyi','zayif')      :'C',
            ('iyi','orta')       :'B',
            ('iyi','iyi')        :'B',
            ('iyi','pekiyi')     :'B',
            ('pekiyi','zayif')   :'B',
            ('pekiyi','orta')    :'B',
            ('pekiyi','iyi')     :'A',
            ('pekiyi','pekiyi')  :'A',
            }

        self.basari_list = []
        
    def kesisimBul(self, sinav, notu):
        rt = {}
        for k, v in sinav.items():
            self.p.noktalariAta(v)
            y = self.p.x_kesme(notu)
            rt[k] = y
        return rt

    def hesabaBasla(self, ara_sinav_notu, genel_sinav_notu, goster=True):
        self.basari_list = []
        
        ara     = self.kesisimBul(self.ara_sinav, ara_sinav_notu)
        genel   = self.kesisimBul(self.genel_sinav, genel_sinav_notu)
        ara     = {k:v for k,v in ara.items() if v != None}
        genel   = {k:v for k,v in genel.items() if v != None}

        # uzman_gorus ve min degerleri bul
        uzman = []
        for gk,gv in genel.items():
            for ak,av in ara.items():
                harf = self.uzman_gorus[gk, ak]
                min_val = min(gv, av)
                uzman.append((harf, min_val))

        topalan = 0
        topalan_xmerkez = 0
        for harf, y in uzman:
            if y > 0:
                self.p.noktalariAta(self.basari[harf])
                alan, xmerkez, ymerkez, xler = self.p.y_kesme(y)

                self.basari_list.append((harf, abs(alan), xmerkez, ymerkez, y, xler))
                
                topalan += abs(alan)
                topalan_xmerkez += abs(alan) * xmerkez

        if topalan > 0:
            puan = topalan_xmerkez / topalan
        else:
            puan = 0

        self.ara    = ara
        self.genel  = genel
        self.uzman  = uzman
        self.puan   = puan

        if goster:
            print('Ara Sınav Notu:',ara_sinav_notu,ara)
            print('Genel Sınav Notu:',genel_sinav_notu, genel)
            print('Uzman:',uzman)
            print('Puan:',puan)
            print()
            

if __name__ == '__main__':
    b = Bulanik()
    b.hesabaBasla(40,90)
    b.hesabaBasla(100,100)
    b.hesabaBasla(99,99)
    b.hesabaBasla(1,1)

