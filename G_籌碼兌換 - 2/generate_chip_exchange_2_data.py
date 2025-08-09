import os
import zipfile
import random
import tempfile
import shutil
import math

def calculate_min_chips_with_limits(M, limits):
    """
    计算带数量限制的最少筹码数量
    M: 需要凑出的金额
    limits: [c1, c2, c3, c4, c5] 分别对应10元、50元、100元、500元、1000元的数量上限
    返回最少筹码数，无法凑出则返回-1
    """
    # 所有面额都是10的倍数，若M不是10的倍数则无法凑出
    if M % 10 != 0:
        return -1
    
    # 简化问题：将金额和面额都除以10
    target = M // 10
    denominations = [1, 5, 10, 50, 100]  # 对应10元、50元、100元、500元、1000元 (除以10后)
    
    # 动态规划数组，dp[i]表示凑出i所需的最少筹码数
    max_val = target
    dp = [float('inf')] * (max_val + 1)
    dp[0] = 0  # 凑出0元需要0个筹码
    
    # 对每种面额进行处理
    for i in range(5):
        d = denominations[i]
        count_limit = limits[i]
        
        # 处理当前面额，使用0到count_limit个
        # 采用逆向遍历避免重复使用同一筹码多次
        for j in range(max_val, d - 1, -1):
            # 尝试使用k个当前面额的筹码
            for k in range(1, min(count_limit, j // d) + 1):
                if dp[j - k * d] + k < dp[j]:
                    dp[j] = dp[j - k * d] + k
    
    return dp[target] if dp[target] != float('inf') else -1

def generate_test_case(case_num, special_case=None):
    """
    生成单个测试案例
    special_case: 特殊案例类型
                  'sample' - 样例案例
                  'not_multiple_10' - M不是10的倍数（无法凑出）
                  'exact_large' - 刚好使用最大面额
                  'limit_constrained' - 受限于数量限制
                  'no_solution' - 无法凑出（数量不足）
                  'min_coins' - 多种方案中选最少数量
                  'one_type' - 只用一种面额
                  'max_M' - 最大金额10^5
    """
    M = 0
    limits = []  # [c1, c2, c3, c4, c5] 对应10元、50元、100元、500元、1000元的数量上限
    
    if special_case == 'sample':
        # 样例输入
        M = 360
        limits = [3, 3, 2, 1, 1]  # 10元3个，50元3个，100元2个，500元1个，1000元1个
        
    elif special_case == 'not_multiple_10':
        # M不是10的倍数，无法凑出
        M = random.randint(1, 100000)
        # 确保不是10的倍数
        while M % 10 == 0:
            M = random.randint(1, 100000)
        # 随机生成数量限制
        limits = [random.randint(1, 100) for _ in range(5)]
        
    elif special_case == 'exact_large':
        # 刚好使用最大面额
        # 1000元面额的数量足够
        count = random.randint(1, 100)
        M = count * 1000
        # 确保不超过最大M值
        if M > 100000:
            count = 100
            M = 100000
        limits = [1, 1, 1, 1, count]  # 1000元数量刚好
        
    elif special_case == 'limit_constrained':
        # 受限于数量限制，必须使用较小面额
        # 例如：需要2000元，但1000元只有1个，必须用500元补充
        M = 2000
        limits = [100, 100, 100, 2, 1]  # 1000元只有1个，需要用2个500元
        
    elif special_case == 'no_solution':
        # 无法凑出（数量不足）
        M = 10000
        # 所有筹码加起来不够
        limits = [5, 5, 5, 5, 5]  # 总金额:5*10 + 5*50 + 5*100 + 5*500 + 5*1000 = 50+250+500+2500+5000=8300 < 10000
        
    elif special_case == 'min_coins':
        # 多种方案中选最少数量
        M = 600
        # 方案1: 1个500 + 1个100 → 2个
        # 方案2: 6个100 → 6个
        # 但限制500元只有0个，所以必须选方案2
        limits = [10, 10, 10, 0, 0]  # 500和1000元数量为0
        
    elif special_case == 'one_type':
        # 只用一种面额
        # 选择100元面额
        count = random.randint(1, 100)
        M = count * 100
        if M > 100000:
            count = 1000
            M = 100000
        limits = [0, 0, count, 0, 0]  # 只有100元有足够数量
        
    elif special_case == 'max_M':
        # 最大金额10^5
        M = 100000
        # 确保可以凑出
        # 1000元 * 100个 = 100000元
        limits = [1, 1, 1, 1, 100]
        
    else:
        # 随机生成案例
        # 确保M是10的倍数
        M = random.randint(1, 10000) * 10
        if M > 100000:
            M = 100000
            
        # 随机生成数量限制
        limits = [random.randint(1, 100) for _ in range(5)]
        
        # 有20%概率生成无法凑出的案例
        if random.random() < 0.2:
            # 确保总金额不足
            total = limits[0]*10 + limits[1]*50 + limits[2]*100 + limits[3]*500 + limits[4]*1000
            # 修复随机数范围错误
            if total + 10 > 100000:
                # 如果总金额已接近或超过上限，调整策略
                M = 100000
                # 确保M大于total
                if M <= total:
                    # 减少一些筹码数量使总金额不足
                    reduce_idx = random.randint(0, 4)
                    limits[reduce_idx] = max(1, limits[reduce_idx] - 1)
                    total = limits[0]*10 + limits[1]*50 + limits[2]*100 + limits[3]*500 + limits[4]*1000
            else:
                # 正常生成比total大的M
                M = random.randint(total + 10, 100000)
                if M % 10 != 0:
                    M += (10 - M % 10)
    
    # 生成输入数据
    input_lines = [str(M)]
    input_lines.append(' '.join(map(str, limits)))
    input_data = "\n".join(input_lines)
    
    # 计算输出数据
    output_data = str(calculate_min_chips_with_limits(M, limits))
    
    # 格式化文件名
    filename = f"{case_num:03d}"
    
    return filename, input_data, output_data

def generate_all_test_cases(num_cases=20):
    """生成所有测试案例"""
    test_cases = []
    
    # 特殊案例
    test_cases.append(generate_test_case(1, 'sample'))            # 样例案例
    test_cases.append(generate_test_case(2, 'not_multiple_10'))   # M不是10的倍数
    test_cases.append(generate_test_case(3, 'exact_large'))       # 刚好使用最大面额
    test_cases.append(generate_test_case(4, 'limit_constrained')) # 受限于数量限制
    test_cases.append(generate_test_case(5, 'no_solution'))       # 无法凑出
    test_cases.append(generate_test_case(6, 'min_coins'))         # 选最少数量
    test_cases.append(generate_test_case(7, 'one_type'))          # 只用一种面额
    test_cases.append(generate_test_case(8, 'max_M'))             # 最大金额
    
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
        
        output_zip = "chip_exchange_2_testcases.zip"
        print(f"正在创建压缩包 {output_zip}...")
        create_zip_archive(temp_dir, output_zip)
        
        print("测试数据生成完成！")
        print(f"生成了 {len(test_cases)} 对测试文件，已打包到 {output_zip}")
        
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
    