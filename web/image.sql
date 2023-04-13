/*
 Navicat Premium Data Transfer

 Source Server         : my
 Source Server Type    : MySQL
 Source Server Version : 80026
 Source Host           : localhost:3306
 Source Schema         : image

 Target Server Type    : MySQL
 Target Server Version : 80026
 File Encoding         : 65001

 Date: 13/04/2023 19:46:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for image
-- ----------------------------
DROP TABLE IF EXISTS `image`;
CREATE TABLE `image`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '图像唯一标识ID',
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '图像名称',
  `path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '图像路径',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '图像描述',
  `upload_time` datetime(0) NULL DEFAULT NULL COMMENT '上传时间',
  `uploader_id` int(0) NULL DEFAULT NULL COMMENT '上传者ID',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_uploader`(`uploader_id`) USING BTREE,
  CONSTRAINT `fk_uploader` FOREIGN KEY (`uploader_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of image
-- ----------------------------
INSERT INTO `image` VALUES (1, 'image1', '/images/image1.jpg', '腹腔镜图像1', '2023-04-13 19:45:10', 1);
INSERT INTO `image` VALUES (2, 'image2', '/images/image2.jpg', '腹腔镜图像2', '2023-04-13 19:45:20', 1);
INSERT INTO `image` VALUES (3, 'image3', '/images/image3.jpg', '腹腔镜图像3', '2023-04-13 19:45:30', 2);
INSERT INTO `image` VALUES (4, 'image4', '/images/image4.jpg', '腹腔镜图像4', '2023-04-13 19:45:40', 2);
INSERT INTO `image` VALUES (5, 'image5', '/images/image5.jpg', '腹腔镜图像5', '2023-04-13 19:45:50', 3);
INSERT INTO `image` VALUES (6, 'image6', '/images/image6.jpg', '腹腔镜图像6', '2023-04-13 19:46:00', 3);
INSERT INTO `image` VALUES (7, 'image7', '/images/image7.jpg', '腹腔镜图像7', '2023-04-13 19:46:10', 4);
INSERT INTO `image` VALUES (8, 'image8', '/images/image8.jpg', '腹腔镜图像8', '2023-04-13 19:46:20', 4);
INSERT INTO `image` VALUES (9, 'image9', '/images/image9.jpg', '腹腔镜图像9', '2023-04-13 19:46:30', 5);
INSERT INTO `image` VALUES (10, 'image10', '/images/image10.jpg', '腹腔镜图像10', '2023-04-13 19:46:40', 5);

-- ----------------------------
-- Table structure for operation_record
-- ----------------------------
DROP TABLE IF EXISTS `operation_record`;
CREATE TABLE `operation_record`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '操作记录唯一标识ID',
  `operator_id` int(0) NULL DEFAULT NULL COMMENT '操作者ID',
  `operate_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作类型',
  `operate_time` datetime(0) NULL DEFAULT NULL COMMENT '操作时间',
  `operate_content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '操作内容',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_operator`(`operator_id`) USING BTREE,
  CONSTRAINT `fk_operator` FOREIGN KEY (`operator_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of operation_record
-- ----------------------------
INSERT INTO `operation_record` VALUES (1, 1, '上传图像', '2023-04-13 19:48:02', '上传了腹腔镜图像1');
INSERT INTO `operation_record` VALUES (2, 1, '上传图像', '2023-04-13 19:48:05', '上传了腹腔镜图像2');
INSERT INTO `operation_record` VALUES (3, 2, '上传图像', '2023-04-13 19:48:08', '上传了腹腔镜图像3');
INSERT INTO `operation_record` VALUES (4, 2, '上传图像', '2023-04-13 19:48:12', '上传了腹腔镜图像4');
INSERT INTO `operation_record` VALUES (5, 3, '上传图像', '2023-04-13 19:48:15', '上传了腹腔镜图像5');
INSERT INTO `operation_record` VALUES (6, 3, '上传图像', '2023-04-13 19:48:20', '上传了腹腔镜图像6');
INSERT INTO `operation_record` VALUES (7, 4, '上传图像', '2023-04-13 19:48:25', '上传了腹腔镜图像7');
INSERT INTO `operation_record` VALUES (8, 4, '上传图像', '2023-04-13 19:48:30', '上传了腹腔镜图像8');
INSERT INTO `operation_record` VALUES (9, 5, '上传图像', '2023-04-13 19:48:35', '上传了腹腔镜图像9');
INSERT INTO `operation_record` VALUES (10, 5, '上传图像', '2023-04-13 19:48:40', '上传了腹腔镜图像10');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(0) NOT NULL AUTO_INCREMENT COMMENT '用户唯一标识ID\r\n',
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户名',
  `password` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码',
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '邮箱',
  `phone` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '电话',
  `real_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '真实姓名',
  `department` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '所属部门',
  `role` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '角色',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'user1', '123456', 'user1@example.com', '12345678901', '张三', '医学影像科', '医生', '2023-04-13 19:35:54', '2023-04-13 19:35:54');
INSERT INTO `users` VALUES (2, 'user2', '123456', 'user2@example.com', '12345678902', '李四', '外科', '医生', '2023-04-13 19:35:54', '2023-04-13 19:35:54');
INSERT INTO `users` VALUES (3, 'user3', '123456', 'user3@example.com', '12345678903', '王五', '内科', '医生', '2023-04-13 19:35:54', '2023-04-13 19:35:54');
INSERT INTO `users` VALUES (4, 'user4', '123456', 'user4@example.com', '12345678904', '赵六', '儿科', '医生', '2023-04-13 19:35:54', '2023-04-13 19:35:54');
INSERT INTO `users` VALUES (5, 'user5', '123456', 'user5@example.com', '12345678905', '刘七', '神经科', '医生', '2023-04-13 19:35:54', '2023-04-13 19:35:54');
INSERT INTO `users` VALUES (6, 'admin1', '123456', 'admin1@example.com', '12345678906', '管理员一', '系统管理部门', '系统管理员', '2023-04-13 19:35:54', '2023-04-13 19:35:54');
INSERT INTO `users` VALUES (7, 'admin2', '123456', 'admin2@example.com', '12345678907', '管理员二', '系统管理部门', '系统管理员', '2023-04-13 19:35:54', '2023-04-13 19:35:54');
INSERT INTO `users` VALUES (8, 'admin3', '123456', 'admin3@example.com', '12345678908', '管理员三', '系统管理部门', '系统管理员', '2023-04-13 19:35:54', '2023-04-13 19:35:54');
INSERT INTO `users` VALUES (9, 'superadmin1', '123456', 'superadmin1@example.com', '12345678909', '超级管理员一', '系统管理部门', '超级管理员', '2023-04-13 19:35:54', '2023-04-13 19:35:54');
INSERT INTO `users` VALUES (10, 'superadmin2', '123456', 'superadmin2@example.com', '12345678910', '超级管理员二', '系统管理部门', '超级管理员', '2023-04-13 19:35:54', '2023-04-13 19:35:54');

SET FOREIGN_KEY_CHECKS = 1;
