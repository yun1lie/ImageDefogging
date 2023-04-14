import cv2
import numpy as np


class FogRemover:
    def __init__(self, img_path):
        self.img_path = img_path

    def estimate_fog_degree(self):
        """
        估计腹腔镜图像的雾化程度
        :return: 腹腔镜图像的雾化程度
        """
        # 读取待处理的有雾腹腔镜图像
        img = cv2.imread(self.img_path)

        # 计算暗通道图像
        window_size = 15
        dark_img = cv2.erode(img, np.ones(
            (window_size, window_size), np.uint8))
        gray_img = cv2.cvtColor(dark_img, cv2.COLOR_BGR2GRAY)

        # 选择非器械区域
        non_instr_area = gray_img[100:600, 100:800]

        # 计算非器械区域的最小值
        min_val = np.min(non_instr_area)

        # 计算整张图像所有非器械区域的最小值的均值，即为腹腔镜图像的雾化程度
        fog_degree = np.mean(min_val)

        return fog_degree

    def get_atmosphere(self, img, percent=0.01):
        """
        估计大气光照
        :param img: 输入图像
        :param percent: 暗通道中最亮的前百分比像素点用于估计大气光照
        :return: 大气光照
        """
        # 将图像转换为暗通道
        dc_img = cv2.erode(img, np.ones((15, 15), np.uint8))
        dc_img = dc_img.min(axis=2)

        # 计算暗通道中最亮的前 percent 像素点的索引
        n_pixels = dc_img.shape[0] * dc_img.shape[1]
        n_top = int(n_pixels * percent)
        top_indices = np.argpartition(dc_img.flatten(), -n_top)[-n_top:]

        # 从图像中获取对应的颜色信息
        top_colors = img.reshape((-1, 3))[top_indices]
        top_intensity = np.max(top_colors, axis=1)

        # 估计大气光照
        atmosphere = np.percentile(top_intensity, 90)

        return atmosphere

    def defog(self, a=0.95, w=15, t0=0.1, percent=0.01):
        """
        对有雾图像进行去雾处理
        :param a: 透射率调整系数
        :param w: 窗口大小
        :param t0: 透射率下限阈值
        :param percent: 暗通道中最亮的前百分比像素点用于估计大气光照
        :return: 去雾后的图像
        """
        # 读入有雾腹腔镜图像
        img = cv2.imread(self.img_path)

        # 转换成浮点数类型
        img = np.float64(img) / 255.0

        # 估计大气光照
        atmosphere = self.get_atmosphere(img, percent)

        # 计算暗通道
        window_size = w
        dc_img = cv2.erode(img, np.ones((window_size, window_size), np.uint8))
        dc_img = np.min(dc_img, axis=2)

        # 估计透射率
        t_est = 1 - a * (dc_img / atmosphere)
        t_est = np.maximum(t_est, t0)

        # 计算去雾后的图像
        J = np.zeros_like(img)
        for c in range(3):
            J[:, :, c] = (img[:, :, c] - atmosphere) / t_est + atmosphere

        # 对像素值进行截断
        J = np.clip(J, 0, 1)

        # 转换为uint8类型
        J = np.uint8(J * 255)

        return J

    def sharpen_image(self, img):
        # 图像锐化
        # 定义卷积核
        kernel_sharpening = np.array([[-1, -1, -1],
                                      [-1, 9, -1],
                                      [-1, -1, -1]])

        # 应用卷积核
        sharp_image = cv2.filter2D(img, -1, kernel_sharpening)

        return sharp_image

    def adjust_contrast(self, img, alpha=1.0, beta=0):
        """
        对比度调整函数
        :param img: 输入图像
        :param alpha: 对比度增强系数，默认为1.0
        :param beta: 亮度调整值，默认为0
        :return: 调整后的图像
        """
        # 对比度调整
        adjusted_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

        return adjusted_img

    def process(self):
        """
        处理图像
        """
        fog_degree = self.estimate_fog_degree()
        print("腹腔镜图像雾化程度为:{:.2f}".format(fog_degree))

        # 进行去雾处理
        defog_img = self.defog()

        # 图像锐化
        # defog_img = self.sharpen_image(defog_img)

        # 对比度调整
        # adjusted_img = self.adjust_contrast(defog_img, alpha=1.5, beta=10)
        # cv2.imshow('Adjusted', defog_img)
        # cv2.waitKey(0)

        # 保存去雾后的图像
        output_path = '.' + \
        self.img_path.split(".")[0] + \
        self.img_path.split(".")[1] + "_defog.jpg"
        cv2.imwrite(output_path, defog_img)
        defog_img = FogRemover(output_path)

        defog_degree = defog_img.estimate_fog_degree()
        print("去雾后腹腔镜图像雾化程度为:{:.2f}".format(defog_degree))
