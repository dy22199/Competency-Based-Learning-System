import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Users, User, ArrowRight, Loader } from 'lucide-react';
import { apiService } from '../services/api';

const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 20px;
`;

const Content = styled.div`
  max-width: 800px;
  margin: 0 auto;
`;

const Header = styled(motion.div)`
  text-align: center;
  margin-bottom: 40px;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 8px;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
`;

const Subtitle = styled.p`
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
`;

const UserGrid = styled(motion.div)`
  display: grid;
  gap: 20px;
  margin-bottom: 40px;
`;

const UserCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    background: white;
  }
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
`;

const UserAvatar = styled.div`
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
`;

const UserDetails = styled.div`
  flex: 1;
`;

const UserName = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
`;

const UserId = styled.p`
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
`;

const ArrowIcon = styled.div`
  color: #667eea;
  transition: transform 0.3s ease;
  
  ${UserCard}:hover & {
    transform: translateX(4px);
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

const UserList = ({ onUserSelect }) => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getUsers();
      setUsers(response.data || []);
    } catch (err) {
      console.error('Error loading users:', err);
      setError(err.message || 'Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const handleUserClick = (user) => {
    onUserSelect(user);
  };

  const getInitials = (username) => {
    return username
      .split(' ')
      .map(word => word.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  if (loading) {
    return (
      <Container>
        <Content>
          <LoadingContainer>
            <Loader size={48} className="animate-spin" />
            <LoadingText>Loading users...</LoadingText>
          </LoadingContainer>
        </Content>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <Content>
          <ErrorContainer>
            <ErrorTitle>Error Loading Users</ErrorTitle>
            <ErrorMessage>{error}</ErrorMessage>
          </ErrorContainer>
        </Content>
      </Container>
    );
  }

  return (
    <Container>
      <Content>
        <Header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Title>Select Your Profile</Title>
          <Subtitle>Choose a user to continue with personalized learning</Subtitle>
        </Header>

        {users.length === 0 ? (
          <EmptyState>
            <EmptyIcon>
              <Users size={32} />
            </EmptyIcon>
            <EmptyTitle>No Users Found</EmptyTitle>
            <EmptyMessage>No users are available in the system yet.</EmptyMessage>
          </EmptyState>
        ) : (
          <UserGrid
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            {users.map((user, index) => (
              <UserCard
                key={user.Id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleUserClick(user)}
              >
                <UserInfo>
                  <UserAvatar>
                    {getInitials(user.UserName)}
                  </UserAvatar>
                  <UserDetails>
                    <UserName>{user.UserName}</UserName>
                    <UserId>User ID: {user.Id}</UserId>
                  </UserDetails>
                  <ArrowIcon>
                    <ArrowRight size={24} />
                  </ArrowIcon>
                </UserInfo>
              </UserCard>
            ))}
          </UserGrid>
        )}
      </Content>
    </Container>
  );
};

export default UserList;



