import matplotlib.pyplot as plt

# # 数据输入
# data = [
#     (0, 3343),
#     (1, 7707),
#     (2, 7810),
#     (6613, 8647),
#     (6652, 8649),
#     (11417, 8667),
#     (11418, 8719),
#     (11419, 8776),
#     (11422, 8789),
#     (11424, 8800),
#     (11430, 8806),
#     (11446, 8809),
#     (11449, 8810),
#     (11471, 8811),
#     (13054, 8812),
#     (31618, 8813),
# ]

# with open('/root/branch/peach_branch_bacnet_peach_bacnet-2025-05-27-10:08:18_7400', 'r') as f:
#     data = [tuple(map(int, line.strip().split())) for line in f if line.strip()]
# with open('/root/branch/peach_branch_bacnet_peach_bacnet-2025-05-27-10:08:18_7400', 'r') as f:
#     # 添加逗号分割处理
#     data = [tuple(map(int, item.strip() for item in line.strip().replace(',', ' ').split())) 
#             for line in f if line.strip()]
with open('/root/branch/peach_branch_bacnet_peach_bacnet-2025-05-27-10:08:18_7400', 'r') as f:
    # 修正括号问题并优化解析逻辑
    data = [tuple(map(int, line.strip().replace(',', ' ').split()))
            for line in f if line.strip()]

# 分离 x 和 y 值
x = [point[0] for point in data]
y = [point[1] for point in data]

# 设置字体和样式
# 修改字体设置为Linux系统常用字体
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']  # Linux系统普遍包含的字体
plt.rcParams['font.size'] = 10
plt.rcParams['lines.markersize'] = 4
plt.rcParams['lines.linewidth'] = 1.5

# 创建图表
fig, ax = plt.subplots(figsize=(6, 4))

# 绘制折线图
ax.plot(x, y, color='black', linestyle='-', marker='o', markevery=1)

# 设置坐标轴标签
ax.set_xlabel('Time(hours)', fontsize=10)
ax.set_ylabel('Covered Branches', fontsize=10)

# 设置网格
ax.grid(True, linestyle='--', alpha=0.5)

# 隐藏右上边框
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# 调整布局
fig.tight_layout()

# 保存为 PDF
plt.savefig('coverage_plot.pdf', format='pdf', dpi=300, bbox_inches='tight')