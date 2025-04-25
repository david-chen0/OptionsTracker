import './index.css';
import React, { useEffect, useState } from "react";
import InputSection from './components/InputSection';
import TableSection from './components/TableSection';
import { fetchOptionsPositions } from "./api/optionsPositionsApi";

function App() {

    // List of all fields in the AddPosition form
    const addPositionFields = [
        "ticker",
        "contract_type",
        "quantity",
        "trade_direction",
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

    // Method to flip the boolean value of the isVisible variable
    const toggleInputSection = () => {
        setIsInputVisible((prev) => !prev);
    };

    return (
        <div className="h-screen flex flex-row overflow-hidden transition-all duration-300">
            {/* Table Section - Expands when InputSection is hidden */}
            <TableSection
                isInputVisible={isInputVisible}
                activeTableName={activeTableName}
                activePositions={activePositions}
                setActivePositions={setActivePositions}
                expiredTableName={expiredTableName}
                expiredPositions={expiredPositions}
                setExpiredPositions={setExpiredPositions}
                addPositionFields={addPositionFields}
            />

            {/* Input Section - Hidden by default */}
            <InputSection
                isInputVisible={isInputVisible}
                toggleIsInputVisible={toggleInputSection}
                setActivePositions={setActivePositions}
                setExpiredPositions={setExpiredPositions}
                addPositionFields={addPositionFields}
            />
        </div>
    );
}

export default App;
