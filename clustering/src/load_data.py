import os
from shutil import copyfile
from tqdm import tqdm

path_iniziale_volti = "./data/raw/dataset_volti/"
path_volti_arrivo = "./data/interim/volti/"
path_all_arrivo = "./data/interim/all/"

lista_img_volti = set()
for root, dirs, files in tqdm(os.walk(path_iniziale_volti)):
    for file in files:
        if file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".png") or file.endswith(".PNG"):
            filename = os.fsdecode(file)
            if filename.startswith("._"):
                continue
            copyfile(root + '/' + filename, path_volti_arrivo + '/' + filename)
            copyfile(root + '/' + filename, path_all_arrivo + '/' + filename)
            lista_img_volti.add(file)


path_iniziale_calchi = "./data/raw/FOTO CALCHI PER SALA/"
path_calchi_arrivo = "./data/interim/calchi/"

for root, dirs, files in tqdm(os.walk(path_iniziale_calchi)):
    for file in files:
        if file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".png") or file.endswith(".PNG"):
            if file not in lista_img_volti:
                filename = os.fsdecode(file)
                if filename.startswith("._"):
                    continue
                copyfile(root + '/' + filename, path_calchi_arrivo + '/' + filename)
                copyfile(root + '/' + filename, path_all_arrivo + '/' + filename)
