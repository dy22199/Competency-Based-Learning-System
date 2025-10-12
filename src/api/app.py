from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the parent directory to the path to import database_manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql.database_manager import DatabaseManager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize database manager
db_manager = DatabaseManager()

@app.before_request
def before_request():
    """Connect to database before each request"""
    db_manager.connect()

@app.after_request
def after_request(response):
    """Close database connection after each request"""
    db_manager.disconnect()
    return response

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': 'An error occurred processing your request'}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'})

# Competency endpoints
@app.route('/api/competencies', methods=['GET'])
def get_all_competencies():
    """Get all competencies"""
    try:
        competencies = db_manager.get_all_competencies()
        return jsonify({
            'success': True,
            'data': competencies,
            'count': len(competencies)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch competencies', 'message': str(e)}), 500

@app.route('/api/competencies/<competency_code>', methods=['GET'])
def get_competency_by_code(competency_code):
    """Get competencies by code"""
    try:
        competencies = db_manager.get_competency_by_code(competency_code)
        if not competencies:
            return jsonify({'error': 'Competency not found'}), 404
        return jsonify({
            'success': True,
            'data': competencies
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch competency', 'message': str(e)}), 500

@app.route('/api/competencies', methods=['POST'])
def add_competency():
    """Add a new competency"""
    try:
        data = request.get_json()
        required_fields = ['competency_code', 'competency_name', 'domain_code', 'domain_name']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        result = db_manager.add_competency(
            data['competency_code'],
            data['competency_name'],
            data['domain_code'],
            data['domain_name'],
            data.get('description', '')
        )
        
        return jsonify({
            'success': True,
            'message': 'Competency added successfully',
            'rows_affected': result
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to add competency', 'message': str(e)}), 500

# Skill endpoints
@app.route('/api/competencies/<int:competency_id>/skills', methods=['GET'])
def get_skills_by_competency(competency_id):
    """Get all skills for a specific competency"""
    try:
        skills = db_manager.get_skills_by_competency(competency_id)
        return jsonify({
            'success': True,
            'data': skills,
            'count': len(skills)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch skills', 'message': str(e)}), 500

@app.route('/api/competencies/code/<competency_code>/skills', methods=['GET'])
def get_skills_by_competency_code(competency_code):
    """Get all skills for a specific competency code"""
    try:
        skills = db_manager.get_skills_by_competency_code(competency_code)
        return jsonify({
            'success': True,
            'data': skills,
            'count': len(skills)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch skills', 'message': str(e)}), 500

@app.route('/api/skills/mmr-range', methods=['GET'])
def get_skills_by_mmr_range():
    """Get skills within a specific MMR range"""
    try:
        min_mmr = request.args.get('min_mmr', type=int)
        max_mmr = request.args.get('max_mmr', type=int)
        
        if min_mmr is None or max_mmr is None:
            return jsonify({'error': 'Both min_mmr and max_mmr parameters are required'}), 400
        
        skills = db_manager.get_skill_by_mmr_range(min_mmr, max_mmr)
        return jsonify({
            'success': True,
            'data': skills,
            'count': len(skills)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch skills', 'message': str(e)}), 500

@app.route('/api/skills', methods=['POST'])
def add_skill():
    """Add a new skill"""
    try:
        data = request.get_json()
        required_fields = ['competency_id', 'stage', 'short_description', 'start_mmr', 'end_mmr']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        result = db_manager.add_skill(
            data['competency_id'],
            data['stage'],
            data['short_description'],
            data.get('description', ''),
            data['start_mmr'],
            data['end_mmr']
        )
        
        return jsonify({
            'success': True,
            'message': 'Skill added successfully',
            'rows_affected': result
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to add skill', 'message': str(e)}), 500

# Question endpoints
@app.route('/api/questions', methods=['GET'])
def get_all_questions():
    """Get all questions"""
    try:
        questions = db_manager.get_all_questions()
        return jsonify({
            'success': True,
            'data': questions,
            'count': len(questions)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch questions', 'message': str(e)}), 500

@app.route('/api/questions/type/<question_type>', methods=['GET'])
def get_questions_by_type(question_type):
    """Get questions by type"""
    try:
        questions = db_manager.get_questions_by_type(question_type)
        return jsonify({
            'success': True,
            'data': questions,
            'count': len(questions)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch questions', 'message': str(e)}), 500

@app.route('/api/skills/<int:skill_id>/questions', methods=['GET'])
def get_questions_by_skill(skill_id):
    """Get questions associated with a specific skill"""
    try:
        questions = db_manager.get_questions_by_skill(skill_id)
        return jsonify({
            'success': True,
            'data': questions,
            'count': len(questions)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch questions', 'message': str(e)}), 500

@app.route('/api/competencies/<int:competency_id>/questions', methods=['GET'])
def get_questions_by_competency(competency_id):
    """Get questions associated with a specific competency"""
    try:
        questions = db_manager.get_questions_by_competency(competency_id)
        return jsonify({
            'success': True,
            'data': questions,
            'count': len(questions)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch questions', 'message': str(e)}), 500

@app.route('/api/questions', methods=['POST'])
def add_question():
    """Add a new question"""
    try:
        data = request.get_json()
        required_fields = ['question_type', 'question_description', 'questions_answer']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        result = db_manager.add_question(
            data['question_type'],
            data['question_description'],
            data.get('options', ''),
            data['questions_answer'],
            data.get('question_hint', '')
        )
        
        return jsonify({
            'success': True,
            'message': 'Question added successfully',
            'rows_affected': result
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to add question', 'message': str(e)}), 500

@app.route('/api/questions/<int:question_id>/skills/<int:skill_id>', methods=['POST'])
def link_question_to_skill(question_id, skill_id):
    """Link a question to a skill"""
    try:
        result = db_manager.link_question_to_skill(question_id, skill_id)
        return jsonify({
            'success': True,
            'message': 'Question linked to skill successfully',
            'rows_affected': result
        })
    except Exception as e:
        return jsonify({'error': 'Failed to link question to skill', 'message': str(e)}), 500

# User endpoints
@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    try:
        users = db_manager.get_all_users()
        return jsonify({
            'success': True,
            'data': users,
            'count': len(users)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users', 'message': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Get user by ID"""
    try:
        users = db_manager.get_user_by_id(user_id)
        if not users:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({
            'success': True,
            'data': users[0]
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch user', 'message': str(e)}), 500

@app.route('/api/users/name/<username>', methods=['GET'])
def get_user_by_name(username):
    """Get user by username"""
    try:
        users = db_manager.get_user_by_name(username)
        if not users:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({
            'success': True,
            'data': users[0]
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch user', 'message': str(e)}), 500

@app.route('/api/users', methods=['POST'])
def add_user():
    """Add a new user"""
    try:
        data = request.get_json()
        if 'username' not in data:
            return jsonify({'error': 'Missing required field: username'}), 400
        
        result = db_manager.add_user(data['username'])
        return jsonify({
            'success': True,
            'message': 'User added successfully',
            'rows_affected': result
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to add user', 'message': str(e)}), 500

# UserQuestions endpoints
@app.route('/api/users/<int:user_id>/attempts', methods=['GET'])
def get_user_attempts(user_id):
    """Get all question attempts for a user"""
    try:
        attempts = db_manager.get_user_attempts(user_id)
        return jsonify({
            'success': True,
            'data': attempts,
            'count': len(attempts)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch user attempts', 'message': str(e)}), 500

@app.route('/api/users/<int:user_id>/questions/<int:question_id>/attempts', methods=['GET'])
def get_user_attempts_by_question(user_id, question_id):
    """Get all attempts for a specific question by a user"""
    try:
        attempts = db_manager.get_user_attempts_by_question(user_id, question_id)
        return jsonify({
            'success': True,
            'data': attempts,
            'count': len(attempts)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch attempts', 'message': str(e)}), 500

@app.route('/api/users/<int:user_id>/attempts', methods=['POST'])
def record_question_attempt(user_id):
    """Record a user's attempt at a question"""
    try:
        data = request.get_json()
        required_fields = ['question_id', 'user_answer', 'is_correct']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        result = db_manager.record_question_attempt(
            user_id,
            data['question_id'],
            data['user_answer'],
            data['is_correct'],
            data.get('attempt_time')
        )
        
        return jsonify({
            'success': True,
            'message': 'Question attempt recorded successfully',
            'rows_affected': result
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to record attempt', 'message': str(e)}), 500

@app.route('/api/users/<int:user_id>/attempts/correct', methods=['GET'])
def get_user_correct_attempts(user_id):
    """Get all correct attempts for a user"""
    try:
        attempts = db_manager.get_user_correct_attempts(user_id)
        return jsonify({
            'success': True,
            'data': attempts,
            'count': len(attempts)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch correct attempts', 'message': str(e)}), 500

@app.route('/api/users/<int:user_id>/attempts/incorrect', methods=['GET'])
def get_user_incorrect_attempts(user_id):
    """Get all incorrect attempts for a user"""
    try:
        attempts = db_manager.get_user_incorrect_attempts(user_id)
        return jsonify({
            'success': True,
            'data': attempts,
            'count': len(attempts)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch incorrect attempts', 'message': str(e)}), 500

# UserSkill endpoints
@app.route('/api/users/<int:user_id>/skill-rankings', methods=['GET'])
def get_user_skill_rankings(user_id):
    """Get all skill rankings for a user"""
    try:
        rankings = db_manager.get_user_skill_rankings(user_id)
        return jsonify({
            'success': True,
            'data': rankings,
            'count': len(rankings)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch skill rankings', 'message': str(e)}), 500

@app.route('/api/users/<int:user_id>/competencies/<int:competency_id>/skill-ranking', methods=['GET'])
def get_user_skill_ranking(user_id, competency_id):
    """Get skill ranking for a specific competency"""
    try:
        rankings = db_manager.get_user_skill_ranking(user_id, competency_id)
        if not rankings:
            return jsonify({'error': 'Skill ranking not found'}), 404
        return jsonify({
            'success': True,
            'data': rankings[0]
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch skill ranking', 'message': str(e)}), 500

@app.route('/api/users/<int:user_id>/competencies/<int:competency_id>/skill-ranking', methods=['PUT'])
def update_user_skill_ranking(user_id, competency_id):
    """Update or insert user skill ranking"""
    try:
        data = request.get_json()
        if 'skill_rank' not in data:
            return jsonify({'error': 'Missing required field: skill_rank'}), 400
        
        result = db_manager.update_user_skill_ranking(user_id, competency_id, data['skill_rank'])
        return jsonify({
            'success': True,
            'message': 'Skill ranking updated successfully',
            'rows_affected': result
        })
    except Exception as e:
        return jsonify({'error': 'Failed to update skill ranking', 'message': str(e)}), 500

@app.route('/api/competencies/<int:competency_id>/users', methods=['GET'])
def get_users_by_competency_ranking(competency_id):
    """Get users ranked by their skill level in a specific competency"""
    try:
        min_rank = request.args.get('min_rank', type=int)
        max_rank = request.args.get('max_rank', type=int)
        
        users = db_manager.get_users_by_competency_ranking(competency_id, min_rank, max_rank)
        return jsonify({
            'success': True,
            'data': users,
            'count': len(users)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users by ranking', 'message': str(e)}), 500

# Analytics endpoints
@app.route('/api/users/<int:user_id>/progress-summary', methods=['GET'])
def get_user_progress_summary(user_id):
    """Get a summary of user's progress across all competencies"""
    try:
        progress = db_manager.get_user_progress_summary(user_id)
        return jsonify({
            'success': True,
            'data': progress,
            'count': len(progress)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch progress summary', 'message': str(e)}), 500

@app.route('/api/competencies/<int:competency_id>/statistics', methods=['GET'])
def get_competency_statistics(competency_id):
    """Get statistics for a specific competency"""
    try:
        stats = db_manager.get_competency_statistics(competency_id)
        return jsonify({
            'success': True,
            'data': stats,
            'count': len(stats)
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch competency statistics', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
