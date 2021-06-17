# Birhan Berk Oktay - 170401075

# Bu Python kodu birdenAltinciDereceyeKadar isimli fonksiyonun �a��r�lmas�yla
# parametre olarak verilen dosyadaki verilerin tamam�n� ve her 10 lu veri grubu
# i�in 1,2,3,4,5 ve 6. dereceden polinoma yak�nla�t�rarak bu polinomlar�n katsay�
# de�erlerini, hata de�erlerini ve en uygun polinomlar� sonuc.txt dosyas�na yazar.


def matristenDiziye(m):
  # Matrisi diziye �eviren fonksiyon
  # matris[[a],[b]] --> dizi[a,b]
  dizi = []
  for i in m:
    dizi.append(i[0])
  return dizi

def matrisCarpimi(m1, m2):
  # �ki matrisi �arp�p sonu� matrisini d�nd�ren fonksiyon
  r, m = [], []
  for i in range(len(m1)):
    for j in range(len(m2[0])):
      toplam = 0
      for k in range(len(m2)):
        toplam += (m1[i][k] * m2[k][j])
      r.append(toplam)
    m.append(r)
    r = []
  return m

def denklemSistemiCoz(m1,m2):
  # Denklem sistemi sonucunu dizi d�nd�ren fonksiyon
  n = len(m1)
  idizi = list(range(n))
  for i in range(n):
    a = 1.0 / m1[i][i]
    for j in range(n):
      m1[i][j] *= a
    m2[i][0] *= a
    for j in idizi[0:i] + idizi[i+1:]:
      b = m1[j][i]
      for k in range(n):
        m1[j][k] = m1[j][k] - b * m1[i][k]
      m2[j][0] = m2[j][0] - b * m2[i][0]
  return matristenDiziye(m2)

def nDerecedenPolinomaYakinlastir(m, veri):
  # Veri k�mesindeki verileri n. dereceden polinoma yak�nla�t�r�p
  # a0,a1,a2,..,an katsay�lar�n� ve hata de�erlerini d�nd�ren fonksiyon

  # xi ussu toplam ve xi ussu yi toplam� hesapla
  # xiussuToplam -> [toplam(xi), toplam(xi^2), ..., toplam(xi^2m)]
  # xiussuyiToplam -> [toplam(xi^0*yi), toplam(xi^1*yi), ..., toplam(xi^m*yi)]
  n = len(veri)
  xiussuToplam = [0] * m * 2
  xiussuyiToplam = []
  for i in range(n):
    for j in range(2 * m):
      xiussuToplam[j] += (i + 1) ** (j + 1)
    for k in range(m + 1):
      if(len(xiussuyiToplam) < m + 1):
        xiussuyiToplam.append([0])
      xiussuyiToplam[k][0] += (i + 1) ** k * veri[i]
      
  # denklem sistemini olu�tur
  # n + toplam(xi) + toplam(xi^2) + ... + toplam(xi^m)
  # toplam(xi) + toplam(xi^2) + ... + toplam(xi^m+1) �eklinde
  a = [[]]
  altSinir = 0
  ustSinir = m + 1
  for i in range(m + 1):
    if(i == 0):
      a[0].append(n)
      for j in range(0, m):
        a[0].append(xiussuToplam[j])
    else:
      a.append([])
      for k in range(altSinir, ustSinir):
        a[i].append(xiussuToplam[k])
      altSinir += 1
      ustSinir += 1
  katsayilar = denklemSistemiCoz(a, xiussuyiToplam)

  # x ortalama ve y ortalama hesapla
  xtoplam = 0
  ytoplam = 0
  for i in range(n):
    xtoplam += i + 1
    ytoplam += veri[i]
  xortalama = xtoplam / n
  yortalama = ytoplam / n

  # hata hesapla
  # sr -> Hatalar�n karelerinin toplam�
  # r -> Korelasyon katsay�s� -> r^2
  # syx -> Standart tahmini hata
  korelasyon = []
  toplamHata = []
  stahminiHata = []
  st = 0
  sr = 0
  for i in range(n):
    b = 0
    for j in range(len(katsayilar)):
      b += katsayilar[j] * (i + 1) ** (j)
    sr += (veri[i] - b) ** 2
    st += (veri[i] - yortalama) ** 2
  r = ((st - sr) / st)
  syx = (sr / (n - (m + 1))) ** (1 / 2) # Veri say�s� m + 1 e e�it olursa 0 a b�lme hatas� ��kar
  toplamHata.append(sr)
  korelasyon.append(r)
  stahminiHata.append(syx)

  """
  # Ger�ek veriler ile tahmin edilen verileri listele
  for i in range(n):
    tahmin = 0
    for j in range(0, len(katsayilar)):
      tahmin += katsayilar[j] * (i + 1) ** (j)
    print(veri[i], tahmin, tahmin-veri[i])
  print("\n")
  """

  return katsayilar, korelasyon, toplamHata, stahminiHata

def birdenAltinciDereceyeKadar(dosya):
  veri = []
  try:
    f = open(dosya, "r")
    for i in f.read().split():
      veri.append(float(i))
    # 8 den az veri olmas� standart tahmin hata hesaplamas�n� (sr/n-(m+1)) 0 a b�lme hatas�na g�t�r�yor.
    if(len(veri) < 10):
      print("L�tfen en az 8 adet veri giriniz")
  except IOError:
    print("Veriler bulunam�yor. Verilerin bulundu�u .txt doyas�n� kontrol edin.")
  finally:
    f.close()

  # T�m veri
  r = [] # Korelasyon de�erleri
  h = [] # Hata de�erleri
  s = [] # Standart hata de�erleri
  f = open("sonuc.txt", "w+")
  f.write("T�m veri i�in\n")
  f.write("-------------\n\n")
  for i in range(1, 7):
    if(i != 1):
      f.write("\n")
    tumSonuc = nDerecedenPolinomaYakinlastir(i, veri)
    f.write(str(i) + ". derece ->\n")
    for j in range(len(tumSonuc[0])):
      f.write("a"+ str(j) +  " = " + str(tumSonuc[0][j]) + "\n")
    r.append(tumSonuc[1][0]**(1/2))
    h.append(tumSonuc[2][0])
    s.append(tumSonuc[3][0])
    f.write("R kare (r^2)= " + str(tumSonuc[1][0]) + "\n")
    f.write("Korelasyon de�eri (r)= " + str(tumSonuc[1][0]**(1/2)) + "\n")
    f.write("Hatalar�n karelerinin toplam� (Sr)= " + str(tumSonuc[2][0]) + "\n")
    f.write("Standart tahmini hata de�eri (Sy/x)= " + str(tumSonuc[3][0]) + "\n")
  f.write("\n\nT�m veri i�in en y�ksek korelasyon katsay�s�na sahip derece = " + str(r.index(max(r)) + 1) + "\n")
  f.write("T�m veri i�in en d���k hatalar�n karelerinin toplam�na sahip derece = " + str(h.index(min(h)) + 1) + "\n")
  f.write("T�m veri i�in en d���k standart tahmin hata de�erine sahip derece = " + str(s.index(min(s)) + 1))
  f.write("\n")
  #------------------------

  # Her 10lu grup
  if(len(veri) > 10):
    sinir = len(veri) - 9
    for i in range(sinir):
      r = [] # Korelasyon de�erleri
      h = [] # Hata de�erleri
      s = [] # Standart hata de�erleri
      f.write("\n" + str(i + 1) + "-" + str(i + 10) + " sat�rlar\n")
      f.write("-------------\n")
      for j in range(1, 7):
        onluSonuc = nDerecedenPolinomaYakinlastir(j, veri[i:i + 10])
        f.write("\n" + str(j) + ". derece ->\n")
        for k in range(len(onluSonuc[0])):
          f.write("a"+ str(k) +  " = " + str(onluSonuc[0][k]) + "\n")
        r.append(onluSonuc[1])
        h.append(onluSonuc[2])
        s.append(onluSonuc[3])
        f.write("R kare (r^2)= " + str(onluSonuc[1][0]) + "\n")
        f.write("Korelasyon de�eri (r)= " + str(onluSonuc[1][0]**(1/2)) + "\n")
        f.write("Hatalar�n karelerinin toplam� (Sr)= " + str(onluSonuc[2][0]) + "\n")
        f.write("Standart tahmini hata de�eri (Sy/x)= " + str(onluSonuc[3][0]) + "\n")
      f.write("\n\n" + str(i + 1) + "-" + str(i + 10) + " sat�rlar i�in en y�ksek korelasyon katsay�s�na sahip derece = " + str(r.index(max(r)) + 1) + "\n")
      f.write(str(i + 1) + "-" + str(i + 10) + " sat�rlar i�in en d���k hatalar�n karelerinin toplam�na sahip derece = " + str(h.index(min(h)) + 1) + "\n")
      f.write(str(i + 1) + "-" + str(i + 10) + " sat�rlar i�in en d���k standart tahmin hata de�erine sahip derece = " + str(s.index(min(s)) + 1) + "\n\n")
  f.close()

birdenAltinciDereceyeKadar("veriler.txt")