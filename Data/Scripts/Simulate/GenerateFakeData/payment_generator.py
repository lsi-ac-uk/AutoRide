"""
    This script generates fake payment transaction id
    in two style swift and aba.

    Dependencies:
        - fake library (install using 'pip install fake')

"""
import datetime
import random
import string
import uuid

from faker import Faker

fake_payment = Faker()

PAYMENT_STATUS = ['Successful']


def generate_random_id(length=10):
    """Generates a random ID of the specified length.

    Args:
      length: The length of the ID to generate.

    Returns:
      A random ID of the specified length.
    """

    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for i in range(length))


def generate_transaction_id():
    """Generates a random transaction ID.

    Returns:
      A random transaction ID.
    """

    prefix = 'txn_'
    random_id = generate_random_id(length=16)
    return prefix + random_id


def generate_payment_info_dict(payment_id: uuid,
                               customer_id: uuid,
                               trip_amount: uuid,
                               payment_status: str,
                               transaction_id: str,
                               transaction_time: datetime.datetime) -> dict:
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
        "PaymentId": payment_id,
        "CustomerId": customer_id,
        "TripAmount": trip_amount,
        "TransactionId": transaction_id,
        "TransactionTime": transaction_time,
        "Status": payment_status
    }


if __name__ == "__main__":
    transactionId = generate_transaction_id()
    print(type(transactionId))
