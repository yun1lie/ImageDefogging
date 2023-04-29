import numpy as np
import os
import cv2


class Dehaze:
    def __init__(self, min_filter_radius=7, guided_filter_radius=81, guided_filter_epsilon=0.001,
                 v1_limit=0.80, v1_weight=0.95, bins=2000, gamma_correction_enabled=False):
        # 初始化函数，设置默认参数
        self.min_filter_radius = min_filter_radius
        self.guided_filter_radius = guided_filter_radius
        self.guided_filter_epsilon = guided_filter_epsilon
        self.v1_limit = v1_limit
        self.v1_weight = v1_weight
        self.bins = bins
        self.gamma_correction_enabled = gamma_correction_enabled

    def _min_filter(self, src):
        # 最小值滤波函数
        return cv2.erode(src, np.ones((2 * self.min_filter_radius + 1, 2 * self.min_filter_radius + 1)))

    def _guided_filter(self, I, p):
        # 引导滤波函数
        height, width = I.shape

        m_I = cv2.boxFilter(
            I, -1, (self.guided_filter_radius, self.guided_filter_radius))
        m_p = cv2.boxFilter(
            p, -1, (self.guided_filter_radius, self.guided_filter_radius))
        m_Ip = cv2.boxFilter(
            I * p, -1, (self.guided_filter_radius, self.guided_filter_radius))

        cov_Ip = m_Ip - m_I * m_p
        m_II = cv2.boxFilter(
            I * I, -1, (self.guided_filter_radius, self.guided_filter_radius))
        var_I = m_II - m_I * m_I

        a = cov_Ip / (var_I + self.guided_filter_epsilon)
        b = m_p - a * m_I

        m_a = cv2.boxFilter(
            a, -1, (self.guided_filter_radius, self.guided_filter_radius))
        m_b = cv2.boxFilter(
            b, -1, (self.guided_filter_radius, self.guided_filter_radius))

        return m_a * I + m_b

    def _get_V1(self, m):
        # 计算大气遮罩图像V1和光照值A
        V1 = np.min(m, 2)
        V1 = self._guided_filter(V1, self._min_filter(V1))
        hist = np.histogram(V1, self.bins)
        cumulative_hist = np.cumsum(hist[0]) / float(V1.size)

        for lmax in range(self.bins - 1, 0, -1):
            if cumulative_hist[lmax] <= 0.999:
                break

        A = np.mean(m, 2)[V1 >= hist[1][lmax]].max()
        V1 = np.minimum(V1 * self.v1_weight, self.v1_limit)
        return V1, A

    def dehaze(self, m):
        # 去雾函数
        Y = np.zeros(m.shape)
        V1, A = self._get_V1(m)

        for k in range(3):
            Y[:, :, k] = (m[:, :, k] - V1) / (1 - V1 / A)

        Y = np.clip(Y, 0, 1)

        if self.gamma_correction_enabled:
            Y = Y ** (np.log(0.5) / np.log(Y.mean()))

        return Y

    def process_images(self, img_name):
        save_path = '.' + \
            img_name.split(".")[0] + \
            img_name.split(".")[1] + "_defogDCP.jpg"
        # 处理图片函数
        if img_name.endswith('jpg') or img_name.endswith('png'):
            # img_path = os.path.join(input_dir, img_name)
            m = self.dehaze(cv2.imread(img_name) / 255.0) * 255
            # save_path = os.path.join(output_path, img_name)
            cv2.imwrite(save_path, m)
            print(save_path)

        print('Done processing images.')
