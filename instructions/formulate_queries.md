instructions: Based on the user’s prompt, generate a list of search queries.

1. Identify the main topics or keywords in the user’s prompt.
2. Break down the prompt into specific subtopics or aspects.
3. For each subtopic or keyword, generate 1-3 relevant search queries and incorporate boolean operators that could retrieve useful information.
4. Ensure the queries are clear, concise, and aimed at gathering focused information.
5. Focus on 聯合報 (UDN). Meaning only search for the news articles from 聯合報 (UDN)
6. Follow this JSON scheme for your search queries
JSON scheme
{
  "userPrompt": "string",
  "mainTopic": "string",
  "subtopics": [
    {
      "subtopic": "string",
      "searchQueries": [
        "string"
      ]
    }
  ]
}
User’s Prompt: "_prompt_"
Generate the search queries based on the above instructions
