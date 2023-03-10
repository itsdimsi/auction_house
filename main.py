print ("hello world")

x = open("newfile.txt")



# sell = {"toaster_id":[10,20,10.00,'maxbidder']}
# bids = {
#     "toaster_id":
#             {
#             "user1": [10,11,13],
#             "user2": [8]
#             }
# }
# columns ...
# toaster_id user_id auction
# toaster_id , 5  , 100 , bid
#  toaster_id , 10  , 70 ,sell


sell = {}
bids = {}

for line in x:

    item = line.strip().split('|')
    if item[1] == "SELL":
        sell[item[2]] = [item[0], item[3], item[4], "maxbidder"]
    elif item[1] == "BID":
        if item[3] not in bids:
            bids[item[3]] = {}
            bids[item[3]][item[1]] = [item[4]]

        elif item[3] in bids:
            if item[4] in bids[item[3]]:
                "update the dictionary"
            else:
                "update different the dictionary"


for new_item  in sell:
    print ("asdasd")

#  toaster_id , 10  , 70 ,sell
# toaster_id , 5  , 100 , bid


# newdict = {
#     "toaster1": ["count_bid","maxbidder",sell_price,100,35,345,46,57,6868],
#      ...  .
#      }
#
# if bid > toaster[-1]:
#     maxbidder = item[1]
#
# count+1
#
# if timer< end_time and bid>toaster[-1]:
#     "update"
#



# if len(toaster) == 3:
#     "UNSOLD"