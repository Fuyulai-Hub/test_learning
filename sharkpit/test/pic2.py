import matplotlib.pyplot as plt
import numpy as np

# 定义文件路径映射
file_map = {
    # "MPFuzz": "/root/branch/mpfuzz_branch.txt",
    "Peach-Parallel": "/root/branch/peach_branch_bacnet_peach_bacnet-2025-05-27-10:08:18_7400",
    # "AFLNet-Parallel": "/root/branch/aflnet_parallel_branch.txt",
    # "SPFuzz": "/root/branch/spfuzz_branch.txt",
    # "AFLTeam": "/root/branch/aflteam_branch.txt"
}

# 处理数据文件的函数
def process_file(file_path):
    minutes = []
    branches = []
    
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                try:
                    time_min = int(parts[0].strip())
                    branch_count = int(parts[1].strip())
                    minutes.append(time_min)
                    branches.append(branch_count)
                except ValueError:
                    continue  # 忽略格式错误的行
    
    # 如果文件为空，返回全0数组
    if not minutes:
        return np.zeros(13)
    
    # 目标时间点（每2小时对应的分钟数）
    target_minutes = [0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440]
    results = []
    last_value = 0
    idx = 0
    
    for t in target_minutes:
        # 推进索引到当前目标时间点
        while idx < len(minutes) and minutes[idx] <= t:
            last_value = branches[idx]
            idx += 1
        results.append(last_value)
    
    return np.array(results)

# 处理所有文件数据
branch_coverage_data = {}
for method, file_path in file_map.items():
    branch_coverage_data[method] = process_file(file_path)

# 时间轴（小时）
time_hours = np.arange(0, 25, 2)  # 0,2,4,...,24

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

# 绘制每条线
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
plt.savefig("branch_coverage_plot1.pdf", format='pdf', bbox_inches='tight')

# 显示图形
plt.show()