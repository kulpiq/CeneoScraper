import requests

#product_code = input("Please enter product code: ")
product_code = "133748381"
print(product_code)

url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
response = requests.get(url)
print(response.status_code)