import cv2
import time
import numpy as np
from datetime import datetime

DATE_FORMAT = "%d/%m/%Y"
TIME_FORMAT = "%H:%M:%S"
SHORT_DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"


def pegar_data_hora_atual():
    atual = datetime.now()
    data = atual.date().strftime(DATE_FORMAT)
    hora = atual.time().strftime(TIME_FORMAT)
    data_hora = atual.strftime(SHORT_DATETIME_FORMAT)
    return data, hora, data_hora


def tirar_foto(frame, dimensoes, file_name):
    (x, y, w, h) = dimensoes[0], dimensoes[1], dimensoes[2], dimensoes[3]
    file = f"imagens/{file_name}.png"
    imagem = frame[y:y+h, x:x+w]
    cv2.namedWindow("foto", cv2.WINDOW_AUTOSIZE)
    cv2.imshow('foto', imagem)
    key = cv2.waitKey(0) & 0xFF
    if key == ord('e'):
        cv2.destroyWindow("foto")
    elif key == ord('s'):
        cv2.imwrite(file, imagem)
        cv2.destroyWindow("foto")
        print(f'foto salva -> {file_name}')


def main():
    car_classificador = cv2.CascadeClassifier('cascades/cars2.xml')
    camera = cv2.VideoCapture('videos/rodovia.mp4')
    reproduzir = False
    detectar_carros = False
    while True:
        retval, frame = camera.read()
        frame = cv2.resize(frame, None, fx=.5, fy=.5)

        width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame = cv2.rectangle(frame, (0, 0), (int(width), int(height/15)), (255, 255, 255), -1)
        comandos = "s - iniciar | p - pausar | e - encerrar"
        comandos2 = "d-detectar/pausar | f-foto (e-cancelar|s-salvar)"
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        cv2.putText(frame, comandos, (10, int(height/40)), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, comandos2, (10, int(height/18)), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if not reproduzir:
            key = cv2.waitKey(0) & 0xFF
            if key == ord('s'):
                print('tecla s -> reprodução do video iniciada')
                reproduzir = True
            elif key == ord('e'):
                print('tecla e -> reprodução do video encerrada')
                break
        else:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('p'):
                print('tecla p -> reprodução do video pausada')
                reproduzir = False

            if key == ord('d'):
                if detectar_carros:
                    print('tecla d -> detecção de veiculos encerrada')
                    detectar_carros = False
                else:
                    print('tecla d -> detecção de veiculos iniciada')
                    detectar_carros = True

            if key == ord('e'):
                print('tecla e -> reprodução do video encerrada')
                break

            if detectar_carros:
                carros = car_classificador.detectMultiScale(gray, 1.4, 2)
                for carro in carros:
                    if carro.all():
                        (x, y, w, h) = carro[0], carro[1], carro[2], carro[3]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
                        horario = pegar_data_hora_atual()
                        cv2.putText(frame, horario[2], (int(x/2), y), font, 1, (255, 255, 0), 1, cv2.LINE_AA)
                        key = cv2.waitKey(1)
                        if key == ord('f'):
                            tirar_foto(frame, carro, x)

        cv2.imshow('Detector de carros', frame)

    camera.release()
    cv2.destroyAllWindows()


main()
# print(pegar_data_hora_atual())
