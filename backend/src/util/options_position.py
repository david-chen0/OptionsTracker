from datetime import datetime
from enum import Enum

class ContractType(Enum):
    """
    Represents the possible contract types
    """
    CALL = "call"
    PUT = "put"

class PositionStatus(Enum):
    """
    Represents the possible statuses of our position
    """
    OPEN = "open"
    CLOSED = "closed"
    EXPIRED = "expired"
    EXERCISED = "exercised"

class OptionsPosition:
    """
    Represents an options position for an underlying security.

    Attributes:
        ticker (str): The ticker symbol(ex: AAPL) for the underlying security
        contract_type (ContractType): The type of contract
        quantity (int): The number of contracts opened
        strike_price (float): The strike price of the contracts
        expiration_date (str): The expiration date of the contracts, represented as YYYY-MM-DD
        premium (float): The premium per security for each of the contracts
        open_price (float): The price of the underlying security when the contract was opened
        open_date (str): The date that the contract was opened, represented as YYYY-MM-DD
        contract_status (PositionStatus): The status of the options position
    """

    ticker: str
    contract_type: ContractType
    quantity: int
    strike_price: float
    expiration_date: str
    premium: float
    open_price: float
    open_date: str
    position_status: PositionStatus

    # Unimplemented for now, uncomment when you come around to implementing this
    # ex: sold call on X, strike price 95, premium 1, expired at 100. profit = 1 + 95 - 100 = -4
    # we could also not store this as a value but instead have it calculated with a method
    # profit: float

    def __init__(
        self,
        ticker: str,
        contract_type: ContractType,
        quantity: int,
        strike_price: float,
        expiration_date: str,
        premium: float,
        open_price: float,
        open_date: str,
        position_status: PositionStatus
    ):
        # Validating that expiration date and open date fit the YYYY-MM-DD format
        self.__validate_date_format(expiration_date)
        self.__validate_date_format(open_date)

        self.ticker = ticker.upper()
        self.contract_type = contract_type
        self.quantity = quantity
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.premium = premium
        self.open_price = open_price
        self.open_date = open_date
        self.position_status = position_status

    def to_dict(self):
        """
        Converts current options position to a dictionary format so that it can be saved to JSON format
        """
        return {
            "ticker": self.ticker,
            "contract_type": self.contract_type.value,
            "quantity": self.quantity,
            "strike_price": self.strike_price,
            "expiration_date": self.expiration_date,
            "premium": self.premium,
            "open_price": self.open_price,
            "open_date": self.open_date,
            "position_status": self.position_status.value
        }

    def __validate_date_format(self, date_str: str):
        """
        Validates that a date string is in 'YYYY-MM-DD' format and raises a ValueError if it isn't.
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Date '{date_str}' is not in the format 'YYYY-MM-DD'.")
        
    def is_expired(self) -> bool:
        """
        Returns whether the contract is expired.
        """
        is_expired = datetime.now().date() > datetime.strptime(self.expiration_date, '%Y-%m-%d')
        if (is_expired):
            print("Implement getting the price here and then setting the option to either ITM or OTM")
        return is_expired
    
    def update_expiry_status(self, underlying_expiration_price: float):
        """
        Updates the contract status for a newly expired contract given the price of the underlying asset at expiry
        """
        if (self.contract_type == ContractType.CALL and underlying_expiration_price > self.strike_price) or \
            (self.contract_type == ContractType.PUT and underlying_expiration_price < self.strike_price):
            self.position_status = PositionStatus.EXERCISED
        else:
            self.position_status = PositionStatus.EXPIRED
    
    def calculate_profit(self) -> float:
        raise NotImplementedError("TODO: Implement this method")
        
def get_options_position(inputs: dict) -> OptionsPosition:
    return OptionsPosition(
        inputs["ticker"],
        ContractType[inputs["contract_type"].lower()],
        inputs["quantity"],
        inputs["strike_price"],
        inputs["expiration_date"],
        inputs["premium"],
        inputs["open_price"],
        inputs["open_date"],
        PositionStatus[inputs["position_status"].lower()]
    )
