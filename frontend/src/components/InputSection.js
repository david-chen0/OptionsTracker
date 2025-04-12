import React, { useRef } from "react";
import { addOptionsPosition, fetchOptionsPositions } from "../api/optionsPositionsApi";

const InputSection = ({
    isInputVisible,
    toggleIsInputVisible,
    setActivePositions,
    setExpiredPositions,
    addPositionFields
}) => {

    // Object used to store all the refs corresponding to the form's input fields
    const formRefs = useRef({});

    // Handles when the AddPosition button is hit
    const handleAddPosition = async (event) => {
        event.preventDefault(); // Stops the page from refreshing
        try {
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

    // This section contains the input fields for creating the positions
    // The section is by default 1/6th of the screen, but gets tucked when a button is hit
    const inputFieldDesign = "flex justify-center text-center w-full rounded-md bg-gray-200 px-3 py-2 focus:outline-none focus:ring focus:ring-blue-500"
    const fieldNameDesign = "block text-center text-sm font-medium text-gray-700"
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

export default InputSection;
