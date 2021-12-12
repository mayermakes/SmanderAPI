import requests
import os
from datetime import date

tokenurl = "https://shop.smander.com/wp-json/jwt-auth/v1/token"

tokenpayload={'username': 'smanderuser',
'password': 'supersecretPw'}
files=[

]
headers = {}

response = requests.request("POST", tokenurl, headers=headers, data=tokenpayload, files=files)
print("aquired Token")
jsondata = response.json()
rawtoken = jsondata['data']['token']
#print(rawtoken)
#token without prefix


url = "https://shop.smander.com/wp-json/dokan/v1/orders/"

payload={}
headers = {
  'Authorization': 'Bearer'+ rawtoken + "'",}
response = requests.request("GET", url, headers=headers, data=payload)

ordersdata = response.json()
#print(ordersdata)
orders = []
status = []
for_packing = []
incomplete = []
done = []
abort = "xxx"
error = 0
for s in range (len(ordersdata)):
    id = ordersdata[s]['id']

    orders.append(id)
#print(orders)
for a in range (len(orders)):
    stat = ordersdata[a]['status']

    status.append(stat)
#print(status)

for (index, item) in enumerate(status):

  if item == "processing":

    for_packing.append(index)

#print(for_packing)
# now we know which orders are ready for packing

os.system("clear")
for x in range (len(for_packing)):
    print("Order number " + str(orders[x]) + ": " + '\n')
    for y in range(len(ordersdata[x]["line_items"])):
        idx = "Product: " + ordersdata[x]["line_items"][y]['name'] + " Quantity: " + \
              "\033[1m" + str(ordersdata[x]["line_items"][y]["quantity"]) +\
              " SKU: " + str(ordersdata[x]["line_items"][y]["sku"]) + "\033[0m"+ '\n'
        print(idx)
    input("\033[1m" + "SCAN something to continue..."+ "\033[0m")

# Start packing
os.system("clear")
print('\n' + '\033[92m' + "\033[1m" + " Please Pack: " + "\033[0m" + '\n')
for x in range (len(for_packing)):
    error = 0
    print("Order number: " + str(orders[x])  + '\n')
    print("Scan Item: " + '\n')
    for y in range(len(ordersdata[x]["line_items"])):

        packid = "Product: " + ordersdata[x]["line_items"][y]['name'] + " Quantity: " + \
              "\033[1m" + str(ordersdata[x]["line_items"][y]["quantity"]) +\
              " SKU: " + str(ordersdata[x]["line_items"][y]["sku"]) + "\033[0m" + '\n'
        print(packid)
        for q in range(ordersdata[x]["line_items"][y]["quantity"]):

            item = ordersdata[x]["line_items"][y]["sku"]
            scan = input("Scan Item: " + ordersdata[x]["line_items"][y]['name'] + " # " + str(q + 1) + '\n')
            while scan != item:
                print('\033[91m' + "!!! incorrect item !!!" + "\033[0m")
                scan = input("Scan Item: " + ordersdata[x]["line_items"][y]['name'] + " # " + str(q + 1) + '\n')

                if scan == abort:
                    print('\033[91m' + "packing aborted" + "\033[0m")
                    incomplete.append( " Order: " + str(orders[x]) + " " + ordersdata[x]["line_items"][y]['name'] + " # " + str(q + 1))


                    error = 1

                    break

                if scan == item:
                    print("correct item picked")
                    continue

    os.system('clear')

    print('\033[92m' +"Order number " + str(orders[x]) + " completed!" + '\n' + "\033[0m")
    done.append(str(orders[x]))
    print(done)
    if error == 1:
        done.remove(str(orders[x]))


if incomplete != []:
    print( '\033[91m' + " incomplete Orders: " + str(incomplete) + "\033[0m" )
    print("Make sure to pack these orders ASAP!")
elif incomplete == []:
    print('\033[92m' +"Congratulations all orders are packed"  + '\n' + "\033[0m")
print("the Smander API currently does not allow directly updating orders,"+ "\n" + "please log in and mark the packed orders as shipped and send the tracking Codes to the customers")

save = input("Do you want to save this to the protocol?(y/n) : ")
if save =="y":

    print("\n" + "printing the protocoll:")
    output = "\n" + "INCOMPLETE Orders: "+ str(incomplete) + "\n" + "Completed Orders: " + str(done)+ "\n"
    print(output)
    today = date.today()
    f = open("protocol.txt", "a")
    f.write(str(today))
    f.write("\n")
    f.write(output)
    f.write("\n")
    f.close()
    print = input("Do you want to print the protocol?(y/n) : ")
    if print == "y":
        os.system("lpr protocol.txt")
