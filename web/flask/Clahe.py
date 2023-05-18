import cv2

class Clahe:
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = cv2.imread(img_path)
    
    def split_channels(self):
        self.red, self.green, self.blue = cv2.split(self.img)
    
    def apply_clahe(self):
        # 创建CLAHE对象
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

        # 对每个通道进行CLAHE处理
        self.red_clahe = clahe.apply(self.red)
        self.green_clahe = clahe.apply(self.green)
        self.blue_clahe = clahe.apply(self.blue)
    
    def merge_channels(self):
        # 合并RGB通道
        self.img_clahe = cv2.merge((self.red_clahe, self.green_clahe, self.blue_clahe))
        
    
    def show_images(self):
        # 显示原图和CLAHE处理后的图像
        cv2.imshow('Original', self.img)
        cv2.imshow('CLAHE', self.img_clahe)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def save_images(self):
        output_path = '.' + self.img_path.split(".")[0] + \
            self.img_path.split(".")[1] + "_CLAHE.jpg"
        cv2.imwrite(output_path, self.img_clahe)
