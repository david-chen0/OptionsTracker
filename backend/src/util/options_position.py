from datetime import date, datetime
from enum import Enum
from src.data.data_fetcher import *

class ContractType(Enum):
    """
    Represents the contract type of the position
    """
    CALL = "call"
    PUT = "put"

class TradeDirection(Enum):
    """
    Represents the trade direction of the position
    """
    LONG = "long"
    SHORT = "short"

class PositionStatus(Enum):
    """
    Represents the current status of the position
    """
    OPEN = "open"
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
        trade_direction (TradeDirection): The direction of the position
        strike_price (float): The strike price of the contracts
        expiration_date (date): The expiration date of the contracts, represented as YYYY-MM-DD
        is_expired (bool): Represents whether the position is expired
        premium (float): The premium per security for each of the contracts
        open_price (float): The price of the underlying security when the contract was opened
        open_date (date): The date that the contract was opened, represented as YYYY-MM-DD
        position_status (PositionStatus): The status of the options position
        close_price (float): The price of the underlying security when the contract closed, set to -1 when the contract is still active
        profit (float): The total profit from this position, set to -1 when the contract is still active(change when we support current prices)
        current_price (float): The current price of the option, set to -1 for expired contracts
        blind_init (bool): Indicates if we are creating the option blind, which means we have to retrieve information like current price, underlying asset price, etc

    Attributes that are retrieved during blind init(don't use blind init if you are setting any of these):
        position_status
        close_price
        profit
        current_price

    Attributes in the object but not stored in the DB:
        current_price
    """

    position_id: int
    ticker: str
    contract_type: ContractType
    quantity: int
    trade_direction: TradeDirection
    strike_price: float
    expiration_date: date
    is_expired: bool
    premium: float
    open_price: float
    open_date: date
    position_status: PositionStatus
    close_price: float
    profit: float
    current_price: float

    def __init__(
        self,
        position_id: int,
        ticker: str,
        contract_type: ContractType,
        quantity: int,
        trade_direction: TradeDirection,
        strike_price: float,
        expiration_date: date,
        premium: float,
        open_price: float,
        open_date: date,
        position_status: PositionStatus = PositionStatus.OPEN,
        close_price: float = None,
        profit: float = None,
        current_price: float = -1,
        blind_init = True
    ):
        # Pre-checks to make sure the arguments make sense
        if not open_date < expiration_date:
            raise Exception("The position's open date must be before the expiration date")
        if not premium > 0:
            raise Exception("The option premium must be positive")
        if not quantity > 0:
            raise Exception("Quantity must be positive")

        self.position_id = position_id
        self.ticker = ticker.upper()
        self.contract_type = contract_type
        self.quantity = quantity
        self.trade_direction = trade_direction
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.is_expired = datetime.now().date() > expiration_date
        self.premium = premium
        self.open_price = open_price
        self.open_date = open_date

        # Fields that are not stored in the DB, needs to be set first, otherwise objects created using the DB will have these fields set to None
        if not self.is_expired:
            self.current_price = get_current_option_price(self.ticker, self.expiration_date, self.strike_price, self.contract_type == ContractType.CALL)
        else:
            self.current_price = -1

        # Fields that are stored in the DB
        if not blind_init:
            self.position_status = position_status
            self.close_price = close_price
            self.profit = profit
        elif not self.is_expired:
            self.update_active_contract()
        else:
            underlying_price = get_security_closing_price(self.ticker, expiration_date)
            self.update_position_at_maturity(underlying_price)
    
    def __json__(self) -> dict:
        """
        Converts current options position to a dictionary format so that it can be saved to JSON format
        """
        return {
            "position_id": self.position_id,
            "ticker": self.ticker,
            "contract_type": self.contract_type.name,
            "quantity": self.quantity,
            "trade_direction": self.trade_direction.name,
            "strike_price": self.strike_price,
            "expiration_date": self.expiration_date.isoformat(),    
            "is_expired": self.is_expired,
            "premium": self.premium,
            "open_price": self.open_price,
            "open_date": self.open_date.isoformat(),
            "position_status": self.position_status.name,
            "close_price": self.close_price,
            "profit": self.profit,
            "current_price": self.current_price
        }
    
    def update_position_id(self, position_id: int):
        """
        Updates the position_id. This should only be used when creating new positions, as we don't know the position_id until we access the DB.
        """
        print(f"Updating the position_id of {self.position_id} to {position_id}")
        self.position_id = position_id

    def update_active_contract(self):
        """
        Retrieves the current price of the active contract and updates the position accordingly
        """
        self.position_status = PositionStatus.OPEN
        self.current_price = get_current_option_price(self.ticker, self.expiration_date, self.strike_price, self.contract_type == ContractType.CALL)
        self.profit = self.calculate_profit()
        self.close_price = -1
    
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
        self.profit = self.calculate_profit()
        self.current_price = -1 # Setting current price to -1 for expired contracts
    
    def calculate_profit(self) -> float:
        """
        Returns the total profit of the position.
        """
        profit_per_underlying = 0 # So profit per contract is 100 times this
        if self.position_status == PositionStatus.OPEN:
            profit_per_underlying = self.current_price - self.premium
        else:
            price_diff = self.close_price - self.strike_price
            profit_per_underlying = -1 * self.premium

            if self.contract_type == ContractType.CALL:
                profit_per_underlying += max(price_diff, 0)
            elif self.contract_type == ContractType.PUT:
                profit_per_underlying += max(-1 * price_diff, 0)
            else:
                raise ValueError(f"Unsupported contract type: {self.contract_type}")
        
        return self.quantity * profit_per_underlying * 100 * (1 if self.trade_direction == TradeDirection.LONG else -1)

# TODO: I just slapped this in here since I can't put it into common, since it'll create a circular dependency
# figure out where to put it
def string_to_date(date_str: str) -> date:
    """
    Converts a date string with the YYYY-MM-DD format into a date object.

    A ValueError will be thrown if the string is not able to be converted
    """
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def blind_create_options_position(inputs: dict) -> OptionsPosition:
    """
    Creates and returns an option position using the input dictionary.

    Creation is blind, which means that we don't have certain pieces of information such as current price of the underlying asset or the option.

    This should be used over OptionsPosition(**inputs) because the constructor has some special checks.
    """
    position_id = -1 if "position_id" not in inputs.keys() else inputs["position_id"]
    expiration_date = string_to_date(inputs["expiration_date"])
    open_date = string_to_date(inputs["open_date"])

    # String checks are because conversions from JavaScript causes many variables to be stored as strings
    contract_type = inputs["contract_type"].upper()
    quantity = inputs["quantity"]
    trade_direction = inputs["trade_direction"].upper()
    strike_price = inputs["strike_price"]
    premium = inputs["premium"]
    open_price = inputs["open_price"]

    if isinstance(contract_type, str):
        contract_type = ContractType[contract_type]

    if isinstance(quantity, str):
        quantity = float(quantity)

    if isinstance(trade_direction, str):
        trade_direction = TradeDirection[trade_direction]

    if isinstance(strike_price, str):
        strike_price = float(strike_price)

    if isinstance(open_price, str):
        open_price = float(open_price)

    if isinstance(premium, str):
        premium = float(premium)

    return OptionsPosition(
        position_id,
        inputs["ticker"],
        contract_type,
        quantity,
        trade_direction,
        strike_price,
        expiration_date,
        premium,
        open_price,
        open_date,
        blind_init = True
    )
