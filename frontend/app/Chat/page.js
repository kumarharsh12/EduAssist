"use client";
import React, { useEffect, useState } from "react";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [selectedMeeting, setSelectedMeeting] = useState(null);
  const [subjects, setSubjects] = useState([]);

  useEffect(() => {
    const fetchSubjects = async () => {
      try {
        const response = await fetch("http://localhost:8000/getlist", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error(
            `Network response was not ok ${response.status} : ${response.statusText}`
          );
        }

        const data = await response.json();
        setSubjects(data.subjects);
      } catch (error) {
        console.error("Fetch error:", error);
      }
    };

    fetchSubjects();
  }, []);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (inputMessage.trim() && selectedMeeting) {
      const userMessage = { text: inputMessage, sender: "user" };
      setMessages([...messages, userMessage]);
      setInputMessage("");
      setIsLoading(true);

      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: inputMessage,
            id: selectedMeeting.id,
          }),
        });

        if (!response.ok) {
          throw new Error(
            `Network response was not ok ${response.status} : ${response.statusText}`
          );
        }

        const data = await response.json();
        const botMessage = { text: data.response, sender: "bot" };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
        setIsLoading(false);
      } catch (error) {
        console.error("Fetch error:", error);
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="flex h-[calc(90vh-2rem)] m-4 bg-gradient-to-r from-zinc-800 to-red-950">
      {/* Subjects Selection */}
      <div className="w-1/4 bg-[#1a1b26] p-4 shadow-lg rounded-xl mr-4">
        <h2 className="text-lg font-bold mb-3 text-[#a9b1d6]">Subjects</h2>
        <ul className="space-y-2">
          {subjects.map((subject, index) => (
            <li
              key={index}
              className={`p-2 rounded-lg cursor-pointer ${
                selectedMeeting === subject
                  ? "bg-[#7aa2f7] text-[#1a1b26]"
                  : "bg-[#24283b] text-[#c0caf5]"
              }`}
              onClick={() => setSelectedMeeting(subject)}
            >
              {subject.name}
            </li>
          ))}
        </ul>
      </div>

      {/* Chat Container */}
      <div className="flex-1 bg-[#1a1b26] p-4 shadow-lg rounded-xl flex flex-col">
        <h2 className="text-lg font-bold mb-3 text-[#a9b1d6]">
          Chat Assistant
        </h2>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto mb-4 p-2 bg-[#24283b] rounded-lg">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`p-2 my-2 rounded-lg text-[#c0caf5] w-fit flex-wrap wrap ${
                message.sender === "user"
                  ? "bg-[#565f89] ml-auto"
                  : "bg-[#414868] mr-10"
              }`}
            >
              {message.text}
            </div>
          ))}
          {isLoading && (
            <div className="p-2 my-2 rounded-lg text-[#c0caf5] bg-[#414868] mr-auto">
              Typing...
            </div>
          )}
        </div>

        {/* Input Form */}
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 rounded-md border border-[#414868] bg-[#24283b] text-[#c0caf5] outline-none focus:ring-2 focus:ring-[#7aa2f7] transition-all"
          />
          <button
            type="submit"
            className="px-4 py-2 rounded-md bg-[#7aa2f7] text-[#1a1b26] font-bold hover:bg-[#6989dd] transition-colors"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default Chat;
