import pandas as pd
# Đọc dữ liệu từ tệp Excel vào DataFrame
data = pd.read_excel("./data/product_info.xlsx")

def get_products_by_group(group_name):
    products = data[data['GROUP_PRODUCT_NAME'] == group_name][['PRODUCT_CODE', 'PRODUCT_NAME']]
    product_list = list(products.itertuples(index=False, name=None))
    return len(product_list), product_list

group_name = input("Nhập tên nhóm sản phẩm: ")
quantity, products = get_products_by_group(group_name)

result_string = f"Số lượng sản phẩm: {quantity}\n"
for index, (code, name) in enumerate(products, start=1):
    result_string += f"{index}. {code}: {name}\n"

print(result_string)