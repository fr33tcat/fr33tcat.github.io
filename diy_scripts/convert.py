import os
import re
import datetime
import urllib.parse

# 1. 设置文件夹路径
source_dir = '_draft_notes'
target_dir = '_posts'

# 如果目标文件夹不存在，则创建它
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# 2. 定义处理图片链接的替换函数
def replace_image_link(match):
    img_name = match.group(1)
    # 处理图片名中的空格等特殊字符，转为 URL 安全的格式 (例如空格变成 %20)
    safe_img_name = urllib.parse.quote(img_name)
    # 转换为 Markdown 标准图片语法，指向 Jekyll 的绝对路径
    return f"![{img_name}](/assets/img/attachments/{safe_img_name})"

# 3. 遍历并处理源文件夹中的所有 markdown 文件
processed_count = 0
for filename in os.listdir(source_dir):
    if not filename.endswith('.md'):
        continue

    file_path = os.path.join(source_dir, filename)

    # 获取文件的最后修改时间
    mtime = os.path.getmtime(file_path)
    dt = datetime.datetime.fromtimestamp(mtime)
    
    # 格式化时间
    date_prefix = dt.strftime('%Y-%m-%d')
    date_front_matter = dt.strftime('%Y-%m-%d %H:%M:%S +0800')

    # 提取纯标题 (去掉 .md 后缀)
    title = os.path.splitext(filename)[0]
    
    # 构造安全的文件名 (将文件名中的空格替换为连字符 -)
    safe_base_name = title.replace(' ', '-')
    new_filename = f"{date_prefix}-{safe_base_name}.md"
    target_path = os.path.join(target_dir, new_filename)

    # 读取文件原始内容 (指定 utf-8 防止中文乱码)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 正则替换：将 ![[图片名]] 替换为标准格式
    # r'!\[\[(.*?)\]\]' 匹配以 ![[ 开头，]] 结尾的任何内容
    content = re.sub(r'!\[\[(.*?)\]\]', replace_image_link, content)

    # 构建 Front Matter 头部信息
    front_matter = f"""---
title: {title}
date: {date_front_matter}
categories: [网安学习, 靶机实战]
tags: [学习笔记, Writeup]
---

"""

    # 将头部信息和修改后的内容写入新文件
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(front_matter + content)

    print(f"✅ 成功转换: {title} -> {new_filename}")
    processed_count += 1

print(f"\n🎉 全部转换完成！共处理了 {processed_count} 篇文章，请去 _posts 文件夹查看！")