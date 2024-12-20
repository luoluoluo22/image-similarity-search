import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image
import numpy as np
import os
import faiss

class ImageSearchEngine:
    def __init__(self, image_folder='images'):
        self.image_folder = image_folder
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 加载预训练模型
        self.model = resnet50(weights=ResNet50_Weights.DEFAULT)
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])  # 移除最后的全连接层
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # 图像预处理
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                              std=[0.229, 0.224, 0.225])
        ])
        
        # 初始化特征索引
        self.image_paths = []
        self.features = None
        self.index = None
        self.build_index()
    
    def extract_features(self, image_path):
        """提取单个图像的特征向量"""
        image = Image.open(image_path).convert('RGB')
        image = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            features = self.model(image)
        
        return features.cpu().numpy().reshape(-1)
    
    def build_index(self):
        """构建图像特征索引"""
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)
            print(f"创建图像文件夹: {self.image_folder}")
            return
        
        # 获取所有图像文件
        self.image_paths = []
        features_list = []
        
        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # 使用 posix 风格的路径（使用正斜杠）
                image_path = os.path.join(self.image_folder, filename).replace('\\', '/')
                self.image_paths.append(image_path)
                features = self.extract_features(image_path)
                features_list.append(features)
        
        if not features_list:
            print("没有找到图像文件")
            return
        
        # 构建特征矩阵
        self.features = np.array(features_list)
        
        # 使用 IndexFlatIP 替代 IndexFlatL2
        dimension = self.features.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # 使用内积相似度
        
        # 归一化特征向量
        faiss.normalize_L2(self.features)  # 将特征向量归一化
        self.index.add(self.features.astype('float32'))
        
        print(f"索引构建完成，共包含 {len(self.image_paths)} 张图像")
    
    def search_similar_images(self, query_image_path, top_k=5):
        """搜索相似图像"""
        # 提取查询图像的特征
        query_features = self.extract_features(query_image_path)
        
        if self.index is None or len(self.image_paths) == 0:
            return []
        
        # 归一化查询特征
        query_features = query_features.reshape(1, -1).astype('float32')
        faiss.normalize_L2(query_features)
        
        # 搜索最相似的图像
        similarities, indices = self.index.search(
            query_features,
            min(top_k, len(self.image_paths))
        )
        
        # 构建结果列表
        results = []
        for similarity, idx in zip(similarities[0], indices[0]):
            results.append({
                'image_path': self.image_paths[idx],
                'similarity': float((similarity + 1) / 2)  # 将相似度范围从[-1,1]转换到[0,1]
            })
        
        return results 