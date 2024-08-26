import pandas as pd

import statsmodels.api as sm

# 数据集
data = {

    'Year': list(range(1991, 2002)),

    'Y': [137.16, 124.56, 107.91, 102.96, 125.24, 162.45, 217.43, 253.42, 251.07, 285.85, 327.26],

    'X1': [1181.4, 1375.7, 1501.2, 1700.6, 2026.6, 2577.4, 3496.2, 4283.0, 4838.9, 5160.3, 5425.1],

    'X2': [115.96, 133.35, 128.21, 124.85, 122.49, 129.86, 139.52, 140.44, 139.12, 133.35, 126.39]

}
# 转换成 pandas DataFrame

df = pd.DataFrame(data)

# 定义自变量和因变量

X = df[['X1', 'X2']]  # 自变量

Y = df['Y']  # 因变量

# 加入常数列以进行截距的计算

X = sm.add_constant(X)

# 建立多元回归模型

model = sm.OLS(Y, X).fit()


# 输出回归模型的详细摘要

model_summary = model.summary()

model_summary