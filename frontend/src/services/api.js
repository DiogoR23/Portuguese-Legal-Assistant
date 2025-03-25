import axios from "axios";

const API = axios.create({
    baseURL: "http://localhost:8000/api/",
});

export const loginUser = (data) => API.post("user/login/", data);
export const registerUser = (data) => API.post("user/register/", data);
export const sendMessage = (data, toke) => API.post("ai/chat/", data, {
    headers: {Authorization: 'Bearer ${token}'}
});