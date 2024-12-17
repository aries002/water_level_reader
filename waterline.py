import cv2
import imutils
import numpy as np
from time import sleep

class water_line:
    def __init__(self, camera, x1 = 0, y1 = 0, x2 = 0, y2 = 0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.kamera = camera
        self.fps = 10
        self.time_delay = 1./self.fps
        self.debug = False
        self.run = True
        self.pause = False
        self.video = True
        # Fine tune sensor
        self.edge_treshold = 30
        self.erode_iteration = 15
        self.dilatte_iteration = 15
        self.Gaussian_ksize = (11, 11)
        self.Gaussian_sigmax = 0
        self.result = 0
        pass
    
    def sensor_loop(self):
        
        while self.run:
            try:
                cam = cv2.VideoCapture(self.kamera)
            except cv2.error as e:
                print("Camera error!")
                print(e)
            tmp_res = []
            time = 0.0
            while cam.isOpened() and not self.pause:
                try:

                    ret,image = cam.read()
                    self.image_read(image)
                    # hitung rata rata dalam 1 detik
                    if self.nilai > 0:
                        tmp_res.append(self.nilai)
                    # jika sudah satu detik maka hitung rata-rata
                    if time >= 1 and len(tmp_res) > 0:
                        # rata rata
                        self.result = int(sum(tmp_res)/max(len(tmp_res),1))
                        # reset
                        time = 0.0
                        tmp_res = []
                    time = time + self.time_delay
                    sleep(self.time_delay)
                except:
                    print("Read image error")
            if self.debug:
                break
            sleep(10)
                
    def image_read(self,img):
        image = img
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2
        image_proses = image[y1:y2, x1:x2]
        hasil = self.find_lines(image_proses)
        nilai = 0;
        garis_tertinggi = 0
        new_contur = []
        if(len(hasil)>0):
            n = 0
            # cari yang tertinggi
            for garis in hasil :
                if(garis['nilai'] > nilai):
                    # nilai = garis['nilai']
                    garis_tertinggi = n
                n=n+1
            nilai = hasil[garis_tertinggi]['nilai']
            contur = hasil[garis_tertinggi]['kontur']
            # sesuaikan contur sesuai koordinat kotak
            # if self.debug:
        self.nilai = nilai
        if self.debug:
            dot = 0
            if(len(hasil)>0):
                new_contur = contur
                for co in contur:
                    co[0][0] = x1 + co[0][0]
                    co[0][1] = y1 + co[0][1]
                    new_contur[dot] = co
                    dot = dot+1
            print("Nilai = ",nilai)
            image = cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (255,0,0))
            image = cv2.circle(image,(int(x1), int(y1)),5,(0,0,255))
            image = cv2.putText(image, '1', (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            image = cv2.circle(image,(int(x2), int(y2)),5,(0,0,255))
            image = cv2.putText(image, '2', (int(x2), int(y2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            if(len(new_contur)>0):
                cv2.drawContours(image, new_contur, -1, (0,255,0), 5)
            cv2.imshow("img", image)
            if cv2.waitKey(1) == ord('q'):
                self.run = False
    
    def find_lines(self,img):
        frame = img
        # rubah warna dari gambar
        out = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # blur gambar untuk mengurangi detail
        out = cv2.GaussianBlur(out, self.Gaussian_ksize, self.Gaussian_sigmax)
        out = cv2.erode(out, None, iterations=self.erode_iteration)
        out = cv2.dilate(out, None, iterations=self.dilatte_iteration)

        # cari tepian dari gambar
        edged = cv2.Canny(out, self.edge_treshold, (self.edge_treshold*3)) 
        # cv2.waitKey(0) 

        # cari countur dari tepian yang sudah didapat
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if self.debug:
            cv2.drawContours(out, contours, -1, (0, 255, 0), 1)
            # getLargestRedContour(out,contours)
            cv2.imshow('edge', edged)
            cv2.imshow("Process", out)
        # cari kontur yang melewati satu garis
        # ambil lebar gambar
        width  = frame.shape[1]
        # cari titik paling kanan dan titik paling kiri dari setiap kontur
        count = 0
        garis = []
        contours_ = list(contours)
        for ctr in contours_:
            
            titik_kanan = ctr[0][0] # titik paling kanan
            titik_kiri =ctr[0][0]   # titik paling kiri
            # cari titik kiri dan kanan
            dot_num = 0;
            for dot in ctr:
                x = int(dot[0][0])
                y = int(dot[0][1])

                dot_num = dot_num +1
                xkiri=int(titik_kiri[0])
                xkanan = int(titik_kanan[0])
                # jika x lebih dari kecil maka ada di sebelah kiri
                if (x <= xkiri):
                    # print("a")
                    titik_kiri = dot[0]
                # juka x lebih besar maka ada disebelah kanan
                if (x >= xkanan):
                    titik_kanan = dot[0]
            # cari kontur dengan posisi x kiri mendekati 0 dan posisi x kanan mendekati maks lebar
            if(titik_kiri[0] == 0 and titik_kanan[0] == (width - 1)):
                # hitung nilai tengah ketinggian
                tinggi = (titik_kanan[1] + titik_kiri[1])/2
                tinggi = float(tinggi)
                # Data yang final dikembalikan
                data = {
                    'id_kontur' : count,
                    'nilai' : tinggi,
                    'kontur' : contours[count]
                }
                garis.append(data)
            count = count + 1
        return garis