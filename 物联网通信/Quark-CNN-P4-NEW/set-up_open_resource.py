#!/usr/bin/env python3

import json
import sys
import random
from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI

# 连接到 BMv2 交换机
controller = SimpleSwitchThriftAPI(9090)  # 默认端口

# 清空所有表项
controller.table_clear("MyIngress.quanti_tbl")
controller.table_clear("MyIngress.quanti_tbl_2")
controller.table_clear("MyIngress.quanti_tbl_l4")
controller.table_clear("MyIngress.quanti_tbl_l5")
controller.table_clear("MyIngress.weight_tbl")
controller.table_clear("MyIngress.add_wei_l1_tbl")
controller.table_clear("MyIngress.get_level_1_tbl")
controller.table_clear("MyIngress.get_level_2_tbl")
controller.table_clear("MyIngress.get_level_3_tbl")
controller.table_clear("MyIngress.get_level_5_tbl")
controller.table_clear("MyIngress.add_multi_l1_tbl")
controller.table_clear("MyIngress.add_multi_l5_tbl")
controller.table_clear("MyIngress.add_multi_tbl")
controller.table_clear("MyIngress.multi_tbl_1")
controller.table_clear("MyIngress.multi_tbl_2")
controller.table_clear("MyIngress.maxpooling_tbl")
controller.table_clear("MyIngress.compare_ret_tbl")
controller.table_clear("MyIngress.bias_tbl")

# ========== 使用提供的具体权重数据替换随机初始化 ==========

# 卷积层权重 (Level 1-3)
conv_weights = {
    # Level 1
    (1, 1): [123, -31, 82, 0],
    (1, 2): [-51, 20, 10, 0],
    (1, 3): [72, -10, 51, 0],
    (1, 4): [0, 0, -41, 0],
    
    # Level 2
    (2, 1): [31, 61, -20, 0],
    (2, 2): [-10, 20, 31, 0],
    (2, 3): [51, -41, -10, 0],
    (2, 4): [61, 20, 0, 0],
    
    # Level 3
    (3, 1): [10, -10, 20, 0],
    (3, 2): [0, 10, -10, 0],
    (3, 3): [20, -31, 41, 0],
    (3, 4): [31, 0, -20, 0],
}

# FC层偏置 (Level 4-5)
fc_biases = {
    # Level 4
    (4, 1): 123,
    (4, 2): -61,
    (4, 3): 41,
    (4, 4): -31,
    
    # Level 5
    (5, 1): -20,
    (5, 2): 51,
    (5, 3): 101,
    (5, 4): -101,
}

# 添加权重表项
for (level, ch_idx), weights in conv_weights.items():
    controller.table_add(
        "MyIngress.weight_tbl",
        "weight_act",
        [str(level), str(ch_idx)],
        [str(w) for w in weights]
    )

# 添加偏置表项
for (level, ch_idx), bias in fc_biases.items():
    controller.table_add(
        "MyIngress.bias_tbl",
        "bias_act",
        [str(level), str(ch_idx)],
        [str(bias)]
    )



# Level 1 表项 - 修正版
controller.table_add("MyIngress.get_level_1_tbl", "write_ab_1", ["1", "1"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_ab_2", ["1", "2"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_ab_3", ["1", "3"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_ab_4", ["1", "4"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_cd_1", ["2", "1"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_cd_2", ["2", "2"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_cd_3", ["2", "3"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_cd_4", ["2", "4"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_ef_1", ["3", "1"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_ef_2", ["3", "2"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_ef_3", ["3", "3"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_ef_4", ["3", "4"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_gh_1", ["4", "1"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_gh_2", ["4", "2"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_gh_3", ["4", "3"], [])
controller.table_add("MyIngress.get_level_1_tbl", "write_gh_4", ["4", "4"], [])

controller.table_add("MyIngress.get_level_2_tbl", "write_abcd_1", ["1", "1"], [])
controller.table_add("MyIngress.get_level_2_tbl", "write_abcd_2", ["1", "2"], [])
controller.table_add("MyIngress.get_level_2_tbl", "write_abcd_3", ["1", "3"], [])
controller.table_add("MyIngress.get_level_2_tbl", "write_abcd_4", ["1", "4"], [])
controller.table_add("MyIngress.get_level_2_tbl", "write_ab_1", ["2", "1"], [])
controller.table_add("MyIngress.get_level_2_tbl", "write_ab_2", ["2", "2"], [])
controller.table_add("MyIngress.get_level_2_tbl", "write_ab_3", ["2", "3"], [])
controller.table_add("MyIngress.get_level_2_tbl", "write_ab_4", ["2", "4"], [])

# Level 3 表项 - 修正版
controller.table_add("MyIngress.get_level_3_tbl", "write_cd_1", ["3", "1"], [])
controller.table_add("MyIngress.get_level_3_tbl", "write_cd_2", ["3", "2"], [])
controller.table_add("MyIngress.get_level_3_tbl", "write_cd_3", ["3", "3"], [])
controller.table_add("MyIngress.get_level_3_tbl", "write_cd_4", ["3", "4"], [])
controller.table_add("MyIngress.get_level_3_tbl", "write_ab_1", ["4", "1"], [])
controller.table_add("MyIngress.get_level_3_tbl", "write_ab_2", ["4", "2"], [])
controller.table_add("MyIngress.get_level_3_tbl", "write_ab_3", ["4", "3"], [])
controller.table_add("MyIngress.get_level_3_tbl", "write_ab_4", ["4", "4"], [])

# Level 5 表项
for i in range(1, 16):
    if i <= 4:
        action = "write_cd_" + str(i)
    elif i <= 8:
        action = "write_ef_" + str(i-4)
    elif i <= 12:
        action = "write_gh_" + str(i-8)
    else:
        action = "write_abcd_" + str(i-12)
    controller.table_add("MyIngress.get_level_5_tbl", action, [], [str(i)])

# 权重相关表项
for i in range(1, 5):
    controller.table_add("MyIngress.add_wei_l1_tbl", f"add_wei_action_l1_{i}", [str(i)], [])
    controller.table_add("MyIngress.add_multi_l1_tbl", f"add_multi_action_l1_{i}", [str(i)], [])

# 多层处理表项
controller.table_add("MyIngress.add_multi_l5_tbl", "add_multi_action_l4_1", ["4", "0"], [])
controller.table_add("MyIngress.add_multi_l5_tbl", "add_multi_action_l4_2", ["4", "2"], [])
controller.table_add("MyIngress.add_multi_l5_tbl", "add_multi_action_l5_1", ["5", "0"], [])
controller.table_add("MyIngress.add_multi_l5_tbl", "add_multi_action_l5_2", ["5", "2"], [])

# 多重操作表项
controller.table_add("MyIngress.add_multi_tbl", "add_multi_action_abcd_1", ["2", "1", "0"], [])
controller.table_add("MyIngress.add_multi_tbl", "add_multi_action_abcd_2", ["2", "1", "1"], [])
controller.table_add("MyIngress.add_multi_tbl", "add_multi_action_abcd_3", ["2", "1", "2"], [])
controller.table_add("MyIngress.add_multi_tbl", "add_multi_action_abcd_4", ["2", "1", "3"], [])

controller.table_add("MyIngress.add_multi_tbl", "add_multi_action_efgh_1", ["2", "2", "0"], [])
controller.table_add("MyIngress.add_multi_tbl", "add_multi_action_efgh_2", ["2", "2", "1"], [])
controller.table_add("MyIngress.add_multi_tbl", "add_multi_action_efgh_3", ["2", "2", "2"], [])
controller.table_add("MyIngress.add_multi_tbl", "add_multi_action_efgh_4", ["2", "2", "3"], [])

controller.table_add("MyIngress.add_multi_tbl", "add_multi_action_ababcd_1", ["3", "1", "0"], [])
controller.table_add("MyIngress.add_multi_tbl", "add_multi_action_ababcd_2", ["3", "1", "1"], [])
controller.table_add("MyIngress.add_multi_tbl", "add_multi_action_ababcd_3", ["3", "1", "2"], [])
controller.table_add("MyIngress.add_multi_tbl", "add_multi_action_ababcd_4", ["3", "1", "3"], [])

# 乘法表项
for i in range(-128, 128):
    for j in range(-128, 128):
        tmp = i * j
        j_d = j if j >= 0 else j + 256
        i_d = i if i >= 0 else i + 256
        tmp_d = tmp if tmp >= 0 else tmp + 65536
        controller.table_add("MyIngress.multi_tbl_1", "multi_act_1", [str(i_d), str(j_d)], [str(tmp_d)])
        controller.table_add("MyIngress.multi_tbl_2", "multi_act_2", [str(i_d), str(j_d)], [str(tmp_d)])

# 最大池化表项
for i in range(128):
    for j in range(i):
        controller.table_add("MyIngress.maxpooling_tbl", "smaller", [str(j), str(i)], [])
        controller.table_add("MyIngress.compare_ret_tbl", "ret_greater", [str(i)], [str(j)])

# 量化函数（不带bias）
def multiply_and_clip_with_constant(M):
    result = []
    for res in range(-128, 128):
        res_t = res + 0.5
        val = res_t / M
        val = int(val)
        result.append(val)
    result.append(32767)
    return result

# 量化函数（带bias）
def multiply_and_clip_with_constant_with_bias(M, bias):
    result = []
    for res in range(-128, 128):
        res_t = res + 0.5
        val = res_t / M - bias
        val = int(val)
        result.append(val)
    result.append(32767)
    return result

# 量化参数（需要填入实际值）
M_1 = 1024
M_2 = 1024
M_3 = 1024
M_4 = 1024
M_5 = 1024

# FC1（level 4）的 bias 参数（模拟中心偏移）
bias_41 = 123
bias_42 = -61
bias_43 = 41
bias_44 = -31

# FC2（level 5）的 bias 参数（输出层，一般靠近 0）
bias_51 = -20
bias_52 = 51
bias_53 = 101
bias_54 = -101

# 添加量化表项（Level 1-3，不带bias）
for level, M in enumerate([M_1, M_2, M_3], 1):
    result = multiply_and_clip_with_constant(M)
    print(f"Level {level} result: {result}")
    for i in range(1, len(result)):
        for j in range(result[i-1]+1, result[i]+1):
            j_d = j if j >= 0 else j + 65536
            controller.table_add("MyIngress.quanti_tbl", "quanti_act", [str(j_d), str(level)], [str(i-128)])
            controller.table_add("MyIngress.quanti_tbl_2", "quanti_act_2", [str(j_d), str(level)], [str(i-128)])

# 添加 Level 4 量化表项（带bias）
result1 = multiply_and_clip_with_constant_with_bias(M_4, bias_41)
result2 = multiply_and_clip_with_constant_with_bias(M_4, bias_42)
result3 = multiply_and_clip_with_constant_with_bias(M_4, bias_43)
result4 = multiply_and_clip_with_constant_with_bias(M_4, bias_44)

for channel, result in enumerate([result1, result2, result3, result4], 1):
    for i in range(1, len(result)):
        for j in range(result[i-1]+1, result[i]+1):
            j_d = j if j >= 0 else j + 65536
            controller.table_add("MyIngress.quanti_tbl_l4", "quanti_act_l4", [str(j_d), str(channel)], [str(i-128)])

# 添加 Level 5 量化表项（带bias）
result1 = multiply_and_clip_with_constant_with_bias(M_5, bias_51)
result2 = multiply_and_clip_with_constant_with_bias(M_5, bias_52)
result3 = multiply_and_clip_with_constant_with_bias(M_5, bias_53)
result4 = multiply_and_clip_with_constant_with_bias(M_5, bias_54)

for channel, result in enumerate([result1, result2, result3, result4], 1):
    for i in range(1, len(result)):
        for j in range(result[i-1]+1, result[i]+1):
            j_d = j if j >= 0 else j + 65536
            controller.table_add("MyIngress.quanti_tbl_l5", "quanti_act_l4", [str(j_d), str(channel)], [str(i-128)])

print("BMv2 表项配置完成")



