"""一些生成器方法，生成随机数，手机号，以及连续数字等"""

import random
from faker import Factory

fake=Factory.create("zh_CN")

def random_name():
    """随机姓名"""
    return fake.name()

def random_address():
    """随机地址"""
    return fake.address()

def random_phone_number():
    """随机手机号"""
    return fake.phone_number()

def random_email():
    """随机email"""
    return fake.email()

def random_ipv4():
    """随机IPV4"""
    return fake.ipv4()

def random_str(min_chars=0,max_chars=8):
    """长度在最小和最大长度之间的随机长度字符串"""
    return fake.pystr(min_chars=min_chars,max_chars=max_chars)

def random_generate_ids(start_id=1,increment=1):
    """返回生成器函数，调用这个函数产生生成器，从satrt_id开始，步长increment"""
    def generate_id():
        val=start_id
        i=increment
        while True:
            yield val
            val+=i
    return generate_id

def random_choice_list(list):
    """返回生成器函数，调用这个函数产生生成器，从指定列表中随机选取一项"""
    def choice_list():
        ram=random.Random()
        while True:
            yield ram.choice(list)
    return  choice_list

def random_choice_dic(**dic):
    """返回生成器函数，调用这个函数产生生成器，从指定列表中随机选取一项"""
    def choice_dic():
        ram=random.Random()
        while True:
            yield ram.choice(**dic)
    return  choice_dic






if __name__ == '__main__':
    # print(random_name())
    # print(random_address())
    # print(random_phone_number())
    # print(random_email())
    # print(random_ipv4())
    # print(random_str(1,10))
    #
    # generate_id=random_generate_ids(start_id=3,increment=3)()
    # for i in range(6):
    #     print(next(generate_id))
    #
    # choice = random_choice_list([1,55,4,"asdh"])()
    # for i in range(6):
    #     print(next(choice))

    choice = random_choice_dic(**{"1":"2332","2":"wqe"})()
    for i in range(6):
        print(next(choice))





