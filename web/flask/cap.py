import cv2 
import numpy as np
import copy 

class Cap:
    def __init__(self, filename, beta=1, theta0=0.121779, theta1=0.959710, theta2=-0.780245, sigma=0.041337, n_size=5, blur_strength=15, noise=0):
        self.filename = filename
        self.beta = beta
        self.theta0 = theta0
        self.theta1 = theta1
        self.theta2 = theta2
        self.sigma = sigma
        self.n_size = n_size
        self.blur_strength = blur_strength
        self.noise = noise

    def quantization(self, pixels, bins, range_):
        m = range_[0]
        interval_size = range_[1]-range_[0]
        interval_size /= bins

        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                pixels[i][j] = ((pixels[i][j]-m)/interval_size)

        return pixels

    def visualise(self, depth_map, name, beta):
        d = copy.deepcopy(depth_map)
        d = self.quantization(d, 255, [d.min(), d.max()]).astype(np.uint8)

        d = cv2.applyColorMap(d, cv2.COLORMAP_HOT)
        # cv2.imwrite(f"./output/{name}_{beta}.jpg", d)

    def relu(self, x):
        if x<0:
            return 0
        else:
            return x

    def reverse_relu(self, bound, x):
        if x>bound:
            return bound
        else:
            return x

    def guided_filter(self, image, g_image, eps=0):
        blur_factor = (50,50)
        mean_i = cv2.blur(image, blur_factor)
        mean_g = cv2.blur(g_image, blur_factor)

        corr_gi = cv2.blur(g_image*image, blur_factor)
        corr_gg = cv2.blur(g_image*g_image, blur_factor)

        var_g = corr_gg - mean_g*mean_g
        cov_gi = corr_gi - mean_g*mean_i

        a = cov_gi / (var_g + eps)
        b = mean_i - (a*mean_g)

        mean_a = cv2.blur(a, blur_factor)
        mean_b = cv2.blur(b, blur_factor)

        q = mean_a * g_image + mean_b

        return q

    def dehaze(self):
        # Reading the image
        h_img = cv2.imread(self.filename)

        #Extracting the value and saturation values from the image
        hsv = cv2.cvtColor(h_img, cv2.COLOR_BGR2HSV)
        value = hsv[:,:,2].astype('float')/255 # Intensity values of image
        saturation = hsv[:,:,1].astype('float')/255 # Saturation values of image

        # Calculating the depth map
        depth_map = self.theta0 + self.theta1*value + self.theta2*saturation + np.random.normal(0,self.sigma, hsv[:,:,0].shape)
        self.visualise(depth_map, "1_depth_map", self.beta)

        #Calculating the min-filtered depth map
        new_depth_map = copy.deepcopy(depth_map)

        width = depth_map.shape[1]
        height = depth_map.shape[0]

        for i in range(height):
            for j in range(width):
                x_low = self.relu(i-self.n_size)
                x_high = self.reverse_relu(height-1, i+self.n_size)+1
                y_low = self.relu(j-self.n_size)
                y_high = self.reverse_relu(width-1, j+self.n_size)+1
                new_depth_map[i][j] = np.min(depth_map[x_low:x_high, y_low:y_high])

        self.visualise(new_depth_map, "2_min_filter_depth_map", self.beta)

        # Refining the depth map
        # blurred_depth_map = cv2.GaussianBlur(new_depth_map,(blur_strength, blur_strength),0) # Gaussian blur of depthmap (d(x))
        blurred_depth_map = self.guided_filter(new_depth_map, depth_map, self.noise)
        self.visualise(blurred_depth_map, "3_blurred_depth_map", self.beta)

        # Restoring scene radiance
        depth_map_1d = np.ravel(blurred_depth_map)
        rankings = np.argsort(depth_map_1d)

        threshold = (99.9*len(rankings))/100
        indices = np.argwhere(rankings>threshold).ravel()

        indices_image_rows = indices//width
        indices_image_columns = indices % width

        atmospheric_light = np.zeros(3) # A
        intensity = -np.inf
        for x in range(len(indices_image_rows)):
            i = indices_image_rows[x]
            j = indices_image_columns[x]

            if value[i][j] >= intensity:
                atmospheric_light = h_img[i][j]
                intensity = value[i][j]

        t = np.exp(-self.beta*blurred_depth_map)

        denom = np.clip(t, 0.1, 0.9)
        numer = h_img.astype("float") - atmospheric_light.astype("float")

        output_image = copy.deepcopy(h_img).astype("float")

        for i in range(len(output_image)):
            for j in range(len(output_image[i])):
                output_image[i][j] = numer[i][j]/denom[i][j]

        output_image += atmospheric_light.astype("float")
        output_image[:,:,0] = self.quantization(output_image[:,:,0], 256, [np.min(output_image[:,:,0]), np.max(output_image[:,:,0])])
        output_image[:,:,1] = self.quantization(output_image[:,:,1], 256, [np.min(output_image[:,:,1]), np.max(output_image[:,:,1])])
        output_image[:,:,2] = self.quantization(output_image[:,:,2], 256, [np.min(output_image[:,:,2]), np.max(output_image[:,:,2])])
        
        output_path = '.' + \
        self.filename.split(".")[0] + \
        self.filename.split(".")[1] + "_Cap.jpg"

        cv2.imwrite(output_path, output_image.astype(np.uint8))


# dehaze = Dehaze("000001.png", beta=1)
# dehaze.dehaze()
