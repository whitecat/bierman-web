# Backend API Documentation

## Overview
This backend offers API endpoints for analyzing codebases, either by providing a URL or uploading a file archive (e.g., .zip). It can generate questions about the code using either a rule-based or LLM-based approach.
The system supports the following file types: .py, .java, and .kt. The analysis recursively processes all supported code files found within the uploaded or linked content.

---

## Endpoints

### 1. Analyze Codebase from URL

- **Endpoint:** `/analyze/url/`
- **Method:** `POST`
- **Description:** Analyzes a codebase from a provided public GitHub repository and generates questions about the code. (Note: This endpoint does not work with private repositories.)

#### Request Body (JSON)
- `url` (string, required): The URL to the codebase (e.g., GitHub repo).
- `llm` (boolean, optional): If true, uses an LLM for question generation. Defaults to false (uses rule-based).
- `focus` (string, optional): Focus area for question generation.

##### Example
```json
{
  "url": "https://github.com/example/repo",
  "llm": true,
  "focus": "security"
}
```

#### Response (JSON)
- `questions` (array): List of generated questions and answers.
- `error` (string, optional): Error message if the request fails.

##### Example
```json
{
  "questions": [
    {
      "question": "...",
      "answer": "...",
      "difficulty": "advanced",
      "component": "my_function",
      "type": "function"
    }
  ]
}
```

---

### 2. Analyze Codebase from File

- **Endpoint:** `/analyze/file/`
- **Method:** `POST`
- **Description:** Accepts a file upload for code analysis. (Implementation details may be similar to `/analyze/url/`.)


#### Request
- Likely expects a file upload (e.g., multipart/form-data).
- May accept similar parameters as `/analyze/url/`.

#### Response
- Similar to `/analyze/url/`.

---

## Error Handling

- Returns HTTP 400 for missing or invalid parameters.
- Returns HTTP 500 for server errors, with an `error` field in the response.

---

## Authentication

- No authentication is required for these endpoints by default.

---

## Notes

- For LLM-based question generation, an OpenAI API key must be provided via the `OPENAI_API_KEY` environment variable or as an argument.
- The number of questions returned is limited to 10 per request.

---

For further details, see the implementation in `analyze/views.py` and `analyze/questions/question_generator.py`.

