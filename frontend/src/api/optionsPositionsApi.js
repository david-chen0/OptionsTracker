const API_URL = "http://127.0.0.1:5000/api/options_positions";

// export async function fetchOptionsPositions() {
//     const response = await fetch(API_URL);
//     if (!response.ok) throw new Error("Failed to fetch positions");
//     return response.json();
// }

// isActive indicates whether this contract we are fetching is in the active or inactive table
export async function fetchOptionsPositions(isActive) {
    let actual_api_url = API_URL + "/";
    if (!isActive) {
        actual_api_url += "in";
    }
    actual_api_url += "active";
    const response = await fetch(actual_api_url);

    if (!response.ok) throw new Error("Failed to fetch positions");
    return response.json();
}

export async function addOptionsPosition(positionData) {
    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(positionData),
    });
    if (!response.ok) throw new Error("Failed to add position");
    return response.json();
}
