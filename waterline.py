import cv2
import imutils
import numpy as np

def getLargestRedContour(img, contours):

    sortedContours = sorted(contours, key=cv2.contourArea, reverse=True)

    for cnt in sortedContours:
        area = cv2.contourArea(cnt)
        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)
            cv2.circle(img, (cx, cy), 3, (0, 0, 0), -1)
            cv2.putText(img, "center", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            cx = (cx + 1) - 320
            cy = -cy + 240
            print("x: {} y: {}".format(cx, cy))

            return cx, cy

    return 0, 0


def water_line(img):
    result = 0
    frame = img
    # Convert the img to grayscale
    out = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # out = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    out = cv2.GaussianBlur(out, (11, 11), 0)
    out = cv2.erode(out, None, iterations=15)
    out = cv2.dilate(out, None, iterations=15)

    # draw countour
    # cari tepian dari gambar
    treshold = 30
    edged = cv2.Canny(out, treshold, (treshold*3)) 
    
    cv2.waitKey(0) 

    # cari countur dari tepian yang sudah didapat
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)
    cv2.drawContours(out, contours, -1, (0, 255, 0), 1)
    # getLargestRedContour(out,contours)
    cv2.imshow('edge', edged)
    cv2.imshow("Process", out)
    # cari kontur yang melewati satu garis
    
    width  = frame.shape[1]
    
    # height = float(frame.shape(1))
    # print(frame.shape)
    count = 0
    garis = []
    contours_ = list(contours)
    for ctr in contours_:
        print("Kontur ke ",count)
        titik_kanan = ctr[0][0]
        titik_kiri =ctr[0][0]
        # cari titik kiri dan kanan
        dot_num = 0;
        for dot in ctr:
            x = int(dot[0][0])
            y = int(dot[0][1])
            print("Titik ",dot_num)
            print("x = ",x)
            print("y = ",y)
            # print(dot)
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
            data = {
                'id_kontur' : count,
                'nilai' : tinggi,
                'kontur' : contours[count]
            }
            garis.append(data)
        print("Titik Kiri = ", titik_kiri)
        # n = titik_kiri[0]
        # int_x = n
        # print(xkiri)
        # # print(type(n))
        # print(type(xkiri))
        print("Titik Kanan = ", titik_kanan)
        count = count + 1
    # print("Kontur garis = ",garis)
    print("Lebar = ",width)
    print("Tingi = ",frame.shape[0])
    print("--------------------------------------")
        
    return garis
# dari 155 menjadi 18?? padahal yang terpilih paling tinggi



