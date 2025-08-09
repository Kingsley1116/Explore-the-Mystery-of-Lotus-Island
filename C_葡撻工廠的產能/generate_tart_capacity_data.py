import os
import zipfile
import random
import tempfile
import shutil

def calculate_max_tarts(A, B, C):
    """计算当前材料能制作的最大葡挞数量"""
    flour_tarts = A // 30
    egg_tarts = B // 2
    milk_tarts = C // 50
    return min(flour_tarts, egg_tarts, milk_tarts)

def find_best_purchase(A, B, C, k, x):
    """
    寻找最佳采购方案，返回k天后能制作的最多葡挞数量
    使用贪心算法：每次采购最能提高产能的材料
    """
    a, b, c = A, B, C
    
    for _ in range(k):
        # 计算当前每种材料能制作的葡挞数量
        flour_tarts = a // 30
        egg_tarts = b // 2
        milk_tarts = c // 50
        
        current_min = min(flour_tarts, egg_tarts, milk_tarts)
        
        # 计算采购每种材料后的最小产能
        if flour_tarts == current_min:
            a += x
            
        elif egg_tarts == current_min:
            b += x
            
        elif milk_tarts == current_min:
            c += x
    
    # 返回最终能制作的葡挞数量
    return calculate_max_tarts(a, b, c)

def generate_test_case(case_num, special_case=None):
    """
    生成单个测试案例
    special_case: 特殊案例类型，None表示随机生成
                  'no_improve' - 采购无法提高产能
                  'flour_bottleneck' - 面粉始终是瓶颈
                  'egg_bottleneck' - 鸡蛋始终是瓶颈
                  'milk_bottleneck' - 牛奶始终是瓶颈
                  'max_k' - 最大采购天数
                  'max_x' - 最大单次采购量
    """
    A, B, C, k, x = 0, 0, 0, 0, 0
    
    if special_case == 'no_improve':
        # 采购无法提高产能（所有材料都很充足）
        base = random.randint(50, 100)
        A = base * 30
        B = base * 2
        C = base * 50
        k = random.randint(1, 100)
        x = random.randint(1, 100)
        
    elif special_case == 'flour_bottleneck':
        # 面粉始终是瓶颈
        flour_base = random.randint(10, 50)
        A = flour_base * 30
        # 其他材料充足
        B = (flour_base + 20) * 2
        C = (flour_base + 20) * 50
        k = random.randint(1, 50)
        x = random.randint(30, 100)  # 采购面粉效果明显
        
    elif special_case == 'egg_bottleneck':
        # 鸡蛋始终是瓶颈
        egg_base = random.randint(10, 50)
        B = egg_base * 2
        # 其他材料充足
        A = (egg_base + 20) * 30
        C = (egg_base + 20) * 50
        k = random.randint(1, 50)
        x = random.randint(2, 50)  # 采购鸡蛋效果明显
        
    elif special_case == 'milk_bottleneck':
        # 牛奶始终是瓶颈
        milk_base = random.randint(10, 50)
        C = milk_base * 50
        # 其他材料充足
        A = (milk_base + 20) * 30
        B = (milk_base + 20) * 2
        k = random.randint(1, 50)
        x = random.randint(50, 100)  # 采购牛奶效果明显
        
    elif special_case == 'max_k':
        # 最大采购天数
        A = random.randint(100, 1000)
        B = random.randint(100, 1000)
        C = random.randint(100, 1000)
        k = 100  # 最大采购天数
        x = random.randint(1, 100)
        
    elif special_case == 'max_x':
        # 最大单次采购量
        A = random.randint(100, 1000)
        B = random.randint(100, 1000)
        C = random.randint(100, 1000)
        k = random.randint(1, 100)
        x = 100  # 最大单次采购量
        
    else:
        # 随机生成
        A = random.randint(1, 1000)
        B = random.randint(1, 1000)
        C = random.randint(1, 1000)
        k = random.randint(1, 100)
        x = random.randint(1, 100)
    
    # 生成输入数据
    input_data = f"{A} {B} {C} {k} {x}"
    
    # 计算输出数据
    output_data = str(find_best_purchase(A, B, C, k, x))
    
    # 格式化文件名，确保至少3位数字
    filename = f"{case_num:03d}"
    
    return filename, input_data, output_data

def generate_all_test_cases(num_cases=10):
    """生成所有测试案例"""
    test_cases = []
    
    # 特殊案例
    test_cases.append(generate_test_case(1, 'no_improve'))        # 采购无法提高产能
    test_cases.append(generate_test_case(2, 'flour_bottleneck'))  # 面粉是瓶颈
    test_cases.append(generate_test_case(3, 'egg_bottleneck'))    # 鸡蛋是瓶颈
    test_cases.append(generate_test_case(4, 'milk_bottleneck'))   # 牛奶是瓶颈
    test_cases.append(generate_test_case(5, 'max_k'))             # 最大采购天数
    test_cases.append(generate_test_case(6, 'max_x'))             # 最大单次采购量
    test_cases.append(generate_test_case(7))                      # 示例输入类似案例
    test_cases[6] = (test_cases[6][0], "300 20 500 2 100", "10")  # 确保有一个案例与样例相同
    
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
        output_zip = "tart_capacity_testcases.zip"
        print(f"正在创建压缩包 {output_zip}...")
        create_zip_archive(temp_dir, output_zip)
        
        print("测试数据生成完成！")
        print(f"生成了 {len(test_cases)} 对测试文件，已打包到 {output_zip}")
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
    