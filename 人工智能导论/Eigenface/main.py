# 在生成 main 文件时, 请勾选该模块

# 导入必要的包
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
import os


# def load_data(file_path):
#     data = np.load(file_path)
#     return data['arr_0'], data['arr_1']
def load_data(file_path):
    data = np.load(file_path)
    images = data['images']  # Change 'arr_0' to the actual key
    labels = data['labels']  # Change 'arr_1' to the actual key
    data.close()
    return images, labels

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


# 在生成 main 文件时, 请勾选该模块

def eigen_train(trainset, k=20):
    avg_img = np.mean(trainset, axis=0)
    norm_img = trainset - avg_img
    # 使用SVD计算特征向量
    U, s, Vt = np.linalg.svd(norm_img, full_matrices=False)
    eigenvectors = Vt.T[:, :k]  # 取前k个特征向量
    eigenvalues = s[:k] ** 2 / (len(trainset) - 1)  # 计算特征值

    # 返回：平均人脸、特征人脸、中心化人脸
    return avg_img, eigenvectors, norm_img


# 在生成 main 文件时, 请勾选该模块

def rep_face(image, avg_img, eigenface_vects, numComponents=20):
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
    #                                                                                 #
    centered_image = image - avg_img
    representation = np.dot(centered_image, eigenface_vects[:, :numComponents])
    #                                                                                 #
    ###################################################################################
    #############             在生成 main 文件时, 请勾选该模块              #############
    ###################################################################################

    # 返回：输入数据的特征向量表示, 特征脸使用数量
    return representation, numComponents


# 在生成 main 文件时, 请勾选该模块

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
    #                                                                             #
    face = np.dot(representations, eigenVectors[:, :numComponents].T) + avg_img
    face = face.reshape(sz)
    #                                                                             #
    ###############################################################################
    #############           在生成 main 文件时, 请勾选该模块            #############
    ###############################################################################

    # 返回: 重建人脸, str 使用的特征人脸数量
    return face, 'numEigenFaces_{}'.format(numComponents)
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
def test_different_numbers_of_eigenfaces(data, labels, feature_numbers, image_index=0):
    train, train_labels, test, test_labels = spilt_data(10, 10, data, labels)  # 示例分割
    avg_img, eigenvectors, _ = eigen_train(train)

    reconstructions = []
    mse_scores = []

    for k in feature_numbers:
        representation, _ = rep_face(test[image_index], avg_img, eigenvectors, k)
        reconstructed_image, _ = recFace(representation, avg_img, eigenvectors, k, (112, 92))
        mse = mean_squared_error(test[image_index].flatten(), reconstructed_image.flatten())
        mse_scores.append(mse)
        reconstructions.append(reconstructed_image)

        plt.figure(figsize=(2, 2))
        plt.imshow(reconstructed_image.reshape(112, 92), cmap='gray')
        plt.title(f'{k} Eigenfaces')
        plt.axis('off')
        plt.show()

    plt.figure()
    plt.plot(feature_numbers, mse_scores, marker='o')
    plt.xlabel('Number of Eigenfaces')
    plt.ylabel('Mean Squared Error')
    plt.title('Reconstruction Error vs. Number of Eigenfaces')
    plt.grid(True)
    plt.show()

    return mse_scores

# Parameters
file_path = './ORL.npz'
data, labels = load_data(file_path)
feature_numbers = [10, 20, 30, 50, 100, 150, 200]  # Different numbers of eigenfaces

# Call the function to test different numbers of eigenfaces
mse_scores = test_different_numbers_of_eigenfaces(data, labels, feature_numbers)
