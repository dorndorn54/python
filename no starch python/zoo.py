import numpy as np

# global list for inputs
customer_age_list = []
price_dictionary = {
    "children": 0,
    "teenagers(13 - 17)": 10,
    "Adults(18 - 50)": 15,
    "seniors(above 50)": 5
}


def main():
    # receive constant user input and store it in custome_age
    while True:
        customer_age = input("what is the customers age: ")
        if customer_age == "":
            break
        customer_age_list.append(int(customer_age))

    # calculate ticket price before discount
    sum_ticket_price = calculate_ticket_price()
    if paying_count() >= 3:
        final_price = sum_ticket_price*0.9

    print(final_price)


def calculate_ticket_price():
    sum_ticket_price = 0
    for age in customer_age_list:
        if age < 13:
            continue
        elif age >= 13 and age < 17:
            sum_ticket_price += 10
        elif age >= 18 and age < 50:
            sum_ticket_price += 15
        elif age > 50:
            sum_ticket_price += 5
    return sum_ticket_price


def paying_count():
    return np.sum(np.array(customer_age_list) > 13)


main()
