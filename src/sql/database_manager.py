import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    """A database manager for the competency-based learning system"""
    
    def __init__(self, db_path="competency_database.db"):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        return self.conn
    
    def disconnect(self):
        """Disconnect from the database"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def execute_query(self, query, params=None):
        """Execute a SELECT query and return results"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Convert rows to dictionaries for easier access
        columns = [description[0] for description in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    
    def execute_update(self, query, params=None):
        """Execute INSERT, UPDATE, or DELETE query"""
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        self.conn.commit()
        return cursor.rowcount
    
    # Competency methods
    def get_all_competencies(self):
        """Get all competencies from the database"""
        query = "SELECT * FROM Competency ORDER BY CompetencyCode, DomainCode"
        return self.execute_query(query)
    
    def get_competency_by_code(self, competency_code):
        """Get competencies by competency code"""
        query = "SELECT * FROM Competency WHERE CompetencyCode = ?"
        return self.execute_query(query, (competency_code,))
    
    def add_competency(self, competency_code, competency_name, domain_code, domain_name, description=""):
        """Add a new competency to the database"""
        query = """
        INSERT INTO Competency (CompetencyCode, CompetencyName, DomainCode, DomainName, Description)
        VALUES (?, ?, ?, ?, ?)
        """
        return self.execute_update(query, (competency_code, competency_name, domain_code, domain_name, description))
    
    # Skill methods
    def get_skills_by_competency(self, competency_id):
        """Get all skills for a specific competency"""
        query = """
        SELECT s.*, c.CompetencyName, c.CompetencyCode
        FROM Skill s
        JOIN Competency c ON s.CompetencyId = c.Id
        WHERE s.CompetencyId = ?
        ORDER BY s.StartMMR
        """
        return self.execute_query(query, (competency_id,))
    
    def get_skills_by_competency_code(self, competency_code):
        """Get all skills for a specific competency code"""
        query = """
        SELECT s.*, c.CompetencyName, c.CompetencyCode
        FROM Skill s
        JOIN Competency c ON s.CompetencyId = c.Id
        WHERE c.CompetencyCode = ?
        ORDER BY s.StartMMR
        """
        return self.execute_query(query, (competency_code,))
    
    def get_skill_by_mmr_range(self, min_mmr, max_mmr):
        """Get skills within a specific MMR range"""
        query = """
        SELECT s.*, c.CompetencyName, c.CompetencyCode
        FROM Skill s
        JOIN Competency c ON s.CompetencyId = c.Id
        WHERE s.StartMMR <= ? AND s.EndMMR >= ?
        ORDER BY s.StartMMR
        """
        return self.execute_query(query, (max_mmr, min_mmr))
    
    def add_skill(self, competency_id, stage, short_description, description, start_mmr, end_mmr):
        """Add a new skill to the database"""
        query = """
        INSERT INTO Skill (CompetencyId, Stage, ShortDescription, Description, StartMMR, EndMMR)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.execute_update(query, (competency_id, stage, short_description, description, start_mmr, end_mmr))
    
    # Question methods
    def get_all_questions(self):
        """Get all questions from the database"""
        query = "SELECT * FROM Questions ORDER BY Id"
        return self.execute_query(query)
    
    def get_questions_by_type(self, question_type):
        """Get questions by type"""
        query = "SELECT * FROM Questions WHERE QuestionType = ? ORDER BY Id"
        return self.execute_query(query, (question_type,))
    
    def get_questions_by_skill(self, skill_id):
        """Get questions associated with a specific skill"""
        query = """
        SELECT q.*, s.ShortDescription as SkillDescription, c.CompetencyName
        FROM Questions q
        JOIN QuestionSkill qs ON q.Id = qs.QuestionId
        JOIN Skill s ON qs.SkillId = s.Id
        JOIN Competency c ON s.CompetencyId = c.Id
        WHERE qs.SkillId = ?
        """
        return self.execute_query(query, (skill_id,))
    
    def get_questions_by_competency(self, competency_id):
        """Get questions associated with a specific competency"""
        query = """
        SELECT DISTINCT q.*, s.ShortDescription as SkillDescription, c.CompetencyName
        FROM Questions q
        JOIN QuestionSkill qs ON q.Id = qs.QuestionId
        JOIN Skill s ON qs.SkillId = s.Id
        JOIN Competency c ON s.CompetencyId = c.Id
        WHERE c.Id = ?
        """
        return self.execute_query(query, (competency_id,))
    
    def add_question(self, question_type, question_description, options, questions_answer, question_hint=""):
        """Add a new question to the database"""
        query = """
        INSERT INTO Questions (QuestionType, QuestionDescription, Options, QuestionsAnswer, QuestionHint)
        VALUES (?, ?, ?, ?, ?)
        """
        return self.execute_update(query, (question_type, question_description, options, questions_answer, question_hint))
    
    def link_question_to_skill(self, question_id, skill_id):
        """Link a question to a skill"""
        query = "INSERT OR IGNORE INTO QuestionSkill (QuestionId, SkillId) VALUES (?, ?)"
        return self.execute_update(query, (question_id, skill_id))
    
    # User methods
    def get_all_users(self):
        """Get all users from the database"""
        query = "SELECT * FROM User ORDER BY UserName"
        return self.execute_query(query)
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        query = "SELECT * FROM User WHERE Id = ?"
        return self.execute_query(query, (user_id,))
    
    def get_user_by_name(self, username):
        """Get user by username"""
        query = "SELECT * FROM User WHERE UserName = ?"
        return self.execute_query(query, (username,))
    
    def add_user(self, username):
        """Add a new user to the database"""
        query = "INSERT INTO User (UserName) VALUES (?)"
        return self.execute_update(query, (username,))
    
    # UserQuestions methods
    def get_user_attempts(self, user_id):
        """Get all question attempts for a user"""
        query = """
        SELECT uq.*, q.QuestionDescription, q.QuestionType
        FROM UserQuestions uq
        JOIN Questions q ON uq.QuestionId = q.Id
        WHERE uq.UserId = ?
        ORDER BY uq.AttemptTime DESC
        """
        return self.execute_query(query, (user_id,))
    
    def get_user_attempts_by_question(self, user_id, question_id):
        """Get all attempts for a specific question by a user"""
        query = """
        SELECT uq.*, q.QuestionDescription, q.QuestionType
        FROM UserQuestions uq
        JOIN Questions q ON uq.QuestionId = q.Id
        WHERE uq.UserId = ? AND uq.QuestionId = ?
        ORDER BY uq.AttemptTime DESC
        """
        return self.execute_query(query, (user_id, question_id))
    
    def record_question_attempt(self, user_id, question_id, user_answer, is_correct, attempt_time=None):
        """Record a user's attempt at a question"""
        if attempt_time is None:
            attempt_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
        INSERT INTO UserQuestions (UserId, QuestionId, UserAnswer, IsCorrect, AttemptTime)
        VALUES (?, ?, ?, ?, ?)
        """
        return self.execute_update(query, (user_id, question_id, user_answer, is_correct, attempt_time))
    
    def get_user_correct_attempts(self, user_id):
        """Get all correct attempts for a user"""
        query = """
        SELECT uq.*, q.QuestionDescription, q.QuestionType
        FROM UserQuestions uq
        JOIN Questions q ON uq.QuestionId = q.Id
        WHERE uq.UserId = ? AND uq.IsCorrect = 1
        ORDER BY uq.AttemptTime DESC
        """
        return self.execute_query(query, (user_id,))
    
    def get_user_incorrect_attempts(self, user_id):
        """Get all incorrect attempts for a user"""
        query = """
        SELECT uq.*, q.QuestionDescription, q.QuestionType
        FROM UserQuestions uq
        JOIN Questions q ON uq.QuestionId = q.Id
        WHERE uq.UserId = ? AND uq.IsCorrect = 0
        ORDER BY uq.AttemptTime DESC
        """
        return self.execute_query(query, (user_id,))
    
    # UserSkill methods
    def get_user_skill_rankings(self, user_id):
        """Get all skill rankings for a user"""
        query = """
        SELECT us.*, c.CompetencyName, c.CompetencyCode
        FROM UserSkill us
        JOIN Competency c ON us.CompetencyId = c.Id
        WHERE us.UserId = ?
        ORDER BY us.SkillRank DESC
        """
        return self.execute_query(query, (user_id,))
    
    def get_user_skill_ranking(self, user_id, competency_id):
        """Get skill ranking for a specific competency"""
        query = """
        SELECT us.*, c.CompetencyName, c.CompetencyCode
        FROM UserSkill us
        JOIN Competency c ON us.CompetencyId = c.Id
        WHERE us.UserId = ? AND us.CompetencyId = ?
        """
        return self.execute_query(query, (user_id, competency_id))
    
    def update_user_skill_ranking(self, user_id, competency_id, skill_rank):
        """Update or insert user skill ranking"""
        query = """
        INSERT OR REPLACE INTO UserSkill (UserId, CompetencyId, SkillRank)
        VALUES (?, ?, ?)
        """
        return self.execute_update(query, (user_id, competency_id, skill_rank))
    
    def get_users_by_competency_ranking(self, competency_id, min_rank=None, max_rank=None):
        """Get users ranked by their skill level in a specific competency"""
        query = """
        SELECT us.*, u.UserName, c.CompetencyName
        FROM UserSkill us
        JOIN User u ON us.UserId = u.Id
        JOIN Competency c ON us.CompetencyId = c.Id
        WHERE us.CompetencyId = ?
        """
        params = [competency_id]
        
        if min_rank is not None:
            query += " AND us.SkillRank >= ?"
            params.append(min_rank)
        
        if max_rank is not None:
            query += " AND us.SkillRank <= ?"
            params.append(max_rank)
        
        query += " ORDER BY us.SkillRank DESC"
        
        return self.execute_query(query, params)
    
    # Analytics methods
    def get_user_progress_summary(self, user_id):
        """Get a summary of user's progress across all competencies"""
        query = """
        SELECT 
            c.CompetencyName,
            c.CompetencyCode,
            us.SkillRank,
            COUNT(DISTINCT uq.QuestionId) as QuestionsAttempted,
            SUM(CASE WHEN uq.IsCorrect = 1 THEN 1 ELSE 0 END) as CorrectAnswers,
            ROUND(SUM(CASE WHEN uq.IsCorrect = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT uq.QuestionId), 2) as Accuracy
        FROM UserSkill us
        JOIN Competency c ON us.CompetencyId = c.Id
        LEFT JOIN UserQuestions uq ON us.UserId = uq.UserId
        LEFT JOIN QuestionSkill qs ON uq.QuestionId = qs.QuestionId
        LEFT JOIN Skill s ON qs.SkillId = s.Id AND s.CompetencyId = c.Id
        WHERE us.UserId = ?
        GROUP BY c.Id, c.CompetencyName, c.CompetencyCode, us.SkillRank
        ORDER BY us.SkillRank DESC
        """
        return self.execute_query(query, (user_id,))
    
    def get_competency_statistics(self, competency_id):
        """Get statistics for a specific competency"""
        query = """
        SELECT 
            c.CompetencyName,
            COUNT(DISTINCT s.Id) as TotalSkills,
            COUNT(DISTINCT q.Id) as TotalQuestions,
            COUNT(DISTINCT us.UserId) as UsersWithRanking,
            AVG(us.SkillRank) as AverageRanking,
            MIN(us.SkillRank) as MinRanking,
            MAX(us.SkillRank) as MaxRanking
        FROM Competency c
        LEFT JOIN Skill s ON c.Id = s.CompetencyId
        LEFT JOIN QuestionSkill qs ON s.Id = qs.SkillId
        LEFT JOIN Questions q ON qs.QuestionId = q.Id
        LEFT JOIN UserSkill us ON c.Id = us.CompetencyId
        WHERE c.Id = ?
        GROUP BY c.Id, c.CompetencyName
        """
        return self.execute_query(query, (competency_id,))

def main():
    """Demonstrate database operations"""
    db = DatabaseManager()
    
    try:
        # Connect to database
        db.connect()
        print("Connected to database successfully!")
        
        # Get all competencies
        print("\n" + "="*50)
        print("ALL COMPETENCIES")
        print("="*50)
        competencies = db.get_all_competencies()
        for comp in competencies[:5]:  # Show first 5
            print(f"ID: {comp['Id']}, Code: {comp['CompetencyCode']}, Name: {comp['CompetencyName']}")
        
        # Get skills for Language Comprehension
        print("\n" + "="*50)
        print("SKILLS FOR LANGUAGE COMPREHENSION (C1)")
        print("="*50)
        skills = db.get_skills_by_competency_code("C1")
        for skill in skills[:3]:  # Show first 3
            print(f"Stage: {skill['Stage']}, Description: {skill['ShortDescription']}")
        
        # Get questions with skills
        print("\n" + "="*50)
        print("QUESTIONS WITH ASSOCIATED SKILLS")
        print("="*50)
        questions = db.get_all_questions()
        for q in questions:
            print(f"ID: {q['Id']}, Type: {q['QuestionType']}")
            print(f"Description: {q['QuestionDescription'][:50]}...")
            # Get associated skills
            question_skills = db.get_questions_by_skill(q['Id'])
            for qs in question_skills:
                print(f"  Skill: {qs['SkillDescription']} | Competency: {qs['CompetencyName']}")
            break  # Show only first question
        
        # Get user skill rankings
        print("\n" + "="*50)
        print("USER SKILL RANKINGS")
        print("="*50)
        users = db.get_all_users()
        if users:
            user_id = users[0]['Id']
            rankings = db.get_user_skill_rankings(user_id)
            for rank in rankings:
                print(f"User: {rank['CompetencyName']} - Rank: {rank['SkillRank']}")
        
        # Get user progress summary
        print("\n" + "="*50)
        print("USER PROGRESS SUMMARY")
        print("="*50)
        if users:
            user_id = users[0]['Id']
            progress = db.get_user_progress_summary(user_id)
            for p in progress:
                print(f"Competency: {p['CompetencyName']} - Rank: {p['SkillRank']}")
                print(f"  Questions Attempted: {p['QuestionsAttempted']}")
                print(f"  Correct Answers: {p['CorrectAnswers']}")
                print(f"  Accuracy: {p['Accuracy']}%")
        
        # Get competency statistics
        print("\n" + "="*50)
        print("COMPETENCY STATISTICS")
        print("="*50)
        if competencies:
            comp_id = competencies[0]['Id']
            stats = db.get_competency_statistics(comp_id)
            for stat in stats:
                print(f"Competency: {stat['CompetencyName']}")
                print(f"  Total Skills: {stat['TotalSkills']}")
                print(f"  Total Questions: {stat['TotalQuestions']}")
                print(f"  Users with Ranking: {stat['UsersWithRanking']}")
                print(f"  Average Ranking: {stat['AverageRanking']}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        db.disconnect()
        print("\nDisconnected from database.")

if __name__ == "__main__":
    main()