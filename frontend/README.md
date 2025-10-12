# Learning Skill - Frontend

A modern React.js frontend for the Competency-Based Learning System, featuring a beautiful splash screen, user selection, adaptive question delivery, and comprehensive profile tracking.

## Features

### 🎨 **Beautiful Design**
- Modern gradient backgrounds and glassmorphism effects
- Smooth animations with Framer Motion
- Responsive design for all screen sizes
- Intuitive user interface with consistent styling

### 🚀 **Splash Screen**
- Animated "Learning Skill" branding
- Feature highlights with icons
- Loading progress with dynamic messages
- One-time display per session

### 👥 **User Management**
- Dynamic user list from API
- User avatar generation with initials
- Smooth selection animations
- Error handling and loading states

### ❓ **Adaptive Questions**
- Skill-based question selection
- Support for MCQ and text-based questions
- Real-time answer validation
- Hint system for learning support
- Progress tracking with attempt recording

### 📊 **Profile Dashboard**
- Comprehensive user statistics
- Skill level visualization with progress bars
- Competency breakdown with color coding
- Performance metrics and accuracy tracking

## Quick Start

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- Backend API running on port 5000

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The app will be available at `http://localhost:3000`

### Building for Production

```bash
# Create production build
npm run build

# Serve the build (requires a server)
npx serve -s build
```

## Project Structure

```
frontend/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/
│   │   ├── SplashScreen.js     # Animated splash screen
│   │   ├── UserList.js         # User selection interface
│   │   ├── QuestionPage.js     # Question display and interaction
│   │   └── ProfilePage.js      # User profile and statistics
│   ├── services/
│   │   └── api.js             # API client and helpers
│   ├── App.js                 # Main app component
│   ├── index.js              # App entry point
│   └── index.css             # Global styles
├── package.json              # Dependencies and scripts
└── README.md                # This file
```

## Components Overview

### SplashScreen
- **Purpose**: Welcome screen with branding and loading
- **Features**: Animated logo, feature highlights, progress bar
- **Duration**: Shows for ~3 seconds with loading simulation

### UserList
- **Purpose**: Display all users and allow selection
- **Features**: User cards with avatars, hover effects, error handling
- **API**: Fetches users from `/api/users`

### QuestionPage
- **Purpose**: Display adaptive questions based on user skill level
- **Features**: MCQ/text support, hints, answer validation, attempt recording
- **API**: Uses `getRandomQuestion()` helper for skill-based selection

### ProfilePage
- **Purpose**: Show user statistics and skill levels
- **Features**: Progress bars, competency breakdown, performance metrics
- **API**: Fetches skill rankings and progress summary

## API Integration

### Service Functions
The app uses a comprehensive API service (`src/services/api.js`) with:

- **Health Check**: Verify API connectivity
- **User Management**: Get users, user details
- **Question System**: Fetch questions, record attempts
- **Skill Tracking**: Get rankings, update progress
- **Analytics**: Progress summaries, competency statistics

### Adaptive Question Selection
The app implements intelligent question selection:

1. **Fetch User Skills**: Get current skill rankings for all competencies
2. **Calculate Range**: Determine MMR range based on current skill level
3. **Find Skills**: Get skills within the calculated range
4. **Select Questions**: Pick questions associated with those skills
5. **Random Selection**: Choose a random question from available options

### Error Handling
- Network error detection and user-friendly messages
- Fallback to basic questions if skill-based selection fails
- Loading states for all async operations
- Graceful degradation when data is unavailable

## Styling and Design

### Design System
- **Colors**: Purple gradient theme (#667eea to #764ba2)
- **Typography**: Inter font family with weight variations
- **Spacing**: Consistent 8px grid system
- **Shadows**: Subtle depth with blur effects
- **Borders**: Rounded corners (8px, 12px, 16px, 20px)

### Animations
- **Framer Motion**: Page transitions and component animations
- **CSS Animations**: Loading spinners and progress bars
- **Hover Effects**: Interactive feedback on buttons and cards
- **Smooth Transitions**: 0.3s ease transitions for state changes

### Responsive Design
- **Mobile First**: Optimized for mobile devices
- **Breakpoints**: 768px for tablet/desktop adjustments
- **Flexible Layouts**: Grid and flexbox for adaptive layouts
- **Touch Friendly**: Appropriate button sizes and spacing

## Key Features Implementation

### Skill-Based Question Selection
```javascript
// Get questions appropriate for user's current skill level
const getQuestionsForUser = async (userId) => {
  const skillRankings = await apiService.getUserSkillRankings(userId);
  // Calculate MMR range based on current skills
  // Find skills within range
  // Get questions for those skills
  // Return unique questions
};
```

### Progress Tracking
```javascript
// Record user attempts and update progress
const recordAttempt = async (userId, questionId, answer, isCorrect) => {
  await apiService.recordAttempt(userId, {
    question_id: questionId,
    user_answer: answer,
    is_correct: isCorrect
  });
};
```

### Visual Feedback
- **Correct Answers**: Green checkmark with success animation
- **Incorrect Answers**: Red X with explanation
- **Skill Levels**: Color-coded progress bars and badges
- **Loading States**: Spinners and skeleton screens

## Configuration

### Environment Variables
The app can be configured with environment variables:

```bash
# API Base URL (default: /api)
REACT_APP_API_BASE_URL=/api

# Enable debug mode
REACT_APP_DEBUG=true
```

### Proxy Configuration
Development server proxies API requests to backend:

```json
{
  "proxy": "http://localhost:5000"
}
```

## Browser Support

- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

## Performance Optimizations

- **Code Splitting**: Automatic with Create React App
- **Lazy Loading**: Components loaded on demand
- **Memoization**: React.memo for expensive components
- **Image Optimization**: Optimized icons and graphics
- **Bundle Analysis**: Use `npm run build` to analyze bundle size

## Development

### Available Scripts
- `npm start`: Start development server
- `npm test`: Run test suite
- `npm run build`: Create production build
- `npm run eject`: Eject from Create React App (not recommended)

### Code Style
- **ESLint**: Configured with React rules
- **Prettier**: Code formatting (if configured)
- **Component Structure**: Functional components with hooks
- **File Naming**: PascalCase for components, camelCase for utilities

## Deployment

### Build Process
```bash
# Create optimized production build
npm run build

# Test the build locally
npx serve -s build
```

### Deployment Options
- **Netlify**: Drag and drop build folder
- **Vercel**: Connect GitHub repository
- **AWS S3**: Upload build folder to S3 bucket
- **Traditional Hosting**: Upload build folder to web server

### Environment Configuration
For production deployment, ensure:
1. API backend is accessible
2. CORS is configured correctly
3. Environment variables are set
4. HTTPS is enabled for security

## Troubleshooting

### Common Issues

**API Connection Errors**
- Verify backend is running on port 5000
- Check CORS configuration
- Ensure proxy is working in development

**Question Loading Issues**
- Check user skill rankings exist
- Verify question-skill relationships in database
- Review API error logs

**Styling Issues**
- Clear browser cache
- Check for CSS conflicts
- Verify all dependencies are installed

### Debug Mode
Enable debug mode to see detailed logs:

```javascript
// In browser console
localStorage.setItem('debug', 'true');
```

## Contributing

1. Follow existing code style and patterns
2. Add appropriate error handling
3. Include loading states for async operations
4. Test on multiple screen sizes
5. Update documentation for new features

## License

This project is part of the Competency-Based Learning System.


