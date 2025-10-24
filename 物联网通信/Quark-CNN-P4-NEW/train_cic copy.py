# -*- coding: utf-8 -*-
"""
Quark-CNN - Paper-Aligned Training Script
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader

# === 超参数配置 ===
BASE_DIR = r"C:\Xing\大三下\物联网通信\Quark-CNN-P4\MachineLearningCSV\MachineLearningCVE"
SELECTED_COLS = [
    'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
    'Total Length of Fwd Packets', 'Total Length of Bwd Packets',
    'Fwd Packet Length Mean', 'Bwd Packet Length Mean', 'Flow IAT Mean'
]
MAX_ROWS = 20000
BATCH_SIZE = 128
EPOCHS = 1
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# === 数据加载 ===
def load_all_csvs(base_dir):
    all_data = []
    for file in os.listdir(base_dir):
        if file.endswith(".csv"):
            path = os.path.join(base_dir, file)
            print(f"加载: {path}")
            try:
                df = pd.read_csv(path, low_memory=False, nrows=MAX_ROWS)
                df.columns = df.columns.str.strip()
                all_data.append(df)
            except Exception as e:
                print(f"读取失败: {e}")
    return pd.concat(all_data, ignore_index=True)

df = load_all_csvs(BASE_DIR)
missing = [c for c in SELECTED_COLS + ['Label'] if c not in df.columns]
if missing:
    print(f"❌ 缺失字段: {missing}")
    exit()

df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=SELECTED_COLS + ['Label'])
X = df[SELECTED_COLS].astype(float)
y = df['Label'].apply(lambda x: 0 if 'Benign' in str(x) else 1)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === 划分数据集 ===
X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
X_train = torch.tensor(X_train[:, :, None], dtype=torch.float32).to(DEVICE)
X_val = torch.tensor(X_val[:, :, None], dtype=torch.float32).to(DEVICE)
y_train = torch.tensor(y_train.values, dtype=torch.long).to(DEVICE)
y_val = torch.tensor(y_val.values, dtype=torch.long).to(DEVICE)

train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=BATCH_SIZE)

# === CNN 模型定义（完全对齐论文结构） ===
class QuarkCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 4, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(4, 4, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool1d(2)
        self.conv3 = nn.Conv1d(4, 4, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool1d(2)
        self.fc1 = nn.Linear(4 * 1, 4)
        self.fc2 = nn.Linear(4, 4)  # 原论文为 4 输出（映射到 bias_l51~l54）

    def forward(self, x):
        x = x.permute(0, 2, 1)
        x = self.pool1(F.relu(self.conv1(x)))
        x = self.pool2(F.relu(self.conv2(x)))
        x = self.pool3(F.relu(self.conv3(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return self.fc2(x)

# === 训练 ===
model = QuarkCNN().to(DEVICE)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0
    for i, (xb, yb) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(xb)
        loss = criterion(output, yb)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    avg_loss = running_loss / len(train_loader)
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for xb, yb in val_loader:
            preds = model(xb).argmax(1)
            correct += (preds == yb).sum().item()
            total += yb.size(0)
    acc = correct / total * 100
    print(f"[Epoch {epoch+1}] Loss: {avg_loss:.4f}, Val Acc: {acc:.2f}%")

torch.save(model.state_dict(), "cnn_model_paper.pt")

# === 导出参数：卷积权重 + 偏置 ===
print("\n# === 权重导出（写入 P4 表项） ===")
for i, conv in enumerate([model.conv1, model.conv2, model.conv3], start=1):
    weight = conv.weight.detach().cpu().numpy()[:, 0, :].astype(int)
    for ch, row in enumerate(weight):
        print(f"p4.pipea.SwitchIngress_a.weight_tbl.add_with_weight_act(level={i}, channel_index={ch+1}, w1={row[0]}, w2={row[1]}, w3={row[2]}, w4=0)")

print("\n# === 偏置导出 ===")
for level, b in zip([4, 5], [model.fc1.bias.detach().cpu().numpy(), model.fc2.bias.detach().cpu().numpy()]):
    for i, v in enumerate(b):
        print(f"bias_l{level}{i+1} = {v:.4f}")
