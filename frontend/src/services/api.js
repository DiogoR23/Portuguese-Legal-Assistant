import API from "./axiosInstance";

// Authentication
export const loginUser = (data) => API.post("users/login/", data);
export const registerUser = (data) => API.post("users/register/", data);
export const sendMessage = (data) => API.post("ai/chat/", data);
export const getUserInfo = () => API.get('protected/');

// Conversations
export const fetchUserConversations = () => API.get("ai/conversations/");
export const fetchConversationMessages = (converdsationId) => 
    API.get(`ai/conversations/${converdsationId}/messages`);
export const createConversation = (title = "") =>
    API.post("ai/create/conversations/", { title });
export const deleteConversation = (conversationId) =>
    API.delete(`ai/conversations/${conversationId}/`);