from .models import Transaction

class ReportCalculator:
    """Returns a dictionary with data about transactions based on limit_amount provided"""

    def __init__(self, transactions, limit_amount):
        """Takes list of transactions to be used in calculations and a limit amount"""
        self.transactions = transactions
        self.limit_amount = limit_amount
        return self.generate_data()
    
    def generate_data(self):
        return {
            'total_spending': self.get_total_spending(),
            'limit_remaining': self.get_limit_remaining(),
            'percentage_of_limit_used': self.get_percentage_of_limit_used(),
            'percentage_of_limit_remaining': self.get_percentage_of_limit_remaining(),
            'is_below_limit': self.get_is_below_limit()
        }

    def get_total_spending(self):
        return sum([transaction.amount for transaction in self.transactions])

    def get_limit_remaining(self):
        return self.limit_amount - self.get_total_spending()
    
    def get_percentage_of_limit_used(self):
        return self.get_total_spending() / self.limit_amount

    def get_percentage_of_limit_remaining(self):
        return self.get_limit_remaining() / self.limit_amount
    
    def get_is_below_limit(self):
        return self.get_total_spending() < self.limit_amount

    



    