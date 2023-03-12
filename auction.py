# Import pandas library to work with dataframes
import pandas as pd
import argparse
# Initialize an empty dataframe with the columns required for the sell and bid events
df1 = pd.DataFrame(columns=['timestamp', 'user_id', 'action', 'item', 'reserve_price', 'close_time'])
df2 = pd.DataFrame(columns=['timestamp', 'user_id', 'action', 'item', 'bid_amount'])

# Define a function to preprocess the input file
def text_preprocessing(file_path):
    global df1,df2
    # Open the input file
    input = open(file_path)
    # create an empty dictionary to store the user's previous bid_amount for each item
    user_item_bid = {}
    # Loop through each line in the input file
    for line in input:
        # Check if the line is not empty
        if len(line.strip()) > 2:
            # Split the line using the '|' delimiter and store it in the item variable
            item = line.strip().split('|')
            # If the action in the item is SELL, create a dictionary with the values and append it to df1
            if item[2] == "SELL":
                row_dict = {f'{df1.columns[i]}': item[i] for i in range(len(df1.columns))}
                df1 = df1.append(row_dict, ignore_index=True)
            # If the action in the item is not SELL, create a dictionary with the values and append it to df2
            else:
                bid_amount = float(item[-1])
                # check if the user has a previous bid_amount for the item
                if (item[1], item[3]) in user_item_bid:
                    if bid_amount < user_item_bid[(item[1], item[3])]:
                        continue  # skip the row if the bid_amount is lower than the previous bid_amount
                row_dict = {f'{df2.columns[i]}': item[i] for i in range(len(df2.columns))}
                df2 = df2.append(row_dict, ignore_index=True)
                user_item_bid[item[1], item[3]] = bid_amount
    # Return the two dataframes
    return df1, df2

# Define a function to perform data manipulation on the input file
def data_manipulation(file_path):
    # Call the text_preprocessing function to populate sells and bids with data from the input file
    sells, bids = text_preprocessing(file_path)

    # Rename the timestamp column in sells to open_time
    sells = sells.rename(columns={"timestamp": "open_time"})

    # Remove the user_id and action columns from sells
    sells = sells.drop(columns=["user_id", "action"], axis=1)

    # Merge sells and bids on the item column and keep only
    # the rows where the timestamps are within the open and close times
    valid = sells.merge(bids, on='item', how="inner")
    valid['bid_amount'] = valid['bid_amount'].astype(float)
    valid['reserve_price'] = valid['reserve_price'].astype(float)
    valid = valid.drop(valid[valid.apply(lambda row: (row['timestamp'] > row['close_time']) |\
                                                     (row['timestamp'] < row['open_time']), axis=1)].index)

    # Group the dataframe by item
    grouped = valid.groupby('item')
    # Initialize an empty dictionary to store the item information
    item_dict = {}
    # Iterate over the groups and add the item information to the dictionary
    for item, group in grouped:
        item_dict[item] = {}
        item_dict[item]['close_time'] = group['close_time'].values[0]
        item_dict[item]['total_bid_count'] = group['bid_amount'].count()
        item_dict[item]['status'] = 'UNSOLD' if group['bid_amount'].max() < group['reserve_price'].values[0] else 'SOLD'
        item_dict[item]['highest_bid'] = group['bid_amount'].max()
        item_dict[item]['lowest_bid'] = group['bid_amount'].min()
        item_dict[item]['user_id'] = valid.loc[group['bid_amount'].idxmax(), 'user_id'] if \
                                                            item_dict[item]['status'] == 'SOLD' else None
        if item_dict[item]['status'] == 'UNSOLD':
            item_dict[item]['paid_price'] = None
        elif len(group['bid_amount'].unique()) == 1:
            item_dict[item]['paid_price'] = group['reserve_price']
        else:
            second_max = group.sort_values(by='bid_amount',ascending=False).\
            drop_duplicates(subset='bid_amount')['bid_amount'].values[1]
            if second_max > group['reserve_price'].values[0]:
                item_dict[item]['paid_price'] = second_max
            else:
                item_dict[item]['paid_price'] = group['reserve_price'].values[0]

    # Return the dictionary containing the item information
    return item_dict

# Define a function to format the output string
def format_output(data):
    output = []
    # Iterate over the items in the dictionary and format the output string for each one
    for key, item in data.items():
        paid_price = f"{item['paid_price']:.2f}" if item['paid_price'] is not None else '0.00'
        output.append(f"{item['close_time']}|{key}|{item['user_id'] or ''}|"
                      f"{item['status']}|{paid_price}|"
                      f"{item['total_bid_count']}|{item['highest_bid']:.2f}|"
                      f"{item['lowest_bid']:.2f}")

    # Join the output strings with newline characters and return the result
    return '\n'.join(output)

def main(file_path):
    item_dict = data_manipulation(file_path)
    output = format_output(item_dict)
    with open('output.txt', 'w') as file:
        file.write(output)
    return output

# Call the main function if this script is being run directly
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', type=str, default='input.txt')
    args, unknown = parser.parse_known_args()
    main(args.file_path)