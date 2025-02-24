import cv2
import numpy as np

resim1 = cv2.imread('resim1.jpg')




gri_ton=cv2.cvtColor(resim1, cv2.COLOR_BGR2GRAY)

a,b=gri_ton.shape

boyut=150

cv2.rectangle(gri_ton,( 0,0),(boyut,boyut),(0,0,0), -1)
cv2.rectangle(gri_ton, (b - boyut, 0), (b, boyut), (0, 0, 0), -1)  
cv2.rectangle(gri_ton, (0, a - boyut), (boyut, a), (0, 0, 0), -1)  
cv2.rectangle(gri_ton, (b - boyut, a - boyut), (b, a), (0, 0, 0), -1)



cv2.imwrite('gri_tonlama_siyah_4kare.jpg', gri_ton)
cv2.imshow('Gri ton ', gri_ton)
cv2.waitKey(0)
cv2.destroyAllWindows()





agac_resmi = cv2.imread('agac.png', cv2.IMREAD_UNCHANGED)

agac_yukseklik, agac_genislik, _ = agac_resmi.shape
resim1_yukseklik, resim1_genislik, _ = resim1.shape

scaling_factor = 0.2
yeni_genislik = int(resim1_genislik * scaling_factor)
yeni_yukseklik = int(agac_yukseklik * (yeni_genislik / agac_genislik))

agac_resmi_boyutlu = cv2.resize(agac_resmi, (yeni_genislik, yeni_yukseklik))

yeni_yukseklik, yeni_genislik, _ = agac_resmi_boyutlu.shape

x_offset = 575
y_offset = 250

if agac_resmi_boyutlu.shape[2] == 4:
    alfa_kanali = agac_resmi_boyutlu[:, :, 3] / 255.0
    agac_resmi_rgb = agac_resmi_boyutlu[:, :, :3]

    for c in range(0, 3):
        resim1[y_offset:y_offset + yeni_yukseklik, x_offset:x_offset + yeni_genislik, c] = \
            (1 - alfa_kanali) * resim1[y_offset:y_offset + yeni_yukseklik, x_offset:x_offset + yeni_genislik, c] + \
            alfa_kanali * agac_resmi_rgb[:, :, c]
else:
    resim1[y_offset:y_offset + yeni_yukseklik, x_offset:x_offset + yeni_genislik] = agac_resmi_boyutlu

#agacın arka planını kaldırmak için stackoverflow sitesinden bu kodu buldum

cv2.imwrite('manzara_ile_agac.png', resim1)

cv2.imshow('Manzara ve Ağaç', resim1)
cv2.waitKey(0)
cv2.destroyAllWindows()








x1, y1 = 252, 269
x2, y2 = 354, 240

yeni_x, yeni_y = 1620, 273
x2_yeni, y2_yeni = 1722, 244

kesilen_resim = resim1[y2:y1, x1:x2]

resim1[yeni_y:yeni_y + (y1 - y2), yeni_x:yeni_x + (x2 - x1)] = kesilen_resim

cv2.imwrite('sonuc_resmi_yeni.jpg', resim1)

cv2.imshow('Sonuç Görüntüsü', resim1)
cv2.waitKey(0)
cv2.destroyAllWindows()





def rotate_image(resim1, angle):
    (a, b) = resim1.shape[:2]
    center = (b // 2, a // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    donmus_resim = cv2.warpAffine(resim1, matrix, (b, a))
    return donmus_resim

resim_45_sola = rotate_image(resim1, 45)
resim_60_saga = rotate_image(resim1, -60)

cv2.imwrite('klasor/45_sola_donmus_resim.jpg', resim_45_sola)
cv2.imwrite('klasor/60_saga_donmus_resim.jpg', resim_60_saga)

cv2.imshow('45 Derece Sola Döndürülmüş', resim_45_sola)
cv2.imshow('60 Derece Sağa Döndürülmüş', resim_60_saga)
cv2.waitKey(0)
cv2.destroyAllWindows()



aranan_bolge = cv2.imread('aranan_bolge.png')

sonuc = cv2.matchTemplate(resim1, aranan_bolge, cv2.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(sonuc)

sol_ust = max_loc

h, w = aranan_bolge.shape[:2]

alt_sag = (sol_ust[0] + w, sol_ust[1] + h)

cv2.rectangle(resim1, sol_ust, alt_sag, (0, 255, 0), 2)

cv2.imshow('Eşleşen Bölge', resim1)
cv2.waitKey(0)  
cv2.destroyAllWindows()
cv2.imwrite('eslesen_bolge.jpg', resim1)
