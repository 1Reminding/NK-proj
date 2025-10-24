# -*- coding: utf-8 -*-
"""
IoT-23 数据集 - CNN 模型训练与导出（适配 Quark）
包含：数据清洗、特征选择、CNN 训练、剪枝、量化、权重导出（Python 调用格式）
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

# 设置路径
BASE_DIR = r"C:\Xing\大三下\物联网通信\Quark-CNN-P4\iot_23_datasets_small\opt\Malware-Project\BigDataset\IoTScenarios"  # ← 替换为你本地数据路径

# ------------------ 1. 加载数据 ------------------
def collect_all_labeled_files(base_dir):
    dfs = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == "conn.log.labeled":
                try:
                    path = os.path.join(root, file)
                    print(f"加载: {path}")
                    df = pd.read_csv(path, sep='\t', engine='python', comment='#')
                    dfs.append(df)
                except:
                    continue
    return pd.concat(dfs, ignore_index=True)

raw_df = collect_all_labeled_files(BASE_DIR)

# ------------------ 2. 特征选择 + 标签处理 ------------------
selected_cols = [
    'duration', 'orig_bytes', 'resp_bytes', 'missed_bytes',
    'orig_pkts', 'resp_pkts', 'orig_ip_bytes', 'resp_ip_bytes'
]

raw_df = raw_df.dropna(subset=selected_cols + ['label'])
X = raw_df[selected_cols].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 标签转为二分类：Benign vs Malware
y = raw_df['label'].apply(lambda x: 0 if 'Benign' in x else 1)

# ------------------ 3. 构建数据集 ------------------
X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

X_train = torch.tensor(X_train[:, :, None], dtype=torch.float32)  # 增加通道维度
X_val = torch.tensor(X_val[:, :, None], dtype=torch.float32)
y_train = torch.tensor(y_train.values, dtype=torch.long)
y_val = torch.tensor(y_val.values, dtype=torch.long)

train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=64, shuffle=True)
val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=64)

# ------------------ 4. 定义 CNN 模型 ------------------
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 4, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(4, 4, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool1d(2)
        self.conv3 = nn.Conv1d(4, 4, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool1d(2)
        self.fc1 = nn.Linear(4 * 1, 4)
        self.fc2 = nn.Linear(4, 2)

    def forward(self, x):
        x = x.permute(0, 2, 1)
        x = self.pool1(F.relu(self.conv1(x)))
        x = self.pool2(F.relu(self.conv2(x)))
        x = self.pool3(F.relu(self.conv3(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return self.fc2(x)

# ------------------ 5. 训练 ------------------
model = SimpleCNN()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

print("\n开始训练 CNN 模型...")
for epoch in range(10):
    model.train()
    total_loss = 0
    for xb, yb in train_loader:
        optimizer.zero_grad()
        out = model(xb)
        loss = criterion(out, yb)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    model.eval()
    total = correct = 0
    with torch.no_grad():
        for xb, yb in val_loader:
            out = model(xb)
            preds = out.argmax(1)
            total += yb.size(0)
            correct += (preds == yb).sum().item()
    acc = correct / total * 100
    print(f"Epoch {epoch+1}: Loss = {total_loss:.4f}, Val Acc = {acc:.2f}%")

# ------------------ 6. 导出权重（适配 P4 控制器） ------------------
def export_weights():
    print("\n# -- 卷积层权重导出 (for set-up_open_resource.py) --")
    for i, conv in enumerate([model.conv1, model.conv2, model.conv3], start=1):
        weight = conv.weight.detach().numpy()[:, 0, :].astype(int)  # 4x3
        for ch, row in enumerate(weight):
            row_str = ", ".join([f"{v}" for v in row])
            print(f"p4.pipea.SwitchIngress_a.weight_tbl.add_with_weight_act(level = {i}, channel_index = {ch+1}, w1 = {row[0]}, w2 = {row[1]}, w3 = {row[2]}, w4 = 0)")

    print("\n# -- 全连接层偏置导出 (for quanti_tbl_l4/l5) --")
    biases = [model.fc1.bias.detach().numpy(), model.fc2.bias.detach().numpy()]
    for level, b in zip([4, 5], biases):
        for i, v in enumerate(b):
            print(f"bias_l{level}{i+1} = {v:.4f}")

export_weights()
