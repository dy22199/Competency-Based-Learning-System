import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error.response?.data || { error: 'Network error' });
  }
);

// API Service Functions
export const apiService = {
  // Health check
  healthCheck: () => api.get('/health'),

  // Competencies
  getCompetencies: () => api.get('/competencies'),
  getCompetencyByCode: (code) => api.get(`/competencies/${code}`),

  // Skills
  getSkillsByCompetency: (competencyId) => api.get(`/competencies/${competencyId}/skills`),
  getSkillsByCompetencyCode: (code) => api.get(`/competencies/code/${code}/skills`),
  getSkillsByMMRRange: (minMMR, maxMMR) => 
    api.get(`/skills/mmr-range?min_mmr=${minMMR}&max_mmr=${maxMMR}`),

  // Questions
  getQuestions: () => api.get('/questions'),
  getQuestionsByType: (type) => api.get(`/questions/type/${type}`),
  getQuestionsBySkill: (skillId) => api.get(`/skills/${skillId}/questions`),
  getQuestionsByCompetency: (competencyId) => api.get(`/competencies/${competencyId}/questions`),

  // Users
  getUsers: () => api.get('/users'),
  getUserById: (userId) => api.get(`/users/${userId}`),
  getUserByName: (username) => api.get(`/users/name/${username}`),

  // User Attempts
  getUserAttempts: (userId) => api.get(`/users/${userId}/attempts`),
  getUserCorrectAttempts: (userId) => api.get(`/users/${userId}/attempts/correct`),
  getUserIncorrectAttempts: (userId) => api.get(`/users/${userId}/attempts/incorrect`),
  recordAttempt: (userId, attemptData) => api.post(`/users/${userId}/attempts`, attemptData),

  // User Skills
  getUserSkillRankings: (userId) => api.get(`/users/${userId}/skill-rankings`),
  getUserSkillRanking: (userId, competencyId) => 
    api.get(`/users/${userId}/competencies/${competencyId}/skill-ranking`),
  updateUserSkillRanking: (userId, competencyId, skillRank) => 
    api.put(`/users/${userId}/competencies/${competencyId}/skill-ranking`, { skill_rank: skillRank }),

  // Analytics
  getUserProgressSummary: (userId) => api.get(`/users/${userId}/progress-summary`),
  getCompetencyStatistics: (competencyId) => api.get(`/competencies/${competencyId}/statistics`),
  getUsersByCompetencyRanking: (competencyId, minRank = null, maxRank = null) => {
    let url = `/competencies/${competencyId}/users`;
    const params = [];
    if (minRank !== null) params.push(`min_rank=${minRank}`);
    if (maxRank !== null) params.push(`max_rank=${maxRank}`);
    if (params.length > 0) url += `?${params.join('&')}`;
    return api.get(url);
  },
};

// Helper function to get appropriate questions based on user skill level
export const getQuestionsForUser = async (userId) => {
  try {
    // Get user's skill rankings
    const skillRankings = await apiService.getUserSkillRankings(userId);
    
    if (!skillRankings.data || skillRankings.data.length === 0) {
      // If no skill rankings, get basic questions
      return await apiService.getQuestionsByMMRRange(0, 1000);
    }

    // Get all competencies
    const competencies = await apiService.getCompetencies();
    
    const questions = [];
    
    // For each competency, find questions within user's skill range
    for (const ranking of skillRankings.data) {
      const competencyId = ranking.CompetencyId;
      const userSkillRank = ranking.SkillRank;
      
      // Get skills within user's range (allow some buffer)
      const buffer = 500; // Allow questions slightly above current skill
      const minMMR = Math.max(0, userSkillRank - buffer);
      const maxMMR = userSkillRank + buffer;
      
      try {
        const skillsInRange = await apiService.getSkillsByMMRRange(minMMR, maxMMR);
        
        // Get questions for each skill in range
        for (const skill of skillsInRange.data) {
          try {
            const skillQuestions = await apiService.getQuestionsBySkill(skill.Id);
            questions.push(...skillQuestions.data);
          } catch (error) {
            console.warn(`No questions found for skill ${skill.Id}`);
          }
        }
      } catch (error) {
        console.warn(`No skills found in MMR range ${minMMR}-${maxMMR} for competency ${competencyId}`);
      }
    }
    
    // Remove duplicates and return
    const uniqueQuestions = questions.filter((question, index, self) => 
      index === self.findIndex(q => q.Id === question.Id)
    );
    
    return { data: uniqueQuestions };
    
  } catch (error) {
    console.error('Error getting questions for user:', error);
    // Fallback to basic questions
    return await apiService.getQuestionsByMMRRange(0, 1000);
  }
};

// Helper function to get a random question
export const getRandomQuestion = async (userId) => {
  try {
    const questionsResponse = await getQuestionsForUser(userId);
    const questions = questionsResponse.data;
    
    if (questions.length === 0) {
      throw new Error('No questions available for user');
    }
    
    const randomIndex = Math.floor(Math.random() * questions.length);
    return questions[randomIndex];
  } catch (error) {
    console.error('Error getting random question:', error);
    throw error;
  }
};

export default api;



