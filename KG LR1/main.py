import numpy as np
from PIL import Image
from math import floor #округление вниз

scale = 5000
img_mat = np.zeros((1000,1000,3), dtype = np.uint8) #беззнаковое целочисленное 8-битное, полутоновый -> цветной белый квадрат

''' for i in range (1000):
   for j in range(1000):
      img_mat[i,j]= (i+j) % 256    '''      #белый квадрат 255,255,255 R,G,B [255, 0,255] 

def make_line (img_mat, x0, y0, x1, y1):
    d_max = max(abs(floor(x0) - floor(x1)), abs(floor(y0) - floor(y1)) )
    L = d_max + 1
    if L == 1:
        img_mat[floor(y0), floor(x0)] = 255 #ставим точку
        return
    d_x = (x1 - x0)/ (L - 1)
    d_y = (y1 - y0)/ (L - 1)

    x = x0
    y = y0
    for _ in range(L): 
        img_mat[floor(y), floor(x)] = 255
        x += d_x
        y += d_y


#make_line(img_mat, x0, y0, x1, y1)

#x0,y0,x1,y1 = 30.5, 40.1, 500.0, 950.9

v = []
f = []
file = open('model.obj')
for s in file:
    spl = s.split()
    if(spl[0] == 'v'):
        v.append([float(spl[1]), float(spl[2]), float(spl[3])])
    elif (spl[0] == 'f' ):
        f.append( [spl[1].split('/')[0], spl[2].split('/')[0], spl[3].split('/')[0]] )#берем первую часть
        


for i in range(len(v)):
    x =  v[i][0] * scale + 500 #добавляем центр изображения, переносим его
    y = -v[i][1] * scale + 500
    img_mat[int(y), int(x)] = [255, 192, 203]   


for i in range (len(f)):   # f[i] - номера вершин i-ого полигона, f[i][0] - номера нулевой вершины i-ого полигона
    x0 = v[int(f[i][0]) - 1][0] * scale + 500  # x координата нулевой точки i-ого полигона
    y0 = -v[int(f[i][0]) - 1][1] * scale + 500
    x1 = v[int(f[i][1]) - 1][0] * scale + 500
    y1 = -v[int(f[i][1]) - 1][1] * scale + 500
    x2 = v[int(f[i][2]) - 1][0] * scale + 500
    y2 = -v[int(f[i][2]) - 1][1] * scale + 500

    make_line(img_mat, x0, y0, x1, y1)
    make_line(img_mat, x0, y0, x2, y2)
    make_line(img_mat, x1, y1, x2, y2)


img = Image.fromarray(img_mat)
img.save('img.png')