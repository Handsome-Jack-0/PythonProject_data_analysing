import pandas as pd

# 读取 CSV 文件
csv_file = 'douban_top250_extended.csv'
df = pd.read_csv(csv_file)

# 将数据保存为 Excel 文件
excel_file = 'douban_top250_extended.xlsx'
df.to_excel(excel_file, index=False)

print(f'已成功将 {csv_file} 转换为 {excel_file}')