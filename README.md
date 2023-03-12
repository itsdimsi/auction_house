# THOUGHT MACHINE Programming Test - Auction House

## Directory Information

This directory contains the following files:

1. `auction.py`: The main script for the auction house poject.
2. `input.txt`: An input file containing sample input for the auction house project.
3. `output.txt`: An output file containing the expected output for the sample input in input.txt.
4. `test_auction.py`: A pytest file containing tests for the auction house program, including edge cases.
5. `test/`: A directory containing input files for the pytest cases in `test_auction.py`.
6. `requirements.txt`: Text recording the required libraries to run the program

## Summary of the code

This code processes an input file containing information about sell and bid events for different items, and performs data manipulation on the input data to extract information about each item.

The code first initializes two empty pandas dataframes named df1 and df2, each with specific columns for the sell and bid events, respectively. It then defines a function named text_preprocessing() that reads in the input file, preprocesses the data, and populates the df1 and df2 dataframes with the corresponding data.

The code then defines a function named data_manipulation() that calls the text_preprocessing() function to obtain the sells and bids dataframes, manipulates the data by merging the two dataframes, filtering rows based on time constraints, grouping the resulting dataframe by item, and computing relevant item information such as bid counts, status, highest and lowest bids, paid price, etc. The computed information is stored in a dictionary named item_dict.

Finally, the code defines a function named format_output() that formats the item information stored in the item_dict dictionary into an output string for each item, which is then stored in a list named output. The output list contains the formatted output strings for each item in the input file

## Assumption

1. There are always users that are selling products.
2. There are no equal bids.

## Prerequisites
Before running the main.py script, ensure that you have installed the necessary packages. 
You can do this by running the following command in your terminal:
``
pip install -r requirements.txt
``

## Usage

To run the main script and produce the output, simply run the auction.py script with the path to the input file as the argument. For example:

`python auction.py input.txt`

To run the pytests simply run in the terminal:

`pytest test_auction.py input.txt` 

you can use your own path.