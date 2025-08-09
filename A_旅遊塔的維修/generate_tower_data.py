import os
import zipfile
import random
import tempfile
import shutil

def calculate_final_height(operations):
    """根据操作序列计算最终高度"""
    height = 0
    max_height = 338  # 旅游塔最大高度
    
    for op, num in operations:
        if op == 'U':
            height += num
            # 不能超过最大高度
            if height > max_height:
                height = max_height
        elif op == 'D':
            height -= num
            # 不能低于地面(0)
            if height < 0:
                height = 0
                
    return height

def generate_test_case(case_num, m, special_case=None):
    """
    生成单个测试案例
    special_case: 特殊案例类型，None表示随机生成
                  'max_up' - 全部上爬操作，最终达到338
                  'max_down' - 全部下滑操作
                  'exceed_max' - 尝试超过最大高度
                  'reach_zero' - 尝试下落到0以下
    """
    operations = []
    
    if special_case == 'max_up':
        # 全部上爬操作，最终达到338
        remaining = 338
        for i in range(m):
            if i == m - 1:
                # 最后一步刚好到达338
                h = remaining if remaining > 0 else 1
            else:
                if remaining <= 0:
                    continue
                h = random.randint(1, min(100, remaining))
            operations.append(('U', h))
            remaining -= h
            if remaining <= 0:
                remaining = 0
                
    elif special_case == 'max_down':
        # 先上爬再全部下滑
        if m > 1:
            # 第一步先上爬一些
            h = random.randint(1, 100)
            operations.append(('U', h))
            # 剩下的步骤都下滑
            for _ in range(m - 1):
                if h <= 0:
                    continue
                s = random.randint(1, min(100, h))
                operations.append(('D', s))
                h -= s
        else:
            # 只有一步操作，只能上爬
            operations.append(('U', random.randint(1, 100)))
            
    elif special_case == 'exceed_max':
        # 尝试超过最大高度
        current = 0
        for i in range(m):
            if current < 338 and random.random() < 0.7:
                # 上爬
                add = random.randint(1, 100)
                operations.append(('U', add))
                current += add
                if current > 338:
                    current = 338
            else:
                # 下滑
                sub = random.randint(1, min(100, current))
                operations.append(('D', sub))
                current -= sub
                
    elif special_case == 'reach_zero':
        # 尝试下落到0以下
        current = random.randint(50, 100)  # 初始先上爬一些
        operations.append(('U', current))
        
        for _ in range(m - 1):
            if random.random() < 0.6:
                # 下滑，可能会尝试滑到0以下
                sub = random.randint(1, current + 50)  # 可能超过当前高度
                operations.append(('D', sub))
                current = max(0, current - sub)
            else:
                # 上爬
                add = random.randint(1, 100)
                operations.append(('U', add))
                current += add
                if current > 338:
                    current = 338
                    
    else:
        # 随机生成操作
        current = 0
        for _ in range(m):
            # 决定是上爬还是下滑
            if current == 0:
                # 当前在地面，只能上爬
                op = 'U'
            else:
                op = random.choice(['U', 'D'])
                
            if op == 'U':
                # 上爬
                max_possible = 338 - current
                h = random.randint(1, min(100, max_possible + 50))  # 可能超过最大高度
                operations.append(('U', h))
                current += h
                if current > 338:
                    current = 338
            else:
                # 下滑
                s = random.randint(1, min(100, current + 50))  # 可能超过当前高度
                operations.append(('D', s))
                current = max(0, current - s)
    
    # 生成输入数据
    input_lines = [str(m)]
    for op, num in operations:
        input_lines.append(f"{op} {num}")
    input_data = "\n".join(input_lines)
    
    # 计算输出数据
    output_data = str(calculate_final_height(operations))
    
    # 格式化文件名，确保至少3位数字
    filename = f"{case_num:03d}"
    
    return filename, input_data, output_data

def generate_all_test_cases(num_cases=10):
    """生成所有测试案例"""
    test_cases = []
    
    # 特殊案例
    test_cases.append(generate_test_case(1, 1, 'max_up'))  # 1次操作，上爬
    test_cases.append(generate_test_case(2, 100, 'max_up'))  # 最大操作次数，上爬至338
    test_cases.append(generate_test_case(3, 50, 'max_down'))  # 以上爬开始，然后下滑
    test_cases.append(generate_test_case(4, 30, 'exceed_max'))  # 尝试超过最大高度
    test_cases.append(generate_test_case(5, 20, 'reach_zero'))  # 尝试下落到0以下
    
    # 边界案例：刚好达到338
    test_cases.append(generate_test_case(6, 2))  # 两次操作刚好达到338
    # 边界案例：刚好为0
    test_cases.append(generate_test_case(7, 5))  # 多次操作后回到0
    
    # 随机生成其他案例
    for i in range(8, num_cases + 1):
        m = random.randint(1, 100)  # 操作次数在1到100之间
        test_cases.append(generate_test_case(i, m))
    
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
        output_zip = "tower_maintenance_testcases.zip"
        print(f"正在创建压缩包 {output_zip}...")
        create_zip_archive(temp_dir, output_zip)
        
        print("测试数据生成完成！")
        print(f"生成了 {len(test_cases)} 对测试文件，已打包到 {output_zip}")
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
    