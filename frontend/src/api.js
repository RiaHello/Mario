const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function getHealth() {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  if (!response.ok) {
    throw new Error(`Health API failed: ${response.status}`);
  }
  return response.json();
}

export async function getMessage() {
  const response = await fetch(`${API_BASE_URL}/api/message`);
  if (!response.ok) {
    throw new Error(`Message API failed: ${response.status}`);
  }
  return response.json();
}

export async function loadGameSave() {
  const response = await fetch(`${API_BASE_URL}/api/game/save`);
  if (!response.ok) {
    throw new Error(`Load save failed: ${response.status}`);
  }
  return response.json();
}

export async function saveGame(payload) {
  const response = await fetch(`${API_BASE_URL}/api/game/save`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    throw new Error(`Save game failed: ${response.status}`);
  }
  return response.json();
}
