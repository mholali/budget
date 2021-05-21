from decimal import Decimal # library for dealing with decimals
import math # for dealing with floor and ceiling divisions of numbers

class Category():
    ledger = [] # make ledger an attribute of the Class itself. becomes a global variable

    def __init__(self, budget_category): # Class constructor takes 1 argument. 'self' argument is the instance's name
        self.budget_category = budget_category
        self.ledger = Category.ledger # access to the global Class variable 'ledger'
    
    # function takes 2 arguments; one of them if optional. 'self' argument is the instance's name
    def deposit(self, amount_being_deposited, description_of_deposit=None): 
        self.amount_being_deposited = Decimal(amount_being_deposited)
        self.description_of_deposit = description_of_deposit

        self.ledger =[{
            "amount": Decimal(self.amount_being_deposited),
            "description": " " if description_of_deposit is None else str(self.description_of_deposit),
            }]

        return

    # function takes 2 arguments; one of them if optional. 'self' argument is the instance's name
    def withdraw(self, amount_being_withdrawn, description_of_withdrawal=None): 
        self.amount_being_withdrawn = Decimal(amount_being_withdrawn)
        self.description_of_withdrawal = description_of_withdrawal

        dictionary_of_withdrawals = {
            "amount": Decimal(self.amount_being_withdrawn * (-1)),
            "description": " " if description_of_withdrawal is None else str(self.description_of_withdrawal),
            }

        if Category.check_funds(self, amount_being_withdrawn):
            self.ledger.append(dictionary_of_withdrawals)
            return True
        else:
            return False
    
     # function takes no outside argument. 'self' argument is the instance's name
    def get_balance(self):
        return Decimal(sum(self.ledger[_]["amount"] for _ in range(len(self.ledger)))) # returns a sum of 'amounts'

    # function takes 2 arguments. 'self' argument is the instance's name           
    def transfer(self, transfer_amount, transfer_to_destination_budget_category):        

        if Category.check_funds(self, transfer_amount): # call check_fund method using instance's name for 'self' and 1 required argument
            
            dictionary_of_transfer_deposit = {
                "amount": Decimal(transfer_amount),
                "description": "Transfer from " + (self.budget_category),
                }

            transfer_to_destination_budget_category.ledger.append(dictionary_of_transfer_deposit)
                        
            dictionary_of_transfer_withdrawal = {
                "amount": Decimal(transfer_amount) * (-1),
                "description": "Transfer to " + (transfer_to_destination_budget_category.budget_category),
                }
          
            self.ledger.append(dictionary_of_transfer_withdrawal)
            
            return True
        else:
            return False

    # function takes 1 argument. 'self' argument is the instance's name
    def check_funds(self, transaction_amount): 
        self.transaction_amount = Decimal(transaction_amount)
        return self.transaction_amount <= Category.get_balance(self) # call get_balance method using instance's name for 'self' and no required argument. returns true if correct

    # function takes no argument. 'self' argument is the instance's name
    def ledger_items_printing(self): 
        string = ""
        self.string = string
        for _ in range(len(self.ledger)):
            self.string += f"{self.ledger[_]['description']:23.23}{self.ledger[_]['amount']:7.2f}"+'\n'
        return self.string        
    
    # function takes no argument. 'self' argument is the instance's name
    def __str__(self): 
        return (
            f"{self.budget_category:*^30}"+'\n'
            f"{Category.ledger_items_printing(self)}"
            f"{'Total: '}{Category.get_balance(self):.2f}"
            )

# function takes any number of arguments. the arguments coming are in a list format
def create_spend_chart(list_collection_of_categories_instances): 
    y_axis_values = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]

    # use of List objects to collate all the strings
    list_of_spent_percentatge_to_nearest_10 = []
    graph_text_strings_collection_header = []
    graph_text_strings_collection_o = []
    graph_text_strings_collection_lower = []

    graph_text_strings_collection_header.append(f"Percentage spent by category"+'\n')

    for _ in list_collection_of_categories_instances:
        categorys_total_withdrawals = (sum(Decimal(_['amount']) for _ in _.ledger if Decimal(_['amount']) < 0)) * (-1)

        spent_percentatge = Decimal(categorys_total_withdrawals) / Decimal(_.ledger[0]['amount'])

        spent_percentatge_to_nearest_10 = int(math.ceil(spent_percentatge * 10) * 10) # this approach used to convert to the nearest 10

        list_of_spent_percentatge_to_nearest_10.append(spent_percentatge_to_nearest_10)

    for _ in y_axis_values:
        graph_text_strings_collection_o.append(f"{str(_):>3}{'|'}")

        for each_value in list_of_spent_percentatge_to_nearest_10:

            if each_value == _:
                graph_text_strings_collection_o.append(f"{' o '}")
            else:
                graph_text_strings_collection_o.append(f"{'   '}")

            if each_value == list_of_spent_percentatge_to_nearest_10[:-1]:
                break

        graph_text_strings_collection_o.append('\n')

    # seek the location/indices of all ' o 's and make it into a list
    locations_of_o = [i_ndex for i_ndex, v_alue in enumerate(graph_text_strings_collection_o) if v_alue == ' o '] 

    # append ' o 's to all other locations based on the distance/sequence formula between each location
    all_locations_of_o = []
    for _ in range(len(locations_of_o)):
        sub_locations_of_o = []
        count = locations_of_o[_]
        while count <= len(graph_text_strings_collection_o):
            sub_locations_of_o.append(count)
            count += (len(list_collection_of_categories_instances) + 2)
        all_locations_of_o += sub_locations_of_o

    for _ in all_locations_of_o:
        graph_text_strings_collection_o[_] = ' o '

    graph_text_strings_collection_lower.append(f"{'    '}{'-' * 3 * len(list_collection_of_categories_instances)}{'-'}"+'\n' + f"{'    '}")

    categories_attributes_into_dict = [_.__dict__ for _ in list_collection_of_categories_instances]

    categories_names_into_list = [_['budget_category'] for _ in categories_attributes_into_dict]    

    for _ in range(len(max(categories_names_into_list, key=len))):
        for each_name in categories_names_into_list:
            if each_name[_:_+1]:
                graph_text_strings_collection_lower.append(f"{' ' + each_name[_:_+1] + ' '}")            

            else:
                graph_text_strings_collection_lower.append(f"{' ' + ' ' + ' '}")

        graph_text_strings_collection_lower.append('\n' + f"{'    '}")

    # return print(f"{'Header of graph = '}{graph_text_strings_collection_header}"'\n'
    #             f"{'Graph marks = '}{graph_text_strings_collection_o}"'\n'
    #             f"{'Horizontal axis = '}{graph_text_strings_collection_lower}")

    return (''.join(graph_text_strings_collection_header + graph_text_strings_collection_o + graph_text_strings_collection_lower))



###### WORKING TEST BENCH AREA ######
if __name__ == '__main__':
    fruits = Category("fruits")
    fruits.deposit(1500.65, "initial deposit")
    fruits.withdraw(45.78, "banana")
    fruits.withdraw(600.67, "pineapple")
    fruits.withdraw(14.78, "peach")
    fruits.withdraw(450.78, "raspberry")
    fruits.withdraw(78.78, "xxxxxxxxxx nnnnnnnnnnnnnnnnxxxxxxccccccccc")

    foods = Category("foods")
    foods.deposit(600.56, "initial deposit")
    foods.withdraw(12.45, "plantain")
    foods.withdraw(1.90, "garri")
    foods.withdraw(120.45, "yams")
    foods.withdraw(67.90, "jjjjjjjj bbbbbbb bbnxxyyyyyyycccc")

    drinks = Category("drinks")
    drinks.deposit(1256.34, "initial deposit")
    drinks.withdraw(478.78, "wine")

    frozen = Category("frozen")
    frozen.deposit(124.34, "initial deposit")
    frozen.withdraw(47.78, "peas")
    frozen.withdraw(7.78, "fish")
    frozen.withdraw(4.78, "yoghurt")

    foods.transfer(20.16, fruits)
    drinks.transfer(2.12, frozen)
    frozen.transfer(3.20, foods)

    print(foods)
    print(fruits)
    print(drinks)
    print(frozen)

    print(create_spend_chart([foods, fruits, drinks, frozen]))

    food = Category("Food")
    food.deposit(1000, "initial deposit")
    food.withdraw(10.15, "groceries")
    food.withdraw(15.89, "restaurant and more food for dessert")
    print(food.get_balance())

    clothing = Category("Clothing")
    food.transfer(50, clothing)
    clothing.withdraw(25.55)
    clothing.withdraw(100)

    auto = Category("Auto")
    auto.deposit(1000, "initial deposit")
    auto.withdraw(15)

    print(food)
    print(clothing)
    print(auto)

    print(create_spend_chart([food, clothing, auto]))