# 引入必要的模块
import numpy as np
import cv2

# 单尺度Retinex算法


def singleScaleRetinex(img, sigma):
    # 计算高斯模糊
    blur = cv2.GaussianBlur(img, (0, 0), sigma)
    # 计算Retinex
    retinex = np.log10(img) - np.log10(blur)
    return retinex

# 多尺度Retinex算法


def multiScaleRetinex(img, sigma_list):
    # 多尺度计算
    retinex = np.sum([singleScaleRetinex(img, sigma) for sigma in sigma_list], axis=0)
    # 计算平均值
    retinex /= len(sigma_list)
    return retinex

# 颜色修复算法


def colorRestoration(img, alpha, beta):
    # 对图像进行通道求和
    img_sum = np.sum(img, axis=2, keepdims=True)
    # 计算颜色修复
    color_restoration = beta * (np.log10(alpha * img) - np.log10(img_sum))
    return color_restoration

# 最简单的颜色平衡算法


def simplestColorBalance(img, low_clip, high_clip):
    # 计算总像素数
    total = img.shape[0] * img.shape[1]
    # 对每个通道进行处理
    for i in range(img.shape[2]):
        # 统计每个像素值的数量
        unique, counts = np.unique(img[:, :, i], return_counts=True)
        current = 0
        # 根据low_clip和high_clip计算上下阈值
        for u, c in zip(unique, counts):
            if float(current) / total < low_clip:
                low_val = u
            if float(current) / total < high_clip:
                high_val = u
            current += c
        # 对每个通道进行像素值的裁剪
        img[:, :, i] = np.maximum(np.minimum(img[:, :, i], high_val), low_val)
    return img

# MSRCR算法


def MSRCR(img, sigma_list, G, b, alpha, beta, low_clip, high_clip):
    # 对图像进行浮点数转换和加1
    img = np.float64(img) + 1.0
    # 计算多尺度Retinex
    img_retinex = multiScaleRetinex(img, sigma_list)
    # 计算颜色修复
    img_color = colorRestoration(img, alpha, beta)
    # 计算MSRCR结果
    img_msrcr = G * (img_retinex * img_color + b)
    # 对每个通道进行像素值范围调整
    for i in range(img_msrcr.shape[2]):
        img_msrcr[:, :, i] = (img_msrcr[:, :, i] - np.min(img_msrcr[:, :, i])) / \
                             (np.max(img_msrcr[:, :, i]) - np.min(img_msrcr[:, :, i])) * \
            255
    # 对MSRCR结果进行转换
    img_msrcr = np.uint8(np.minimum(np.maximum(img_msrcr, 0), 255))
    # 对MSRCR结果进行最简单的颜色平衡
    img_msrcr = simplestColorBalance(img_msrcr, low_clip, high_clip)
    return img_msrcr

# 自动MSRCR算法


def automatedMSRCR(img, sigma_list):
    # 将图像转换为浮点数并加1
    img = np.float64(img) + 1.0

    # 计算多尺度Retinex
    img_retinex = multiScaleRetinex(img, sigma_list)

    # 对每个通道进行调整
    for i in range(img_retinex.shape[2]):
        # 统计每个像素值的数量
        unique, count = np.unique(
            np.int32(img_retinex[:, :, i] * 100), return_counts=True)

        # 获取像素值为0的数量
        zero_count = count[np.where(unique == 0)[0][0]]

        # 找到上下阈值
        for u, c in zip(unique, count):
            if u < 0 and c < zero_count * 0.1:
                low_val = u / 100.0
            if u > 0 and c < zero_count * 0.1:
                high_val = u / 100.0
                break

        # 对每个通道进行像素值的裁剪和调整
        img_retinex[:, :, i] = np.clip(img_retinex[:, :, i], low_val, high_val)
        img_retinex[:, :, i] = ((img_retinex[:, :, i] - np.min(img_retinex[:, :, i])) /
                                (np.max(img_retinex[:, :, i]) - np.min(img_retinex[:, :, i])) *
                                255).astype(np.uint8)

    return img_retinex

# MSRCR+算法


def MSRCP(img, sigma_list, low_clip, high_clip):
    # 对图像进行浮点数转换和加1
    img = np.float64(img) + 1.0
    # 对图像进行亮度计算
    intensity = np.sum(img, axis=2) / img.shape[2]
    # 计算多尺度Retinex
    retinex = multiScaleRetinex(intensity, sigma_list)
    # 对亮度进行扩展
    intensity = np.expand_dims(intensity, 2)
    retinex = np.expand_dims(retinex, 2)
    # 对Retinex进行最简单的颜色平衡
    intensity1 = simplestColorBalance(retinex, low_clip, high_clip)
    # 对Retinex进行像素值范围调整
    intensity1 = (intensity1 - np.min(intensity1)) / \
                 (np.max(intensity1) - np.min(intensity1)) * \
        255.0 + 1.0
    # 计算MSRCP结果
    img_msrcp = np.zeros_like(img)
    for y in range(img_msrcp.shape[0]):
        for x in range(img_msrcp.shape[1]):
            B = np.max(img[y, x])
            A = np.minimum(256.0 / B, intensity1[y, x, 0] / intensity[y, x, 0])
            img_msrcp[y, x, 0] = A * img[y, x, 0]
            img_msrcp[y, x, 1] = A * img[y, x, 1]
            img_msrcp[y, x, 2] = A * img[y, x, 2]
    # 对MSRCP结果进行转换
    img_msrcp = np.uint8(img_msrcp - 1.0)
    return img_msrcp
