import os
import zipfile
import random
import tempfile
import shutil
import math

def calculate_walk_time(x1, y1, x2, y2):
    """计算两点间步行时间（向下取整的直线距离）"""
    distance = math.hypot(x2 - x1, y2 - y1)
    return int(math.floor(distance))

def compute_best_tour(n, spots):
    """
    计算最多能游览的景点数量和对应的最少总耗时
    spots格式: [(x, y, s, e, t), ...]
    返回值: (max_count, min_total_time)
    """
    if n == 0:
        return (0, 0)
    
    # 预处理步行时间
    # 从起点(0,0)到各景点的步行时间
    walk_from_start = [calculate_walk_time(0, 0, x, y) for x, y, _, _, _ in spots]
    
    # 各景点之间的步行时间
    walk_between = [[0]*n for _ in range(n)]
    for i in range(n):
        x1, y1, _, _, _ = spots[i]
        for j in range(n):
            if i != j:
                x2, y2, _, _, _ = spots[j]
                walk_between[i][j] = calculate_walk_time(x1, y1, x2, y2)
    
    # DP状态: (mask, last_idx) -> (last_time, total_time)
    # mask: 已游览景点的位掩码, last_idx: 最后游览的景点索引
    dp = {}
    
    # 初始化: 只游览单个景点
    for i in range(n):
        x, y, s, e, t = spots[i]
        d = walk_from_start[i]
        # 检查是否可以游览该景点
        if d >= s and d <= e - t:
            mask = 1 << i
            last_time = d + t
            total_time = d + t  # 步行时间+游览时间
            dp[(mask, i)] = (last_time, total_time)
    
    # 迭代扩展路径
    max_count = 0
    min_total = 0
    
    # 初始检查
    for (mask, idx) in dp:
        cnt = bin(mask).count('1')
        if cnt > max_count:
            max_count = cnt
            min_total = dp[(mask, idx)][1]
        elif cnt == max_count and dp[(mask, idx)][1] < min_total:
            min_total = dp[(mask, idx)][1]
    
    # 尝试扩展所有可能的路径
    changed = True
    while changed:
        changed = False
        new_dp = dp.copy()
        
        for (mask, last_idx) in dp:
            current_last_time, current_total = dp[(mask, last_idx)]
            current_count = bin(mask).count('1')
            
            # 尝试添加新的景点
            for j in range(n):
                if not (mask & (1 << j)):  # j未被游览
                    # 计算从last_idx到j的步行时间
                    walk_time = walk_between[last_idx][j]
                    arrival_time = current_last_time + walk_time
                    
                    # 获取j的时间信息
                    s_j, e_j, t_j = spots[j][2], spots[j][3], spots[j][4]
                    
                    # 检查是否可以游览j
                    if arrival_time >= s_j and arrival_time <= e_j - t_j:
                        new_mask = mask | (1 << j)
                        new_last_time = arrival_time + t_j
                        new_total = current_total + walk_time + t_j
                        new_state = (new_mask, j)
                        
                        # 更新状态
                        if new_state not in new_dp or new_total < new_dp[new_state][1]:
                            new_dp[new_state] = (new_last_time, new_total)
                            changed = True
                            
                            # 更新最大数量和最小耗时
                            new_count = current_count + 1
                            if new_count > max_count:
                                max_count = new_count
                                min_total = new_total
                            elif new_count == max_count and new_total < min_total:
                                min_total = new_total
        
        dp = new_dp
    
    return (max_count, min_total) if max_count > 0 else (0, 0)

def generate_test_case(case_num, special_case=None):
    """
    生成单个测试案例
    special_case: 特殊案例类型
                  'sample' - 样例案例
                  'single_spot' - 单个景点
                  'two_sequential' - 两个可连续游览的景点
                  'two_conflict' - 两个时间冲突的景点
                  'unreachable' - 所有景点都无法到达
                  'max_n' - 最大n值(15个景点)
                  'same_count' - 多个方案游览数量相同，选总耗时最少的
                  'just_in_time' - 刚好在时间限制内到达
    """
    n = 0
    spots = []
    
    if special_case == 'sample':
        # 样例输入
        n = 2
        spots = [
            (100, 0, 60, 180, 30),
            (0, 100, 30, 120, 20)
        ]
        
    elif special_case == 'single_spot':
        # 单个可游览的景点
        n = 1
        # 确保可以到达
        x, y = random.randint(0, 200), random.randint(0, 200)
        walk_time = calculate_walk_time(0, 0, x, y)
        s = random.randint(0, walk_time)
        e = walk_time + random.randint(30, 120)  # 确保e - t >= walk_time
        t = random.randint(1, min(60, e - walk_time))
        spots = [(x, y, s, e, t)]
        
    elif special_case == 'two_sequential':
        # 两个可连续游览的景点
        n = 2
        # 第一个景点
        x1, y1 = random.randint(0, 100), random.randint(0, 100)
        walk1 = calculate_walk_time(0, 0, x1, y1)
        s1 = random.randint(0, walk1)
        t1 = random.randint(10, 30)
        e1 = walk1 + t1 + random.randint(60, 120)  # 留出足够时间去第二个景点
        spots.append((x1, y1, s1, e1, t1))
        
        # 第二个景点，距离第一个不远
        x2, y2 = x1 + random.randint(-50, 50), y1 + random.randint(-50, 50)
        walk2 = calculate_walk_time(x1, y1, x2, y2)
        # 到达第二个景点的时间
        arrival2 = (walk1 + t1) + walk2
        s2 = random.randint(0, arrival2)
        t2 = random.randint(10, 30)
        e2 = arrival2 + t2 + random.randint(30, 60)
        spots.append((x2, y2, s2, e2, t2))
        
    elif special_case == 'two_conflict':
        # 两个时间冲突的景点，只能选一个
        n = 2
        # 第一个景点
        x1, y1 = random.randint(0, 100), random.randint(0, 100)
        walk1 = calculate_walk_time(0, 0, x1, y1)
        s1 = random.randint(0, walk1)
        t1 = random.randint(60, 120)
        e1 = walk1 + t1 + 30
        spots.append((x1, y1, s1, e1, t1))
        
        # 第二个景点，时间冲突
        x2, y2 = random.randint(150, 250), random.randint(150, 250)
        walk2 = calculate_walk_time(0, 0, x2, y2)
        s2 = random.randint(0, walk2)
        t2 = random.randint(60, 120)
        e2 = walk2 + t2 + 30
        spots.append((x2, y2, s2, e2, t2))
        
    elif special_case == 'unreachable':
        # 所有景点都无法到达
        n = random.randint(2, 5)
        for _ in range(n):
            x, y = random.randint(0, 200), random.randint(0, 200)
            walk_time = calculate_walk_time(0, 0, x, y)
            # 到达时间 > e-t，确保无法游览
            s = random.randint(0, 100)
            e = walk_time - random.randint(10, 30)  # e - t < walk_time（即使t=1）
            t = random.randint(1, 60)
            spots.append((x, y, s, e, t))
        
    elif special_case == 'max_n':
        # 最大n值(15个景点)
        n = 15
        spots = []
        for i in range(n):
            x, y = random.randint(0, 500), random.randint(0, 500)
            walk_time = calculate_walk_time(0, 0, x, y)
            s = random.randint(0, max(0, walk_time - 10)) if random.random() < 0.7 else random.randint(walk_time + 10, walk_time + 60)
            t = random.randint(1, 60)
            e = walk_time + t + random.randint(30, 240) if random.random() < 0.7 else walk_time - random.randint(10, 30)
            spots.append((x, y, s, e, t))
        
    elif special_case == 'same_count':
        # 多个方案游览数量相同，选总耗时最少的
        n = 3
        # 景点1和2可以组成一条路径，景点1和3可以组成另一条路径，数量都是2，但耗时不同
        x1, y1 = 0, 0
        walk1 = 0
        s1 = 0
        t1 = 10
        e1 = 1000
        spots.append((x1, y1, s1, e1, t1))
        
        # 景点2：距离近，耗时少
        x2, y2 = 10, 0
        walk2 = 10  # 从景点1到2的步行时间
        s2 = 20  # 景点1游览完是10，步行10分钟到达20
        t2 = 10
        e2 = 1000
        spots.append((x2, y2, s2, e2, t2))
        
        # 景点3：距离远，耗时长
        x3, y3 = 100, 0
        walk3 = 100  # 从景点1到3的步行时间
        s3 = 120  # 10+100=110到达，s3=120需要等待10分钟
        t3 = 10
        e3 = 1000
        spots.append((x3, y3, s3, e3, t3))
        
    elif special_case == 'just_in_time':
        # 刚好在时间限制内到达
        n = 1
        x, y = 100, 0
        walk_time = 100  # 步行时间正好100
        s = 100  # 到达时间正好等于s
        t = 30
        e = 130  # e - t = 100，到达时间正好等于e - t
        spots.append((x, y, s, e, t))
        
    else:
        # 随机生成案例
        n = random.randint(1, 15)
        spots = []
        for _ in range(n):
            x = random.randint(0, 500)
            y = random.randint(0, 500)
            s = random.randint(0, 1000)
            e = random.randint(s + 30, 1440)
            t = random.randint(1, min(60, e - s))
            spots.append((x, y, s, e, t))
    
    # 生成输入数据
    input_lines = [str(n)]
    for spot in spots:
        x, y, s, e, t = spot
        input_lines.append(f"{x} {y} {s} {e} {t}")
    input_data = "\n".join(input_lines)
    
    # 计算输出数据
    max_count, min_total = compute_best_tour(n, spots)
    output_data = f"{max_count} {min_total}"
    
    # 格式化文件名
    filename = f"{case_num:03d}"
    
    return filename, input_data, output_data

def generate_all_test_cases(num_cases=20):
    """生成所有测试案例"""
    test_cases = []
    
    # 特殊案例
    test_cases.append(generate_test_case(1, 'sample'))         # 样例案例
    test_cases.append(generate_test_case(2, 'single_spot'))    # 单个景点
    test_cases.append(generate_test_case(3, 'two_sequential')) # 两个可连续游览的景点
    test_cases.append(generate_test_case(4, 'two_conflict'))   # 两个时间冲突的景点
    test_cases.append(generate_test_case(5, 'unreachable'))    # 所有景点都无法到达
    test_cases.append(generate_test_case(6, 'max_n'))          # 最大n值
    test_cases.append(generate_test_case(7, 'same_count'))     # 相同数量选耗时少的
    test_cases.append(generate_test_case(8, 'just_in_time'))   # 刚好在时间限制内到达
    
    # 随机生成其他案例
    for i in range(9, num_cases + 1):
        test_cases.append(generate_test_case(i))
    
    return test_cases

def save_test_cases(test_cases, output_dir):
    """保存测试案例到文件"""
    for filename, input_data, output_data in test_cases:
        with open(os.path.join(output_dir, f"{filename}.in"), "w", encoding="utf-8") as f:
            f.write(input_data)
        with open(os.path.join(output_dir, f"{filename}.out"), "w", encoding="utf-8") as f:
            f.write(output_data)

def create_zip_archive(input_dir, output_file):
    """创建ZIP压缩包"""
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith(('.in', '.out')):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=file)

def main():
    print("正在生成测试案例...")
    test_cases = generate_all_test_cases(20)
    
    temp_dir = tempfile.mkdtemp()
    try:
        print("正在保存测试案例...")
        save_test_cases(test_cases, temp_dir)
        
        output_zip = "historical_tour_testcases.zip"
        print(f"正在创建压缩包 {output_zip}...")
        create_zip_archive(temp_dir, output_zip)
        
        print("测试数据生成完成！")
        print(f"生成了 {len(test_cases)} 对测试文件，已打包到 {output_zip}")
        
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
    