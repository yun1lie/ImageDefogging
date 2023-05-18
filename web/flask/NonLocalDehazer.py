import cv2
import numpy as np
import sys
import kdtree
import utils
import wls
import regularization


class NonLocalDehazer:
    def __init__(self, file_path, filter_size=15, p=0):
        self.file_path = file_path
        self.filter_size = filter_size
        self.p = p

    def non_local_transmission(self, img, air, gamma=1):
        # find airlight first (same method with DCP)
        img_hazy_corrected = np.power(img, gamma)

        # img = img / 255
        dist_from_airlight = utils.getDistAirlight(img_hazy_corrected, air)

        row, col, n_colors = img.shape

        # Calculate radius(Eq.(5))
        # 3 - dimentional
        radius = np.sqrt(np.sum(dist_from_airlight ** 2, axis=2))

        # Cluster the pixels to haze-lines
        # Use a KD-tree impementation for fast clustering according to their angles
        dist_sphere_radius = np.reshape(radius, [col * row], order='F')

        # 3-di To 2-di      (col*row, 3)
        dist_unit_radius = np.reshape(dist_from_airlight, [col * row, n_colors], order='F')

        dist_norm = np.sqrt(np.sum(dist_unit_radius ** 2, axis=1))

        for i in range(len(dist_unit_radius)):
            dist_unit_radius[i] = dist_unit_radius[i] / dist_norm[i]

        n_points = 1000

        file_path = "./TR" + str(n_points) + ".txt"
        points = np.loadtxt(file_path).tolist()

        mdl = kdtree.create(points)
        # lines stores cluster result
        # [(<KDNode - [0.6256, 0.5636, 0.5394]>, 0.003957329357625813)]
        #       cluster node from points              distance
        cluster = [[]] * n_points
        for i in range(n_points):
            cluster[i] = []
        # save pixel cluster to which point (save index)
        cluster_Points = np.zeros(row * col, dtype=np.int64)

        for r in range(len(dist_unit_radius)):
            kdNode = mdl.search_knn(dist_unit_radius[r], 1)
            self.findPosition(kdNode[0][0].data, dist_sphere_radius[r], cluster, points, r, cluster_Points)

        # how to use the data in kdNode
        # print(lines[0][0][0].data[0])

        # Estimating Initial Transmission
        # Estimate radius as the maximal radius in each haze-line (Eq. (11))
        maxRadius = np.zeros(row * col, dtype=np.float64)
        for i in range(n_points):
            # find max radius
            maxR = 0
            for j in range(len(cluster[i])):
                maxR = max(maxR, cluster[i][j])
            maxRadius[i] = maxR
        np.reshape(maxRadius, [row, col], order='F')

        # Initial Transmission
        # save maxRadius to all pixels
        dist_sphere_maxRadius = np.zeros(row * col, np.float64)
        for i in range(row * col):
            index = cluster_Points[i]
            dist_sphere_maxRadius[i] = maxRadius[index]
        radius_new = np.reshape(dist_sphere_maxRadius, [row, col], order='F')

        transmission_estimation = radius / (radius_new + self.p)

        # Limit the transmission to the range [trans_min, 1] for numerical stability
        trans_min = 0.1

        transmission_estimation = np.minimum(np.maximum(transmission_estimation, trans_min), 1)

        transmission = regularization.regularization(row, col, transmission_estimation, img_hazy_corrected, n_points, air,
                                      cluster_Points, cluster)
        return transmission

    # cluster into 1000length arr
    def findPosition(self, kdNode, radius, cluster, points, r, cluster_Points):
        for i in range(len(points)):
            if (points[i][0] == kdNode[0]) and (points[i][1] == kdNode[1]) and (points[i][2] == kdNode[2]):
                cluster[i].append(radius)
                cluster_Points[r] = i
                break

    def dehaze(self, img, img_norm, transmission_estimission, air):
        h, w, n_colors = img.shape
        img_dehazed = np.zeros((h, w, n_colors), dtype=float)
        leave_haze = 1.06
        for color_idx in range(3):
            img_dehazed[:, :, color_idx] = (img_norm[:, :, color_idx] - (1 - leave_haze * transmission_estimission) * air[
                color_idx]) / np.maximum(transmission_estimission, 0.1)

        img_dehazed = np.where(img_dehazed > 1, 1, img_dehazed)
        img_dehazed = np.where(img_dehazed < 0, 0, img_dehazed)
        img_dehazed = np.power(img_dehazed, 1 / 1)
        adj_percent = [0.005, 0.995]

        # img_dehazed = adjust(img_dehazed, adj_percent)
        # img_dehazed = (img_dehazed * 255).astype(np.uint8)
        # print(img_dehazed)
        return img_dehazed

    def run(self):
        # 读取图像
        image = cv2.imread(self.file_path)

        # 归一化并转换为浮点类型
        normalized_image = cv2.normalize(
            image.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)

        # 暗通道先验估计
        dark_channel = utils.dark_channel(image, self.filter_size)

        # 大气光估计
        atmospheric_light = utils.air_light(image, dark_channel)
        atmospheric_light = atmospheric_light[0] / 255

        # 非局部传输估计
        transmission_estimation = self.non_local_transmission(
            normalized_image, atmospheric_light)

        # 去雾处理
        dehazed_image = self.dehaze(
            image, normalized_image, transmission_estimation, atmospheric_light)

        # 保存去雾后的图像
        output_path = '.' + self.file_path.split(".")[0] + \
            self.file_path.split(".")[1] + "_NonLocal.jpg"
        


        # cv2.imshow("result", dehazed_image)
        cv2.imwrite(output_path, dehazed_image*255)
        # cv2.imshow("non-local transmission", transmission_estimission)
        # cv2.waitKey(0)

# if __name__ == '__main__':
#     file_path = "./Pics/city_input.png"
#     nld = NonLocalDehazer(file_path)
#     nld.run()