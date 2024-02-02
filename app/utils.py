def calculate_change(money):
    """
    Create an array of coins for change
    """
    change = []
    for coin in (100, 50, 20, 10, 5):
        if coin <= money:
            change.append(coin)
            money -= coin
        else:
            continue
    return change
