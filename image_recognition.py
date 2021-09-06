import matplotlib.pyplot as plt
import glob
import cv2
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
# from google.colab.patches import cv2_imshow


def show_img(Input, Output):
    # 画像を表示するための関数を定義
    plt.subplot(121)  # 画像の位置を指定
    plt.imshow(Input)  # 画像を表示
    plt.title('Input')  # 画像の上にInputと表記
    plt.xticks([])  # x軸の目盛りを非表示
    plt.yticks([])  # y軸の目盛りを非表示

    plt.subplot(122)  # 画像の位置を指定
    plt.imshow(Output)  # 画像を表示
    plt.title('Output')  # 画像の上にOutputと表記
    plt.xticks([])  # x軸の目盛りを非表示
    plt.yticks([])  # y軸の目盛りを非表示


# 画像をグレースケール化して読み込み ※画像ファイル名の箇所は適宜変更してください。
original = cv2.imread('./uploads/dog_image.jpg', 0)

# 画像のサイズを変更
img0 = cv2.resize(original, (250, 180))

# 画像を表示
cv2_imshow(original)
cv2_imshow(img0)

# Google Colab以外でOpenCVを用いて画像を表示する場合に必要なコード
cv2.waitKey(0)  # キーボードが押されるまで待機
cv2.destroyAllWindows()  # 全てのウィンドウを閉じる

# # 画像の色をmatplotlibに合わせて変換
# img = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)

# # 画像を表示
# show_img(img0, img)
