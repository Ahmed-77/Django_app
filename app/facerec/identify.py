import cv2
import numpy as np
import mtcnn
from . import architecture
from .architecture import InceptionResNetV2
from .train_model import normalize,l2_normalizer
from scipy.spatial.distance import cosine
from tensorflow.keras.models import load_model
import pickle


confidence_t=0.99
recognition_t=0.5
required_size = (160,160)

def get_face(img, box):
    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)

def get_encode(face_encoder, face, size):
    face = normalize(face)
    face = cv2.resize(face, size)
    encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
    return encode


def load_pickle(path):
    with open(path, 'rb') as f:
        encoding_dict = pickle.load(f)
    return encoding_dict

def detect(img ,detector,encoder,encoding_dict):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(img_rgb)
    for res in results:
        if res['confidence'] < confidence_t:
            continue
        face, pt_1, pt_2 = get_face(img_rgb, res['box'])
        encode = get_encode(encoder, face, required_size)
        encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
        name = 'unknown'

        distance = float("inf")
        for db_name, db_encode in encoding_dict.items():
            dist = cosine(db_encode, encode)
            if dist < recognition_t and dist < distance:
                name = db_name
                distance = dist
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255 ,255,255)
        if name == 'unknown':
            cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
            cv2.putText(img, name, pt_1, font, 1, (0, 0, 255), 1)
        else:
            conf=f'  {(100-(distance*100))}'
            name1 =name + conf
            cv2.rectangle(img, pt_1, pt_2, color, 2)
            cv2.putText(img, name1, (pt_1[0], pt_1[1] - 5), font, 1,
                        color, 2)
    return img



def identify2():
    required_shape = (160,160)
    face_encoder = InceptionResNetV2()
    path_m = "app/facerec/facenet_keras_weights.h5"
    face_encoder.load_weights(path_m)
    encodings_path = 'app/facerec/encodings/encodings.pkl'
    face_detector = mtcnn.MTCNN()
    encoding_dict = load_pickle(encodings_path)

    cap = cv2.VideoCapture(0)

    while (True):
        ret,frame = cap.read()

        if not ret:
            print("Camera cannot be opened")
            break

        frame= detect(frame , face_detector , face_encoder , encoding_dict)

        cv2.imshow('Identification System', frame)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
