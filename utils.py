from math import sqrt, exp, tan, pi

from PIL import Image
from PIL.ExifTags import TAGS


def count_P(Rвпис, Rопис, S, G, L, Lоб, Lф, lm, R, N, O, kпр):
    O = 62*pi/180

    K = abs(Lоб-Lф)/Lф
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
