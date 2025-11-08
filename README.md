# CodePilot Raindrop Backend

A Raindrop MCP application that automatically reviews GitHub push events using Claude AI.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root with your API keys:

```env
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
RAINDROP_API_KEY=lm_apikey_xxxxxxxxxxxxxxxxx
```

## Usage

### Local Development

Start the Raindrop development server:

```bash
raindrop dev
```

The server will start on `http://localhost:8787`.

### Testing

Execute the test script to trigger a mock GitHub push event:

```bash
bash test.sh
```

This will:
1. Send a POST request to the GitHub webhook endpoint with `mock_push.json`
2. Fetch the latest review from the API

### Deployment

Deploy the backend to production:

```bash
bash deploy.sh
```

After deployment, copy the webhook URL provided and configure it in GitHub → Settings → Webhooks.

## Architecture

The application processes GitHub push events through the following flow:

1. **GitHub Webhook** receives push events
2. **extract_diff.py** parses the payload and extracts:
   - Repository name
   - Commit SHA
   - Author information
   - Changed files
   - Diff text
3. **review_with_claude.py** sends the diff to Claude API for code review
4. Results are stored in the `reviews` bucket
5. Notification is sent to `/api/notify` endpoint

## Claude JSON Response Format

### Review Response (`review_with_claude.py`)

The Claude API returns a JSON object with the following structure:

```json
{
  "summary": [
    "Brief summary point 1",
    "Brief summary point 2",
    "Brief summary point 3"
  ],
  "risks": [
    "Potential security issue in authentication",
    "Missing input validation"
  ],
  "tests": [
    "Add unit tests for new API endpoint",
    "Test error handling paths"
  ],
  "refactor_suggestions": [
    "Extract common logic into helper function",
    "Consider using async/await for better performance"
  ]
}
```

### Improvement Response (`improve_with_claude.py`)

For code improvement requests, Claude returns:

```json
{
  "explanation": "This refactoring improves code readability by extracting the validation logic into a separate function, making the main function more focused and testable.",
  "patch": "def validate_input(data):\n    # validation logic\n    return True\n\n# updated code using validate_input"
}
```

## Example Output

When you run `test.sh`, you should see output similar to:

```json
{
  "repo": "test-owner/test-repo",
  "sha": "def456ghi789",
  "author": "testuser",
  "files_changed": ["src/api/endpoints.py", "src/utils/errors.py"],
  "diff_text": "Message: Update API endpoints and add error handling\nFiles: ['src/api/endpoints.py', 'src/utils/errors.py']",
  "created_at": "2024-01-15T10:30:00.123456",
  "summary": [
    "Added error handling to API endpoints",
    "Improved error utility functions",
    "Enhanced code maintainability"
  ],
  "risks": [
    "Missing input validation on new endpoints"
  ],
  "tests": [
    "Add tests for error handling paths"
  ],
  "refactor_suggestions": [
    "Consider extracting error handling into middleware"
  ]
}
```

## Project Structure

```
Hackathon_Project/
├── raindrop/
│   ├── app.rd                    # Raindrop graph definition
│   ├── transforms/
│   │   ├── extract_diff.py      # Parse GitHub push payload
│   │   ├── review_with_claude.py # Generate code review with Claude
│   │   └── improve_with_claude.py # Improve code with Claude
│   └── prompts/
│       ├── review_prompt.txt     # Code review prompt template
│       └── improve_prompt.txt    # Code improvement prompt template
├── mock_push.json                # Sample GitHub push payload
├── test.sh                       # Test script
├── deploy.sh                     # Deployment script
├── .env                          # Environment variables (not in git)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Notes

- The application expects Claude to return strict JSON format
- JSON parsing errors are handled gracefully with default fallback values
- All prompts use Python string formatting with placeholders (e.g., `{repo}`, `{sha}`)
- The `improve_with_claude.py` transform is optional and can be used for targeted code improvements

