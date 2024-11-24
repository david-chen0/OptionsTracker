const API_URL = "http://127.0.0.1:5000/api/options_positions";

export async function fetchOptionsPositions() {
    const response = await fetch(API_URL);
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
