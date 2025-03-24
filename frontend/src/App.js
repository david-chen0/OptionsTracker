import './index.css';
import React, { useEffect, useRef, useState } from "react";
import { addOptionsPosition, deleteOptionsPosition, fetchOptionsPositions } from "./api/optionsPositionsApi";

function App() {
    // List of all fields in the AddPosition form
    const addPositionFields = [
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

    // List corresponding to expired positions
    const [expiredPositions, setExpiredPositions] = useState([]);

    // Names for the tables
    const activeTableName = "Active Positions";
    const expiredTableName = "Expired Positions";

    // State mapping from table name to the sort key and direction of that table
    const [tablesSortConfig, setTablesSortConfig] = useState({
        [activeTableName]: { key: "expiration_date", direction: "asc" },
        [expiredTableName]: { key: "expiration_date", direction: "asc" }
    });
    
    // Object used to store all the refs corresponding to the form's input fields
    const formRefs = useRef({});

    // Used to track whether the InputSection is visible/extended out
    const [isInputVisible, setIsInputVisible] = useState(true);

    useEffect(() => {
        async function loadPositions() {
            try {
                // Fetching and setting active data
                const activeData = await fetchOptionsPositions(true);
                setActivePositions(activeData);
                
                // Fetching and setting expired data
                const expiredData = await fetchOptionsPositions(false);
                setExpiredPositions(expiredData);
            } catch (error) {
                console.error("Error fetching positions:", error);
            }
        }
        loadPositions();
    }, []);

    // Handles when the AddPosition button is hit
    const handleAddPosition = async () => {
        try {
            // const newPosition = { ...formData };
            const newPosition = {
                ticker: formRefs.current.ticker.value,
                contract_type: formRefs.current.contract_type.value,
                quantity: formRefs.current.quantity.value,
                strike_price: formRefs.current.strike_price.value,
                expiration_date: formRefs.current.expiration_date.value,
                premium: formRefs.current.premium.value,
                open_price: formRefs.current.open_price.value,
                open_date: formRefs.current.open_date.value
            };

            // Checking to make sure all fields are filled out
            const missingFields = addPositionFields.filter((field) => !formRefs.current[field]);
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

            // Response from server on whether the newly added position is expired
            if (addPositionResponse["expired"]) {
                // Fetch the updated expired positions list from the backend and set the table accordingly
                const updatedExpiredPositions = await fetchOptionsPositions(false);
                setExpiredPositions(updatedExpiredPositions);
            } else {
                // Fetch the updated active positions list from the backend and set the table accordingly
                const updatedActivePositions = await fetchOptionsPositions(true);
                setActivePositions(updatedActivePositions);
            }

            // Resetting the form to be the default form
            for (let field of addPositionFields) {
                formRefs.current[field].value = "";
            }
        } catch (error) {
            console.error("Error adding position:", error);
        }
    };

    // Handles when the DeletePosition button(the red X next to positions) is hit
    const handleDelete = async (position) => {
        // User must confirm that they want to delete the position
        console.log(`Deleting position with ticker ${position.ticker} corresponding to serial id ${position.position_id}`);
        if (!window.confirm("Are you sure you want to delete this position?")) {
            return;
        }

        // Delete the position in the backend
        const deletePositionResponse = await deleteOptionsPosition(position.position_id);

        // Delete the position from the corresponding table
        if (deletePositionResponse["expired"]) {
            setExpiredPositions(expiredPositions.filter((item, index) => item.position_id !== position.position_id));
        } else {
            setActivePositions(activePositions.filter((item, index) => item.position_id !== position.position_id));
        }
    };

    // Helper method for sorting the table
    const compareValues = (a, b, key, direction) => {
        if (!addPositionFields.includes(key)) {
            console.error("Trying to sort by unknown key " + key);
        }

        let valA = a[key];
        let valB = b[key];

        if (key === "expiration_date" || key === "open_date") {
            valA = new Date(valA);
            valB = new Date(valB);
        }

        if (typeof valA === "number") {
            return direction === "asc" ? valA - valB : valB - valA;
        } else if (typeof valA === "string") {
            return direction === "asc"
                ? valA.localeCompare(valB)
                : valB.localeCompare(valA);
        } else {
            return direction === "asc" ? valA - valB : valB - valA;
        }
    };

    // Method to handle sorting the input table
    const sortPositions = (tableName, field) => {
        setTablesSortConfig((prevState) => {
            const currentSortConfig = prevState[tableName];
            const newDirection = currentSortConfig.key === field && currentSortConfig.direction === "asc" ? "desc" : "asc";

            if (tableName === activeTableName) {
                setActivePositions([...activePositions].sort((a, b) => 
                    compareValues(a, b, field, newDirection)
                ));
            } else if (tableName === expiredTableName) {
                setExpiredPositions([...expiredPositions].sort((a, b) => 
                    compareValues(a, b, field, newDirection)
                ));
            }
            
            return {
                ...prevState,
                [tableName]: { key: field, direction: newDirection }
            };
        });
    };

    // Method to flip the boolean value of the isVisible variable
    const toggleInputSection = () => {
        setIsInputVisible((prev) => !prev);
    };

    // Table to display the positions for both active and expired positions.
    // This is to enforce that the active and expired positions tables are identical.
    const PositionsTable = ({ positions, title }) => {
        return (
            <div className="w-full max-w-full mt-20 px-4">
                <h1 className="text-white text-center text-2xl font-bold">{title}</h1>
                <table className="w-full border border-gray-300">
                    <thead>
                        <tr>
                            {/* This mapping creates the sorting buttons next to each header */}
                            {[
                                { key: "ticker", label: "Ticker" },
                                { key: "contract_type", label: "Type" },
                                { key: "quantity", label: "Quantity" },
                                { key: "strike_price", label: "Strike Price" },
                                { key: "expiration_date", label: "Expiration Date" },
                                { key: "premium", label: "Premium" },
                                { key: "open_price", label: "Open Price" },
                                { key: "open_date", label: "Open Date" },
                                { key: "position_status", label: "Position Status" },
                                { key: "close_price", label: "Close Price" },
                            ].map(({ key, label }) => (
                                <th key={key} className="px-4 py-2 text-white">
                                    <div className="flex items-center">
                                        {label}
                                        <button
                                            onClick={() => sortPositions(title, key)}
                                            className="ml-2 text-xs"
                                        >
                                            <span className={tablesSortConfig[title].key === key && tablesSortConfig[title].direction === "asc" ? "text-amber-400" : "text-gray-400"}>
                                                ▲
                                            </span>
                                            <span className={tablesSortConfig[title].key === key && tablesSortConfig[title].direction === "desc" ? "text-amber-400" : "text-gray-400"}>
                                                ▼
                                            </span>
                                        </button>
                                    </div>
                                </th>
                            ))}
                            <th>Actions</th> {/* New column for delete button */}
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
                                <td>
                                    <button
                                        onClick={() => handleDelete(pos)}
                                        className="text-white hover:text-red-500 p-1"
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        )
    };


    // This section contains with all the tables
    const TableSection = ({ isInputVisible }) => {
        return (
            <div className={`bg-gray-700 flex flex-col items-center justify-center transition-all duration-300 ${isInputVisible ? "w-5/6" : "w-full"}`}>
                {/* List of the position tables */}
                <PositionsTable positions={activePositions} title={activeTableName} />
                <PositionsTable positions={expiredPositions} title={expiredTableName} />
            </div>
        )
    };

    // This section contains the input fields for creating the positions
    // The section is by default tucked, but expands to cover 25% of the screen width when the toggle is hit
    const inputFieldDesign = "flex justify-center text-center w-full rounded-md bg-gray-200 px-3 py-2 focus:outline-none focus:ring focus:ring-blue-500"
    const fieldNameDesign = "block text-center text-sm font-medium text-gray-700"
    const InputSection = ({ isInputVisible, toggleIsInputVisible }) => {
        return (
            <>
                {/* Toggle Button - Always Visible */}
                <button
                    className={`fixed ${isInputVisible ? "right-1/6" : "right-0"} top-1/2 bg-blue-500 text-white p-2 rounded-l-md transform -translate-y-1/2`}
                    onClick={toggleIsInputVisible}
                >
                    {isInputVisible ? "→" : "←"}
                </button>
        
                {/* Input Panel */}
                {isInputVisible && (
                    <div className={`bg-gray-600 relative transition-all duration-300 ${isInputVisible ? "w-1/6" : "w-0"} flex flex-col h-screen items-center justify-center`}>
                        <h2 className="text-white text-center text-2xl font-bold">Add New Position</h2>
                        <form className="block w-full items-center gap-3 mt-4" onSubmit={handleAddPosition}>
                            <label htmlFor="ticker" className={fieldNameDesign}>
                                Ticker
                            </label>
                            <input
                                type="text"
                                className={inputFieldDesign}
                                name="ticker"
                                id="ticker"
                                placeholder="Ticker"
                                ref={(e) => (formRefs.current.ticker = e)}
                                required
                            />

                            <label htmlFor="contract_type" className={fieldNameDesign}>
                                Contract Type
                            </label>
                            <select
                                className={inputFieldDesign}
                                name="contract_type"
                                defaultValue=""
                                ref={(e) => (formRefs.current.contract_type = e)}
                                required
                            >
                                <option value="" disabled>Choose Contract Type</option>
                                <option value="Call">Call</option>
                                <option value="Put">Put</option>
                            </select>

                            <label htmlFor="quantity" className={fieldNameDesign}>
                                Quantity
                            </label>
                            <input
                                type="number"
                                className={inputFieldDesign}
                                name="quantity"
                                id="quantity"
                                placeholder="Quantity"
                                ref={(e) => (formRefs.current.quantity = e)}
                                required
                            />

                            <label htmlFor="strike_price" className={fieldNameDesign}>
                                Strike Price
                            </label>
                            <input
                                type="number"
                                className={inputFieldDesign}
                                name="strike_price"
                                id="strike_price"
                                placeholder="Strike Price"
                                ref={(e) => (formRefs.current.strike_price = e)}
                                required
                            />

                            <label htmlFor="expiration_date" className={fieldNameDesign}>
                                Expiration Date
                            </label>
                            <input
                                type="date"
                                className={inputFieldDesign}
                                name="expiration_date"
                                id="expiration_date"
                                ref={(e) => (formRefs.current.expiration_date = e)}
                                required
                            />

                            <label htmlFor="premium" className={fieldNameDesign}>
                                Premium
                            </label>
                            <input
                                type="number"
                                className={inputFieldDesign}
                                name="premium"
                                id="premium"
                                placeholder="Premium"
                                ref={(e) => (formRefs.current.premium = e)}
                                required
                            />

                            <label htmlFor="open_price" className={fieldNameDesign}>
                                Open Price
                            </label>
                            <input
                                type="number"
                                className={inputFieldDesign}
                                name="open_price"
                                id="open_price"
                                placeholder="Open Price"
                                ref={(e) => (formRefs.current.open_price = e)}
                                required
                            />

                            <label htmlFor="open_date" className={fieldNameDesign}>
                                Open Date
                            </label>
                            <input
                                type="date"
                                className={inputFieldDesign}
                                name="open_date"
                                id="open_date"
                                ref={(e) => (formRefs.current.open_date = e)}
                                required
                            />

                            <button
                                className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md w-full"
                                type="submit"
                            >
                                Add Position
                            </button>
                        </form>
                    </div>
                )}
            </>
          );
    }

    return (
        <div className="h-screen flex flex-row transition-all duration-300">
            {/* Table Section - Expands when InputSection is hidden */}
            <TableSection isInputVisible={isInputVisible}></TableSection>

            {/* Input Section - Hidden by default */}
            <InputSection isInputVisible={isInputVisible} toggleIsInputVisible={toggleInputSection} />
        </div>
    );
}

export default App;
