import cv2
import numpy as np
import scipy
import scipy.spatial
from imageio import imread
import pickle
import random
import os
import matplotlib.pyplot as plt

# Feature extractor
def extract_features(image_path, vector_size=32):
    image = imread(image_path, pilmode="RGB")
    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        alg = cv2.KAZE_create()
        # Dinding image keypoints
        kps = alg.detect(image)
        # Getting first 32 of them. 
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
        kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        # computing descriptors vector
        kps, dsc = alg.compute(image, kps)
        # Flatten all of them in one big vector - our feature vector
        dsc = dsc.flatten()
        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if dsc.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
    except cv2.error as e:
        print('Error: ', e)
        return None

    return dsc

def batch_extractor_uji(images_path, pickled_db_path="features_uji.pck"):
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]

    result = {}
    for f in files:
        print('Extracting features from image %s' % f)
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f)
    
    # saving all our feature vectors in pickled file
    with open(pickled_db_path, 'wb') as fp:
        pickle.dump(result, fp)

def batch_extractor_referensi(images_path, pickled_db_path="features_referensi.pck"):
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]

    result = {}
    for f in files:
        print('Extracting features from image %s' % f)
        name = f.split('/')[-1].lower()
        result[name] = extract_features(f)
    
    # saving all our feature vectors in pickled file
    with open(pickled_db_path, 'wb') as fp:
        pickle.dump(result, fp)

class Matcher(object):

    def __init__(self, pickled_db_path="features_referensi.pck"):
        with open(pickled_db_path, 'rb') as fp:
            self.data = pickle.load(fp)
        self.names = []
        self.matrix = []
        for k, v in self.data.items():
            self.names.append(k)
            self.matrix.append(v)
        self.matrix = np.array(self.matrix) # Image database
        self.names = np.array(self.names)

    def cos_cdist(self, vector):
        # getting cosine distance between search image and images database
        v = vector.reshape(1, -1)
        return scipy.spatial.distance.cdist(self.matrix, v, 'cosine').reshape(-1)

    def euclidianDistance(self, vector):
        # getting euclidean distance between search image and images database
        v = vector.reshape(1,-1) # Search Image

        distance = np.empty([len(v), len(self.matrix)])

        for i in range(0,len(v)):
            for j in range(0, len(self.matrix)):
                distance[i][j] = 0
                for k in range(0, 2048):
                    distance[i][j] += (v[i][k] - self.matrix[j][k])**2
                distance[i][j] = np.sqrt(distance[i][j])

        return distance.reshape(-1)

    def cosineSimilarity(self, vector):
        v = vector.reshape(1,-1) # Search Image

        distance = np.empty([len(v), len(self.matrix)])
        for i in range(0,len(v)):
            for j in range(0, len(self.matrix)):
                distance[i][j] = (np.dot(v[i], self.matrix[j]) / (np.linalg.norm(v[i]) * np.linalg.norm(self.matrix[j])))
                

        return distance.reshape(-1)

        
            

    
    def match(self, image_path, topn, method):
        features = extract_features(image_path)
        if (method == '1'):
            img_distances = self.euclidianDistance(features)
            
            nearest_ids = np.argsort(img_distances)[:topn].tolist()
            nearest_img_paths = self.names[nearest_ids].tolist()
        elif (method == '2'):
            img_distances = self.cosineSimilarity(features)
            
            nearest_ids = np.argsort(img_distances)[::-1][:topn].tolist()
            nearest_img_paths = self.names[nearest_ids].tolist()
        else :
            print("Salah input")


        return nearest_img_paths, img_distances[nearest_ids].tolist()

def show_img(path):
    img = imread(path, pilmode="RGB")
    plt.imshow(img)
    plt.show()
    
def run():
    # ini data dari data uji
    images_path = 'pins-face-recognition/Data Uji/'
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    
    for i in range(len(files)):
        num = 1+i
        print (num, ".", files[i])

    x = input("pilih nomer berapa : ")
    sample = files[int(x)-1] 
    # misalnya : pins-face-recognition/Data Uji/Jesse Eisenberg0.jpg

    # kalo misalnya blm ada file .pck untuk data uji
    extracted = os.path.isfile('./features_uji.pck')
    if not(extracted):
        batch_extractor_uji(images_path)

    # ini data dari referensi
    images_path = 'pins-face-recognition/Data Referensi/'

    # kalo misalnya blm ada file .pck untuk data referensi
    extracted = os.path.isfile('./features_referensi.pck')
    if not(extracted):
        batch_extractor_referensi(images_path)

    ma = Matcher('features_referensi.pck')

    user_input = input("1. Euclidean\n2. Cosine\n")
    
    
    print('Query image ==========================================')
    show_img(sample)
    y = input("Mau ditampilin berapa yang mirip : ")
    names, match = ma.match(sample, int(y), user_input)
    print('Result images ========================================')
    for i in range(int(y)):
        # we got cosine distance, less cosine distance between vectors
        # more they similar, thus we subtruct it from 1 to get match value
        print('Match %s' % (match[i]))
        show_img(os.path.join(images_path, names[i]))

run()