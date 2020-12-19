import face_recognition
import numpy as np


def face_compare(unknown_face, queryset):
    face_encodings = []
    for face in queryset:
        face_encoding = [np.float(i) for i in face.encoding.split()]
        face_encodings.append(face_encoding)
    result = face_recognition.face_distance(face_encodings, unknown_face)
    min_result = result.min()
    print(f'min result: {min_result}')
    if min_result <= 0.6:
        return queryset[result.tolist().index(min_result)]
    return False


def face_compare2(unknown_face, queryset):
    for face in queryset:
        face_encoding = [np.float(i) for i in face.encoding.split()]
        results = face_recognition.compare_faces(np.array([face_encoding]),
                                                 unknown_face)
        if results[0]:
            return face
    return False


def get_face_encoding(image):
    face = face_recognition.load_image_file(image)
    face_encoding = face_recognition.face_encodings(face)
    if face_encoding:
        return face_encoding[0]


def get_face_encoding_string(image):
    face_encoding = get_face_encoding(image)
    face_encoding = [str(i) for i in face_encoding]
    face_encoding = ' '.join(face_encoding)
    return face_encoding
