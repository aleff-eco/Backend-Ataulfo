from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path
import tensorflow as tf
import numpy as np
import cv2

from mangos.serializers import mangosSerializer

BASE_DIR = Path(__file__).resolve().parent.parent
path = str(BASE_DIR)
path = path.replace('\\', '/')

model = tf.keras.models.load_model(path+"/modelo.h5")
ESTADOS = ["Verde", "Maduro", "Descomposicion", "Semi maduro", "Temprana descomposicion"]

# Create your views here.
class mangosClasificacionView(APIView):
    def get_resultado(self, data):
        imagenes = []
        imagen = data.get('imagen', None)
        try:
            frame = cv2.imread(path+imagen)
            frame = cv2.resize(frame, (64, 64), interpolation=cv2.INTER_AREA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = np.expand_dims(frame, axis=-1)
            imagenes.append(frame)
        except:
            print("Error leyendo la imagen")
            print(imagen)

        imagen_data = np.array(imagenes)
        imagen_data = tf.cast(imagen_data, tf.float32)
        imagen_data /= 255

        resultado = model.predict(imagen_data) 
        res = np.argmax(resultado)
        
        print(ESTADOS[res])
        return ESTADOS[res]


    def post(self, request):
        serializer = mangosSerializer(data=request.data)
        if serializer.is_valid():        
            serializer.save()
            res = self.get_resultado(serializer.data)
            
            return Response(res, status=status.HTTP_200_OK)
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)