import pandas as pd
# Đọc dữ liệu từ tệp Excel vào DataFrame
df = pd.read_excel("./data/product_info.xlsx")
# Tính tổng số lượng giá trị rỗng trong mỗi cột
empty_count = df.isna().sum()

print(empty_count)