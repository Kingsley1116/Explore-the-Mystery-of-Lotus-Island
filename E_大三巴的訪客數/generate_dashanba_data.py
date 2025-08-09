import os
import zipfile
import random
import tempfile
import shutil

def generate_test_case(case_num, n, dashanba_count):
    """生成單個測試案例"""
    # 澳门其他著名景点
    other_attractions = [
        "媽閣廟", "海事及水務局大樓", "亞婆井前地", "鄭家大屋", "風順堂",
        "崗頂前地", "崗頂劇院", "何東圖書館大樓", "聖奧斯定教堂", "市政署大樓",
        "議事亭前地", "三街會館", "澳門仁慈堂大樓", "主教座堂", "盧家大屋",
        "玫瑰聖母堂", "哪咤廟", "大炮台", "東望洋炮台", "聖安多尼堂及前地",
        "東方基金會會址", "基督教墳場", "大堂前地", "板樟堂前地", "白鴿巢前地", "耶穌會紀念廣場"
    ]
    
    # 生成输入数据
    input_data = [str(n)]
    dashanba_used = 0
    
    for i in range(n):
        # 决定当前行是否为"大三巴"
        if dashanba_used < dashanba_count and (i == n - 1 and dashanba_used < dashanba_count or 
                                              random.random() < dashanba_count / (n - i)):
            input_data.append("大三巴")
            dashanba_used += 1
        else:
            # 随机选择其他景点
            input_data.append(random.choice(other_attractions))
    
    # 生成输出数据
    output_data = str(dashanba_count)
    
    # 格式化文件名，确保至少3位数字
    filename = f"{case_num:03d}"
    
    return filename, "\n".join(input_data), output_data

def generate_all_test_cases(num_cases=10):
    """生成所有测试案例"""
    test_cases = []
    
    # 特殊案例：最小输入
    test_cases.append(generate_test_case(1, 1, 0))  # 不是大三巴
    test_cases.append(generate_test_case(2, 1, 1))  # 是大三巴
    
    # 特殊案例：最大输入
    test_cases.append(generate_test_case(3, 1000, 0))   # 全不是大三巴
    test_cases.append(generate_test_case(4, 1000, 1000)) # 全是大三巴
    
    # 随机生成其他案例
    for i in range(5, num_cases + 1):
        n = random.randint(1, 1000)
        dashanba_count = random.randint(0, n)
        test_cases.append(generate_test_case(i, n, dashanba_count))
    
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
        output_zip = "dashanba_visitor_testcases.zip"
        print(f"正在创建压缩包 {output_zip}...")
        create_zip_archive(temp_dir, output_zip)
        
        print("测试数据生成完成！")
        print(f"生成了 {len(test_cases)} 对测试文件，已打包到 {output_zip}")
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
    