# GitHub Copilot Instructions - Mergington High School Activities API

## Project Overview

This is a **GitHub Copilot skills learning exercise** demonstrating a simple full-stack application. The project shows how to build and enhance a FastAPI backend with a vanilla HTML/CSS/JavaScript frontend.

**Purpose**: Learn GitHub Copilot capabilities by building features for managing high school extracurricular activities.

## Project Structure

```
/src
├── app.py                 # FastAPI backend (main application)
└── static/
    ├── index.html         # Frontend HTML structure
    ├── app.js             # Frontend JavaScript (API interaction, DOM manipulation)
    └── styles.css         # Frontend styling
requirements.txt           # Python dependencies (FastAPI, uvicorn, httpx, watchfiles)
pytest.ini                 # Pytest configuration
```

## Technology Stack

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: Vanilla JavaScript (no frameworks), HTML5, CSS3
- **Testing**: pytest
- **Package Manager**: pip

## Application Features

The application manages extracurricular activities at Mergington High School:

- **View Activities**: Display all available activities with descriptions, schedules, and current enrollment
- **Sign Up**: Students can register for activities (with capacity limits)
- **Unregister**: Students can cancel their enrollment
- **Data Storage**: In-memory database (resets on server restart)

### API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Redirects to frontend |
| GET | `/activities` | Returns all activities with details |
| POST | `/activities/{name}/signup?email=...` | Student sign-up |
| POST | `/activities/{name}/unregister?email=...` | Student unregister |

## Development Workflow

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Start the development server (with auto-reload)
python src/app.py
# or
uvicorn src.app:app --reload
```

Server runs at `http://localhost:8000`
- API docs: `http://localhost:8000/docs` (Swagger UI)
- Alternative docs: `http://localhost:8000/redoc` (ReDoc)

### Running Tests

```bash
pytest
# or with verbose output
pytest -v
```

## Code Style & Conventions

### Python (Backend)

- Use FastAPI best practices: route organization, proper HTTP status codes, exception handling
- Add docstrings to endpoints and functions
- In-memory data model with activity names as keys
- Validate inputs (email format, activity existence, capacity limits)
- Use snake_case for variables and functions

### JavaScript (Frontend)

- Vanilla JavaScript (no frameworks like React/Vue)
- Use fetch API for HTTP requests
- Clear naming: fetch functions should start with `fetch`, handlers with `handle`, etc.
- Use const/let (no var)
- Add error handling and user feedback (success/error messages)
- DOM selectors via id: `document.getElementById()`

### CSS

- Use semantic class names (e.g., `.activity-card`, `form-group`)
- Mobile-responsive design with max-width constraints
- Consistent color scheme (currently: #1a237e for headers)
- Utility classes for common patterns (e.g., `.hidden`)

## When Working with This Codebase

### Backend Tasks

- When adding API endpoints: Include proper error handling and HTTP status codes
- When modifying the activities model: Keep the in-memory structure simple
- When adding validation: Check email format, capacity limits, duplicate signups

### Frontend Tasks

- When updating HTML: Keep semantic structure; avoid changing element IDs
- When modifying JavaScript: Use async/await for fetch calls; always handle errors
- When styling: Update styles.css directly; maintain mobile responsiveness

### Adding New Features

1. First update the backend API (`app.py`)
2. Then update the frontend JavaScript (`app.js`)
3. Add styling to `styles.css` if needed
4. Test via the browser and API docs

## Common Patterns & Examples

### Adding API Errors

```python
if not condition:
    raise HTTPException(status_code=400, detail="Clear error message")
```

### Fetching and Handling API Responses

```javascript
try {
    const response = await fetch("/activities");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    // Process data
} catch (error) {
    console.error("Error:", error);
    messageDiv.textContent = "Failed to load activities";
}
```

## Git Workflow

- Main branch: `main` (default)
- Feature branches: Create feature branches for exercises (e.g., `accelerate-with-copilot`)
- Commit messages: Use clear, descriptive commits (e.g., "Add unregister endpoint" or "Update activity styling")

## Troubleshooting & Tips

- **Port already in use**: Change port with `uvicorn src.app:app --reload --port 8001`
- **Module not found**: Ensure dependencies are installed (`pip install -r requirements.txt`)
- **Frontend not loading**: Check browser console for errors; ensure server is running
- **Cors issues**: FastAPI automatically handles CORS for routes under `/static`

## Exercise Goals & Learning Outcomes

This project teaches:

1. **API Design**: RESTful endpoint structure and HTTP methods
2. **Frontend Integration**: Fetching data and handling responses
3. **Input Validation**: Server-side and client-side validation
4. **Error Handling**: Graceful error messages for users
5. **Full-Stack Development**: Connecting backend logic with UI

