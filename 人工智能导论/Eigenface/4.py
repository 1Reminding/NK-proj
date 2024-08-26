# 在生成 main 文件时, 请勾选该模块

# 导入必要的包
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
import os
import numpy as np
from sklearn.preprocessing import normalize

def load_data(file_path):
    data = np.load(file_path)
    return data['arr_0'], data['arr_1']


def spilt_data(nPerson, nPicture, data, label):
    """
    分割数据集

    :param nPerson : 志愿者数量
    :param nPicture: 各志愿者选入训练集的照片数量
    :param data : 等待分割的数据集
    :param label: 对应数据集的标签
    :return: 训练集, 训练集标签, 测试集, 测试集标签
    """
    # 数据集大小和意义
    allPerson, allPicture, rows, cols = data.shape

    # 划分训练集和测试集
    train = data[:nPerson, :nPicture, :, :].reshape(nPerson * nPicture, rows * cols)
    train_label = label[:nPerson, :nPicture].reshape(nPerson * nPicture)
    test = data[:nPerson, nPicture:, :, :].reshape(nPerson * (allPicture - nPicture), rows * cols)
    test_label = label[:nPerson, nPicture:].reshape(nPerson * (allPicture - nPicture))

    # 返回: 训练集, 训练集标签, 测试集, 测试集标签
    return train, train_label, test, test_label


def plot_gallery(images, titles, n_row=3, n_col=5, h=112, w=92):  # 3行4列
    """
    展示多张图片

    :param images: numpy array 格式的图片
    :param titles: 图片标题
    :param h: 图像reshape的高
    :param w: 图像reshape的宽
    :param n_row: 展示行数
    :param n_col: 展示列数
    :return:
    """
    # 展示图片
    plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(n_row * n_col):
        plt.subplot(n_row, n_col, i + 1)
        plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
        plt.title(titles[i], size=12)
        plt.xticks(())
        plt.yticks(())
    plt.show()


#输入训练集。提取主特征数
def eigen_train(trainset, k=20):
    """
    训练特征脸（eigenface）算法的实现

    :param trainset: 使用 get_images 函数得到的处理好的人脸数据训练集
    :param K: 希望提取的主特征数
    :return: 训练数据的平均脸, 特征脸向量, 中心化训练数据
    """

    ###############################################################################
    ####                   训练特征脸（eigenface）算法的实现                     ####
    ####                        请勿修改该函数的输入输出                         ####
    ###############################################################################
    avg_img = np.sum(trainset, axis=0)
    avg_img = avg_img/trainset.shape[0]                             #获得平均人脸
    differential_matrix = trainset - avg_img                                    #获得差值矩阵(200,10304)
    norm_img = differential_matrix                                       #中心化人脸即差值矩阵
    differential_matrix_t = differential_matrix.T                                    #差值矩阵的转置
    covariance_matrix = np.mat(differential_matrix) * np.mat(differential_matrix_t)     #获得协方差矩阵转置
    eigenvalue, featurevector = np.linalg.eig(covariance_matrix)                   #获得特征值、特征向量
    k_min = min(featurevector.shape[1], k)                          #k的取值限
    feature_vector = np.mat(differential_matrix_t) * np.mat(featurevector[:,:k_min])    #原始特征向量(10304,20)
    feature = np.mat(differential_matrix_t) * np.mat(differential_matrix) * np.mat(feature_vector)
    feature = np.array(feature).T                                                       #特征向量格式

    ###############################################################################
    #############           在生成 main 文件时, 请勾选该模块            #############
    ###############################################################################

    # 返回：平均人脸、特征人脸、中心化人脸
    return avg_img, feature, norm_img


def rep_face(image, avg_img, eigenface_vects, numComponents=0):
    """
    用特征脸（eigenface）算法对输入数据进行投影映射，得到使用特征脸向量表示的数据

    :param image: 输入数据
    :param avg_img: 训练集的平均人脸数据
    :param eigenface_vects: 特征脸向量
    :param numComponents: 选用的特征脸数量
    :return: 输入数据的特征向量表示, 最终使用的特征脸数量
    """

    ###################################################################################
    ####  用特征脸（eigenface）算法对输入数据进行投影映射，得到使用特征脸向量表示的数据  ####
    ####                          请勿修改该函数的输入输出                           ####
    ###################################################################################

    difference_image = np.array(image) - np.array(avg_img)                          #差值图像(10304,)
    num = min(eigenface_vects.shape[0], numComponents)
    eigenface_vect = normalize(np.array(eigenface_vects[:num, :]), norm = 'l2')         #归一化的矩阵(20,10304)
    linear_space = eigenface_vect.T                                                     #人脸的线性空间(10304, 20)
    coordinate = np.mat(difference_image) * np.mat(linear_space)
    representation = coordinate                                                         #特征向量表示人脸
    numEigenFaces = numComponents
    ###################################################################################
    #############             在生成 main 文件时, 请勾选该模块              #############
    ###################################################################################

    # 返回：输入数据的特征向量表示, 特征脸使用数量
    return representation, numEigenFaces


###人脸重建模型

def recFace(representations, avg_img, eigenVectors, numComponents, sz=(112, 92)):
    """
    利用特征人脸重建原始人脸

    :param representations: 表征数据
    :param avg_img: 训练集的平均人脸数据
    :param eigenface_vects: 特征脸向量
    :param numComponents: 选用的特征脸数量
    :param sz: 原始图片大小
    :return: 重建人脸, str 使用的特征人脸数量
    """

    ###############################################################################
    ####                        利用特征人脸重建原始人脸                         ####
    ####                        请勿修改该函数的输入输出                         ####
    ###############################################################################

    num = min(numComponents, eigenVectors.shape[0])                                #获得符合规范的特征脸数量
    eigenface_vects = np.array(eigenVectors[:num, :])                                  #根据需要的数量获得对应的矩阵
    eigenface_vects = normalize(eigenface_vects, norm = 'l2')                           #二范式归一化
    linear_space = eigenface_vects.T                                      #获得线性空间
    matrix = np.mat(linear_space) * np.mat(linear_space).T                              #右乘线性空间的转置变方阵
    matrix_inversion = np.linalg.inv(np.mat(matrix))                                 #求方阵逆矩阵
    face = np.mat(representations) * np.mat(linear_space).T * np.mat(matrix_inversion)  #获得差值图片
    face = np.array(face) + np.array(avg_img)                                           #获得原始图片

    ###############################################################################
    #############           在生成 main 文件时, 请勾选该模块            #############
    ###############################################################################

    # 返回: 重建人脸, str 使用的特征人脸数量
    return face, 'numEigenFaces_{}'.format(numComponents)

