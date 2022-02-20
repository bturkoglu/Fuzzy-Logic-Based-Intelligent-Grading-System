import sys

class Dogru:
    def dogruDenklemi(self, n1, n2):
        x1, y1 = n1
        x2, y2 = n2
        
        fark_y = y2 - y1
        fark_x = x2 - x1

        #ax + by + c = 0
        a = - fark_y
        b = fark_x
        c = fark_y * x2 - fark_x * y2
        return (a,b,c)
            
        
    def y_bul(self, n1, n2, x):
        denklem = self.dogruDenklemi(n1,n2)
        a,b,c = denklem
        #ax + by + c = 0
        # y = (-ax-c)/b
        
        if b:
            y = (-a*x - c)/b
            return round(y,4)
        else:
            return None

    def x_bul(self, n1, n2, y):
        denklem = self.dogruDenklemi(n1,n2)
        a,b,c = denklem
        #ax + by + c = 0
        # x = (-by-c)/a
        
        if a:
            x = (-b*y - c)/a
            return round(x,4)
        else:
            return None

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

        self.genel_sinav = dict(
            zayif=[(0, 0), (0, 1), (50, 0)],
            orta=[(0, 0), (50, 1), (100, 0)],
            iyi=[(50, 0), (100, 1), (100, 0)],
        )
        
        self.ara_sinav1 = dict(
                zayif   = [(0,0),(0,1),(50,0)],
                orta    = [(0,0),(50,1),(100,0)],
                iyi     = [(50,0),(100,1),(100,0)],
                )

        self.ara_sinav2 = dict(
            zayif=[(0, 0), (0, 1), (50, 0)],
            orta=[(0, 0), (50, 1), (100, 0)],
            iyi=[(50, 0), (100, 1), (100, 0)],
        )


        self.basari = dict(
                S   = [(0, 0), (0, 1), (50, 0)],
                M   = [(0, 0), (50, 1), (100, 0)],
                L   = [(50, 0), (100, 1), (100, 0)],
                )


        self.uzman_gorus = {
            #('genel','ara1','ara2'):Harf
            ('zayif', 'zayif', 'zayif'): 'L',
            ('zayif', 'zayif', 'orta'): 'L',
            ('zayif', 'zayif', 'iyi'): 'L',

            ('zayif', 'orta', 'zayif'): 'L',
            ('zayif', 'orta', 'orta'): 'L',
            ('zayif', 'orta', 'iyi'): 'L',

            ('zayif', 'iyi', 'zayif'): 'L',
            ('zayif', 'iyi', 'orta'): 'L',
            ('zayif', 'iyi', 'iyi'): 'L',



            ('orta', 'zayif', 'zayif'): 'L',
            ('orta', 'zayif', 'orta'): 'M',
            ('orta', 'zayif', 'iyi'): 'M',

            ('orta', 'orta', 'zayif'): 'L',
            ('orta', 'orta', 'orta'): 'L',
            ('orta', 'orta', 'iyi'): 'M',

            ('orta', 'iyi', 'zayif'): 'S',
            ('orta', 'iyi', 'orta'): 'S',
            ('orta', 'iyi', 'iyi'): 'S',



            ('iyi', 'zayif', 'zayif'): 'M',
            ('iyi', 'zayif', 'orta'): 'M',
            ('iyi', 'zayif', 'iyi'): 'M',

            ('iyi', 'orta', 'zayif'): 'S',
            ('iyi', 'orta', 'orta'): 'S',
            ('iyi', 'orta', 'iyi'): 'S',

            ('iyi', 'iyi', 'zayif'): 'L',
            ('iyi', 'iyi', 'orta'): 'M',
            ('iyi', 'iyi', 'iyi'): 'S',


            }

        self.basari_list = []
        
    def kesisimBul(self, sinav, notu):
        rt = {}
        for k, v in sinav.items():
            self.p.noktalariAta(v)
            y = self.p.x_kesme(notu)
            rt[k] = y
        return rt

    def hesabaBasla(self, ara_sinav_notu1, ara_sinav_notu2, genel_sinav_notu, goster=True):
        self.basari_list = []
        
        ara1     = self.kesisimBul(self.ara_sinav1, ara_sinav_notu1)
        ara2     = self.kesisimBul(self.ara_sinav2, ara_sinav_notu2)
        genel   = self.kesisimBul(self.genel_sinav, genel_sinav_notu)
        ara1     = {k:v for k,v in ara1.items() if v != None}
        ara2     = {k:v for k,v in ara2.items() if v != None}
        genel   = {k:v for k,v in genel.items() if v != None}

        # uzman_gorus ve min degerleri bul
        uzman = []
        for gk,gv in genel.items():
            for ak1,av1 in ara1.items():
                for ak2,av2 in ara2.items():
                    harf = self.uzman_gorus[gk, ak1, ak2]
                    min_val = min(gv, av1, av2)
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

        self.ara1    = ara1
        self.ara2    = ara2
        self.genel  = genel
        self.uzman  = uzman
        self.puan   = puan

        if goster:
            print('Ara Sınav Notu1:',ara_sinav_notu1,ara1)
            print('Ara Sınav Notu2:',ara_sinav_notu2,ara2)
            print('Genel Sınav Notu:',genel_sinav_notu, genel)
            print('Uzman:',uzman)
            print('Puan:',puan)
            print()
            

if __name__ == '__main__':
    b = Bulanik()
    b.hesabaBasla(40, 40, 90)
    b.hesabaBasla(100, 100, 100)
    b.hesabaBasla(99, 99, 99)
    b.hesabaBasla(1, 1, 1)

