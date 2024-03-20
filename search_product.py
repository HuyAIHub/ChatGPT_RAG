import pandas as pd
import time

path="./data/product_info.xlsx"
df = pd.read_excel(path)
df = df.fillna('')

def product_seeking(results,texts):    
    # Đọc dữ liệu từ tệp Excel vào DataFrame
    # Bắt đầu đo thời gian
    start_time = time.time()

    for index, row in df.iterrows():
        if row['PRODUCT_NAME'] and row['PRODUCT_NAME'] in texts:
            product =  {
                "code" : "",
                "name" : "",
                "link" : ""
            }
            product = {
                "code": row['PRODUCT_CODE'],
                "name": row['PRODUCT_NAME'],
                "link": row['link_product']
            }
            results["products"].append(product)
    execution_time = time.time() - start_time
    print("time to find product link: ",execution_time)
    return results

def get_products_by_group(group_name):
    products = df[df['GROUP_PRODUCT_NAME'] == group_name][['PRODUCT_CODE', 'PRODUCT_NAME']]
    product_list = list(products.itertuples(index=False, name=None))
    return len(product_list), product_list