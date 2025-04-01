CREATE SEQUENCE IF NOT EXISTS current_position_id START WITH 1 INCREMENT BY 1;


CREATE TABLE IF NOT EXISTS option_positions (
    position_id INT PRIMARY KEY,
    ticker TEXT NOT NULL,
    contract_type TEXT NOT NULL,
    quantity INT NOT NULL,
    strike_price NUMERIC(10, 2) NOT NULL,
    expiration_date DATE NOT NULL,
    is_expired BOOLEAN NOT NULL,
    premium NUMERIC(10, 2) NOT NULL,
    open_price NUMERIC(10, 2) NOT NULL,
    open_date DATE NOT NULL,
    position_status TEXT NOT NULL,
    close_price NUMERIC(10, 2)
);

CREATE INDEX IF NOT EXISTS idx_expiration_date ON option_positions (expiration_date);
CREATE INDEX IF NOT EXISTS idx_is_expired_true ON option_positions (position_id) WHERE is_expired = TRUE;
CREATE INDEX IF NOT EXISTS idx_is_expired_false ON option_positions (position_id) WHERE is_expired = FALSE;
