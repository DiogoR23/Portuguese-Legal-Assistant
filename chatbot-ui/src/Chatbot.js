import React, { useState, useEffect } from "react";

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    useEffect(() => {
        // Carregar histórico do localStorage
        const savedMessages = JSON.parse(localStorage.getItem("chatHistory")) || [];
        setMessages(savedMessages);
    }, []);

    const sendMessage = async () => {
        if (input.trim() === "") return;

        const newMessages = [...messages, { sender: "user", text: input }];
        setMessages(newMessages);
        localStorage.setItem("chatHistory", JSON.stringify(newMessages));  // Salvar no localStorage

        const response = await fetch("http://127.0.0.1:8000/api/chat/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input }),
        });

        const data = await response.json();
        const botResponse = { sender: "bot", text: data.response };

        const updatedMessages = [...newMessages, botResponse];
        setMessages(updatedMessages);
        localStorage.setItem("chatHistory", JSON.stringify(updatedMessages));

        setInput("");
    };

    return (
        <div style={{ maxWidth: "600px", margin: "auto", padding: "20px", textAlign: "center" }}>
            <h2>Chatbot</h2>
            <div style={{ border: "1px solid #ccc", padding: "10px", minHeight: "300px", overflowY: "auto" }}>
                {messages.map((msg, index) => (
                    <div key={index} style={{ textAlign: msg.sender === "user" ? "right" : "left" }}>
                        <b>{msg.sender === "user" ? "Você" : "Chatbot"}:</b> {msg.text}
                    </div>
                ))}
            </div>
            <input 
                type="text" 
                value={input} 
                onChange={(e) => setInput(e.target.value)} 
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                style={{ width: "80%", padding: "10px", marginTop: "10px" }}
            />
            <button onClick={sendMessage} style={{ padding: "10px", marginLeft: "5px" }}>Enviar</button>
        </div>
    );
};

export default Chatbot;
