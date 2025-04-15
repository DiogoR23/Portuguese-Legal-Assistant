import API from "@/services/axiosInstance";

// Authentication
export const loginUser = (data) => API.post("users/login/", data);
export const registerUser = (data) => API.post("users/register/", data);
export const getUserInfo = () => API.get('protected/');

// AI Connection
export const sendMessage = (payload) => API.post("ai/chat/", payload);
export const fetchUserConversations = () => API.get("ai/conversations/");
export const fetchConversationMessages = (converdsationId) => 
    API.get(`ai/conversations/${converdsationId}/messages`);
export const createConversation = (title = "") =>
    API.post("ai/create/conversations/", { title });
export const deleteConversation = (conversationId) =>
    API.delete(`ai/conversations/${conversationId}/`);