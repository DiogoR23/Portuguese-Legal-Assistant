import React, { useState, useRef, useEffect } from "react";

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [darkMode, setDarkMode] = useState(false);
    const chatBoxRef = useRef(null);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        if (chatBoxRef.current) {
            chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
        }
    };

    const toggleTheme = () => {
        setDarkMode(!darkMode);
    };

    const sendMessage = async () => {
        if (input.trim() === "") return;

        setMessages((prevMessages) => [
            ...prevMessages, 
            { sender: "user", text: input }
        ]);

        setInput("");

        try {
            const response = await fetch("http://127.0.0.1:8000/api/chat/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: input }),
            });

            const data = await response.json();
            setMessages((prevMessages) => [
                ...prevMessages, 
                { sender: "bot", text: data.response }
            ]);
        } catch (error) {
            setMessages((prevMessages) => [
                ...prevMessages, 
                { sender: "bot", text: "Erro ao conectar com o servidor." }
            ]);
        }
    };

    return (
        <div style={darkMode ? styles.containerDark : styles.containerLight}>
            <div style={styles.header}>
                <h1>PTLaws AI</h1>
                <button onClick={toggleTheme} style={styles.themeButton}>
                    {darkMode ? "🌞 Modo Claro" : "🌙 Modo Escuro"}
                </button>
            </div>
            <div ref={chatBoxRef} style={darkMode ? styles.chatBoxDark : styles.chatBoxLight}>
                {messages.map((msg, index) => (
                    <div 
                        key={index} 
                        style={msg.sender === "user" ? (darkMode ? styles.userMessageDark : styles.userMessageLight) 
                                                     : (darkMode ? styles.botMessageDark : styles.botMessageLight)}
                    >
                        <b>{msg.sender === "user" ? "Você" : "PTLaws"}:</b> {msg.text}
                    </div>
                ))}
            </div>
            <div style={styles.inputContainer}>
                <input 
                    type="text" 
                    value={input} 
                    onChange={(e) => setInput(e.target.value)} 
                    onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                    style={darkMode ? styles.inputDark : styles.inputLight}
                    placeholder="Digite sua mensagem..."
                />
                <button onClick={sendMessage} style={styles.button}>Enviar</button>
            </div>
        </div>
    );
};

const styles = {
    containerLight: {
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(to right, #ece9e6, #ffffff)",
        color: "#333",
        fontFamily: "Arial, sans-serif",
        padding: "20px",
    },
    containerDark: {
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(to right, #232526, #414345)",
        color: "#fff",
        fontFamily: "Arial, sans-serif",
        padding: "20px",
    },
    header: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        width: "100%",
        maxWidth: "1000px",
        padding: "10px 0",
    },
    themeButton: {
        padding: "10px",
        borderRadius: "5px",
        border: "none",
        backgroundColor: "#007bff",
        color: "white",
        cursor: "pointer",
    },
    chatBoxLight: {
        width: "100%",
        maxWidth: "1000px",
        height: "75vh",
        border: "1px solid #ccc",
        padding: "10px",
        overflowY: "auto",
        backgroundColor: "#fff",
        borderRadius: "15px",
        display: "flex",
        flexDirection: "column",
        boxShadow: "0px 5px 15px rgba(0, 0, 0, 0.1)",
    },
    chatBoxDark: {
        width: "100%",
        maxWidth: "1000px",
        height: "75vh",
        border: "1px solid #444",
        padding: "10px",
        overflowY: "auto",
        backgroundColor: "#1e1e1e",
        borderRadius: "15px",
        display: "flex",
        flexDirection: "column",
        boxShadow: "0px 5px 15px rgba(255, 255, 255, 0.1)",
    },
    userMessageLight: {
        alignSelf: "flex-end",
        backgroundColor: "#007bff",
        color: "white",
        padding: "12px",
        margin: "5px",
        borderRadius: "20px",
        maxWidth: "80%",
        transition: "opacity 0.3s ease-in-out",
    },
    userMessageDark: {
        alignSelf: "flex-end",
        backgroundColor: "#3b82f6",
        color: "#fff",
        padding: "12px",
        margin: "5px",
        borderRadius: "20px",
        maxWidth: "80%",
        transition: "opacity 0.3s ease-in-out",
    },
    botMessageLight: {
        alignSelf: "flex-start",
        backgroundColor: "#e9ecef",
        color: "#333",
        padding: "12px",
        margin: "5px",
        borderRadius: "20px",
        maxWidth: "80%",
        transition: "opacity 0.3s ease-in-out",
    },
    botMessageDark: {
        alignSelf: "flex-start",
        backgroundColor: "#444",
        color: "#fff",
        padding: "12px",
        margin: "5px",
        borderRadius: "20px",
        maxWidth: "80%",
        transition: "opacity 0.3s ease-in-out",
    },
    inputContainer: {
        display: "flex",
        width: "100%",
        maxWidth: "1000px",
        marginTop: "10px",
    },
    inputLight: {
        flex: 1,
        padding: "12px",
        borderRadius: "20px",
        border: "1px solid #ccc",
        backgroundColor: "#fff",
        color: "#000",
        outline: "none",
    },
    inputDark: {
        flex: 1,
        padding: "12px",
        borderRadius: "20px",
        border: "1px solid #444",
        backgroundColor: "#222",
        color: "#fff",
        outline: "none",
    },
    button: {
        marginLeft: "10px",
        padding: "12px",
        borderRadius: "20px",
        border: "none",
        backgroundColor: "#007bff",
        color: "white",
        cursor: "pointer",
        transition: "0.2s",
    }
};

export default Chatbot;
