import os
import zipfile
import random
import tempfile
import shutil

def divide_large_number(num_str, divisor):
    """
    处理大数字字符串除以整数的运算
    返回 (商的字符串, 余数)
    """
    return str(int(num_str) // divisor), int(num_str) % divisor

def calculate_min_chips(M_str):
    """计算凑出M元所需的最少筹码数量，支持超大数（字符串形式）"""
    # 筹码面额，从大到小排列
    denominations = [1000, 500, 100, 50, 10]
    count = 0
    current = M_str
    
    for d in denominations:
        if current == '0':
            break
            
        # 计算当前金额能换多少个d面额的筹码
        quotient, remainder = divide_large_number(current, d)
        count += int(quotient)
        current = str(remainder)
            
    return count

def generate_large_number(min_len, max_len):
    """生成一个指定长度范围的大数字字符串，确保是10的倍数"""
    if min_len == max_len:
        length = min_len
    else:
        length = random.randint(min_len, max_len)
    
    # 第一位不能为0
    first_digit = random.randint(1, 9)
    # 中间位可以是任意数字
    middle_digits = [random.randint(0, 9) for _ in range(length - 2)]
    # 最后一位必须是0，确保是10的倍数
    last_digit = 0
    
    # 组合成数字字符串
    digits = [str(first_digit)] + [str(d) for d in middle_digits] + [str(last_digit)]
    return ''.join(digits)

def generate_test_case(case_num, special_case=None):
    """
    生成单个测试案例
    special_case: 特殊案例类型，None表示随机生成
                  'small' - 小金额 (1 ≤ M ≤ 10^3)
                  'medium' - 中等金额 (10^3 ≤ M ≤ 10^5)
                  'large' - 超大金额 (10^5 ≤ M ≤ 10^500)
                  'exact' - 正好是某个面额的倍数
                  'mixed' - 需要混合使用各种面额
                  'sample' - 与样例相同的案例
    """
    M_str = ""
    
    if special_case == 'small':
        # 小金额 (1 ≤ M ≤ 10^3)
        M = random.randint(10, 1000)
        # 确保M是10的倍数
        M = (M // 10) * 10
        M_str = str(M)
        
    elif special_case == 'medium':
        # 中等金额 (10^3 ≤ M ≤ 10^5)
        M = random.randint(1000, 100000)
        M = (M // 10) * 10
        M_str = str(M)
        
    elif special_case == 'large':
        # 超大金额 (10^500 ≤ M ≤ 10^2000)
        min_len = 500
        max_len = 2000
        M_str = generate_large_number(min_len, max_len)
        
    elif special_case == 'exact':
        # 正好是某个面额的倍数
        denominations = [10, 50, 100, 500, 1000]
        d = random.choice(denominations)
        
        # 随机决定是小、中金额
        range_choice = random.choice(['small', 'medium'])
        if range_choice == 'small':
            multiplier = random.randint(1, 100)  # 最大100*1000=100000
        elif range_choice == 'medium':
            multiplier = random.randint(10, 1000)

        M = d * multiplier
        M_str = str(M)
        
    elif special_case == 'mixed':
        # 需要混合使用各种面额
        # 确保每个面额至少使用一个
        counts = [
            random.randint(1, 10),   # 1000元的数量
            random.randint(1, 10),   # 500元的数量
            random.randint(1, 10),   # 100元的数量
            random.randint(1, 10),   # 50元的数量
            random.randint(1, 10)    # 10元的数量
        ]
        denominations = [1000, 500, 100, 50, 10]
        M = sum(c * d for c, d in zip(counts, denominations))
        M_str = str(M)
        
    elif special_case == 'sample':
        # 与样例相同的案例
        M_str = "360"
        
    else:
        # 随机生成，覆盖所有范围
        range_choice = random.choice(['small', 'medium', 'large'])
        if range_choice == 'small':
            M = random.randint(10, 1000)
            M = (M // 10) * 10
            M_str = str(M)
        elif range_choice == 'medium':
            M = random.randint(1000, 100000)
            M = (M // 10) * 10
            M_str = str(M)
        else:
            M_str = generate_large_number(500, 2000)
    
    # 计算输出数据
    output_data = str(calculate_min_chips(M_str))
    
    # 格式化文件名，确保至少3位数字
    filename = f"{case_num:03d}"
    
    return filename, M_str, output_data

def generate_all_test_cases(num_cases=50):
    """生成所有测试案例"""
    test_cases = []
    
    # 特殊案例
    test_cases.append(generate_test_case(1, 'sample'))       # 样例案例
    test_cases.append(generate_test_case(2, 'exact'))        # 正好是某个面额的倍数
    test_cases.append(generate_test_case(3, 'exact'))        # 正好是某个面额的倍数
    test_cases.append(generate_test_case(4, 'mixed'))        # 正好是某个面额的倍数
    test_cases.append(generate_test_case(5, 'mixed'))        # 需要混合使用各种面额
    test_cases.append(generate_test_case(6, 'mixed'))        # 需要混合使用各种面额
    
    # 生成更多不同范围的案例
    for i in range(7, 11):
        test_cases.append(generate_test_case(i, 'small'))    # 更多小金额案例
        
    for i in range(11, 15):
        test_cases.append(generate_test_case(i, 'medium'))   # 更多中等金额案例
        
    for i in range(15, num_cases + 1):
        test_cases.append(generate_test_case(i, 'large'))    # 更多超大金额案例
    
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
    test_cases = generate_all_test_cases(50)  # 生成 50 个测试案例
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    try:
        # 保存测试案例
        print("正在保存测试案例...")
        save_test_cases(test_cases, temp_dir)
        
        # 创建ZIP压缩包
        output_zip = "chip_exchange_testcases.zip"
        print(f"正在创建压缩包 {output_zip}...")
        create_zip_archive(temp_dir, output_zip)
        
        print("测试数据生成完成！")
        print(f"生成了 {len(test_cases)} 对测试文件，已打包到 {output_zip}")
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
    