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

    const [positions, setPositions] = useState([]);
    const [formData, setFormData] = useState(defaultForm);

    useEffect(() => {
        async function loadPositions() {
            try {
                const data = await fetchOptionsPositions(true);
                setPositions(data);
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

            newPosition["position_status"] = "Open"

            // TODO: Add verifications on the fields, ex: expiration date is a date, strike price is a number with at most 2 decimals, and more

            await addOptionsPosition(newPosition);
            // Temp to add to list of positions, delete this once we have the backend completely figured out
            // TODO: Change this to show the updated list rather than just displaying exactly what we added
            // start with just showing actives, then we can display inactives later
            // setPositions((prev) => [...prev, newPosition]);

            // Fetch the updated list of positions from the backend
            // currently only using the active list, will change to include inactive list too later
            const updatedActivePositions = await fetchOptionsPositions(true);

            // Setting the updated positions
            setPositions(updatedActivePositions);

            // Resetting the form to be the default form
            // TODO: Change this to not happen on errors
            setFormData(defaultForm);
        } catch (error) {
            console.error("Error adding position:", error);
        }
    };

    return (
        <div>
            <h1>Options Positions</h1>
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
                        </tr>
                    ))}
                </tbody>
            </table>

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
