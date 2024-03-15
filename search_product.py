import pandas as pd
import time

def product_seeking(results,texts,path):    
    # Đọc dữ liệu từ tệp Excel vào DataFrame
    # Bắt đầu đo thời gian
    start_time = time.time()
    df = pd.read_excel(path)
    df = df.fillna('')
    for index, row in df.iterrows():
        if row['PRODUCT_NAME'] and row['PRODUCT_NAME'] in texts:
            print('da vao day!')
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