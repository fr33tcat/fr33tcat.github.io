import os
import re
from datetime import datetime

# 1. 设置文章所在的文件夹（如果你放在了其他地方，请修改这里）
target_dir = '_posts'

if not os.path.exists(target_dir):
    print(f"❌ 找不到 {target_dir} 文件夹，请确认路径是否正确！")
    exit()

processed_count = 0

# 2. 遍历文件夹里的 markdown 文件
for filename in os.listdir(target_dir):
    if not filename.endswith('.md'):
        continue

    # 提取文件名中的日期部分 (匹配格式如 2025-06-04 或 2025-6-4)
    match = re.match(r'^(\d{4}-\d{1,2}-\d{1,2})-(.*)$', filename)
    if not match:
        print(f"⚠️ 跳过不符合命名格式的文件: {filename}")
        continue

    date_str = match.group(1)       # 提取出的日期，比如 2025-06-6
    rest_of_name = match.group(2)   # 文件名剩余部分，比如 002-Jarbas.md

    try:
        # 将提取的字符串解析为真实日期对象
        parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print(f"⚠️ 日期解析失败，跳过: {filename}")
        continue

    # 强制格式化为标准的 YYYY-MM-DD (自动补零)
    standard_date_str = parsed_date.strftime('%Y-%m-%d')
    
    # 构建标准的新文件名
    standard_filename = f"{standard_date_str}-{rest_of_name}"
    
    old_filepath = os.path.join(target_dir, filename)
    new_filepath = os.path.join(target_dir, standard_filename)

    # 3. 读取原文件内容
    with open(old_filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 构建头部需要写入的新日期 (时间默认设置为中午 12:00:00，时区 +0800)
    new_front_matter_date = f"{standard_date_str} 12:00:00 +0800"

    # 使用正则替换文件头部 (Front Matter) 中的 date 字段
    # 只替换第一个匹配到的 date: 所在行
    new_content = re.sub(
        r'^date:\s*.*$', 
        f'date: {new_front_matter_date}', 
        content, 
        count=1, 
        flags=re.MULTILINE
    )

    # 4. 保存文件并重命名（如果名字有变动）
    if old_filepath != new_filepath:
        # 如果文件名缺 0，先写入新文件，再删掉旧文件
        with open(new_filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        os.remove(old_filepath)
        print(f"✅ [修复并更新]: {filename} -> {standard_filename}")
    else:
        # 名字本来就标准，直接覆盖更新内容
        with open(old_filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ [成功更新]: {filename}")
        
    processed_count += 1

print(f"\n🎉 搞定！一共自动修正和更新了 {processed_count} 篇文章。")