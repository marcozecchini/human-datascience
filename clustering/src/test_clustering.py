import os
from shutil import copyfile
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from tqdm import tqdm
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from src.img_to_vec import Img2Vec


def make_clustering(input_path, k_value, do_pca=True):
    auxx = input_path.split("/")[3]
    if do_pca:
        output_path = "./data/output/" + str(auxx) + "/pca/"
    else:
        output_path = "./data/output/" + str(auxx) + "/no_pca/"
    os.makedirs(output_path, exist_ok=True)

    files = os.listdir(input_path)
    # Eliminiamo i file nascosti
    files = [i for i in files if not i.startswith("._")]
    files = [i for i in files if "DS_Store" not in i]

    img2vec = Img2Vec()
    vec_length = 512  # Using resnet-18 as default

    samples = len(files)  # Amount of samples to take from input path

    # Matrix to hold the image vectors
    vec_mat = np.zeros((samples, vec_length))
    # If samples is < the number of files in the folder, we sample them randomly
    sample_indices = np.random.choice(range(0, len(files)), size=samples, replace=False)

    print('Reading images...')
    conta_errore = []
    for index, i in tqdm(enumerate(sample_indices)):
        file = files[i]
        filename = os.fsdecode(file)
        img = Image.open(os.path.join(input_path, filename))
        try:
            vec = img2vec.get_vec(img)
        # Non consideriamo i casi di immagini in bianco e nero (59)
        except:
            conta_errore.append(file)
        vec_mat[index, :] = vec
    print("Numero di immagini non considerate: {}".format(len(conta_errore)))

    if do_pca:
        print('Applying PCA...')
        reduced_data = PCA(n_components=2).fit_transform(vec_mat)

    if type(k_value) == list:
        wcss = []
        for kk in k_value:
            kmeans = KMeans(init='k-means++', n_clusters=kk, n_init=10)
            if do_pca:
                kmeans.fit(reduced_data)
            else:
                kmeans.fit(vec_mat)
            wcss.append(kmeans.inertia_)
        plt.plot(k_value, wcss)
        plt.title('The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()
        return None

    else:
        kmeans = KMeans(init='k-means++', n_clusters=k_value, n_init=10)
        if do_pca:
            print('Applying PCA...')
            kmeans.fit(reduced_data)
        else:
            kmeans.fit(vec_mat)

        # Create a folder for each cluster (0, 1, 2, ..)
        for i in set(kmeans.labels_):
            try:
                os.mkdir(output_path + str(i))
            except FileExistsError:
                continue

        print('Predicting...')
        if do_pca:
            preds = kmeans.predict(reduced_data)
        else:
            preds = kmeans.predict(vec_mat)

        print('Copying images...')
        for index, i in enumerate(sample_indices):
            file = files[i]
            filename = os.fsdecode(file)
            copyfile(input_path + '/' + filename, output_path + str(preds[index]) + '/' + filename)
        print('Done!')


if __name__ == '__main__':
    path_calchi_arrivo = "./data/interim/calchi/"
    path_volti_arrivo = "./data/interim/volti/"
    path_all_arrivo = "./data/interim/all/"

    # Analizziamo il dataset dei volti
    make_clustering(input_path=path_volti_arrivo, k_value=list(range(2, 11)), do_pca=True) # 4
    make_clustering(input_path=path_volti_arrivo, k_value=list(range(2, 11)), do_pca=False) # 7

    make_clustering(input_path=path_volti_arrivo, k_value=4, do_pca=True)
    make_clustering(input_path=path_volti_arrivo, k_value=7, do_pca=False)

    # Analizziamo il dataset dei calchi
    make_clustering(input_path=path_calchi_arrivo, k_value=list(range(2, 11)), do_pca=True) # 4
    make_clustering(input_path=path_calchi_arrivo, k_value=list(range(2, 11)), do_pca=False) # 4

    make_clustering(input_path=path_calchi_arrivo, k_value=4, do_pca=True)
    make_clustering(input_path=path_calchi_arrivo, k_value=4, do_pca=False)

    # Analizziamo il dataset all
    make_clustering(input_path=path_all_arrivo, k_value=list(range(2, 11)), do_pca=True) # 5
    make_clustering(input_path=path_all_arrivo, k_value=list(range(2, 11)), do_pca=False) # 9

    make_clustering(input_path=path_all_arrivo, k_value=5, do_pca=True)
    make_clustering(input_path=path_all_arrivo, k_value=9, do_pca=False)
