import pandas as pd
# Đọc dữ liệu từ tệp Excel vào DataFrame
data = pd.read_excel("./data/product_info_2.xlsx")

def get_products_by_group(group_name):
    products = data[data['GROUP_PRODUCT_NAME'] == group_name][['PRODUCT_INFO_ID', 'PRODUCT_NAME']]
    product_list = list(products.itertuples(index=False, name=None))
    return len(product_list), product_list

group_name = input("Nhập tên nhóm sản phẩm: ")
quantity, product_list = get_products_by_group(group_name)

# result_string = f"Số lượng sản phẩm: {quantity}\n"
# for index, (code, name) in enumerate(products, start=1):
#     result_string += f"{index}. {code}: {name}\n"

# print(result_string)


# Khởi tạo danh sách sản phẩm rỗng
products = []

# Duyệt qua từng tuple trong product_list
for idx, (product_id, product_name) in enumerate(product_list, start=1):
    # Tạo một dictionary để lưu thông tin của sản phẩm
    product = {
        'PRODUCT_INFO_ID': product_id,
        'PRODUCT_NAME': product_name,
        # Các trường thông tin khác có thể thêm tại đây
        # Ví dụ: 'LIFECARE_PRICE': ..., 'SHORT_DESCRIPTION': ..., vv.
    }
    # Thêm sản phẩm vào danh sách products
    products.append(product)


print(products)
# In danh sách sản phẩm
for idx, product in enumerate(products, start=1):
    print(f"Product {idx}: {product['PRODUCT_INFO_ID']} - {product['PRODUCT_NAME']}")