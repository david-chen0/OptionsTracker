import React, { useState, useEffect } from "react";
import { fetchOptionsPositions, addOptionsPosition } from "./api/optionsPositionsApi";

function App() {
    // Default form for the form to be reset to after AddPosition is called
    const defaultForm = {
        ticker: "",
        contract_type: "",
        quantity: "",
        strike_price: "",
        expiration_date: "",
        premium: "",
        open_price: "",
        open_date: ""
    }
    // List of all fields that must be filled out in the AddPosition form
    const requiredFields = [
        "ticker",
        "contract_type",
        "quantity",
        "strike_price",
        "expiration_date",
        "premium",
        "open_price",
        "open_date"
    ];

    // List corresponding to active positions
    const [activePositions, setActivePositions] = useState([]);

    // List corresponding to inactive positions
    const [inactivePositions, setInactivePositions] = useState([]);

    // Form for the user to input their addPosition data
    const [formData, setFormData] = useState(defaultForm);

    useEffect(() => {
        async function loadPositions() {
            try {
                // Fetching and setting active data
                const activeData = await fetchOptionsPositions(true);
                setActivePositions(activeData);
                
                // Fetching and setting inactive data
                const inactiveData = await fetchOptionsPositions(false);
                setInactivePositions(inactiveData);
            } catch (error) {
                console.error("Error fetching positions:", error);
            }
        }
        loadPositions();
    }, []);

    // Handles changes to the inputs
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
          ...prev,
          [name]: value,
        }));
    };

    // Handles when the AddPosition button is hit
    const handleAddPosition = async () => {
        try {
            const newPosition = { ...formData };

            // Checking to make sure all fields are filled out
            const missingFields = requiredFields.filter((field) => !formData[field]);
            if (missingFields.length > 0) {
                alert(`Please fill out all fields. Missing: ${missingFields.join(", ")}`);
                return;
            }

            // Default values since we don't allow user input for these fields
            newPosition["position_status"] = "Open";
            newPosition["close_price"] = -1;

            // TODO: Add verifications on the fields, ex: expiration date is a date, strike price is a number with at most 2 decimals, and more
            // verification should be done in backend rather than frontend
            await addOptionsPosition(newPosition);

            // TODO: Add a way to check if the newly added position is active or inactive, then just update that table instead of updating both

            // Fetch the updated active positions list from the backend and set the table accordingly
            const updatedActivePositions = await fetchOptionsPositions(true);
            setActivePositions(updatedActivePositions);

            // Fetch the updated inactive positions list from the backend and set the table accordingly
            const updatedInactivePositions = await fetchOptionsPositions(false);
            setInactivePositions(updatedInactivePositions);

            // Resetting the form to be the default form
            setFormData(defaultForm);
        } catch (error) {
            console.error("Error adding position:", error);
        }
    };

    // Table to display the positions for both active and inactive positions.
    // This is to enforce that the active and inactive positions tables are identical.
    const PositionsTable = ({ positions, title }) => {
        return (
            <div>
                <h1>{title}</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Ticker</th>
                            <th>Type</th>
                            <th>Quantity</th>
                            <th>Strike Price</th>
                            <th>Expiration Date</th>
                            <th>Premium</th>
                            <th>Open Price</th>
                            <th>Open Date</th>
                            <th>Position Status</th>
                            <th>Close Price</th>
                        </tr>
                    </thead>
                    <tbody>
                        {positions.map((pos, idx) => (
                            <tr key={idx}>
                                <td>{pos.ticker}</td>
                                <td>{pos.contract_type}</td>
                                <td>{pos.quantity}</td>
                                <td>{pos.strike_price}</td>
                                <td>{pos.expiration_date}</td>
                                <td>{pos.premium}</td>
                                <td>{pos.open_price}</td>
                                <td>{pos.open_date}</td>
                                <td>{pos.position_status}</td>
                                <td>{pos.close_price}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        )
    }

    return (
        <div>
            <h1>Options Positions</h1>
            <div>
                <PositionsTable positions={activePositions} title="Active Positions" />
                <PositionsTable positions={inactivePositions} title="Inactive Positions" />
            </div>

            <h2>Add New Position</h2>
            <form onSubmit={(e) => e.preventDefault()}>
                <input
                    type="text"
                    name="ticker"
                    placeholder="Ticker"
                    value={formData.ticker}
                    onChange={handleInputChange}
                    required
                />
                <select
                    name="contract_type"
                    value={formData.contract_type}
                    onChange={handleInputChange}
                    required
                >
                    <option value="" disabled>Select Contract Type</option>
                    <option value="Call">Call</option>
                    <option value="Put">Put</option>
                </select>
                <input
                    type="number"
                    name="quantity"
                    placeholder="Quantity"
                    value={formData.quantity}
                    onChange={handleInputChange}
                    required
                />
                <input
                    type="number"
                    name="strike_price"
                    placeholder="Strike Price"
                    value={formData.strike_price}
                    onChange={handleInputChange}
                    required
                    step=".01" // TODO: This doesn't work right yet, fix this later
                />
                <input
                    type="date"
                    name="expiration_date"
                    placeholder="Expiration Date"
                    value={formData.expiration_date}
                    onChange={handleInputChange}
                    required
                />
                <input
                    type="number"
                    name="premium"
                    placeholder="Premium"
                    value={formData.premium}
                    onChange={handleInputChange}
                    required
                    min="0"
                    step=".01"
                />
                <input
                    type="number"
                    name="open_price"
                    placeholder="Open Price"
                    value={formData.open_price}
                    onChange={handleInputChange}
                    required
                    step=".01"
                />
                <input
                    type="date"
                    name="open_date"
                    placeholder="Open Date"
                    value={formData.open_date}
                    onChange={handleInputChange}
                    required
                />
                {/* Add additional inputs for other fields if needed */}
                <button onClick={handleAddPosition}>Add Position</button>
            </form>
        </div>
    );
}

export default App;
