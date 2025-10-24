# -*- coding: utf-8 -*-
"""
CICIDS-2017 - CNN 模型训练与导出（适配 Quark）
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 设置路径（替换为你自己的目录）
BASE_DIR = r"C:\Xing\大三下\物联网通信\Quark-CNN-P4\MachineLearningCSV\MachineLearningCVE"

# ------------------ 1. 加载所有 CSV 文件 ------------------
def load_all_csvs(base_dir):
    all_data = []
    for file in os.listdir(base_dir):
        if file.endswith('.csv'):
            path = os.path.join(base_dir, file)
            print(f"加载: {path}")
            try:
                df = pd.read_csv(path, low_memory=False)
                df.columns = df.columns.str.strip()  # 清除列名空格
                print(f"字段名: {df.columns.tolist()}")
                all_data.append(df)
            except Exception as e:
                print(f"失败: {path}, 错误: {e}")
    return pd.concat(all_data, ignore_index=True)

df = load_all_csvs(BASE_DIR)

# ------------------ 2. 特征选择 + 标签处理 ------------------
selected_cols = [
    'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
    'Total Length of Fwd Packets', 'Total Length of Bwd Packets',
    'Fwd Packet Length Mean', 'Bwd Packet Length Mean', 'Flow IAT Mean'
]

# 打印缺失字段（如果有）
missing = [col for col in selected_cols + ['Label'] if col not in df.columns]
if missing:
    print(f"⚠️ 缺失字段: {missing}")
else:
    print(f"✅ 所有字段已就绪: {selected_cols + ['Label']}")

df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=selected_cols + ['Label'])
X = df[selected_cols].astype(float)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

y = df['Label'].apply(lambda x: 0 if 'Benign' in str(x) else 1)

# ------------------ 3. 构建数据集 ------------------
X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
X_train = torch.tensor(X_train[:, :, None], dtype=torch.float32)
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
        self.bn1 = nn.BatchNorm1d(4)  # 添加批归一化
        self.pool1 = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(4, 4, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(4)  # 添加批归一化
        self.pool2 = nn.MaxPool1d(2)
        self.fc1 = nn.Linear(4 * 2, 4)
        self.fc2 = nn.Linear(4, 2)

    def forward(self, x):
        x = x.permute(0, 2, 1)
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return self.fc2(x)

# ------------------ 5. 模型训练 ------------------
model = SimpleCNN()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
# 添加学习率调度器
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=2, factor=0.5)
criterion = nn.CrossEntropyLoss()

print("\n开始训练 CNN 模型...")
# 添加变量跟踪最佳验证准确率
best_val_acc = 0
total_batches = len(train_loader)

for epoch in range(10):
    model.train()
    epoch_loss = 0.0
    batch_count = 0
    
    # 打印进度条
    print(f"Epoch {epoch+1}/10 训练进度: ", end="")
    progress_step = max(1, total_batches // 10)  # 将进度分为10个部分
    
    for xb, yb in train_loader:
        optimizer.zero_grad()  # 确保在每个batch开始前清零梯度
        out = model(xb)
        loss = criterion(out, yb)
        loss.backward()
        optimizer.step()
        
        # 累计loss
        epoch_loss += loss.item()
        batch_count += 1
        
        # 简化的进度显示
        if batch_count % progress_step == 0:
            print(".", end="", flush=True)
    
    # 计算平均loss
    avg_train_loss = epoch_loss / batch_count if batch_count > 0 else 0
    print(f" 完成! 平均训练 loss = {avg_train_loss:.4f}")
    
    # 验证阶段
    model.eval()
    val_loss = 0.0
    val_batch_count = 0
    total = correct = 0
    
    with torch.no_grad():
        for xb, yb in val_loader:
            out = model(xb)
            loss = criterion(out, yb)
            val_loss += loss.item()
            
            preds = out.argmax(1)
            total += yb.size(0)
            correct += (preds == yb).sum().item()
            val_batch_count += 1
    
    # 计算平均验证loss和准确率
    avg_val_loss = val_loss / val_batch_count if val_batch_count > 0 else 0
    acc = correct / total * 100 if total > 0 else 0
    
    # 更新学习率调度器
    scheduler.step(avg_val_loss)
    
    # 跟踪最佳模型
    is_best = ""
    if acc > best_val_acc:
        best_val_acc = acc
        is_best = "(最佳模型)"
    
    # 打印每个epoch的结果
    print(f"Epoch {epoch+1}/10 结果: "
          f"训练 Loss = {avg_train_loss:.4f}, "
          f"验证 Loss = {avg_val_loss:.4f}, "
          f"验证准确率 = {acc:.2f}%, "
          f"学习率 = {optimizer.param_groups[0]['lr']:.6f} {is_best}")

# ------------------ 6. 导出权重（控制器参数） ------------------
def export_weights():
    print("\n# -- 卷积层权重导出 --")
    # 修复：只导出模型中实际存在的卷积层
    for i, conv in enumerate([model.conv1, model.conv2], start=1):  # 移除model.conv3
        weight = conv.weight.detach().numpy()[:, 0, :].astype(int)
        for ch, row in enumerate(weight):
            print(f"p4.pipea.SwitchIngress_a.weight_tbl.add_with_weight_act(level = {i}, channel_index = {ch+1}, w1 = {row[0]}, w2 = {row[1]}, w3 = {row[2]}, w4 = 0)")

    print("\n# -- FC 偏置导出 (quanti_tbl_l4/l5) --")
    biases = [model.fc1.bias.detach().numpy(), model.fc2.bias.detach().numpy()]
    for level, b in zip([4, 5], biases):
        for i, v in enumerate(b):
            print(f"bias_l{level}{i+1} = {v:.4f}")

export_weights()