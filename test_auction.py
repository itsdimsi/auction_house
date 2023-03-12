import pytest
from auction import data_manipulation

def test_data_manipulation_with_no_valid_bids():
    # call the data_manipulation function with the sample data
    item_dict = data_manipulation('tests/no_valid_bid.txt')
    # check if the item is not sold
    assert item_dict['item1']['status'] == 'UNSOLD'
    # check if the paid price for the item is zero
    assert item_dict['item1']['paid_price'] == None


def test_data_manipulation_with_one_valid_bid():
    # call the data_manipulation function with the sample data
    item_dict = data_manipulation('tests/one_valid_bid.txt')
    # check if the paid price for the item is correct
    assert item_dict['item1']['paid_price'] == 150


def test_data_manipulation_with_multiple_valid_bids():
    # call the data_manipulation function with the sample data
    item_dict = data_manipulation('tests/multiple_valid_bid.txt')
    # check if the paid price for the item is correct
    assert item_dict['item1']['paid_price'] == 165

