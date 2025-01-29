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
    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormData((prev) => ({
          ...prev,
          [name]: event.target.type === "number" ? Number(value) : value,
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
            const addPositionResponse = await addOptionsPosition(newPosition);

            // Response from server on whether the newly added position is inactive
            if (addPositionResponse["inactive"]) {
                // Fetch the updated inactive positions list from the backend and set the table accordingly
                const updatedInactivePositions = await fetchOptionsPositions(false);
                setInactivePositions(updatedInactivePositions);
            } else {
                // Fetch the updated active positions list from the backend and set the table accordingly
                const updatedActivePositions = await fetchOptionsPositions(true);
                setActivePositions(updatedActivePositions);
            }

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
            <div className="container mt-5">
                <h1 className="text-center">{title}</h1>
                <table className="table table-striped table-bordered">
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
            <h1 className="text-center">Options Positions Tracker</h1>
            <div>
                <PositionsTable positions={activePositions} title="Active Positions" />
                <PositionsTable positions={inactivePositions} title="Inactive Positions" />
            </div>

            <h2 className="text-center">Add New Position</h2>
            <form class="d-flex flex-wrap align-items-center gap-3" onSubmit={(e) => e.preventDefault()}>
                <label for="ticker" class="form-label">Ticker</label>
                <input
                    type="text"
                    class="form-control"
                    name="ticker"
                    id="ticker"
                    placeholder="Ticker"
                    onChange={handleInputChange}
                    required
                />
                <label for="contract_type" class="form-label">Contract Type</label>
                <select 
                    class="form-select"
                    name="contract_type"
                    onChange={handleInputChange}
                    required
                >
                    <option value="" disabled selected>Choose Contract Type</option>
                    <option value="Call">Call</option>
                    <option value="Put">Put</option>
                </select>
                <label for="quantity" class="form-label">Quantity</label>
                <input
                    type="number"
                    class="form-control"
                    name="quantity"
                    id="quantity"
                    placeholder="Quantity"
                    onChange={handleInputChange}
                    required
                />
                <label for="strike_price" class="form-label">Strike Price</label>
                <input
                    type="number"
                    class="form-control"
                    name="strike_price"
                    id="strike_price"
                    placeholder="Strike Price"
                    onChange={handleInputChange}
                    required
                />
                <label for="expiration_date" class="form-label">Expiration Date</label>
                <input
                    type="date"
                    class="form-control"
                    name="expiration_date"
                    id="expiration_date"
                    placeholder="Expiration Date"
                    onChange={handleInputChange}
                    required
                />
                <label for="premium" class="form-label">Premium</label>
                <input
                    type="number"
                    class="form-control"
                    name="premium"
                    id="premium"
                    placeholder="Premium"
                    onChange={handleInputChange}
                    required
                />
                <label for="open_price" class="form-label">Open Price</label>
                <input
                    type="number"
                    class="form-control"
                    name="open_price"
                    id="open_price"
                    placeholder="Open Price"
                    onChange={handleInputChange}
                    required
                />
                <label for="open_date" class="form-label">Open Date</label>
                <input
                    type="date"
                    class="form-control"
                    name="open_date"
                    id="open_date"
                    placeholder="Open Date"
                    onChange={handleInputChange}
                    required
                />
                <button class="btn btn-primary" onClick={handleAddPosition}>Add Position</button>
            </form>
        </div>
    );
}

export default App;
