import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from config_app.config import get_config
from langchain.chains import LLMChain
import openpyxl
import time
import pandas as pd
import json
from module.search_product import product_seeking_terms
config_app = get_config()

os.environ['OPENAI_API_KEY'] = config_app["parameter"]["openai_api_key"]
llm = ChatOpenAI(model_name=config_app["parameter"]["gpt_model_to_use"], temperature=config_app["parameter"]["temperature"])
data = pd.read_excel("./data/10_groupitem.xlsx")

def split_sentences(text_input):
    # First, create the list of few shot examples.
    examples = [
        {
            "command":"Tôi muốn mua hai chiếc máy lọc không khí giá 5 triệu",
            "object": ["Tôi muốn mua hai chiếc máy lọc không khí giá 5 triệu"],
        },
        {
            "command": "Tôi muốn mua tủ lạnh tầm 600 nghìn và bếp từ 1 triệu",
            "object": ["Tôi muốn mua tủ lạnh tầm 600 nghìn", "bếp từ 1 triệu"],
        },
        {
            "command": "Tôi muốn mua nồi cơm điện, máy hút bụi, máy lọc không khí với số tiền từ 8 triệu đến 9 triệu",
            "object": ["Tôi muốn mua nồi cơm điện, máy hút bụi, máy lọc không khí với số tiền từ 8 triệu đến 9 triệu"],
        },
        {
            "command": "Mua lò vi sóng, máy giặt, tủ lạnh với số tiền 10 triệu và giới thiệu giúp tôi sản phẩm điều hòa giá rẻ nhất hiện nay",
            "object": ["Mua lò vi sóng, máy giặt, tủ lạnh với số tiền 10 triệu", "giới thiệu giúp tôi sản phẩm điều hòa giá rẻ nhất hiện nay"],
        },
        {
            "command":"Cho tôi 4 máy lọc không khí giá tầm 20 triệu và 3 tủ lạnh, 5 máy giặt với tổng giá trị 50 triệu",
            "object": ["Cho tôi 4 máy lọc không khí giá tầm 20 triệu", "3 tủ lạnh, 5 máy giặt với tổng giá trị 50 triệu"],
        },
        {
            "command": "Cho tôi 4 máy lọc không khí Daiki với giá tiền phù hợp từ 7 triệu đến 15 triệu và mua nồi cơm điện, nồi chiên không dầu, bếp từ với số tiền khoảng 13,5 triệu",
            "object":["Cho tôi 4 máy lọc không khí Daiki với giá tiền phù hợp từ 7 triệu đến 15 triệu", "mua nồi cơm điện, nồi chiên không dầu, bếp từ với số tiền khoảng 13,5 triệu"],
        },
        {
            "command": "Tôi muốn mua sản phẩm tivi số lượng 3 cái với giá đắt nhất, điều hòa 2 cái với số tiền là 20 triệu",
            "object": ["Tôi muốn mua sản phẩm tivi số lượng 3 cái với giá đắt nhất", "điều hòa 2 cái với số tiền là 20 triệu"],
        },
        {
            "command": "Đèn năng lượng mặt trời giá 15 triệu, nồi cơm điện 4 triệu, máy giặt 10 triệu",
            "object": ["Đèn năng lượng mặt trời giá 15 triệu", "nồi cơm điện 4 triệu", "máy giặt 10 triệu"],
        }
    ]

    example_formatter_template = """
        Input command from user: {command}
        The information extracted from above command:\n
        {object}
    """

    example_prompt = PromptTemplate(
        input_variables=["command", "object"],
        template=example_formatter_template,
    )

    few_shot_prompt = FewShotPromptTemplate(
        # These are the examples we want to insert into the prompt.
        examples=examples,
        # This is how we want to format the examples when we insert them into the prompt.
        example_prompt=example_prompt,
        # The prefix is some text that goes before the examples in the prompt.
        # Usually, this consists of intructions.
        prefix="Extract the detail information for an IoT input command. Return the corresponding object. Below are some examples:",
        # The suffix is some text that goes after the examples in the prompt.
        # Usually, this is where the user input will go
        suffix="Input command from user: {command}\nThe information extracted from above command::",
        # The input variables are the variables that the overall prompt expects.
        input_variables=["command"],
        # The example_separator is the string we will use to join the prefix, examples, and suffix together with.
        example_separator="\n\n",
    )

    # print(few_shot_prompt.format(command="Mua đèn năng lượng mặt trời giá 15 triệu"))

    chain = LLMChain(llm=llm, prompt=few_shot_prompt)

    return chain.run(command=text_input)

def search_obj_val(text_input):
    # First, create the list of few shot examples.
    examples = [
        {
            "command": "Tôi muốn mua tủ lạnh tầm 600 nghìn",
            "object": ["1 tủ lạnh"],
            "value": ["600 nghìn"],
        },
        {
            "command": "Mua lò vi sóng và máy giặt với số tiền mười triệu",
            "object": ["1 lò vi sóng", "1 máy giặt"],
            "value": ["10 triệu"],
        },
        {
            "command":"Cho tôi xem các loại nồi cơm điện có giá từ 2 triệu đến 3 triệu đồng",
            "object": ["1 nồi cơm điện"],
            "value": ["2 triệu đến 3 triệu đồng"],
        },
        {
            "command": "Với số tiền 30 triệu tôi mua được ti vi, tủ lạnh ,điều hòa không?" ,
            "object": ["1 ti vi", "1 tủ lạnh", "1 điều hòa"],
            "value": ["30 triệu"],
        },
        {
            "command": "Cho tôi 4 máy lọc không khí Daiki với giá tiền phù hợp từ 7 triệu đến 15 triệu",
            "object":["4 máy lọc không khí"],
            "value": ["7 triệu đến 15 triệu"]
        },
        {
            "command": "Tôi muốn mua sản phẩm tivi số lượng 3 cái, điều hòa 2 cái với số tiền hiện tại tôi có là 20 triệu",
            "object": ["3 tủ lạnh", "2 điều hòa"],
            "value": ["20 triệu"]
        },
        {
            "command": "Đèn năng lượng mặt trời, bếp từ với mười lăm triệu",
            "object": ["1 Đèn năng lượng mặt trời", "1 bếp từ"],
            "value": ["15 triệu"],
        },
        {
            "command": "Nồi chiên không dầu và điều hòa với bốn triệu",
            "object": ["1 Nồi chiên không dầu",  "1 điều hòa"],
            "value": ["4 triệu"],
        }
    ]

    example_formatter_template = """
        Input command from user: {command}
        The information extracted from above command:\n
        {object}\n{value}
    """

    example_prompt = PromptTemplate(
        input_variables=["command", "object", "value"],
        template=example_formatter_template,
    )

    few_shot_prompt = FewShotPromptTemplate(
        # These are the examples we want to insert into the prompt.
        examples=examples,
        # This is how we want to format the examples when we insert them into the prompt.
        example_prompt=example_prompt,
        # The prefix is some text that goes before the examples in the prompt.
        # Usually, this consists of intructions.
        prefix="Extract the detail information for an IoT input command. Return the corresponding object and value. Below are some examples:",
        # The suffix is some text that goes after the examples in the prompt.
        # Usually, this is where the user input will go
        suffix="Input command from user: {command}\nThe information extracted from above command::",
        # The input variables are the variables that the overall prompt expects.
        input_variables=["command"],
        # The example_separator is the string we will use to join the prefix, examples, and suffix together with.
        example_separator="\n\n",
    )

    # print(few_shot_prompt.format(command="Mua đèn năng lượng mặt trời giá 15 triệu"))

    chain = LLMChain(llm=llm, prompt=few_shot_prompt)

    return chain.run(command=text_input)

def value_str2int(value):
    if value == '':
        return 0
    value = value[1:-1].lower()
    int_value = 0
    for s in value.split(' '):
        if s.isdigit():
            int_value = int(s)
    if 'triệu' in value:
        int_value *= 1000000
    if 'nghìn' in value or 'k' in value:
        int_value *= 1000

    return int_value

def find_product(object, value):
    object = object.split(',')

    # change price of product from str to int
    value = value_str2int(value)

    # take product from DB
    
    list_product = []
    number_product = []
    a = []
    cnt = 0
    for row in data.index:
        for name_product in object:
            name_product = name_product.strip()[1:-1]
            if data['GROUP_PRODUCT_NAME'][row].lower() in name_product and (row == 0 or data['GROUP_PRODUCT_NAME'][row-1] != data['GROUP_PRODUCT_NAME'][row]):
                a = []
                cnt += 1

                # take the product list
                for row_2 in range(row, data.shape[0]):
                    if data['GROUP_PRODUCT_NAME'][row_2].lower() == data['GROUP_PRODUCT_NAME'][row].lower():
                        a.append([data['PRODUCT_INFO_ID'][row_2], data['GROUP_PRODUCT_NAME'][row_2], data['PRODUCT_NAME'][row_2], data['VAT_PRICE_3'][row_2], data['COMMISSION_3'][row_2]])
                list_product.append(a)

                # take number of product in input
                number_product.append(int(name_product.split(' ')[0]))


    # sort product from highest price to lowest
    def key_sort(s):
        return s[2]
    sort_product = []
    for i in range(0,cnt):
        a = sorted(list_product[i], key = key_sort, reverse=True)
        sort_product.append(a)

    # backtrack to find products that satisfy the condition
    result = []
    def BT(dem, sum):
        if sum > value:
            return False
        if dem == cnt and sum <= value:
            return True
        for product in sort_product[dem]:
            check = BT(dem+1, sum+number_product[dem]*product[3])
            if check:
                a = product
                a.append(number_product[dem])
                result.append(a)
                return True
    BT(0, 0)

    return result

def find_level(total_price, list_product):
    # take product from DB
    result = []

    for product in list_product:
        for row in data.index:
            if data['PRODUCT_INFO_ID'][row] == product[0]:
                ans = product
                if data['THRESHOLD_1'][row] == '':
                    ans.append(0)
                    ans.append('GÓI MUA SẮM MỨC 3')
                    result.append(ans)
                    continue
                price_level1 = int(data['THRESHOLD_1'][row].split('>')[1].strip().split('triệu')[0].strip())*1000000
                price_level2 = int(data['THRESHOLD_2'][row].split('-')[0].strip().split(' ')[-1])*1000000
                if total_price >= price_level1:
                    ans.append(data['COMMISSION_1'][row])
                    ans.append('GÓI MUA SẮM MỨC 1')
                    ans[3] = data['VAT_PRICE_1'][row]
                elif total_price >= price_level2:
                    ans.append(data['COMMISSION_2'][row])
                    ans.append('GÓI MUA SẮM MỨC 2')
                    ans[3] = data['VAT_PRICE_2'][row]
                else:
                    ans.append(0)
                    ans.append('GÓI MUA SẮM MỨC 3')
                
                result.append(ans)
    return result


def take_product(text_input):
    print('take product input:',text_input)
    results = {
    "products" : [],
    "terms" : [],
    "content" : "",
    "status" : 200,
    "message": "",
    "time_processing":''
    }
    t1 = time.time()
    results['message'] = text_input
    # text nhu cau
    out_text = 'Dựa trên yêu cầu của anh/chị:'
    # get the satisfied product list
    list_input = split_sentences(text_input)[2:-2].split("'")
    list_product = []
    obj_list = []
    print('list_input', list_input)
    for input in list_input:
        if len(input) < 4:
            continue
        obj_val = search_obj_val(input)
        print('check object', obj_val)

        _object = obj_val.split('\n')[0][1:-1]
        _value = obj_val.split('\n')[1][1:-1]

        out_text += '\n\t- {} với giá {}'.format(_object.replace("'", ""),_value.replace("'", ""))

        for j in _object.split("'"):
            s = j.strip()
            if s == '' or s == ',':
                continue
            obj_list.append(s[2:].strip())

        product = find_product(_object, _value)
        for j in product:
            list_product.append(j)
    
    out_text += '\n\nĐể phù hợp với ngân sách và nhu cầu sử dụng của khách hàng, chúng tôi đề xuất sản phẩm sau:'
    # product level calculation
    total_price = 0
    for product in list_product:
        total_price = product[3]*product[4]
    list_value = find_level(total_price, list_product)
    print('list_value:',list_value)
    notfound_product = []
    for i in obj_list:
        check = False
        for j in list_value:
            if i.lower() in j[1].lower():
                check = True
        if check == False:
            notfound_product.append("Không có sản phẩm '" + i + "' phù hợp với nhu cầu của bạn.")


    # embed to dict into list
    list_key = ["product_code", 'GROUP_PRODUCT_NAME',"product_name", "product_price", "commission_saler", "amount", "commission_implementer", "level"]
    
    result = [{list_key[i]: row[i] for i in range(len(list_key))} for row in list_value]

    # # Ghi danh sách này vào file JSON
    # with open("output.json", "w",encoding="utf-8") as json_file:
    #     json.dump(json_data, json_file, indent=4, ensure_ascii=False)
    total_price = 0
    total_commission_saler = 0
    total_commission_implementer = 0
    for x in result:
        out_text += '\n\t+ Với {} {}: {}VND - {}'.format(x['amount'],x['product_name'],x['product_price'],x['level'])
        out_text += '\n\t\t(Hoa hòng bán hàng nhận được là: {}VND và hoa hồng triển khai nhận được là: {}VND)'.format(x['commission_saler'],x['commission_implementer'])
        # total prices
        total_price += float(x['product_price'])
        total_commission_saler += float(x['commission_saler'])
        total_commission_implementer += float(x['commission_implementer'])
        #
        results = product_seeking_terms(results = results, texts=x["product_name"])
    if len(notfound_product) > 0:
        for i in notfound_product:
            out_text += '\n\n'+ i
    out_text += '\n\nTổng giá trị của gói sản phẩm này là {}VND, giúp khách hàng tiết kiệm và đáp ứng đầy đủ nhu cầu sử dụng.'.format(str(total_price))
    
    out_text += '\nNếu có bất kỳ câu hỏi hoặc yêu cầu nào khác, vui lòng liên hệ với chúng tôi. Chúng tôi luôn sẵn lòng hỗ trợ.'
    
    results['content'] = out_text
    results['time_processing'] = str(time.time()-t1)
    # print(out_text)
    # print('results:',results)
    
    return results, out_text


# # code test
# t1 = time.time()
# results = {
# "products" : [],
# "terms" : [],
# "content" : "",
# "status" : 200,
# "message": "",
# "time_processing":''
# }
# print(take_product("Cho tôi mua máy ép giá tầm 900 nghìn, máy giặt và 2 bếp từ với tổng giá trị 30 triệu"))
# print(time.time()-t1)

# [509330, 'Bếp Từ Đôi Bluestone Icb-6833', 10125830.0, 571468.8000000002, 2, 92053, 'GÓI MUA SẮM MỨC 1']]
# [mã sản phẩm, tên sản phẩm, giá theo mức, hoa hồng BH, số lượng, hoa hồng cho người triển khái,  mức]
# [product_code,product_name,product_price,commission,amount,commission_implementer,level]