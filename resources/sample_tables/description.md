These are the following tables in the database:

## Competency
- Id
- CompetencyCode
- CompetencyName
- DomainCode
- DomainName
- Description

## Questions
- Id
- QuestionType
- QuestionDescription
- Options
- QuestionsAnswer
- QuestionHint

## QuestionSkill
- QuestionId
- SkillId

## Skill
- Id
- CompetencyId
- Stage
- ShortDescription
- Description
- StartMMR
- EndMMR

## User
- Id
- UserName

## UserQuestions
- UserId
- QuestionId
- UserAnswer
- IsCorrect
- AttemptTime

## UserSkill
- UserId
- CompetencyId
- SkillRank

Following are the table properties
## Competency
Primary Key: Id

## Skill
Primary Key: Id
CompetencyId is foreign key to Compenetency.Id

## Questions
Primary Key: Id

## QuestionSkill
Holds the link between Questions and Skill table
Primary key: (QuestionId, SkillId)
QuestionId is linked to Questions.Id in Questions table
SkillId is linked to Skill.Id in Skill table

## User
Holds user information
PrimaryKey: Id

## UserQuestions
Holds the information of the questions attempted by user in the past along with the results. This table is not modified so records will sorted by AttemptTime column
Indexed on UserId and QuestionId
AttemptTime is of DateTime format
Sorted in AttemptTime
QuestionId is linked to Questions.Id in Questions table
UserId is linked to User.Id in User table

## UserSkill
PrimaryKey: (UserId, CompetencyId)
UserId is linked to User.Id in User table
CompetencyId is foreign key to Compenetency.Id in Compenetency table




