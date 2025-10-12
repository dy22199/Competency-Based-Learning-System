import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { 
  User, 
  ArrowLeft, 
  Target, 
  TrendingUp, 
  Award, 
  BookOpen,
  Loader,
  BarChart3,
  CheckCircle
} from 'lucide-react';
import { apiService } from '../services/api';

const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 30px;
`;

const BackButton = styled.button`
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

const HeaderTitle = styled.h1`
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
`;

const ProfileContainer = styled.div`
  max-width: 900px;
  margin: 0 auto;
`;

const UserInfoCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 32px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
`;

const UserHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
`;

const UserAvatar = styled.div`
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2rem;
  font-weight: 700;
`;

const UserDetails = styled.div`
  flex: 1;
`;

const UserName = styled.h2`
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
`;

const UserId = styled.p`
  font-size: 1rem;
  color: #666;
  font-weight: 500;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 24px;
`;

const StatCard = styled.div`
  background: #f8f9ff;
  border: 1px solid #e0e7ff;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
`;

const StatIcon = styled.div`
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  color: white;
`;

const StatValue = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 4px;
`;

const StatLabel = styled.div`
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
`;

const SkillLevelsCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 32px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
`;

const CardHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
`;

const CardTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
`;

const CompetenciesGrid = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const CompetencyCard = styled.div`
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: #667eea;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
  }
`;

const CompetencyHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
`;

const CompetencyName = styled.h4`
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
`;

const CompetencyCode = styled.span`
  font-size: 0.9rem;
  color: #667eea;
  font-weight: 600;
  text-transform: uppercase;
`;

const SkillRank = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
`;

const SkillBar = styled.div`
  width: 100%;
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 12px;
`;

const SkillProgress = styled.div`
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  transition: width 0.6s ease;
  width: ${props => Math.min(props.percentage, 100)}%;
`;

const SkillLabel = styled.div`
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 0.85rem;
  color: #666;
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

const EmptyState = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 60px 32px;
  text-align: center;
  color: #666;
`;

const EmptyIcon = styled.div`
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  color: white;
`;

const EmptyTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
`;

const EmptyMessage = styled.p`
  font-size: 1rem;
  opacity: 0.8;
`;

const ProfilePage = ({ user, onBackToQuestions, onBackToUsers }) => {
  const [skillRankings, setSkillRankings] = useState([]);
  const [progressSummary, setProgressSummary] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadUserData();
  }, [user]);

  const loadUserData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [rankingsResponse, progressResponse] = await Promise.all([
        apiService.getUserSkillRankings(user.Id),
        apiService.getUserProgressSummary(user.Id)
      ]);
      
      setSkillRankings(rankingsResponse.data || []);
      setProgressSummary(progressResponse.data || []);
    } catch (err) {
      console.error('Error loading user data:', err);
      setError(err.message || 'Failed to load user data');
    } finally {
      setLoading(false);
    }
  };

  const getInitials = (username) => {
    return username
      .split(' ')
      .map(word => word.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const getSkillLevel = (skillRank) => {
    if (skillRank >= 5000) return 'Expert';
    if (skillRank >= 4000) return 'Advanced';
    if (skillRank >= 3000) return 'Intermediate';
    if (skillRank >= 2000) return 'Beginner+';
    if (skillRank >= 1000) return 'Beginner';
    return 'Novice';
  };

  const getSkillColor = (skillRank) => {
    if (skillRank >= 5000) return '#059669';
    if (skillRank >= 4000) return '#0891b2';
    if (skillRank >= 3000) return '#7c3aed';
    if (skillRank >= 2000) return '#ea580c';
    if (skillRank >= 1000) return '#dc2626';
    return '#6b7280';
  };

  const calculateProgressPercentage = (skillRank) => {
    // Assuming max skill rank is 7000 (from the database schema)
    return (skillRank / 7000) * 100;
  };

  if (loading) {
    return (
      <Container>
        <LoadingContainer>
          <Loader size={48} className="animate-spin" />
          <LoadingText>Loading your profile...</LoadingText>
        </LoadingContainer>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <ProfileContainer>
          <ErrorContainer>
            <ErrorTitle>Error Loading Profile</ErrorTitle>
            <ErrorMessage>{error}</ErrorMessage>
          </ErrorContainer>
        </ProfileContainer>
      </Container>
    );
  }

  const totalAttempts = progressSummary.reduce((sum, comp) => sum + (comp.QuestionsAttempted || 0), 0);
  const totalCorrect = progressSummary.reduce((sum, comp) => sum + (comp.CorrectAnswers || 0), 0);
  const averageAccuracy = totalAttempts > 0 ? ((totalCorrect / totalAttempts) * 100).toFixed(1) : 0;

  return (
    <Container>
      <Header>
        <BackButton onClick={onBackToQuestions}>
          <ArrowLeft size={16} />
          Back to Questions
        </BackButton>
        <HeaderTitle>User Profile</HeaderTitle>
      </Header>

      <ProfileContainer>
        <UserInfoCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <UserHeader>
            <UserAvatar>
              {getInitials(user.UserName)}
            </UserAvatar>
            <UserDetails>
              <UserName>{user.UserName}</UserName>
              <UserId>User ID: {user.Id}</UserId>
            </UserDetails>
          </UserHeader>

          <StatsGrid>
            <StatCard>
              <StatIcon>
                <Target size={24} />
              </StatIcon>
              <StatValue>{skillRankings.length}</StatValue>
              <StatLabel>Competencies</StatLabel>
            </StatCard>
            
            <StatCard>
              <StatIcon>
                <CheckCircle size={24} />
              </StatIcon>
              <StatValue>{totalAttempts}</StatValue>
              <StatLabel>Questions Attempted</StatLabel>
            </StatCard>
            
            <StatCard>
              <StatIcon>
                <TrendingUp size={24} />
              </StatIcon>
              <StatValue>{averageAccuracy}%</StatValue>
              <StatLabel>Accuracy</StatLabel>
            </StatCard>
            
            <StatCard>
              <StatIcon>
                <Award size={24} />
              </StatIcon>
              <StatValue>{Math.round(skillRankings.reduce((sum, r) => sum + r.SkillRank, 0) / skillRankings.length) || 0}</StatValue>
              <StatLabel>Average Skill Level</StatLabel>
            </StatCard>
          </StatsGrid>
        </UserInfoCard>

        <SkillLevelsCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <CardHeader>
            <BarChart3 size={24} color="#667eea" />
            <CardTitle>Skill Levels by Competency</CardTitle>
          </CardHeader>

          {skillRankings.length === 0 ? (
            <EmptyState>
              <EmptyIcon>
                <BookOpen size={32} />
              </EmptyIcon>
              <EmptyTitle>No Skill Data</EmptyTitle>
              <EmptyMessage>No skill rankings available for this user.</EmptyMessage>
            </EmptyState>
          ) : (
            <CompetenciesGrid>
              {skillRankings.map((ranking, index) => (
                <CompetencyCard
                  key={ranking.CompetencyId}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                >
                  <CompetencyHeader>
                    <div>
                      <CompetencyName>{ranking.CompetencyName}</CompetencyName>
                      <CompetencyCode>{ranking.CompetencyCode}</CompetencyCode>
                    </div>
                    <SkillRank style={{ color: getSkillColor(ranking.SkillRank) }}>
                      {ranking.SkillRank}
                    </SkillRank>
                  </CompetencyHeader>
                  
                  <SkillBar>
                    <SkillProgress 
                      percentage={calculateProgressPercentage(ranking.SkillRank)}
                      style={{ background: `linear-gradient(90deg, ${getSkillColor(ranking.SkillRank)} 0%, ${getSkillColor(ranking.SkillRank)}88 100%)` }}
                    />
                  </SkillBar>
                  
                  <SkillLabel>
                    <span>{getSkillLevel(ranking.SkillRank)}</span>
                    <span>{Math.round(calculateProgressPercentage(ranking.SkillRank))}% Complete</span>
                  </SkillLabel>
                </CompetencyCard>
              ))}
            </CompetenciesGrid>
          )}
        </SkillLevelsCard>
      </ProfileContainer>
    </Container>
  );
};

export default ProfilePage;



