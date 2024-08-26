# 在生成 main 文件时, 请勾选该模块

# 导入必要的包
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
import os


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
    avg_img = np.mean(trainset, axis=0)
    norm_img = trainset - avg_img
    # 使用SVD代替直接的特征值分解，以提高数值稳定性
    U, S, Vt = np.linalg.svd(norm_img, full_matrices=False)
    # 选择前k个特征向量
    feature = Vt[:k].T
    return avg_img, feature, norm_img



def rep_face(image, avg_img, eigenface_vects, numComponents=0):
    if numComponents == 0:
        numComponents = len(eigenface_vects)
    difference_image = image - avg_img
    # 归一化差异图像
    normalized_difference = difference_image / np.linalg.norm(difference_image)
    representation = np.dot(eigenface_vects[:numComponents], normalized_difference)
    return representation, numComponents


###人脸重建模型
import numpy as np
from sklearn.preprocessing import normalize
def recFace(representations, avg_img, eigenVectors, numComponents, sz=(112, 92)):
    if representations.ndim == 1:
        representations = representations.reshape(1, -1)
    num = min(eigenVectors.shape[0], numComponents)
    # 使用Tikhonov正则化
    regularization_term = 0.1 * np.eye(num)
    eigenVectors_used = eigenVectors[:, :num]
    reconstructed_diff = np.dot(eigenVectors_used, np.linalg.inv(np.dot(eigenVectors_used.T, eigenVectors_used) + regularization_term))
    face = np.dot(reconstructed_diff, representations.T).flatten() + avg_img
    reconstruction_image = face.reshape(sz)
    return reconstruction_image, 'numEigenFaces_{}'.format(numComponents)

