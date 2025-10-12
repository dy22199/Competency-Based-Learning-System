import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import SplashScreen from './components/SplashScreen';
import UserList from './components/UserList';
import QuestionPage from './components/QuestionPage';
import ProfilePage from './components/ProfilePage';

const AppContainer = styled.div`
  min-height: 100vh;
  width: 100%;
`;

const App = () => {
  const [currentView, setCurrentView] = useState('splash');
  const [selectedUser, setSelectedUser] = useState(null);
  const [splashComplete, setSplashComplete] = useState(false);

  useEffect(() => {
    // Check if splash has been completed in this session
    const splashCompleted = sessionStorage.getItem('splashCompleted');
    if (splashCompleted) {
      setSplashComplete(true);
      setCurrentView('users');
    }
  }, []);

  const handleSplashComplete = () => {
    setSplashComplete(true);
    setCurrentView('users');
    sessionStorage.setItem('splashCompleted', 'true');
  };

  const handleUserSelect = (user) => {
    setSelectedUser(user);
    setCurrentView('questions');
  };

  const handleBackToUsers = () => {
    setSelectedUser(null);
    setCurrentView('users');
  };

  const handleProfileClick = () => {
    setCurrentView('profile');
  };

  const handleBackToQuestions = () => {
    setCurrentView('questions');
  };

  const renderCurrentView = () => {
    switch (currentView) {
      case 'splash':
        return <SplashScreen onComplete={handleSplashComplete} />;
      
      case 'users':
        return <UserList onUserSelect={handleUserSelect} />;
      
      case 'questions':
        return (
          <QuestionPage
            user={selectedUser}
            onProfileClick={handleProfileClick}
            onBackToUsers={handleBackToUsers}
          />
        );
      
      case 'profile':
        return (
          <ProfilePage
            user={selectedUser}
            onBackToQuestions={handleBackToQuestions}
            onBackToUsers={handleBackToUsers}
          />
        );
      
      default:
        return <UserList onUserSelect={handleUserSelect} />;
    }
  };

  return (
    <AppContainer>
      {renderCurrentView()}
    </AppContainer>
  );
};

export default App;



