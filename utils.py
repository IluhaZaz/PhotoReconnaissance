from math import sqrt, exp, tan, pi, atan

from PIL import Image
from PIL.ExifTags import TAGS


def count_P(Rвпис, Rопис, S, G, L, Lоб, Lф, lm, R, N, w, f, kпр):
    Lоб = 0.2126*Lоб[0] + 0.7152*Lоб[1] + 0.0722*Lоб[2]
    Lф = 0.2126*Lф[0] + 0.7152*Lф[1] + 0.0722*Lф[2]

    O = 2*atan(w/(2*f))

    K = abs(Lоб-Lф)/(Lф + Lоб)
    B = sqrt(G*(Rвпис + Rопис)/(2*S))

    lпикс = 360*N*tan(lm/(2*R))/(kпр*pi*O)

    try:
        Pобн = exp(-(B*L/(4*lпикс*sqrt(K)))**2)
        Pрасп = exp(-(B*L/(lпикс*sqrt(K)))**2)
    except ZeroDivisionError:
        Pобн, Pрасп = -1, -1

    return Pобн, Pрасп


def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = {}
    
    if hasattr(image, '_getexif'):
        exif_info = image._getexif()
        if exif_info is not None:
            for tag, value in exif_info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
    
    return exif_data
