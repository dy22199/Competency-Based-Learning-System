import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { BookOpen, Brain, Target, Zap } from 'lucide-react';

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const pulse = keyframes`
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
`;

const float = keyframes`
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
`;

const SplashContainer = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  overflow: hidden;
`;

const BackgroundPattern = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  animation: ${float} 6s ease-in-out infinite;
`;

const LogoContainer = styled.div`
  position: relative;
  z-index: 2;
  text-align: center;
  animation: ${fadeIn} 1s ease-out;
`;

const LogoIcon = styled.div`
  width: 120px;
  height: 120px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
  animation: ${pulse} 2s ease-in-out infinite;
`;

const AppTitle = styled.h1`
  font-size: 3rem;
  font-weight: 700;
  color: white;
  margin-bottom: 8px;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  letter-spacing: -0.02em;
`;

const AppSubtitle = styled.p`
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 40px;
  font-weight: 400;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
`;

const FeaturesContainer = styled.div`
  display: flex;
  gap: 32px;
  margin-top: 40px;
  animation: ${fadeIn} 1s ease-out 0.5s both;
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 20px;
  }
`;

const Feature = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  color: white;
  opacity: 0.9;
  transition: opacity 0.3s ease;
  
  &:hover {
    opacity: 1;
  }
`;

const FeatureIcon = styled.div`
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
`;

const FeatureText = styled.span`
  font-size: 0.9rem;
  font-weight: 500;
  text-align: center;
`;

const LoadingContainer = styled.div`
  position: absolute;
  bottom: 60px;
  left: 50%;
  transform: translateX(-50%);
  animation: ${fadeIn} 1s ease-out 1s both;
`;

const LoadingText = styled.p`
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  margin-bottom: 16px;
  text-align: center;
`;

const ProgressBar = styled.div`
  width: 200px;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  overflow: hidden;
`;

const ProgressFill = styled.div`
  height: 100%;
  background: white;
  border-radius: 2px;
  width: ${props => props.progress}%;
  transition: width 0.3s ease;
`;

const SplashScreen = ({ onComplete }) => {
  const [progress, setProgress] = useState(0);
  const [loadingText, setLoadingText] = useState('Initializing...');

  useEffect(() => {
    const loadingMessages = [
      'Initializing...',
      'Loading competencies...',
      'Preparing questions...',
      'Setting up user profiles...',
      'Almost ready...'
    ];

    let messageIndex = 0;
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + 20;
        if (newProgress >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            onComplete();
          }, 500);
          return 100;
        }
        return newProgress;
      });

      if (messageIndex < loadingMessages.length - 1) {
        setLoadingText(loadingMessages[messageIndex]);
        messageIndex++;
      }
    }, 600);

    return () => clearInterval(interval);
  }, [onComplete]);

  return (
    <SplashContainer>
      <BackgroundPattern />
      
      <LogoContainer>
        <LogoIcon>
          <BookOpen size={48} color="white" />
        </LogoIcon>
        
        <AppTitle>Learning Skill</AppTitle>
        <AppSubtitle>Master Your Competencies</AppSubtitle>
        
        <FeaturesContainer>
          <Feature>
            <FeatureIcon>
              <Brain size={24} color="white" />
            </FeatureIcon>
            <FeatureText>Smart Learning</FeatureText>
          </Feature>
          
          <Feature>
            <FeatureIcon>
              <Target size={24} color="white" />
            </FeatureIcon>
            <FeatureText>Skill Tracking</FeatureText>
          </Feature>
          
          <Feature>
            <FeatureIcon>
              <Zap size={24} color="white" />
            </FeatureIcon>
            <FeatureText>Adaptive Questions</FeatureText>
          </Feature>
        </FeaturesContainer>
      </LogoContainer>
      
      <LoadingContainer>
        <LoadingText>{loadingText}</LoadingText>
        <ProgressBar>
          <ProgressFill progress={progress} />
        </ProgressBar>
      </LoadingContainer>
    </SplashContainer>
  );
};

export default SplashScreen;



