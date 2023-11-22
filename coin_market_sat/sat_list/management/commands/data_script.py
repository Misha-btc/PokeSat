from django.core.management.base import BaseCommand
from sat_list.models import Transaction, Sat
from dateutil import parser

import requests


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        response = requests.get('https://api-mainnet.magiceden.dev/v2/ord/btc/activities?collectionSymbol=rare-sats&kind=buying_broadcasted', headers=headers)  # URL вашего API
        data = response.json()
        filtered_first = [
            activity for activity in data['activities']
            if any(nakamoto in sub for sub in activity.get('satributes', []))
        ]
        for activity in filtered_first:
            sublists = activity.get('satributes', [])

            num_sublists = len(sublists)
            contains_nakamoto = any(nakamoto in sub_list for sub_list in sublists)
            contains_not_nakamoto = any(any(item not in [nakamoto] for item in sub_list) for sub_list in sublists)
            if contains_nakamoto and not contains_not_nakamoto:
                new_owner = activity.get('newOwner')
                price = activity.get('listedPrice')
                satribute_amount = activity.get('satributesAmount')
                date = activity.get('createdAt')
                nakamoto_dict[activity.get('txId')]= {
                    'New Owner': new_owner,
                    'Listed Price': price,
                    'Satribute': satribute_amount,
                    'Date': date
                }

        general_dict[nakamoto] = nakamoto_dict
                
                
        general_dict[nakamoto] = nakamoto_dict
        #перебор словаря накамото в общем словаре
        #for key, value in general_dict[nakamoto].items():
            #print(f"Key: {key}, Values: {value}")


        ##################################.PALINDROME.##############################
        filtered_palindrome = [
            activity for activity in data['activities']
            if any(palindrome in sub for sub in activity.get('satributes', []))
        ]

        for activity in filtered_palindrome:
            sublists = activity.get('satributes', [])
            num_sublists = len(sublists)
            contains_palindrom = any(palindrome in sub_list for sub_list in sublists)
            contains_not_palindrome = any(any(item not in [common, palindrome] for item in sub_list) for sub_list in sublists)
            if num_sublists <= 2 and contains_palindrom and not contains_not_palindrome:
                new_owner = activity.get('newOwner')
                price = activity.get('listedPrice')
                satribute_amount = activity.get('satributesAmount')
                date = activity.get('createdAt')
                palindrome_dict[activity.get('txId')]= {
                    'New Owner': new_owner,
                    'Listed Price': price,
                    'Satribute': satribute_amount,
                    'Date': date
                }

        general_dict[palindrome] = palindrome_dict

        ####################################.BLOCK9.##################################
        filtered_block9 = [
            activity for activity in data['activities']
            if any(block9 in sub for sub in activity.get('satributes', []))
        ]

        for activity in filtered_block9:
            sublists = activity.get('satributes', [])
            num_sublists = len(sublists)
            contains_block9 = any(block9 in sub_list for sub_list in sublists)
            contains_not_block9 = any(any(item not in [common, block9, first_transaction, vintage, nakamoto] for item in sub_list) for sub_list in sublists)
            if num_sublists <= 2 and contains_block9 and not contains_not_block9:
                new_owner = activity.get('newOwner')
                price = activity.get('listedPrice')
                satribute_amount = activity.get('satributesAmount')
                date = activity.get('createdAt')
                block9_dict[activity.get('txId')]= {
                    'New Owner': new_owner,
                    'Listed Price': price,
                    'Satribute': satribute_amount,
                    'Date': date
                }

        general_dict[block9] = block9_dict

        ##################################.VINTAGE.################################

        filtered_vintage = [
            activity for activity in data['activities']
            if any(vintage in sub for sub in activity.get('satributes', []))
        ]
        for activity in filtered_vintage:
            sublists = activity.get('satributes', [])
            num_sublists = len(sublists)
            contains_vintage = any(vintage in sub_list for sub_list in sublists)
            contains_not_vintage = any(any(item not in [vintage] for item in sub_list) for sub_list in sublists)
            if num_sublists <= 2 and contains_vintage and not contains_not_vintage:
                new_owner = activity.get('newOwner')
                price = activity.get('listedPrice')
                satribute_amount = activity.get('satributesAmount')
                date = activity.get('createdAt')
                vintage_dict[activity.get('txId')]= {
                    'New Owner': new_owner,
                    'Listed Price': price,
                    'Satribute': satribute_amount,
                    'Date': date
                }

        general_dict[vintage] = vintage_dict

        #######################################.PIZZA.###############################

        filtered_pizza = [
            activity for activity in data['activities']
            if any(pizza in sub for sub in activity.get('satributes', []))
        ]
        for activity in filtered_pizza:
            sublists = activity.get('satributes', [])
            num_sublists = len(sublists)
            contains_pizza = any(pizza in sub_list for sub_list in sublists)
            contains_not_pizza = any(any(item not in [pizza] for item in sub_list) for sub_list in sublists)
            if num_sublists <= 2 and contains_pizza and not contains_not_pizza:
                new_owner = activity.get('newOwner')
                price = activity.get('listedPrice')
                satribute_amount = activity.get('satributesAmount')
                date = activity.get('createdAt')
                pizza_dict[activity.get('txId')]= {
                    'New Owner': new_owner,
                    'Listed Price': price,
                    'Satribute': satribute_amount,
                    'Date': date
                }

        general_dict[pizza] = pizza_dict

        ########################################.UNCOMMON.############################

        filtered_uncommon = [
            activity for activity in data['activities']
            if any(uncommon in sub for sub in activity.get('satributes', []))
        ]
        for activity in filtered_uncommon:
            sublists = activity.get('satributes', [])
            num_sublists = len(sublists)
            contains_uncommon = any(uncommon in sub_list for sub_list in sublists)
            contains_not_uncommon = any(any(item not in [uncommon, common] for item in sub_list) for sub_list in sublists)
            if num_sublists <= 2 and contains_uncommon and not contains_not_uncommon:
                new_owner = activity.get('newOwner')
                price = activity.get('listedPrice')
                satribute_amount = activity.get('satributesAmount')
                date = activity.get('createdAt')
                uncommon_dict[activity.get('txId')]= {
                    'New Owner': new_owner,
                    'Listed Price': price,
                    'Satribute': satribute_amount,
                    'Date': date
                }

        general_dict[uncommon] = uncommon_dict

        ##################################.BLOCK78.####################################

        filtered_block78 = [
            activity for activity in data['activities']
            if any(block78 in sub for sub in activity.get('satributes', []))
        ]
        for activity in filtered_block78:
            sublists = activity.get('satributes', [])
            num_sublists = len(sublists)
            contains_block78 = any(block78 in sub_list for sub_list in sublists)
            contains_not_block78 = any(any(item not in [block78, vintage] for item in sub_list) for sub_list in sublists)
            if num_sublists <= 2 and contains_block78 and not contains_not_block78:
                new_owner = activity.get('newOwner')
                price = activity.get('listedPrice')
                satribute_amount = activity.get('satributesAmount')
                date = activity.get('createdAt')
                block78_dict[activity.get('txId')]= {
                    'New Owner': new_owner,
                    'Listed Price': price,
                    'Satribute': satribute_amount,
                    'Date': date
                }

        general_dict[block78] = block78_dict

        ###################################.RARE.################################

        filtered_rare = [
            activity for activity in data['activities']
            if any(rare in sub for sub in activity.get('satributes', []))
        ]
        for activity in filtered_rare:
            sublists = activity.get('satributes', [])
            num_sublists = len(sublists)
            contains_rare = any(rare in sub_list for sub_list in sublists)
            if num_sublists <= 2 and contains_rare:
                new_owner = activity.get('newOwner')
                price = activity.get('listedPrice')
                satribute_amount = activity.get('satributesAmount')
                date = activity.get('createdAt')
                rare_dict[activity.get('txId')]= {
                    'New Owner': new_owner,
                    'Listed Price': price,
                    'Satribute': satribute_amount,
                    'Date': date
                }

        general_dict[rare] = rare_dict

        ###################################.BLACK UNCOMMON.##########################

        filtered_black = [
            activity for activity in data['activities']
            if any(black in sub for sub in activity.get('satributes', []))
        ]
        for activity in filtered_black:
            sublists = activity.get('satributes', [])
            num_sublists = len(sublists)
            contains_black = any(black in sub_list for sub_list in sublists)
            contains_not_black = any(any(item not in [black, common] for item in sub_list) for sub_list in sublists)
            if num_sublists <= 2 and contains_black and not contains_not_black:
                new_owner = activity.get('newOwner')
                price = activity.get('listedPrice')
                satribute_amount = activity.get('satributesAmount')
                date = activity.get('createdAt')
                black_dict[activity.get('txId')]= {
                    'New Owner': new_owner,
                    'Listed Price': price,
                    'Satribute': satribute_amount,
                    'Date': date
                }

        general_dict[black] = black_dict

        ###################################.BLACK RARE.##########################

        filtered_black_rare = [
            activity for activity in data['activities']
            if any(black_rare in sub for sub in activity.get('satributes', []))
        ]
        for activity in filtered_black_rare:
            sublists = activity.get('satributes', [])
            print(sublists)
            num_sublists = len(sublists)
            contains_black_rare = any(black_rare in sub_list for sub_list in sublists)
            if num_sublists <= 2 and contains_black_rare:
                new_owner = activity.get('newOwner')
                price = activity.get('listedPrice')
                satribute_amount = activity.get('satributesAmount')
                date = activity.get('createdAt')
                black_rare_dict[activity.get('txId')]= {
                    'New Owner': new_owner,
                    'Listed Price': price,
                    'Satribute': satribute_amount,
                    'Date': date
                }
        general_dict[black_rare] = black_rare_dict

        for satrib, trans in general_dict.items():
            for _, trans_data in trans.items():
                sat_instance = Sat.objects.get(satribute=satrib)
                first_satribute = int(trans_data['Satribute'][0])
                parsed_date = parser.parse(trans_data['Date'])
                transaction, created = Transaction.objects.get_or_create(
                    date=parsed_date,
                    defaults={
                        'new_owner': trans_data['New Owner'],
                        'listed_price': trans_data['Listed Price'],
                        'date': parsed_date,
                        'satribute_amount': first_satribute,
                        'satribute': satrib,
                        'sat': sat_instance
                    }
                )
                if created:
                    transaction.save()

headers = {
    'Authorization': 'Bearer 5004ff5b-bb45-46e0-b84c-06f5bb79a2f9'
}

nakamoto = 'Nakamoto'
block78 = 'Block 78'
vintage = 'Vintage'
common = 'Common'
palindrome = 'Palindrome'
block9 = 'Block 9'
pizza = 'Pizza'
uncommon = 'Uncommon'
rare = 'Rare'
black = 'Black Uncommon'
black_rare = 'Black Rare'
first_transaction = 'First Transaction'


# Списоки для хранения актуальных данных.

general_dict = {}

block9_dict = {}
palindrome_dict = {}
vintage_dict = {}
pizza_dict = {}
uncommon_dict = {}
nakamoto_dict = {}
block78_dict = {}
rare_dict = {}
black_dict = {}
black_rare_dict = {}
