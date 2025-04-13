import React, { useState } from "react";
import { deleteOptionsPosition } from "../api/optionsPositionsApi";

// This section contains all the tables
const TableSection = ({
    isInputVisible,
    activeTableName,
    activePositions,
    setActivePositions,
    expiredTableName,
    expiredPositions,
    setExpiredPositions,
    addPositionFields
}) => {
    
    // State mapping from table name to the sort key and direction of that table
    const [tablesSortConfig, setTablesSortConfig] = useState({
        [activeTableName]: { key: "expiration_date", direction: "asc" },
        [expiredTableName]: { key: "expiration_date", direction: "asc" }
    });

    // Enum representing the different tables we'll have
    // might need to move this into app.js so it can reference it or just put it in a diff file or export it here idk
    const TableType = Object.freeze({
        ACTIVE: 'active',
        EXPIRED: 'expired'
    });

    // Configs for each of the tables
    // title {string} - The title of the table
    // extraFields {string[]} - The extra fields to include for that table on top of the default fields, specified by their table key and label
    const TableDetails = {
        [TableType.ACTIVE]: {
            title: "Active Positions",
            extraFields: []
        },
        [TableType.EXPIRED]: {
            title: "Expired Positions",
            extraFields: [
                { key: "profit", label: "Profit" }
            ]
        },
    };

    // Fields to translate to USD format(ex: 1000.25 -> $1,000.25)
    const currencyFields = [
        "strike_price",
        "premium",
        "open_price",
        "close_price",
        "profit"
    ];

    // Translates a number into dollar format, where it's prefixed by $, is comma separated, and has 2 decimal points
    const formatToUSD = (number) => {
        return number.toLocaleString('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

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

    // Table to display the positions for both active and expired positions.
    // This is to enforce that the active and expired positions tables are identical.
    const PositionsTable = ({ positions, tableType }) => {
        const title = TableDetails[tableType].title;
        const extraFields = TableDetails[tableType].extraFields;
        
        const baseFields = [
            { key: "ticker", label: "Ticker" },
            { key: "contract_type", label: "Type" },
            { key: "quantity", label: "Quantity" },
            { key: "trade_direction", label: "Trade Direction" },
            { key: "strike_price", label: "Strike Price" },
            { key: "expiration_date", label: "Expiration Date" },
            { key: "premium", label: "Premium" },
            { key: "open_price", label: "Open Price" },
            { key: "open_date", label: "Open Date" },
            { key: "position_status", label: "Position Status" },
            { key: "close_price", label: "Close Price" },
        ];
        const combinedFields = [...baseFields, ...extraFields];

        return (
            <div className="w-full max-w-full mt-20 px-4">
                <h1 className="text-white text-center text-2xl font-bold">{title}</h1>
                <table className="w-full border border-gray-300">
                    <thead>
                        <tr>
                            {/* This mapping creates the sorting buttons next to each header */}
                            {combinedFields.map(({ key, label }) => (
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
                                {combinedFields.map(field => {
                                    const value = pos[field.key];
                                    const isCurrencyField = currencyFields.includes(field.key);
                                    return (
                                        <td>
                                            {isCurrencyField ? formatToUSD(value) : value}
                                        </td>
                                    );
                                })}
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

    return (
        <div className={`bg-gray-700 flex flex-col items-center justify-center transition-all duration-300 ${isInputVisible ? "w-5/6" : "w-full"}`}>
            {/* List of the position tables */}
            <PositionsTable positions={activePositions} tableType={TableType.ACTIVE} />
            <PositionsTable positions={expiredPositions} tableType={TableType.EXPIRED} />
        </div>
    )
}

export default TableSection;
