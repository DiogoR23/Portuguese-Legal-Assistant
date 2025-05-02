/*
api.js

This file contains all the API calls to the backend.
It uses the axiosInstance to make requests to the backend.
The API calls are organized into different sections based on their functionality.
1. Authentication
2. AI Connection
3. User Conversations
4. Conversation Messages
6. Conversation Deletion
7. Conversation Update
8. Conversation Creation
9. Conversation Fetching
*/

import API from "@/services/axiosInstance";

// Authentication
export const loginUser = (data) => API.post("users/login/", data);

export const registerUser = (data) => API.post("users/register/", data);

export const getUserInfo = () => API.get('protected/');


// AI Connection
export const sendMessage = (payload, controller) =>
    fetch("http://localhost:8000/api/ai/chat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access")}`,
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    }).then(async (res) => {
      if (!res.ok) throw new Error("Erro na resposta do servidor");
      const data = await res.json();
      return data;
    });

export const fetchUserConversations = () => API.get("ai/conversations/");

export const fetchConversationMessages = (converdsationId) =>
    API.get(`ai/conversations/${converdsationId}/messages`);

export const createConversation = (title = "") =>
    API.post("ai/create/conversations/", { title });

export const deleteConversation = (conversationId) =>
    API.delete(`ai/conversations/${conversationId}/`);

export const updateConversation = (conversationId, title) =>
    API.put(`ai/conversations/${conversationId}/title/`, { title });
