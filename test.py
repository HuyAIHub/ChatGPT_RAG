# import pandas as pd
# # Đọc dữ liệu từ tệp Excel vào DataFrame
# data = pd.read_excel("./data/product_info_final.xlsx")
# print(data[['PRODUCT_INFO_ID', 'PRODUCT_NAME', 'LINK_SP']])
# def get_products_by_group(group_name):
#     products = data[data['GROUP_PRODUCT_NAME'] == group_name][['PRODUCT_INFO_ID', 'PRODUCT_NAME', 'LINK_SP']]
#     product_list = list(products.itertuples(index=False, name=None))
#     return len(product_list), product_list

# group_name = input("Nhập tên nhóm sản phẩm: ")
# quantity, product_list = get_products_by_group(group_name)

# result_string = f"Số lượng sản phẩm: {quantity}\n"
# for index, (code, name) in enumerate(product_list, start=1):
#     result_string += f"{index}. {code}: {name}\n"

# print(result_string)


import pandas as pd

# Đọc dữ liệu từ tệp Excel vào DataFrame
data = pd.read_excel("./data/product_info_final.xlsx")

# Kiểm tra cấu trúc của DataFrame data
print(data.head())

def get_products_by_group(group_name):
    products = data[data['GROUP_PRODUCT_NAME'] == group_name]
    # Kiểm tra xem cả 3 cột 'PRODUCT_INFO_ID', 'PRODUCT_NAME', và 'LINK_SP' tồn tại trong DataFrame products
    if all(col in products.columns for col in ['PRODUCT_INFO_ID', 'PRODUCT_NAME', 'LINK_SP']):
        # Chọn cả 3 cột 'PRODUCT_INFO_ID', 'PRODUCT_NAME', và 'LINK_SP'
        products = products[['PRODUCT_INFO_ID', 'PRODUCT_NAME', 'LINK_SP']]
        # Chuyển đổi DataFrame thành danh sách các tuple
        product_list = list(products.itertuples(index=False, name=None))
        return len(product_list), product_list
    else:
        return 0, []

group_name = input("Nhập tên nhóm sản phẩm: ")
quantity, product_list = get_products_by_group(group_name)

result_string = f"Số lượng sản phẩm: {quantity}\n"
# for index, (code, name, link) in enumerate(product_list, start=1):
#     result_string += f"{index}. {code}: {name} ({link})\n"

# print(result_string)

print(product_list)