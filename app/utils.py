def is_deposited_right_amount(money: int):
    """
    Validate if right amount is deposited.
    """
    return money in (5, 10, 20, 50, 100)
