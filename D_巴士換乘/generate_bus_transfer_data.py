import os
import zipfile
import random
import tempfile
import shutil
from collections import defaultdict, deque

def calculate_min_transfers(routes, start, end):
    """计算从起点到终点的最少换乘次数"""
    if start == end:
        return 0
    
    # 构建站点到线路的映射
    station_to_routes = defaultdict(set)
    for route_idx, route in enumerate(routes):
        for station in route:
            station_to_routes[station].add(route_idx)
    
    # BFS求解最少换乘次数
    # 队列元素: (当前站点, 换乘次数, 已使用线路)
    visited = set()
    queue = deque()
    
    # 初始化：从起点可直接到达的所有线路
    for route_idx in station_to_routes[start]:
        queue.append((start, 0, route_idx))
        visited.add((start, route_idx))
    
    while queue:
        station, transfers, route_idx = queue.popleft()
        
        # 检查当前线路上的所有站点
        for s in routes[route_idx]:
            if s == end:
                return transfers
            
            # 如果没访问过这个站点和线路的组合
            if (s, route_idx) not in visited:
                visited.add((s, route_idx))
                queue.append((s, transfers, route_idx))
        
        # 尝试换乘到其他线路
        for other_route in station_to_routes[station]:
            if other_route != route_idx and (station, other_route) not in visited:
                visited.add((station, other_route))
                queue.append((station, transfers + 1, other_route))
    
    # 无法到达
    return -1

def generate_station_name(index):
    """生成站点名称，如A, B, ..., Z, AA, AB等"""
    name = ""
    while True:
        index -= 1
        name = chr(ord('A') + (index % 26)) + name
        index = index // 26
        if index == 0:
            break
    return name

def generate_test_case(case_num, special_case=None):
    """
    生成单个测试案例
    special_case: 特殊案例类型，None表示随机生成
                  'direct' - 无需换乘（同一线路）
                  'one_transfer' - 需要1次换乘
                  'multiple_transfers' - 需要多次换乘
                  'unreachable' - 无法到达
                  'same_station' - 起点终点相同
    """
    # 生成站点名称
    stations = [generate_station_name(i) for i in range(1, 50)]  # 生成49个站点
    
    k = 0  # 路线数
    routes = []  # 路线列表
    start = ""
    end = ""
    
    if special_case == 'direct':
        # 无需换乘（同一线路）
        k = random.randint(2, 5)
        # 第一条线路包含起点和终点
        t = random.randint(5, 15)
        route1 = random.sample(stations, t)
        start_idx = random.randint(0, t-2)
        end_idx = random.randint(start_idx+1, t-1)
        start = route1[start_idx]
        end = route1[end_idx]
        routes.append(route1)
        
        # 添加其他线路
        for _ in range(k-1):
            t = random.randint(2, 10)
            route = random.sample(stations, t)
            routes.append(route)
            
    elif special_case == 'one_transfer':
        # 需要1次换乘
        k = 2
        # 第一条线路
        t1 = random.randint(3, 10)
        route1 = random.sample(stations, t1)
        # 第二条线路，与第一条线路有一个共同站点
        common_idx1 = random.randint(0, t1-1)
        common_station = route1[common_idx1]
        t2 = random.randint(3, 10)
        route2 = [common_station]
        route2 += random.sample([s for s in stations if s not in route1 or s == common_station], t2-1)
        
        # 选择起点和终点
        start = random.choice([s for s in route1 if s != common_station])
        end = random.choice([s for s in route2 if s != common_station])
        
        routes = [route1, route2]
        
    elif special_case == 'multiple_transfers':
        # 需要多次换乘（2-3次）
        k = random.randint(3, 5)
        routes = []
        prev_route = None
        
        # 生成相互连接的线路
        for i in range(k):
            if i == 0:
                # 第一条线路
                t = random.randint(3, 10)
                route = random.sample(stations, t)
                routes.append(route)
                prev_route = route
            else:
                # 后续线路与前一条线路有一个共同站点
                common_station = random.choice(prev_route)
                t = random.randint(3, 10)
                route = [common_station]
                route += random.sample([s for s in stations if s not in prev_route or s == common_station], t-1)
                routes.append(route)
                prev_route = route
        
        # 选择需要多次换乘的起点和终点
        start = random.choice(routes[0])
        end = random.choice(routes[-1])
        # 确保起点和终点不在同一条线路上
        while any(start in route and end in route for route in routes):
            start = random.choice(routes[0])
            end = random.choice(routes[-1])
            
    elif special_case == 'unreachable':
        # 无法到达
        k = 2
        # 两条完全不相交的线路
        t1 = random.randint(3, 10)
        route1 = random.sample(stations, t1)
        t2 = random.randint(3, 10)
        route2 = random.sample([s for s in stations if s not in route1], t2)
        
        start = random.choice(route1)
        end = random.choice(route2)
        
        routes = [route1, route2]
        
    elif special_case == 'same_station':
        # 起点终点相同
        k = random.randint(1, 5)
        routes = []
        for _ in range(k):
            t = random.randint(2, 10)
            route = random.sample(stations, t)
            routes.append(route)
        
        # 选择一个在某个线路上的站点作为起点和终点
        start = random.choice(routes[0])
        end = start
        
    else:
        # 随机生成
        k = random.randint(1, 10)
        routes = []
        for _ in range(k):
            t = random.randint(2, 20)
            route = random.sample(stations, t)
            routes.append(route)
        
        # 随机选择起点和终点
        all_stations = set()
        for route in routes:
            all_stations.update(route)
        start, end = random.sample(list(all_stations), 2)
    
    # 生成输入数据
    input_lines = [str(k)]
    for route in routes:
        t = len(route)
        input_lines.append(f"{t} {' '.join(route)}")
    input_lines.append(f"{start} {end}")
    input_data = "\n".join(input_lines)
    
    # 计算输出数据
    output_data = str(calculate_min_transfers(routes, start, end))
    
    # 格式化文件名，确保至少3位数字
    filename = f"{case_num:03d}"
    
    return filename, input_data, output_data

def generate_all_test_cases(num_cases=10):
    """生成所有测试案例"""
    test_cases = []
    
    # 特殊案例
    test_cases.append(generate_test_case(1, 'direct'))             # 无需换乘
    test_cases.append(generate_test_case(2, 'one_transfer'))       # 1次换乘
    test_cases.append(generate_test_case(3, 'multiple_transfers')) # 多次换乘
    test_cases.append(generate_test_case(4, 'unreachable'))        # 无法到达
    test_cases.append(generate_test_case(5, 'same_station'))       # 起点终点相同
    test_cases.append(generate_test_case(6, 'direct'))             # 另一个无需换乘的案例
    test_cases.append(generate_test_case(7, 'one_transfer'))       # 另一个1次换乘的案例
    
    # 随机生成其他案例
    for i in range(8, num_cases + 1):
        test_cases.append(generate_test_case(i))
    
    return test_cases

def save_test_cases(test_cases, output_dir):
    """保存测试案例到文件"""
    for filename, input_data, output_data in test_cases:
        # 保存输入文件
        with open(os.path.join(output_dir, f"{filename}.in"), "w", encoding="utf-8") as f:
            f.write(input_data)
        
        # 保存输出文件
        with open(os.path.join(output_dir, f"{filename}.out"), "w", encoding="utf-8") as f:
            f.write(output_data)

def create_zip_archive(input_dir, output_file):
    """创建ZIP压缩包"""
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                # 只添加.in和.out文件
                if file.endswith(('.in', '.out')):
                    file_path = os.path.join(root, file)
                    # 不保留目录结构，直接添加文件到zip根目录
                    zipf.write(file_path, arcname=file)

def main():
    # 生成测试案例
    print("正在生成测试案例...")
    test_cases = generate_all_test_cases(20)  # 生成20个测试案例
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    try:
        # 保存测试案例
        print("正在保存测试案例...")
        save_test_cases(test_cases, temp_dir)
        
        # 创建ZIP压缩包
        output_zip = "bus_transfer_testcases.zip"
        print(f"正在创建压缩包 {output_zip}...")
        create_zip_archive(temp_dir, output_zip)
        
        print("测试数据生成完成！")
        print(f"生成了 {len(test_cases)} 对测试文件，已打包到 {output_zip}")
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
    