"use server";
import dotenv from "dotenv";
import OpenAI from "openai";

dotenv.config();

const token = process.env["GITHUB_TOKEN_1"];
const endpoint = "https://models.inference.ai.azure.com";
const modelName = "gpt-4o";
const client = new OpenAI({ baseURL: endpoint, apiKey: token });

export async function handleChatRequest({ message, id }) {
  console.log("message", message);
  console.log("id", id);

  // Perform similarity search
  const similarityResponse = await fetch(
    "http://localhost:8000/similarity_search/",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: message, id }),
    }
  );

  if (!similarityResponse.ok) {
    throw new Error(
      `Network response was not ok ${similarityResponse.status} : ${similarityResponse.statusText}`
    );
  }

  const similarityData = await similarityResponse.json();
  const similarContent = similarityData.results.join("\n");

  // Create the prompt with the similarity search results
  const prompt = `Based on the following content:\n${similarContent}\n\n${message} in 100 words or less, what is the main idea of the text?`;

  // Generate the chat response
  const response = await client.chat.completions.create({
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: `${prompt}` },
    ],
    temperature: 1.0,
    top_p: 1.0,
    max_tokens: 1000,
    model: modelName,
  });

  return response.choices[0].message.content;
}

handleChatRequest().catch((err) => {
  console.error("The sample encountered an error:", err);
});
