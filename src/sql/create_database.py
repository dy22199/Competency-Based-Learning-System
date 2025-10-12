import sqlite3
import os
import csv

def create_database_and_tables():
    """
    Create a SQLite database and tables for the competency-based learning system
    """
    # Create or connect to database
    db_path = "competency_database.db"
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Created database: {db_path}")
    
    # Create Competency table
    cursor.execute('''
        CREATE TABLE Competency (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            CompetencyCode VARCHAR(10) NOT NULL,
            CompetencyName VARCHAR(100) NOT NULL,
            DomainCode VARCHAR(10) NOT NULL,
            DomainName VARCHAR(100) NOT NULL,
            Description TEXT
        )
    ''')
    print("Created 'Competency' table")
    
    # Create Skill table
    cursor.execute('''
        CREATE TABLE Skill (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            CompetencyId INTEGER NOT NULL,
            Stage VARCHAR(10) NOT NULL,
            ShortDescription VARCHAR(200) NOT NULL,
            Description TEXT,
            StartMMR INTEGER NOT NULL,
            EndMMR INTEGER NOT NULL,
            FOREIGN KEY (CompetencyId) REFERENCES Competency(Id)
        )
    ''')
    print("Created 'Skill' table")
    
    # Create Questions table
    cursor.execute('''
        CREATE TABLE Questions (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            QuestionType VARCHAR(20) NOT NULL,
            QuestionDescription TEXT NOT NULL,
            Options TEXT,
            QuestionsAnswer TEXT NOT NULL,
            QuestionHint TEXT
        )
    ''')
    print("Created 'Questions' table")
    
    # Create QuestionSkill table
    cursor.execute('''
        CREATE TABLE QuestionSkill (
            QuestionId INTEGER NOT NULL,
            SkillId INTEGER NOT NULL,
            PRIMARY KEY (QuestionId, SkillId),
            FOREIGN KEY (QuestionId) REFERENCES Questions(Id),
            FOREIGN KEY (SkillId) REFERENCES Skill(Id)
        )
    ''')
    print("Created 'QuestionSkill' table")
    
    # Create User table
    cursor.execute('''
        CREATE TABLE User (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            UserName VARCHAR(50) UNIQUE NOT NULL
        )
    ''')
    print("Created 'User' table")
    
    # Create UserQuestions table
    cursor.execute('''
        CREATE TABLE UserQuestions (
            UserId INTEGER NOT NULL,
            QuestionId INTEGER NOT NULL,
            UserAnswer TEXT,
            IsCorrect BOOLEAN NOT NULL,
            AttemptTime DATETIME NOT NULL,
            FOREIGN KEY (UserId) REFERENCES User(Id),
            FOREIGN KEY (QuestionId) REFERENCES Questions(Id)
        )
    ''')
    print("Created 'UserQuestions' table")
    
    # Create UserSkill table
    cursor.execute('''
        CREATE TABLE UserSkill (
            UserId INTEGER NOT NULL,
            CompetencyId INTEGER NOT NULL,
            SkillRank INTEGER NOT NULL,
            PRIMARY KEY (UserId, CompetencyId),
            FOREIGN KEY (UserId) REFERENCES User(Id),
            FOREIGN KEY (CompetencyId) REFERENCES Competency(Id)
        )
    ''')
    print("Created 'UserSkill' table")
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX idx_userquestions_userid_questionid ON UserQuestions(UserId, QuestionId)')
    cursor.execute('CREATE INDEX idx_userquestions_attempttime ON UserQuestions(AttemptTime)')
    print("Created indexes")
    
    # Insert sample data from CSV files
    insert_sample_data_from_csv(cursor)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"\nDatabase '{db_path}' created successfully with sample data!")
    return db_path

def insert_sample_data_from_csv(cursor):
    """Insert sample data from CSV files"""
    
    # Insert Competency data
    competency_file = "resources/sample_tables/DB tables - Competency.csv"
    if os.path.exists(competency_file):
        with open(competency_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute('''
                    INSERT INTO Competency (Id, CompetencyCode, CompetencyName, DomainCode, DomainName, Description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (row['Id'], row['CompetencyCode'], row['CompetencyName'], 
                      row['DomainCode'], row['DomainName'], row['Description']))
        print("Inserted Competency data from CSV")
    
    # Insert Skill data
    skill_file = "resources/sample_tables/DB tables - Skill.csv"
    if os.path.exists(skill_file):
        with open(skill_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute('''
                    INSERT INTO Skill (Id, CompetencyId, Stage, ShortDescription, Description, StartMMR, EndMMR)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (row['Id'], row['CompetencyId'], row['Stage'], 
                      row['ShortDescription'], row['Description'], 
                      row['StartMMR'], row['EndMMR']))
        print("Inserted Skill data from CSV")
    
    # Insert Questions data
    questions_file = "resources/sample_tables/DB tables - Questions.csv"
    if os.path.exists(questions_file):
        with open(questions_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute('''
                    INSERT INTO Questions (Id, QuestionType, QuestionDescription, Options, QuestionsAnswer, QuestionHint)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (row['Id'], row['QuestionType'], row['QuestionDescription'], 
                      row['Options'], row['QuestionsAnswer'], row['QuestionHint']))
        print("Inserted Questions data from CSV")
    
    # Insert QuestionSkill data
    questionskill_file = "resources/sample_tables/DB tables - QuestionSkill.csv"
    if os.path.exists(questionskill_file):
        with open(questionskill_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute('''
                    INSERT INTO QuestionSkill (QuestionId, SkillId)
                    VALUES (?, ?)
                ''', (row['QuestionId'], row['SkillId']))
        print("Inserted QuestionSkill data from CSV")
    
    # Insert User data
    user_file = "resources/sample_tables/DB tables - User.csv"
    if os.path.exists(user_file):
        with open(user_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute('''
                    INSERT INTO User (Id, UserName)
                    VALUES (?, ?)
                ''', (row['Id'], row['UserName']))
        print("Inserted User data from CSV")
    
    # Insert UserQuestions data
    userquestions_file = "resources/sample_tables/DB tables - UserQuestions.csv"
    if os.path.exists(userquestions_file):
        with open(userquestions_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Convert boolean string to integer
                is_correct = 1 if row['IsCorrect'].upper() == 'TRUE' else 0
                cursor.execute('''
                    INSERT INTO UserQuestions (UserId, QuestionId, UserAnswer, IsCorrect, AttemptTime)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['UserId'], row['QuestionId'], row['UserAnswer'], 
                      is_correct, row['AttemptTime']))
        print("Inserted UserQuestions data from CSV")
    
    # Insert UserSkill data
    userskill_file = "resources/sample_tables/DB tables - UserSkill.csv"
    if os.path.exists(userskill_file):
        with open(userskill_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute('''
                    INSERT INTO UserSkill (UserId, CompetencyId, SkillRank)
                    VALUES (?, ?, ?)
                ''', (row['UserId'], row['CompetencyId'], row['SkillRank']))
        print("Inserted UserSkill data from CSV")

def query_database(db_path):
    """Demonstrate querying the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n" + "="*50)
    print("SAMPLE QUERIES")
    print("="*50)
    
    # Query 1: Get all competencies
    print("\n1. All Competencies:")
    cursor.execute('SELECT * FROM Competency LIMIT 5')
    competencies = cursor.fetchall()
    for comp in competencies:
        print(f"   ID: {comp[0]}, Code: {comp[1]}, Name: {comp[2]}")
    
    # Query 2: Get skills for a specific competency
    print("\n2. Skills for Language Comprehension (C1):")
    cursor.execute('''
        SELECT s.Stage, s.ShortDescription, s.StartMMR, s.EndMMR
        FROM Skill s 
        JOIN Competency c ON s.CompetencyId = c.Id
        WHERE c.CompetencyCode = 'C1'
        LIMIT 3
    ''')
    skills = cursor.fetchall()
    for skill in skills:
        print(f"   {skill[0]}: {skill[1]} (MMR: {skill[2]}-{skill[3]})")
    
    # Query 3: Get questions with their skills
    print("\n3. Questions with Associated Skills:")
    cursor.execute('''
        SELECT q.QuestionDescription, s.ShortDescription, c.CompetencyName
        FROM Questions q
        JOIN QuestionSkill qs ON q.Id = qs.QuestionId
        JOIN Skill s ON qs.SkillId = s.Id
        JOIN Competency c ON s.CompetencyId = c.Id
        LIMIT 3
    ''')
    questions = cursor.fetchall()
    for q in questions:
        print(f"   Q: {q[0][:50]}...")
        print(f"      Skill: {q[1]} | Competency: {q[2]}")
    
    # Query 4: Get user's skill rankings
    print("\n4. User Skill Rankings:")
    cursor.execute('''
        SELECT u.UserName, c.CompetencyName, us.SkillRank
        FROM User u
        JOIN UserSkill us ON u.Id = us.UserId
        JOIN Competency c ON us.CompetencyId = c.Id
        ORDER BY us.SkillRank DESC
        LIMIT 5
    ''')
    rankings = cursor.fetchall()
    for rank in rankings:
        print(f"   {rank[0]}: {rank[1]} - Rank: {rank[2]}")
    
    # Query 5: Get user's question attempts
    print("\n5. User Question Attempts:")
    cursor.execute('''
        SELECT u.UserName, q.QuestionDescription, uq.UserAnswer, uq.IsCorrect, uq.AttemptTime
        FROM User u
        JOIN UserQuestions uq ON u.Id = uq.UserId
        JOIN Questions q ON uq.QuestionId = q.Id
        ORDER BY uq.AttemptTime DESC
    ''')
    attempts = cursor.fetchall()
    for attempt in attempts:
        correct = "✓" if attempt[3] else "✗"
        print(f"   {attempt[0]}: {correct} | {attempt[1][:30]}... | {attempt[4]}")
    
    conn.close()

if __name__ == "__main__":
    # Create database and tables
    db_path = create_database_and_tables()
    
    # Show sample queries
    query_database(db_path)
    
    print(f"\nDatabase file created at: {os.path.abspath(db_path)}")
    print("You can now use this database with any SQLite client or Python scripts!")