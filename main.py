import cv2
import time


longueur = 25
interval = 0.1
pix_depart = 0
t_depart = time.time()


def motionDetector(cam, blur, thresh0, thresh1, area, T):
    cv2.namedWindow('Frames')
    cv2.namedWindow('Thresh')
    cv2.namedWindow('Security Feed')

    prevFrame = None
    cap = cv2.VideoCapture(cam)
    loop = True
    while loop:
        rval, frame = cap.read()
        if rval:
            gray = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY), (blur, blur), 0)
            if prevFrame is None:
                prevFrame = gray
            else:
                # Ecart entre les frames
                delta = cv2.absdiff(prevFrame, gray)
                # Seuil
                thresh = cv2.threshold(delta, thresh0, thresh1, cv2.THRESH_BINARY)[1]
                # Dilatation des zones
                thresh = cv2.dilate(thresh, None, iterations=2)
                # Contours des zones
                contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                # Affichage des contours
                for c in contours:
                    if cv2.contourArea(c) > area:
                        # Un rectangle incluant la zone
                        (x, y, w, h) = cv2.boundingRect(c)
                        # print((w-x)/2)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                        a = w * longueur / 1080

                        cv2.imshow("Frames", delta)
                        cv2.imshow("Thresh", thresh)
                        cv2.imshow("Security Feed", frame)
                        # Echap pour quitter dans une fenêtre
                        if cv2.waitKey(T) & 0xFF == 27:
                            loop = False
                        t_2 = time.time()
                        global t_depart
                        global pix_depart
                        if t_2 - t_depart > interval:
                            t_depart = time.time()
                        v = (a - pix_depart) / interval
                        print('v = ', v, 'cm/s')
                        pix_depart = a


if __name__ == '__main__':
    cv2.destroyAllWindows()
    # Numero de webcam
    CAM = 0
    # Valeur de flou, impair
    FLOU = 11
    # Seuils sur le gris
    SEUIL_0, SEUIL_1 = 40, 150
    # Aire minimal avec différence de pixels
    AREA = 5000
    # Attente en ms entre 2 capture
    TEMPO = 30
    motionDetector(CAM, FLOU, SEUIL_0, SEUIL_1, AREA, TEMPO)
