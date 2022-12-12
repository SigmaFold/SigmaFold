import itertools

perm_list = []
product_list = list(itertools.product('HP', repeat=3))
for product in product_list:
    product_str = ''.join(product)
    perm_list.append(product_str)