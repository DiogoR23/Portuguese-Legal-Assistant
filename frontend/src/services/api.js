import API from "./axiosInstance";

// Authentication
export const loginUser = (data) => API.post("users/login/", data);
export const registerUser = (data) => API.post("users/register/", data);
export const sendMessage = (data) => API.post("ai/chat/", data);
export const getUserInfo = () => API.get('protected/');

