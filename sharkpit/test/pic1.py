import matplotlib.pyplot as plt
import numpy as np

# 模拟数据（共24小时）
time_hours = np.arange(0, 25, 2)  # 步长为2，从0到24

branch_coverage_data = {
    "MPFuzz": np.array([0, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000]),
    "Peach-Parallel": np.array([0, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000]),
    "AFLNet-Parallel": np.array([0, 3000, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000, 4000, 4000]),
    "SPFuzz": np.array([0, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000]),
    "AFLTeam": np.array([0, 2500, 2800, 3000, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000])
}

# 绘图设置
plt.figure(figsize=(10, 6))

# 定义线条样式和标记
styles = {
    "MPFuzz": {"color": "red", "marker": "s", "linestyle": "-"},
    "Peach-Parallel": {"color": "black", "marker": "o", "linestyle": "--"},
    "AFLNet-Parallel": {"color": "green", "marker": "^", "linestyle": ":"},
    "SPFuzz": {"color": "orange", "marker": "*", "linestyle": "-."},
    "AFLTeam": {"color": "purple", "marker": "d", "linestyle": "-"}
}

for method, data in branch_coverage_data.items():
    plt.plot(time_hours, data, label=method, **styles[method])

# 添加图例（放在右下角）
plt.legend(loc="lower right")

# 设置坐标轴标签和标题
plt.xlabel("Time (hours)")
plt.ylabel("Branch Coverage")
plt.title("Branch Coverage Over Time")

# 设置x轴刻度为每2小时显示一次
plt.xticks(time_hours)

# 不显示网格线
plt.grid(False)

# 保存为PDF文件
plt.savefig("branch_coverage_plot.pdf", format='pdf', bbox_inches='tight')

# 显示图形
plt.show()