# MediVault - Healthcare Emergency Frontend

A modern React.js frontend application for healthcare emergency management, built with a focus on clean design and responsive UI.

## Features

- Emergency notification system with location sharing
- AI/ML voice analysis integration
- User profile management
- Responsive design for all device sizes
- Modern healthcare-themed UI with Tailwind CSS

## Technology Stack

- React.js - UI library
- React Router - Navigation and routing
- Tailwind CSS - Styling and responsive design
- Axios - API integration

## Prerequisites

- Node.js (v14.0.0 or higher)
- npm (v6.0.0 or higher)

## Installation

1. Clone the repository
```
git clone <repository-url>
```

2. Navigate to the frontend directory
```
cd frontend
```

3. Install dependencies
```
npm install
```

## Development

Start the development server:
```
npm start
```

The application will be available at `http://localhost:3000`.

## Building for Production

Create an optimized production build:
```
npm run build
```

## API Integration

The application is designed to integrate with the following backend endpoints:

- `/notify-emergency` - POST endpoint to notify emergency services with location data
- `/ai/emergency-voice` - GET endpoint for AI voice analysis

## Integration with Backend

The Axios HTTP client is pre-configured to make API calls to your backend services. Update the base URL in a production environment.

## Folder Structure

```
/frontend
│
├── public/              # Public assets
│   └── index.html       # Root HTML file
│
├── src/                 # Source code
│   ├── App.js           # Main app component with routing
│   ├── App.css          # Global styles
│   ├── Sidebar.js       # Navigation sidebar
│   ├── EmergencyPage.js # Emergency notification UI
│   ├── Dashboard.js     # Main dashboard
│   ├── Profile.js       # User profile management
│   ├── Settings.js      # User settings
│   └── index.js         # Application entry point
│
└── package.json         # Dependencies and scripts
```

## License

[MIT License](LICENSE) 