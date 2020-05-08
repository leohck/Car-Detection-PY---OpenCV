import cv2
import time
import numpy as np
from datetime import datetime

def main(args):
    car_classificador = cv2.CascadeClassifier('cascades/haarcascade_car.xml')
    camera = cv2.VideoCapture('imagens/video.mp4')
    camera_port = 0
    nFrames = 30
    file = "imagens/imagenTeste.png"
    emLoop = True

    print
    "Digite <ESC> para sair / <s> para Salvar"

    while (emLoop):

        retval, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        carros = car_classificador.detectMultiScale(gray, 1.4, 2)

        for (x, y, w, h) in carros:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('Detector de carros', frame)

        k = cv2.waitKey(100)
        if k == 27:
            emLoop = False

        elif k == ord('s'):
            now = datetime.now()
            font = cv2.FONT_HERSHEY_SIMPLEX
            #print(now)
            #frame = cv2.putText(frame, now, (10, 500), font, 4, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imwrite(file, frame)
            emLoop = True

          if print == 's':
            cv2.imshow('fototirada', frame)

    cv2.destroyAllWindows()
    camera.release()
    return 0

if __name__ == '__main__':
    import sys

sys.exit(main(sys.argv))
