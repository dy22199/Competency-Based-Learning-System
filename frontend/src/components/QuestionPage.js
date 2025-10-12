import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  HelpCircle, 
  CheckCircle, 
  XCircle, 
  ArrowRight, 
  RotateCcw, 
  Loader,
  User,
  Target,
  Brain
} from 'lucide-react';
import { getRandomQuestion, apiService } from '../services/api';

const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  color: white;
`;

const UserAvatar = styled.div`
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  backdrop-filter: blur(10px);
`;

const UserName = styled.span`
  font-size: 1.1rem;
  font-weight: 500;
`;

const ProfileButton = styled.button`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
  }
`;

const QuestionContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const QuestionCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 32px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
`;

const QuestionHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
`;

const QuestionIcon = styled.div`
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
`;

const QuestionInfo = styled.div`
  flex: 1;
`;

const QuestionType = styled.div`
  font-size: 0.9rem;
  color: #667eea;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const QuestionText = styled.h2`
  font-size: 1.4rem;
  font-weight: 600;
  color: #333;
  line-height: 1.5;
  margin: 16px 0;
`;

const OptionsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 24px 0;
`;

const OptionButton = styled.button`
  padding: 16px 20px;
  background: ${props => props.selected ? '#667eea' : 'white'};
  color: ${props => props.selected ? 'white' : '#333'};
  border: 2px solid ${props => props.selected ? '#667eea' : '#e0e0e0'};
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  
  &:hover {
    border-color: #667eea;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const TextInput = styled.input`
  width: 100%;
  padding: 16px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const HintContainer = styled.div`
  background: #f8f9ff;
  border: 1px solid #e0e7ff;
  border-radius: 12px;
  padding: 16px;
  margin: 20px 0;
`;

const HintTitle = styled.div`
  font-size: 0.9rem;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const HintText = styled.p`
  font-size: 0.95rem;
  color: #555;
  line-height: 1.5;
`;

const AnswerContainer = styled(motion.div)`
  margin-top: 24px;
  padding: 20px;
  border-radius: 12px;
  background: ${props => props.correct ? '#f0f9ff' : '#fef2f2'};
  border: 1px solid ${props => props.correct ? '#bfdbfe' : '#fecaca'};
`;

const AnswerHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
`;

const AnswerTitle = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: ${props => props.correct ? '#059669' : '#dc2626'};
`;

const AnswerText = styled.p`
  font-size: 1rem;
  color: #333;
  font-weight: 500;
`;

const ActionButtons = styled.div`
  display: flex;
  gap: 12px;
  margin-top: 24px;
`;

const ActionButton = styled.button`
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
  }
  
  &.secondary {
    background: white;
    color: #667eea;
    border: 2px solid #667eea;
    
    &:hover {
      background: #667eea;
      color: white;
    }
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const LoadingContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: white;
`;

const LoadingText = styled.p`
  margin-top: 16px;
  font-size: 1.1rem;
  opacity: 0.9;
`;

const ErrorContainer = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  color: #c53030;
  border: 1px solid rgba(197, 48, 48, 0.2);
`;

const ErrorTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 8px;
`;

const ErrorMessage = styled.p`
  font-size: 1rem;
  opacity: 0.8;
`;

const QuestionPage = ({ user, onProfileClick, onBackToUsers }) => {
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [showAnswer, setShowAnswer] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadQuestion();
  }, []);

  const loadQuestion = async () => {
    try {
      setLoading(true);
      setError(null);
      setShowAnswer(false);
      setSelectedAnswer('');
      
      const question = await getRandomQuestion(user.Id);
      setCurrentQuestion(question);
    } catch (err) {
      console.error('Error loading question:', err);
      setError(err.message || 'Failed to load question');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (answer) => {
    if (showAnswer) return;
    setSelectedAnswer(answer);
  };

  const handleSubmit = async () => {
    if (!selectedAnswer || !currentQuestion) return;

    const correct = selectedAnswer.trim().toLowerCase() === 
                   currentQuestion.QuestionsAnswer.trim().toLowerCase();
    
    setIsCorrect(correct);
    setShowAnswer(true);

    // Record the attempt
    try {
      await apiService.recordAttempt(user.Id, {
        question_id: currentQuestion.Id,
        user_answer: selectedAnswer,
        is_correct: correct
      });
    } catch (err) {
      console.error('Error recording attempt:', err);
    }
  };

  const handleNextQuestion = () => {
    loadQuestion();
  };

  const getInitials = (username) => {
    return username
      .split(' ')
      .map(word => word.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const parseOptions = (optionsString) => {
    if (!optionsString) return [];
    try {
      return JSON.parse(optionsString);
    } catch {
      return optionsString.split(',').map(opt => opt.trim());
    }
  };

  if (loading) {
    return (
      <Container>
        <LoadingContainer>
          <Loader size={48} className="animate-spin" />
          <LoadingText>Loading your personalized question...</LoadingText>
        </LoadingContainer>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <QuestionContainer>
          <ErrorContainer>
            <ErrorTitle>Error Loading Question</ErrorTitle>
            <ErrorMessage>{error}</ErrorMessage>
            <ActionButton className="primary" onClick={loadQuestion}>
              <RotateCcw size={16} />
              Try Again
            </ActionButton>
          </ErrorContainer>
        </QuestionContainer>
      </Container>
    );
  }

  if (!currentQuestion) {
    return (
      <Container>
        <QuestionContainer>
          <ErrorContainer>
            <ErrorTitle>No Questions Available</ErrorTitle>
            <ErrorMessage>No questions are available for your skill level.</ErrorMessage>
          </ErrorContainer>
        </QuestionContainer>
      </Container>
    );
  }

  const isMCQ = currentQuestion.QuestionType === 'MCQ';
  const options = isMCQ ? parseOptions(currentQuestion.Options) : [];

  return (
    <Container>
      <Header>
        <UserInfo>
          <UserAvatar>
            {getInitials(user.UserName)}
          </UserAvatar>
          <UserName>{user.UserName}</UserName>
        </UserInfo>
        
        <ProfileButton onClick={onProfileClick}>
          <User size={16} />
          Profile
        </ProfileButton>
      </Header>

      <QuestionContainer>
        <AnimatePresence mode="wait">
          <QuestionCard
            key={currentQuestion.Id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
          >
            <QuestionHeader>
              <QuestionIcon>
                <HelpCircle size={24} />
              </QuestionIcon>
              <QuestionInfo>
                <QuestionType>{currentQuestion.QuestionType}</QuestionType>
              </QuestionInfo>
            </QuestionHeader>

            <QuestionText>{currentQuestion.QuestionDescription}</QuestionText>

            {currentQuestion.QuestionHint && (
              <HintContainer>
                <HintTitle>
                  <Brain size={16} />
                  Hint
                </HintTitle>
                <HintText>{currentQuestion.QuestionHint}</HintText>
              </HintContainer>
            )}

            {isMCQ ? (
              <OptionsContainer>
                {options.map((option, index) => (
                  <OptionButton
                    key={index}
                    selected={selectedAnswer === option}
                    onClick={() => handleAnswerSelect(option)}
                    disabled={showAnswer}
                  >
                    {option}
                  </OptionButton>
                ))}
              </OptionsContainer>
            ) : (
              <TextInput
                type="text"
                placeholder="Enter your answer..."
                value={selectedAnswer}
                onChange={(e) => setSelectedAnswer(e.target.value)}
                disabled={showAnswer}
                onKeyPress={(e) => e.key === 'Enter' && !showAnswer && handleSubmit()}
              />
            )}

            {!showAnswer && (
              <ActionButtons>
                <ActionButton 
                  className="primary" 
                  onClick={handleSubmit}
                  disabled={!selectedAnswer}
                >
                  Submit Answer
                  <ArrowRight size={16} />
                </ActionButton>
              </ActionButtons>
            )}

            {showAnswer && (
              <AnswerContainer
                correct={isCorrect}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                <AnswerHeader>
                  {isCorrect ? (
                    <>
                      <CheckCircle size={20} color="#059669" />
                      <AnswerTitle correct={isCorrect}>Correct!</AnswerTitle>
                    </>
                  ) : (
                    <>
                      <XCircle size={20} color="#dc2626" />
                      <AnswerTitle correct={isCorrect}>Incorrect</AnswerTitle>
                    </>
                  )}
                </AnswerHeader>
                
                <AnswerText>
                  <strong>Your answer:</strong> {selectedAnswer}
                </AnswerText>
                <AnswerText>
                  <strong>Correct answer:</strong> {currentQuestion.QuestionsAnswer}
                </AnswerText>

                <ActionButtons>
                  <ActionButton className="primary" onClick={handleNextQuestion}>
                    Next Question
                    <ArrowRight size={16} />
                  </ActionButton>
                </ActionButtons>
              </AnswerContainer>
            )}
          </QuestionCard>
        </AnimatePresence>
      </QuestionContainer>
    </Container>
  );
};

export default QuestionPage;



