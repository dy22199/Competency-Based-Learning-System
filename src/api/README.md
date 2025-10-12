# Competency-Based Learning API

A REST API for managing competency-based learning systems, built with Flask and SQLite.

## Features

- **Complete CRUD Operations** for all database entities
- **RESTful API Design** with consistent response formats
- **Data Validation** with comprehensive error handling
- **CORS Support** for frontend integration
- **Configuration Management** for different environments
- **Analytics Endpoints** for progress tracking and reporting

## Quick Start

### 1. Installation

```bash
# Navigate to the API directory
cd src/api

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

Make sure you have the database created:

```bash
# From the project root
cd src/sql
python create_database.py
```

### 3. Run the API

```bash
# Development mode
python run.py

# Or directly
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /api/health` - Check API status

### Competencies
- `GET /api/competencies` - Get all competencies
- `GET /api/competencies/{code}` - Get competency by code
- `POST /api/competencies` - Create new competency

### Skills
- `GET /api/competencies/{id}/skills` - Get skills by competency ID
- `GET /api/competencies/code/{code}/skills` - Get skills by competency code
- `GET /api/skills/mmr-range?min_mmr=X&max_mmr=Y` - Get skills by MMR range
- `POST /api/skills` - Create new skill

### Questions
- `GET /api/questions` - Get all questions
- `GET /api/questions/type/{type}` - Get questions by type
- `GET /api/skills/{id}/questions` - Get questions by skill
- `GET /api/competencies/{id}/questions` - Get questions by competency
- `POST /api/questions` - Create new question
- `POST /api/questions/{id}/skills/{skill_id}` - Link question to skill

### Users
- `GET /api/users` - Get all users
- `GET /api/users/{id}` - Get user by ID
- `GET /api/users/name/{username}` - Get user by username
- `POST /api/users` - Create new user

### User Attempts
- `GET /api/users/{id}/attempts` - Get user's question attempts
- `GET /api/users/{id}/questions/{question_id}/attempts` - Get attempts for specific question
- `GET /api/users/{id}/attempts/correct` - Get correct attempts
- `GET /api/users/{id}/attempts/incorrect` - Get incorrect attempts
- `POST /api/users/{id}/attempts` - Record question attempt

### Skill Rankings
- `GET /api/users/{id}/skill-rankings` - Get user's skill rankings
- `GET /api/users/{id}/competencies/{id}/skill-ranking` - Get specific skill ranking
- `PUT /api/users/{id}/competencies/{id}/skill-ranking` - Update skill ranking
- `GET /api/competencies/{id}/users` - Get users by competency ranking

### Analytics
- `GET /api/users/{id}/progress-summary` - Get user progress summary
- `GET /api/competencies/{id}/statistics` - Get competency statistics

## Request/Response Format

### Standard Response Format

```json
{
  "success": true,
  "data": [...],
  "count": 10,
  "message": "Operation completed successfully"
}
```

### Error Response Format

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

## Example Usage

### Create a New User

```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe"}'
```

### Record a Question Attempt

```bash
curl -X POST http://localhost:5000/api/users/1001/attempts \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": 1001,
    "user_answer": "The car\'s speed is 60 km/h",
    "is_correct": true
  }'
```

### Get User Progress Summary

```bash
curl http://localhost:5000/api/users/1001/progress-summary
```

### Get Questions for a Specific Skill

```bash
curl http://localhost:5000/api/skills/1/questions
```

## Configuration

### Environment Variables

Copy `env_example.txt` to `.env` and configure:

```bash
cp env_example.txt .env
```

Key configuration options:

- `FLASK_ENV`: Environment (development/production/testing)
- `SECRET_KEY`: Secret key for Flask sessions
- `DATABASE_PATH`: Path to SQLite database file
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)
- `RATE_LIMIT`: API rate limit (requests per minute)

### Development vs Production

**Development Mode:**
- Debug mode enabled
- CORS allows localhost origins
- Uses local database file

**Production Mode:**
- Debug mode disabled
- Requires SECRET_KEY environment variable
- Stricter CORS configuration
- Can use different database path

## Data Models

### Competency
```json
{
  "id": 1,
  "competency_code": "C1",
  "competency_name": "Language Comprehension",
  "domain_code": "D1",
  "domain_name": "Ability/pace of reading",
  "description": ""
}
```

### Skill
```json
{
  "id": 1,
  "competency_id": 1,
  "stage": "S1",
  "short_description": "Print Concepts & Tracking",
  "description": "Follow left-to-right, top-to-bottom...",
  "start_mmr": 0,
  "end_mmr": 1000
}
```

### Question
```json
{
  "id": 1001,
  "question_type": "MCQ",
  "question_description": "Choose the sentence that reads correctly...",
  "options": "[\"Option 1\", \"Option 2\", \"Option 3\"]",
  "questions_answer": "The car's speed is 60 km/h",
  "question_hint": "Pick correct unit and a well-formed sentence."
}
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid request data or missing required fields
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side errors

All errors return a consistent JSON format with error type and message.

## Testing

### Manual Testing

Use tools like curl, Postman, or any HTTP client to test endpoints.

### Example Test Script

```python
import requests

# Test health endpoint
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# Test getting competencies
response = requests.get('http://localhost:5000/api/competencies')
print(f"Found {response.json()['count']} competencies")
```

## Deployment

### Using Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## Integration Examples

### Frontend Integration (JavaScript)

```javascript
// Fetch competencies
fetch('/api/competencies')
  .then(response => response.json())
  .then(data => {
    console.log('Competencies:', data.data);
  });

// Record question attempt
fetch('/api/users/1001/attempts', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question_id: 1001,
    user_answer: 'My answer',
    is_correct: true
  })
});
```

### Python Client

```python
import requests

class CompetencyAPIClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
    
    def get_competencies(self):
        response = requests.get(f'{self.base_url}/api/competencies')
        return response.json()
    
    def record_attempt(self, user_id, question_id, answer, is_correct):
        data = {
            'question_id': question_id,
            'user_answer': answer,
            'is_correct': is_correct
        }
        response = requests.post(
            f'{self.base_url}/api/users/{user_id}/attempts',
            json=data
        )
        return response.json()

# Usage
client = CompetencyAPIClient()
competencies = client.get_competencies()
```

## Contributing

1. Follow RESTful API conventions
2. Add proper error handling for new endpoints
3. Update documentation for new features
4. Test all endpoints before submitting changes

## License

This project is part of the Competency-Based Learning System.
