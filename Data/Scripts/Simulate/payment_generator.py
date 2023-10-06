"""
    This script generates fake payment transaction id
    in two style swift and aba.

    Dependencies:
        - fake library (install using 'pip install fake')

"""
import random

from faker import Faker

fake_payment = Faker()

PAYMENT_STATUS = ['Successful', 'Unsuccessful']  # TODO remove it


def generate_transaction_id() -> str:
    """
    This function generates two kinds of transaction ids then randomly choice one of them.

    Returns
    -------
    str
        Transaction id.
    """
    transaction_id = [fake_payment.unique.aba(), fake_payment.unique.swift()]
    return random.choice(transaction_id)


def generate_payment_info_dict(payment_id: int,
                               customer_id: int,
                               trip_amount: int,
                               payment_status: str,
                               transaction_id: str,
                               transaction_time: str) -> dict:
    """
    This function creates a dictionary of payment information.

    Parameters
    ----------
    payment_id: int
    customer_id: int
    trip_amount: int
    payment_status: str
    transaction_id: str
    transaction_time: str

    Returns
    -------
    dict
        A dictionary contain payment information
    """

    return {
        "payment_id": payment_id,
        "customer_id": customer_id,
        "trip_amount": trip_amount,
        "transaction_id": transaction_id,
        "transaction_time": transaction_time,
        "status": payment_status
    }


if __name__ == "__main__":
    transactionId = generate_transaction_id()
    print(type(transactionId))
