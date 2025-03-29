import axios from "axios";

const API = axios.create({
    baseURL: "http://localhost:8000/api/",
});

// POST to user login (expects email & password or your defined schema)
export const loginUser = (data) => API.post("user/login/", data);

// POST to register a user (expects username, email, password)
export const registerUser = (data) => API.post("user/register/", data);

// POST to chat with the AI, token must be included in header
export const sendMessage = (data, token) =>
    API.post("ai/chat/", data, {
        headers: {Authorization: 'Bearer ${token}'}
});