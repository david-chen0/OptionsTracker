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
        position_id (int): The serial ID of this position in the DB
        ticker (str): The ticker symbol(ex: AAPL) for the underlying security
        contract_type (ContractType): The type of contract
        quantity (int): The number of contracts opened
        strike_price (float): The strike price of the contracts
        expiration_date (datetime): The expiration date of the contracts, represented as YYYY-MM-DD
        is_expired (bool): Represents whether the position is expired
        premium (float): The premium per security for each of the contracts
        open_price (float): The price of the underlying security when the contract was opened
        open_date (datetime): The date that the contract was opened, represented as YYYY-MM-DD
        position_status (PositionStatus): The status of the options position
        close_price (float): The price of the underlying security when the contract closed, set to -1 when the contract is still open
    """

    position_id: int
    ticker: str
    contract_type: ContractType
    quantity: int
    strike_price: float
    expiration_date: datetime
    is_expired: bool
    premium: float
    open_price: float
    open_date: datetime
    position_status: PositionStatus
    close_price: float

    # Unimplemented for now, uncomment when you come around to implementing this
    # ex: sold call on X, strike price 95, premium 1, expired at 100. profit = 1 + 95 - 100 = -4
    # we could also not store this as a value but instead have it calculated with a method
    # profit: float

    def __init__(
        self,
        position_id: int,
        ticker: str,
        contract_type: ContractType,
        quantity: int,
        strike_price: float,
        expiration_date: datetime,
        premium: float,
        open_price: float,
        open_date: datetime,
        position_status: PositionStatus = PositionStatus.OPEN,
        close_price: float = -1
    ):
        # check open date before expiration date
        
        # check positive premium

        self.position_id = position_id
        self.ticker = ticker.upper()
        self.contract_type = contract_type
        self.quantity = quantity
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.is_expired = datetime.now().date() > expiration_date
        self.premium = premium
        self.open_price = open_price
        self.open_date = open_date
        self.position_status = position_status
        self.close_price = close_price

    def to_dict(self):
        """
        Converts current options position to a dictionary format so that it can be saved to JSON format
        """
        return {
            "position_id": self.position_id,
            "ticker": self.ticker,
            "contract_type": self.contract_type.name,
            "quantity": self.quantity,
            "strike_price": self.strike_price,
            "expiration_date": self.expiration_date,
            "is_expired": self.is_expired,
            "premium": self.premium,
            "open_price": self.open_price,
            "open_date": self.open_date,
            "position_status": self.position_status.name,
            "close_price": self.close_price
        }
    
    def update_position_id(self, position_id: int):
        """
        Updates the position_id. This should only be used when creating new positions, as we don't know the position_id until we access the DB.
        """
        print(f"Updating the position_id of {self.position_id} to {position_id}")
        self.position_id = position_id
    
    def update_position_at_maturity(self, underlying_expiration_price: float):
        """
        Updates the newly expired position given the price of the underlying asset at expiry
        """
        underlying_expiration_price = float(underlying_expiration_price) # Prevents numpy floats from being used
        if (self.contract_type == ContractType.CALL and underlying_expiration_price > self.strike_price) or \
            (self.contract_type == ContractType.PUT and underlying_expiration_price < self.strike_price):
            self.position_status = PositionStatus.EXERCISED
        else:
            self.position_status = PositionStatus.EXPIRED
        self.close_price = underlying_expiration_price
    
    def calculate_profit(self) -> float:
        """
        Returns the total profit of the position.
        """
        if self.position_status == PositionStatus.OPEN:
            raise NotImplementedError("Position value has not been implemented for open positions yet")
        
        price_diff = self.close_price - self.strike_price
        profit_per_contract = -self.premium

        if self.contract_type == ContractType.CALL:
            profit_per_contract += max(price_diff, 0)
        elif self.contract_type == ContractType.PUT:
            profit_per_contract += max(-price_diff, 0)
        else:
            raise ValueError(f"Unsupported contract type: {self.contract_type}")
        
        return self.quantity * profit_per_contract
        
# TODO: frontend API calls add, which calls this, but expiration_date and open_date are still strings, not datetime
# figure out a way to make it into daytime. we could use datetime.strptime rn, but not sure if that's best way to do it
def create_options_position(inputs: dict) -> OptionsPosition:
    """
    Creates and returns an option position using the input dictionary.

    This should be used over OptionsPosition(**inputs) because the constructor has some special checks.
    """
    position_id = -1 if "position_id" not in inputs.keys() else inputs["position_id"]

    # String checks are because conversions from JavaScript causes many variables to be stored as strings
    contract_type = inputs["contract_type"].upper()
    quantity = inputs["quantity"]
    strike_price = inputs["strike_price"]
    position_status = inputs["position_status"].upper()
    open_price = inputs["open_price"]
    close_price = inputs["close_price"]

    if isinstance(contract_type, str):
        contract_type = ContractType[contract_type]

    if isinstance(quantity, str):
        quantity = float(quantity)

    if isinstance(strike_price, str):
        strike_price = float(strike_price)
        
    if isinstance(position_status, str):
        position_status = PositionStatus[position_status]

    if isinstance(open_price, str):
        open_price = float(open_price)

    if isinstance(close_price, str):
        close_price = float(close_price)

    return OptionsPosition(
        position_id,
        inputs["ticker"],
        contract_type,
        quantity,
        strike_price,
        inputs["expiration_date"],
        inputs["premium"],
        open_price,
        inputs["open_date"],
        position_status,
        close_price
    )
