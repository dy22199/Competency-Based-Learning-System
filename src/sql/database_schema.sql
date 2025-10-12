-- SQL Database Schema for Competency-Based Learning System
-- This file contains the SQL commands to create tables for the competency tracking system
-- You can run these commands in any SQL database (SQLite, MySQL, PostgreSQL)

-- Create Competency table
CREATE TABLE Competency (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    CompetencyCode VARCHAR(10) NOT NULL,
    CompetencyName VARCHAR(100) NOT NULL,
    DomainCode VARCHAR(10) NOT NULL,
    DomainName VARCHAR(100) NOT NULL,
    Description TEXT
);

-- Create Skill table (references Competency)
CREATE TABLE Skill (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    CompetencyId INTEGER NOT NULL,
    Stage VARCHAR(10) NOT NULL,
    ShortDescription VARCHAR(200) NOT NULL,
    Description TEXT,
    StartMMR INTEGER NOT NULL,
    EndMMR INTEGER NOT NULL,
    FOREIGN KEY (CompetencyId) REFERENCES Competency(Id)
);

-- Create Questions table
CREATE TABLE Questions (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    QuestionType VARCHAR(20) NOT NULL,
    QuestionDescription TEXT NOT NULL,
    Options TEXT,
    QuestionsAnswer TEXT NOT NULL,
    QuestionHint TEXT
);

-- Create QuestionSkill table (many-to-many relationship between Questions and Skill)
CREATE TABLE QuestionSkill (
    QuestionId INTEGER NOT NULL,
    SkillId INTEGER NOT NULL,
    PRIMARY KEY (QuestionId, SkillId),
    FOREIGN KEY (QuestionId) REFERENCES Questions(Id),
    FOREIGN KEY (SkillId) REFERENCES Skill(Id)
);

-- Create User table
CREATE TABLE User (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    UserName VARCHAR(50) UNIQUE NOT NULL
);

-- Create UserQuestions table (tracks user attempts and results)
CREATE TABLE UserQuestions (
    UserId INTEGER NOT NULL,
    QuestionId INTEGER NOT NULL,
    UserAnswer TEXT,
    IsCorrect BOOLEAN NOT NULL,
    AttemptTime DATETIME NOT NULL,
    FOREIGN KEY (UserId) REFERENCES User(Id),
    FOREIGN KEY (QuestionId) REFERENCES Questions(Id)
);

-- Create UserSkill table (tracks user skill rankings)
CREATE TABLE UserSkill (
    UserId INTEGER NOT NULL,
    CompetencyId INTEGER NOT NULL,
    SkillRank INTEGER NOT NULL,
    PRIMARY KEY (UserId, CompetencyId),
    FOREIGN KEY (UserId) REFERENCES User(Id),
    FOREIGN KEY (CompetencyId) REFERENCES Competency(Id)
);

-- Create indexes for better performance
CREATE INDEX idx_userquestions_userid_questionid ON UserQuestions(UserId, QuestionId);
CREATE INDEX idx_userquestions_attempttime ON UserQuestions(AttemptTime);

-- Sample data insertion from CSV files
INSERT INTO Competency (Id, CompetencyCode, CompetencyName, DomainCode, DomainName, Description) VALUES 
(1, 'C1', 'Language Comprehension', 'D1', 'Ability/pace of reading', ''),
(2, 'C1', 'Language Comprehension', 'D2', 'Vocabulary', ''),
(3, 'C1', 'Language Comprehension', 'D3', 'Grammar/ Syntax', ''),
(4, 'C2', 'Math Fact Fluency', 'D1', 'Representation & Understanding', ''),
(5, 'C2', 'Math Fact Fluency', 'D2', 'Strategy Use', ''),
(6, 'C2', 'Math Fact Fluency', 'D3', 'Accuracy', ''),
(7, 'C2', 'Math Fact Fluency', 'D4', 'Efficiency & Automaticity', ''),
(8, 'C3', 'Conceptual understanding', 'D1', 'Speed–Distance–Time', ''),
(9, 'C3', 'Conceptual understanding', 'D2', 'Geometry & Spatial Reasoning', ''),
(10, 'C3', 'Conceptual understanding', 'D3', 'Measurement & Units', ''),
(11, 'C3', 'Conceptual understanding', 'D4', 'Data & Chance', ''),
(12, 'C3', 'Conceptual understanding', 'D5', 'Probability', ''),
(13, 'C4', 'Problem Solving & Reasoning', 'D1', 'Understanding & Representing', ''),
(14, 'C4', 'Problem Solving & Reasoning', 'D2', 'Strategic Thinking & Planning', ''),
(15, 'C4', 'Problem Solving & Reasoning', 'D3', 'Logical Reasoning & Justification', ''),
(16, 'C4', 'Problem Solving & Reasoning', 'D4', 'Flexibility & Creativity', ''),
(17, 'C4', 'Problem Solving & Reasoning', 'D5', 'Reflection & Metacognition', '');

INSERT INTO Skill (Id, CompetencyId, Stage, ShortDescription, Description, StartMMR, EndMMR) VALUES 
(1, 1, 'S1', 'Print Concepts & Tracking', 'Follow left-to-right, top-to-bottom; point to each word; match spoken words to printed words; know basic letter sounds.', 0, 1000),
(2, 1, 'S2', 'Sound Out & Sight Words', 'Sound out simple words (cat, ship, stop); know many common words without sounding them out.', 1001, 2000),
(3, 1, 'S3', 'Smooth Sentences & Punctuation', 'Read short sentences in phrases (not word-by-word); pause at commas; stop at periods and question marks.', 2001, 3000),
(4, 1, 'S4', 'Paragraph Fluency & Stamina', 'Read a short paragraph smoothly and accurately; keep reading for several minutes; fix mistakes when noticed.', 3001, 4000),
(5, 1, 'S5', 'Expression & Speed', 'Read with expression; control speed (not too fast or slow); keep phrases smooth.', 4001, 5000),
(6, 1, 'S6', 'Self-Check & Expressive Reading', 'Read a new grade-level text with steady pace and expression; notice when meaning breaks and reread to fix it.', 5001, 6000),
(7, 2, 'S1', 'Everyday & School Words', 'Learn and use everyday school words; link words to pictures/actions; know many common words by sight.', 0, 1000),
(8, 2, 'S2', 'Word Relationships', 'Know words that mean the same or the opposite; sort words into groups; build word families.', 1001, 2000),
(9, 2, 'S3', 'Use Context Clues', 'Use the sentence or paragraph to guess a word''s meaning; pick the meaning that fits best.', 2001, 3000),
(10, 2, 'S4', 'Word Parts (Roots, Prefixes, Suffixes)', 'Break words into parts and use the parts to figure out meaning; make related words.', 3001, 4000),
(11, 2, 'S5', 'Academic Words (Tier 2)', 'Learn useful school words across subjects (e.g., compare, explain); say them in your own words; choose precise terms.', 4001, 5000),
(12, 2, 'S6', 'Subject Words (Tier 3)', 'Understand topic words for science, social studies, etc.; explain them clearly; tell apart close meanings.', 5001, 6000),
(13, 3, 'S1', 'Sentences & End Marks', 'Spot/write complete sentences (who/what + action); start with a capital; end with . ? or !', 0, 1000),
(14, 3, 'S2', 'Verbs & Agreement', 'Use the right tense (past/present/future) and make verbs match the subject; form questions and "not" sentences correctly.', 1001, 2000),
(15, 3, 'S3', 'Join Sentences', 'Join ideas with and, but, or; use commas in a list; avoid run-ons and fragments.', 2001, 3000),
(16, 3, 'S4', 'Add Clauses for Detail', 'Use because/when/if to add reasons or time; use who/that to add details; punctuate these correctly.', 3001, 4000),
(17, 3, 'S5', 'Clear Connections', 'Use pronouns so the reader knows who/what you mean; use transition words (first, then, however) to link ideas; keep similar parts parallel.', 4001, 5000),
(18, 3, 'S6', 'Edit for Clarity', 'Edit writing: keep tense the same, match pronouns to nouns, use commas/apostrophes/quotes correctly; make sentences clearer.', 5001, 6000),
(19, 4, 'S1', 'Concrete', 'Uses counters/cubes/fingers to show facts.', 0, 1000),
(20, 4, 'S2', 'Pictorial', 'Draws or visualizes models (arrays, number lines).', 1001, 2000),
(21, 4, 'S3', 'Abstract', 'Works with symbols and numbers without models.', 2001, 3000),
(22, 4, 'S4', 'Relational', 'Connects facts across operations; uses equivalence.', 3001, 4000),
(23, 5, 'S1', 'Counting', 'Counts on/back or repeats addition.', 0, 1000),
(24, 5, 'S2', 'Derived Facts', 'Uses known facts: doubles, near doubles, make 10.', 1001, 2000),
(25, 5, 'S3', 'Properties-Based', 'Applies commutative/associative/distributive laws.', 2001, 3000),
(26, 5, 'S4', 'Adaptive', 'Chooses the most efficient strategy for the problem.', 3001, 4000),
(27, 6, 'S1', 'Emerging', 'Frequent errors; needs prompts.', 0, 1000),
(28, 6, 'S2', 'Developing', 'Mostly correct with familiar facts.', 1001, 2000),
(29, 6, 'S3', 'Proficient', 'Accurate across all basic facts.', 2001, 3000),
(30, 6, 'S4', 'Mastery', 'Very rare errors, even with time pressure.', 3001, 4000),
(31, 7, 'S1', 'Slow Recall', 'Takes time or tools to recall facts.', 0, 1000),
(32, 7, 'S2', 'Partial Automaticity', 'Quick on some facts; others take effort.', 1001, 2000),
(33, 7, 'S3', 'Full Automaticity', 'Fast recall of all basic facts (<=3s).', 2001, 3000),
(34, 7, 'S4', 'Transfer & Application', 'Uses facts fluently in multi-step, real contexts.', 3001, 4000),
(35, 8, 'S1', 'Time & Distance Units', 'Minutes/hours/seconds; meters/kilometers; read clocks & trip schedules; recognize "per"', 0, 1000),
(36, 8, 'S2', 'Uniform Motion Basics', 'Use d = v × t; solve for a missing variable, keep units consistent', 1001, 2000),
(37, 8, 'S3', 'Unit Conversions for Rates', 'Convert min↔hr, m↔km to express speeds (km/h, m/s);', 2001, 3000),
(38, 8, 'S4', 'Converting Equations', '"rate triangle" strategy', 3001, 4000),
(39, 8, 'S5', 'Word Problems with Tables', 'One–two step SDT problems; organize with d–v–t tables; compare two trips', 4001, 5000),
(40, 8, 'S6', 'Average & Comparative Speed', 'Average speed over multi-leg trips; compare speeds; reasonableness checks', 5001, 6000),
(41, 8, 'S7', 'Relative Motion (Intro)', 'Meeting/overtake problems at constant speeds (same/opposite directions)', 6001, 7000),
(42, 9, 'S1', 'Shape Recognition & Attributes', 'Name 2-D/3-D shapes; faces/edges/vertices; positional language', 0, 1000),
(43, 9, 'S2', 'Compose/Decompose & Nets', 'Put shapes together and take them apart. Lay a 3-D shape flat like a cut-out (a net), and imagine folding the cut-out back into the 3-D shape.', 1001, 2000),
(44, 9, 'S3', 'Classify by Properties', 'Hierarchies of triangles/quadrilaterals; parallel/perpendicular; visual congruence', 2001, 3000),
(45, 9, 'S4', 'Symmetry & Transformations', 'Lines of symmetry; translations/rotations/reflections; congruent images', 3001, 4000),
(46, 9, 'S5', 'Coordinate Location', 'Plot/read points; draw polygons on grids; step-count paths only', 4001, 5000),
(47, 9, 'S6', 'Spatial Visualization', 'Cross-sections and rotations of solids; mental imagery of moves', 5001, 6000),
(48, 10, 'S1', 'Understanding units, Compare & Estimate', 'Choose attribute (length/mass/capacity/time); non-standard units; estimation', 0, 1000),
(49, 10, 'S2', 'Standard Tools & Scales', 'Rulers/balances/thermometers/; read to nearest mark;', 1001, 2000),
(50, 10, 'S3', 'Perimeter, Area & Elapsed Time', 'Perimeter; area of rectangles/composites; elapsed time within a day', 2001, 3000),
(51, 10, 'S4', 'Angles & Scale/Maps', 'Measure angles with protractor; interpret map scales; simple within-system conversions', 3001, 4000),
(52, 10, 'S5', 'Volume & Capacity', 'Unit cubes; V = l×w×h for prisms; relate cm³↔mL↔L; simple composites', 4001, 5000),
(53, 10, 'S6', 'Precision & Chained Conversions', 'Within-system conversions; track units; choose/justify precision', 5001, 6000),
(54, 11, 'S1', 'Collect & Sort Data', 'Tally/categorize; simple tables; picture/bar charts,', 0, 1000),
(55, 11, 'S2', 'Read & Make Graphs (Scaled)', 'Tables ↔ scaled bar graphs; one/two-step questions; choose a sensible scale', 1001, 2000),
(56, 11, 'S3', 'Line Plots & Trends', 'Time-series/line plots; min/max/range; compare datasets', 2001, 3000),
(57, 11, 'S4', 'Centers & Variability', 'Mean/median/mode; when each is appropriate; outliers', 3001, 4000),
(58, 11, 'S5', 'Probability Basics', 'Experiments; sample space; likelihood as fractions; fairness', 4001, 5000),
(59, 11, 'S6', 'Reason from Data', 'Choose best display; support claims with evidence; spot misleading graphs', 5001, 6000),
(60, 12, 'S1', 'Fundamentals', 'Understand dice rolls, coin tosses', 0, 1000),
(61, 12, 'S2', 'Experiments', 'Calculating chances of rolling multiple die or tossing multiple coins', 1001, 2000),
(62, 12, 'S3', 'Probability Basics', 'Sample space; likelihood as fractions; fairness', 2001, 3000),
(63, 13, 'S1', 'Surface recognition of numbers or keywords.', '', 0, 1000),
(64, 13, 'S2', 'Organizes information using visuals (diagrams, tables).', '', 1001, 2000),
(65, 13, 'S3', 'Identifies relationships and structures (e.g., part-whole, comparison).', '', 2001, 3000),
(66, 13, 'S4', 'Uses abstract representations (algebraic, symbolic).', '', 3001, 4000),
(67, 14, 'S1', 'Random trial-and-error attempts.', '', 0, 1000),
(68, 14, 'S2', 'Applies known strategies to familiar problems.', '', 1001, 2000),
(69, 14, 'S3', 'Selects strategies based on context and efficiency.', '', 2001, 3000),
(70, 14, 'S4', 'Designs new strategies for unfamiliar problems.', '', 3001, 4000),
(71, 15, 'S1', 'Gives intuitive answers without explanation.', '', 0, 1000),
(72, 15, 'S2', 'Justifies steps using rules or procedures.', '', 1001, 2000),
(73, 15, 'S3', 'Explains reasoning using mathematical concepts.', '', 2001, 3000),
(74, 15, 'S4', 'Constructs formal arguments or proofs.', '', 3001, 4000),
(75, 16, 'S1', 'Sticks to one method regardless of outcome.', '', 0, 1000),
(76, 16, 'S2', 'Tries alternative methods when prompted.', '', 1001, 2000),
(77, 16, 'S3', 'Transfers known strategies to new contexts.', '', 2001, 3000),
(78, 16, 'S4', 'Invents novel approaches or connects across domains.', '', 3001, 4000),
(79, 17, 'S1', 'Unaware of errors or strategy effectiveness.', '', 0, 1000),
(80, 17, 'S2', 'Reflects after feedback.', '', 1001, 2000),
(81, 17, 'S3', 'Monitors and adjusts thinking during problem solving.', '', 2001, 3000),
(82, 17, 'S4', 'Independently plans, monitors, and regulates learning.', '', 3001, 4000);

INSERT INTO Questions (Id, QuestionType, QuestionDescription, Options, QuestionsAnswer, QuestionHint) VALUES 
(1001, 'MCQ', 'Choose the sentence that reads correctly left to right and uses the right unit.', '[The car''s speed is 60 km/h,Car speed 60 km/h is,The car''s speed is 60 kilograms]', 'The car''s speed is 60 km/h', 'Pick correct unit and a well-formed sentence.'),
(1002, 'Integer', 'Write the exact sentence: "Speed = ___ km/h." A bike travels 6 km in 30 minutes.', '', '12', 'Time = d ÷ v = 21 ÷ 7.');

INSERT INTO QuestionSkill (QuestionId, SkillId) VALUES 
(1001, 7),
(1001, 13),
(1001, 28),
(1002, 13),
(1002, 26);

INSERT INTO User (Id, UserName) VALUES 
(1001, 'Avadh');

INSERT INTO UserQuestions (UserId, QuestionId, UserAnswer, IsCorrect, AttemptTime) VALUES 
(10001, 1001, 'abc', 0, '2025-01-01 10:00:00');

INSERT INTO UserSkill (UserId, CompetencyId, SkillRank) VALUES 
(1001, 1, 2133),
(1001, 2, 4324),
(1001, 3, 34),
(1001, 6, 123),
(1001, 7, 2342),
(1001, 8, 4321);

-- Sample queries to test the database
-- Get all competencies
SELECT * FROM Competency;

-- Get all skills for a specific competency
SELECT s.*, c.CompetencyName 
FROM Skill s 
JOIN Competency c ON s.CompetencyId = c.Id 
WHERE c.CompetencyCode = 'C1';

-- Get questions with their associated skills
SELECT q.*, s.ShortDescription as SkillDescription, c.CompetencyName
FROM Questions q
JOIN QuestionSkill qs ON q.Id = qs.QuestionId
JOIN Skill s ON qs.SkillId = s.Id
JOIN Competency c ON s.CompetencyId = c.Id;

-- Get user's skill rankings
SELECT u.UserName, c.CompetencyName, us.SkillRank
FROM User u
JOIN UserSkill us ON u.Id = us.UserId
JOIN Competency c ON us.CompetencyId = c.Id
ORDER BY u.UserName, c.CompetencyName;

-- Get user's question attempts
SELECT u.UserName, q.QuestionDescription, uq.UserAnswer, uq.IsCorrect, uq.AttemptTime
FROM User u
JOIN UserQuestions uq ON u.Id = uq.UserId
JOIN Questions q ON uq.QuestionId = q.Id
ORDER BY u.UserName, uq.AttemptTime DESC;