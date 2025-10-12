from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Competency:
    """Competency model"""
    id: int
    competency_code: str
    competency_name: str
    domain_code: str
    domain_name: str
    description: Optional[str] = None

@dataclass
class Skill:
    """Skill model"""
    id: int
    competency_id: int
    stage: str
    short_description: str
    description: Optional[str] = None
    start_mmr: int = 0
    end_mmr: int = 0

@dataclass
class Question:
    """Question model"""
    id: int
    question_type: str
    question_description: str
    options: Optional[str] = None
    questions_answer: str = ""
    question_hint: Optional[str] = None

@dataclass
class User:
    """User model"""
    id: int
    username: str

@dataclass
class UserQuestion:
    """User question attempt model"""
    user_id: int
    question_id: int
    user_answer: Optional[str] = None
    is_correct: bool = False
    attempt_time: Optional[datetime] = None

@dataclass
class UserSkill:
    """User skill ranking model"""
    user_id: int
    competency_id: int
    skill_rank: int

@dataclass
class QuestionSkill:
    """Question-Skill relationship model"""
    question_id: int
    skill_id: int

# Request/Response models
@dataclass
class CreateCompetencyRequest:
    """Request model for creating a competency"""
    competency_code: str
    competency_name: str
    domain_code: str
    domain_name: str
    description: Optional[str] = ""

@dataclass
class CreateSkillRequest:
    """Request model for creating a skill"""
    competency_id: int
    stage: str
    short_description: str
    description: Optional[str] = ""
    start_mmr: int = 0
    end_mmr: int = 0

@dataclass
class CreateQuestionRequest:
    """Request model for creating a question"""
    question_type: str
    question_description: str
    options: Optional[str] = ""
    questions_answer: str = ""
    question_hint: Optional[str] = ""

@dataclass
class CreateUserRequest:
    """Request model for creating a user"""
    username: str

@dataclass
class RecordAttemptRequest:
    """Request model for recording a question attempt"""
    question_id: int
    user_answer: str
    is_correct: bool
    attempt_time: Optional[str] = None

@dataclass
class UpdateSkillRankingRequest:
    """Request model for updating skill ranking"""
    skill_rank: int

@dataclass
class APIResponse:
    """Standard API response model"""
    success: bool
    data: Optional[any] = None
    message: Optional[str] = None
    count: Optional[int] = None
    error: Optional[str] = None

# Validation functions
def validate_competency_data(data: dict) -> tuple[bool, str]:
    """Validate competency creation data"""
    required_fields = ['competency_code', 'competency_name', 'domain_code', 'domain_name']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        if not isinstance(data[field], str) or not data[field].strip():
            return False, f"Field {field} must be a non-empty string"
    
    # Validate competency code format
    if len(data['competency_code']) > 10:
        return False, "Competency code must be 10 characters or less"
    
    if len(data['competency_name']) > 100:
        return False, "Competency name must be 100 characters or less"
    
    return True, ""

def validate_skill_data(data: dict) -> tuple[bool, str]:
    """Validate skill creation data"""
    required_fields = ['competency_id', 'stage', 'short_description', 'start_mmr', 'end_mmr']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate competency_id
    if not isinstance(data['competency_id'], int) or data['competency_id'] <= 0:
        return False, "Competency ID must be a positive integer"
    
    # Validate stage
    if not isinstance(data['stage'], str) or not data['stage'].strip():
        return False, "Stage must be a non-empty string"
    
    # Validate short_description
    if not isinstance(data['short_description'], str) or not data['short_description'].strip():
        return False, "Short description must be a non-empty string"
    
    if len(data['short_description']) > 200:
        return False, "Short description must be 200 characters or less"
    
    # Validate MMR values
    if not isinstance(data['start_mmr'], int) or data['start_mmr'] < 0:
        return False, "Start MMR must be a non-negative integer"
    
    if not isinstance(data['end_mmr'], int) or data['end_mmr'] < 0:
        return False, "End MMR must be a non-negative integer"
    
    if data['start_mmr'] > data['end_mmr']:
        return False, "Start MMR must be less than or equal to End MMR"
    
    return True, ""

def validate_question_data(data: dict) -> tuple[bool, str]:
    """Validate question creation data"""
    required_fields = ['question_type', 'question_description', 'questions_answer']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        if not isinstance(data[field], str) or not data[field].strip():
            return False, f"Field {field} must be a non-empty string"
    
    # Validate question type
    valid_types = ['MCQ', 'Integer', 'Text', 'Boolean']
    if data['question_type'] not in valid_types:
        return False, f"Question type must be one of: {', '.join(valid_types)}"
    
    return True, ""

def validate_user_data(data: dict) -> tuple[bool, str]:
    """Validate user creation data"""
    if 'username' not in data:
        return False, "Missing required field: username"
    
    if not isinstance(data['username'], str) or not data['username'].strip():
        return False, "Username must be a non-empty string"
    
    if len(data['username']) > 50:
        return False, "Username must be 50 characters or less"
    
    return True, ""

def validate_attempt_data(data: dict) -> tuple[bool, str]:
    """Validate question attempt data"""
    required_fields = ['question_id', 'user_answer', 'is_correct']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate question_id
    if not isinstance(data['question_id'], int) or data['question_id'] <= 0:
        return False, "Question ID must be a positive integer"
    
    # Validate user_answer
    if not isinstance(data['user_answer'], str):
        return False, "User answer must be a string"
    
    # Validate is_correct
    if not isinstance(data['is_correct'], bool):
        return False, "Is correct must be a boolean"
    
    return True, ""

def validate_skill_ranking_data(data: dict) -> tuple[bool, str]:
    """Validate skill ranking update data"""
    if 'skill_rank' not in data:
        return False, "Missing required field: skill_rank"
    
    if not isinstance(data['skill_rank'], int) or data['skill_rank'] < 0:
        return False, "Skill rank must be a non-negative integer"
    
    return True, ""

# Helper functions for data conversion
def dict_to_competency(data: dict) -> Competency:
    """Convert dictionary to Competency object"""
    return Competency(
        id=data['Id'],
        competency_code=data['CompetencyCode'],
        competency_name=data['CompetencyName'],
        domain_code=data['DomainCode'],
        domain_name=data['DomainName'],
        description=data.get('Description', '')
    )

def dict_to_skill(data: dict) -> Skill:
    """Convert dictionary to Skill object"""
    return Skill(
        id=data['Id'],
        competency_id=data['CompetencyId'],
        stage=data['Stage'],
        short_description=data['ShortDescription'],
        description=data.get('Description', ''),
        start_mmr=data.get('StartMMR', 0),
        end_mmr=data.get('EndMMR', 0)
    )

def dict_to_question(data: dict) -> Question:
    """Convert dictionary to Question object"""
    return Question(
        id=data['Id'],
        question_type=data['QuestionType'],
        question_description=data['QuestionDescription'],
        options=data.get('Options', ''),
        questions_answer=data['QuestionsAnswer'],
        question_hint=data.get('QuestionHint', '')
    )

def dict_to_user(data: dict) -> User:
    """Convert dictionary to User object"""
    return User(
        id=data['Id'],
        username=data['UserName']
    )

def dict_to_user_question(data: dict) -> UserQuestion:
    """Convert dictionary to UserQuestion object"""
    return UserQuestion(
        user_id=data['UserId'],
        question_id=data['QuestionId'],
        user_answer=data.get('UserAnswer', ''),
        is_correct=bool(data.get('IsCorrect', False)),
        attempt_time=data.get('AttemptTime')
    )

def dict_to_user_skill(data: dict) -> UserSkill:
    """Convert dictionary to UserSkill object"""
    return UserSkill(
        user_id=data['UserId'],
        competency_id=data['CompetencyId'],
        skill_rank=data['SkillRank']
    )
