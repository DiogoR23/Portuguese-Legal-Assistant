import axios from "axios";

const API = axios.create({
    baseURL: "http://localhost:8000/api/",
});

// Authentication
export const loginUser = (data) => API.post("user/login/", data);
export const registerUser = (data) => API.post("user/register/", data);

// Chat (Send a question to the AI)
export const sendMessage = (data, token) =>
    API.post("ai/chat/", data, {
        headers: { Authorization: `Bearer ${token}` },
    });

// Conversation History
// export const fetchChatHistory = (token) =>
//     API.get("conversas")\

// POST to chat with the AI, token must be included in header
export const sendMessage = (data, token) =>
    API.post("ai/chat/", data, {
        headers: {Authorization: `Bearer ${token}`}
});