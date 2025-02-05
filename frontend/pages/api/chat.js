"use server";
import { handleChatRequest } from "@/actions/chatbotapi";

export default async function handler(req, res) {
  if (req.method === "POST") {
    try {
      const request = req.body;
      const response = await handleChatRequest(request);
      res.status(200).json({ response });
    } catch (error) {
      console.error("Error handling chat request:", error);
      res.status(500).json({ error: "Internal Server Error" });
    }
  } else {
    res.setHeader("Allow", ["POST"]);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
