const API_URL = "http://127.0.0.1:5000/api/options_positions";

// isActive indicates whether this contract we are fetching is in the active or expired table
export async function fetchOptionsPositions(isActive) {
    let actual_api_url = API_URL + "/get_";
    if (!isActive) {
        actual_api_url += "expired_position";
    } else {
        actual_api_url += "active_position";
    }
    const response = await fetch(actual_api_url);

    if (!response.ok) throw new Error("Failed to fetch positions");
    return response.json();
}

export async function addOptionsPosition(positionData) {
    const actual_api_url = API_URL + "/add_position";
    const response = await fetch(actual_api_url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(positionData),
    });
    if (!response.ok) throw new Error("Failed to add position");
    return response.json();
}

export async function deleteOptionsPosition(positionId) {
    const actual_api_url = API_URL + "/delete_position";
    const response = await fetch(actual_api_url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({position_id: positionId}),
    });
    if (!response.ok) throw new Error("Failed to delete position");
    return response.json();
}
