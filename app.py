from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
import json
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'astroventure_secret_key_2025'

# Configure Gemini AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# Level configurations with expanded topics for variety
LEVEL_CONFIG = {
    'easy': {
        'name': 'ROOKIE',
        'description': 'Basic astronomy and space science questions suitable for beginners',
        'topics': [
            'solar system', 'planets', 'stars', 'moon', 'basic space facts', 
            'sun', 'earth', 'space exploration basics', 'astronauts', 'rockets',
            'comets', 'meteors', 'constellations', 'day and night', 'seasons'
        ]
    },
    'medium': {
        'name': 'EXPLORER', 
        'description': 'Intermediate astronomy questions about space missions, satellites, and celestial phenomena',
        'topics': [
            'space missions', 'satellites', 'galaxies', 'astronauts', 'space exploration history',
            'space stations', 'telescopes', 'space technology', 'lunar missions', 'mars exploration',
            'nebulae', 'star formation', 'planetary rings', 'asteroid belt', 'space agencies'
        ]
    },
    'hard': {
        'name': 'COMMANDER',
        'description': 'Advanced astrophysics and cosmology questions for space experts',
        'topics': [
            'black holes', 'dark matter', 'stellar evolution', 'quantum mechanics in space', 'advanced cosmology',
            'neutron stars', 'quasars', 'supernovae', 'gravitational waves', 'exoplanets',
            'cosmic microwave background', 'redshift', 'space-time', 'relativity', 'particle physics'
        ]
    }
}

def generate_questions(level, count=5):
    """Generate questions using Gemini AI based on difficulty level"""
    config = LEVEL_CONFIG[level]
    
    # Create a much more unique session identifier
    import time
    import hashlib
    timestamp = str(time.time())
    random_seed = str(random.random())
    session_id = hashlib.md5((timestamp + random_seed).encode()).hexdigest()[:8]
    
    # Get previously asked questions to avoid repetition
    used_questions = session.get('used_questions', [])
    
    # Select random topics and focus areas for maximum variety
    random_topics = random.sample(config['topics'], min(4, len(config['topics'])))
    random_focus = random.choice([
        "recent space discoveries", "historical space milestones", "scientific principles", 
        "space missions and exploration", "celestial objects and phenomena", "physics in space",
        "astronomical measurements", "space technology", "cosmic mysteries and theories",
        "planetary science", "stellar evolution", "galactic structures", "cosmological concepts"
    ])
    
    # Create specific question categories to ensure variety
    question_styles = random.sample([
        "What happens when", "How does", "Which of these", "What is the difference between",
        "Why does", "What causes", "How long does it take", "What is the largest/smallest",
        "Which planet/star/galaxy", "What would happen if", "How do scientists measure",
        "What discovery", "Which mission", "What phenomenon"
    ], min(3, 13))
    
    # Add temporal variety
    time_periods = ["ancient astronomy", "20th century discoveries", "21st century findings", "future space exploration"]
    selected_period = random.choice(time_periods)
    
    prompt = f"""
    You are creating astronomy questions for session ID: {session_id}
    
    CRITICAL: Generate {count} COMPLETELY UNIQUE questions that have NEVER been asked before.
    
    AVOID these question patterns if any exist:
    {'; '.join(used_questions[-10:]) if used_questions else 'None yet - this is a fresh start!'}
    
    Session Parameters:
    - Difficulty: {level} ({config['description']})
    - Focus Topics: {', '.join(random_topics)}
    - Question Style: {', '.join(question_styles)}
    - Thematic Focus: {random_focus}
    - Time Period Emphasis: {selected_period}
    - Uniqueness ID: {session_id}
    
    REQUIREMENTS:
    1. Each question must be completely different from any previous questions
    2. Use varied question formats: {', '.join(question_styles)}
    3. Mix topics creatively: {', '.join(random_topics)}
    4. Include {selected_period} perspectives when relevant
    5. Focus on {random_focus}
    6. Make questions engaging and thought-provoking
    7. Ensure scientific accuracy
    8. Provide fascinating explanations with fun space facts
    
    Return ONLY this JSON format:
    [
        {{
            "question": "Unique engaging question using one of these styles: {', '.join(question_styles[:2])}?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,
            "explanation": "Fascinating explanation with a mind-blowing space fact"
        }}
    ]
    
    Make every question fresh, creative, and scientifically fascinating!
    Session: {session_id} | Focus: {random_focus} | Topics: {', '.join(random_topics)}
    """
    
    try:
        response = model.generate_content(prompt)
        questions_text = response.text.strip()
        
        # Clean up response - remove any markdown or extra text
        if '```json' in questions_text:
            questions_text = questions_text.split('```json')[1].split('```')[0].strip()
        elif '```' in questions_text:
            questions_text = questions_text.split('```')[1].split('```')[0].strip()
        
        # Remove any text before the JSON array starts
        if questions_text.find('[') > 0:
            questions_text = questions_text[questions_text.find('['):]
        
        # Remove any text after the JSON array ends
        if questions_text.rfind(']') < len(questions_text) - 1:
            questions_text = questions_text[:questions_text.rfind(']') + 1]
        
        questions = json.loads(questions_text)
        
        # Validate questions and track them to prevent repetition
        valid_questions = []
        for q in questions:
            if all(key in q for key in ['question', 'options', 'correct', 'explanation']):
                if len(q['options']) == 4 and 0 <= q['correct'] <= 3:
                    # Check if this question is too similar to previous ones
                    question_text = q['question'].lower()
                    is_unique = True
                    
                    for used_q in used_questions:
                        # Simple similarity check - you could make this more sophisticated
                        if len(set(question_text.split()) & set(used_q.lower().split())) > 3:
                            is_unique = False
                            break
                    
                    if is_unique:
                        valid_questions.append(q)
                        # Track this question to avoid repetition
                        if 'used_questions' not in session:
                            session['used_questions'] = []
                        session['used_questions'].append(q['question'])
                        
                        # Keep only last 50 questions to prevent unlimited growth
                        if len(session['used_questions']) > 50:
                            session['used_questions'] = session['used_questions'][-50:]
        
        if len(valid_questions) >= count:
            print(f"✅ Generated {len(valid_questions)} truly unique questions for session #{session_id}")
            print(f"📝 Tracking {len(session.get('used_questions', []))} questions to prevent repetition")
            return valid_questions[:count]
        else:
            print(f"⚠️ Not enough unique questions. Got {len(valid_questions)}, trying alternative approach...")
            return generate_alternative_questions(level, count, session_id)
        
    except Exception as e:
        print(f"❌ Error generating questions: {e}")
        print(f"Response: {questions_text if 'questions_text' in locals() else 'No response'}")
        return generate_alternative_questions(level, count, session_id)

def generate_alternative_questions(level, count=5, session_id=None):
    """Alternative approach when main generation fails"""
    config = LEVEL_CONFIG[level]
    used_questions = session.get('used_questions', [])
    
    # Use different approach - ask for specific types of questions
    question_types = [
        "comparison questions", "fact-based questions", "definition questions",
        "calculation questions", "historical questions", "discovery questions",
        "cause and effect questions", "process questions", "measurement questions"
    ]
    selected_type = random.choice(question_types)
    random_topic = random.choice(config['topics'])
    
    # Add more variety to alternative prompts
    perspective = random.choice([
        "from a scientist's viewpoint", "from an explorer's perspective", 
        "focusing on recent discoveries", "emphasizing physics principles",
        "highlighting space missions", "exploring cosmic phenomena"
    ])
    
    simple_prompt = f"""
    Session: {session_id or 'alt'}
    Create {count} completely UNIQUE {selected_type} about {random_topic} for {level} difficulty.
    Approach: {perspective}
    
    AVOID these patterns: {'; '.join(used_questions[-5:]) if used_questions else 'None yet'}
    
    Make each question fresh and different. Focus on {random_topic} {perspective}.
    
    Return as JSON array:
    [{{"question": "unique question text?", "options": ["A", "B", "C", "D"], "correct": 0, "explanation": "fascinating explanation"}}]
    
    Requirements:
    - Each question must be completely different
    - Use creative {selected_type} format
    - Focus specifically on {random_topic}
    - Approach {perspective}
    - Include amazing space facts in explanations
    """
    
    try:
        response = model.generate_content(simple_prompt)
        questions_text = response.text.strip()
        
        # Extract and clean JSON
        if '[' in questions_text and ']' in questions_text:
            start = questions_text.find('[')
            end = questions_text.rfind(']') + 1
            questions_text = questions_text[start:end]
        
        questions = json.loads(questions_text)
        
        # Filter for uniqueness and validity
        valid_unique = []
        for q in questions:
            if all(k in q for k in ['question', 'options', 'correct', 'explanation']) and len(q['options']) == 4:
                question_text = q['question'].lower()
                is_unique = True
                
                # Check uniqueness against used questions
                for used_q in used_questions:
                    if len(set(question_text.split()) & set(used_q.lower().split())) > 2:
                        is_unique = False
                        break
                
                if is_unique:
                    valid_unique.append(q)
                    # Track the question
                    if 'used_questions' not in session:
                        session['used_questions'] = []
                    session['used_questions'].append(q['question'])
        
        if valid_unique:
            print(f"✅ Alternative generation successful: {len(valid_unique)} unique questions")
            print(f"📝 Now tracking {len(session.get('used_questions', []))} total questions")
            return valid_unique[:count]
        else:
            print("⚠️ Alternative generation failed, using minimal fallback")
            return create_minimal_questions(level, count)
            
    except Exception as e:
        print(f"❌ Alternative generation error: {e}")
        return create_minimal_questions(level, count)

def generate_simple_questions(level, count=5):
    """Generate questions with a simpler prompt if the complex one fails"""
    config = LEVEL_CONFIG[level]
    
    prompt = f"""
    Create {count} astronomy quiz questions for {level} difficulty level.
    Topics: {', '.join(config['topics'])}
    
    Format as JSON array:
    [{{"question": "text?", "options": ["A", "B", "C", "D"], "correct": 0, "explanation": "why"}}]
    
    Make sure each question has exactly 4 options and the correct answer index (0-3).
    """
    
    try:
        response = model.generate_content(prompt)
        questions_text = response.text.strip()
        
        # Clean up the response
        if '```json' in questions_text:
            questions_text = questions_text.split('```json')[1].split('```')[0]
        elif '```' in questions_text:
            questions_text = questions_text.split('```')[1].split('```')[0]
        
        questions = json.loads(questions_text)
        return questions[:count] if len(questions) > count else questions
        
    except Exception as e:
        print(f"Error with simple prompt: {e}")
        # Only now use minimal fallback
        return create_minimal_questions(level, count)

def create_minimal_questions(level, count=5):
    """Create varied basic questions when AI completely fails"""
    import random
    
    # Get used questions to try to avoid repeats even in fallback
    used_questions = session.get('used_questions', [])
    
    if level == 'easy':
        all_easy_questions = [
            {"question": "What is the center of our solar system?", "options": ["Earth", "Sun", "Moon", "Mars"], "correct": 1, "explanation": "The Sun is at the center of our solar system and provides light and heat to all planets."},
            {"question": "How many planets are in our solar system?", "options": ["7", "8", "9", "10"], "correct": 1, "explanation": "There are 8 planets in our solar system since Pluto was reclassified as a dwarf planet in 2006."},
            {"question": "What is Earth's natural satellite called?", "options": ["Star", "Moon", "Planet", "Comet"], "correct": 1, "explanation": "The Moon is Earth's natural satellite and is about 384,400 km away from us."},
            {"question": "Which planet is closest to Earth?", "options": ["Mars", "Venus", "Jupiter", "Mercury"], "correct": 1, "explanation": "Venus is the closest planet to Earth, though Mars gets closer during certain alignments."},
            {"question": "What gives the Sun its energy?", "options": ["Coal", "Nuclear fusion", "Electricity", "Fire"], "correct": 1, "explanation": "Nuclear fusion converts hydrogen into helium in the Sun's core, releasing enormous amounts of energy."},
            {"question": "Which planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "correct": 1, "explanation": "Mars appears red due to iron oxide (rust) on its surface."},
            {"question": "What do we call a group of stars that form a pattern?", "options": ["Galaxy", "Constellation", "Nebula", "Cluster"], "correct": 1, "explanation": "Constellations are patterns of stars that have been recognized by humans for thousands of years."},
            {"question": "How long does it take Earth to orbit the Sun?", "options": ["24 hours", "1 month", "1 year", "10 years"], "correct": 2, "explanation": "Earth takes approximately 365.25 days (1 year) to complete one orbit around the Sun."},
            {"question": "What causes day and night on Earth?", "options": ["Earth's orbit", "Earth's rotation", "The Moon", "Clouds"], "correct": 1, "explanation": "Earth rotates on its axis once every 24 hours, causing day and night."},
            {"question": "Which is the largest planet in our solar system?", "options": ["Saturn", "Earth", "Jupiter", "Neptune"], "correct": 2, "explanation": "Jupiter is the largest planet and could fit more than 1,300 Earths inside it."}
        ]
    elif level == 'medium':
        all_easy_questions = [
            {"question": "What was the first human mission to land on the Moon?", "options": ["Apollo 10", "Apollo 11", "Apollo 12", "Gemini 7"], "correct": 1, "explanation": "Apollo 11 was the first mission to land humans on the Moon on July 20, 1969."},
            {"question": "Which planet has the most prominent ring system?", "options": ["Jupiter", "Saturn", "Uranus", "Neptune"], "correct": 1, "explanation": "Saturn has the most spectacular and visible ring system made of ice and rock particles."},
            {"question": "What is the nearest star to our solar system?", "options": ["Sirius", "Proxima Centauri", "Alpha Centauri", "Betelgeuse"], "correct": 1, "explanation": "Proxima Centauri is 4.24 light-years away and is part of the Alpha Centauri system."},
            {"question": "How long does light from the Sun take to reach Earth?", "options": ["8 minutes", "1 hour", "1 day", "1 second"], "correct": 0, "explanation": "Light travels at 300,000 km/s and takes about 8 minutes and 20 seconds to reach Earth."},
            {"question": "What is the name of our galaxy?", "options": ["Andromeda", "Milky Way", "Whirlpool", "Sombrero"], "correct": 1, "explanation": "We live in the Milky Way galaxy, which contains over 100 billion stars."},
            {"question": "What is the International Space Station?", "options": ["A satellite", "A space laboratory", "A telescope", "A rocket"], "correct": 1, "explanation": "The ISS is a space laboratory where astronauts conduct experiments in microgravity."},
            {"question": "Which space agency first sent humans to space?", "options": ["NASA", "ESA", "Roscosmos", "CNSA"], "correct": 2, "explanation": "The Soviet space program (now Roscosmos) sent Yuri Gagarin to space in 1961."},
            {"question": "What is a light-year?", "options": ["A unit of time", "A unit of distance", "A type of star", "A space mission"], "correct": 1, "explanation": "A light-year is the distance light travels in one year, about 9.46 trillion kilometers."},
            {"question": "Which planet has the Great Red Spot?", "options": ["Mars", "Jupiter", "Saturn", "Neptune"], "correct": 1, "explanation": "Jupiter's Great Red Spot is a massive storm that has been raging for centuries."},
            {"question": "What are asteroids?", "options": ["Small planets", "Rocky objects", "Gas clouds", "Ice balls"], "correct": 1, "explanation": "Asteroids are rocky objects that orbit the Sun, mostly found in the asteroid belt between Mars and Jupiter."}
        ]
    else:  # hard
        all_easy_questions = [
            {"question": "What is the event horizon of a black hole?", "options": ["The point where time stops", "The boundary of no return", "The center of the black hole", "A ring around it"], "correct": 1, "explanation": "The event horizon is the boundary around a black hole beyond which nothing can escape, not even light."},
            {"question": "What percentage of the universe is dark matter?", "options": ["About 27%", "About 68%", "About 5%", "About 85%"], "correct": 0, "explanation": "Dark matter makes up about 27% of the universe, while dark energy comprises about 68%."},
            {"question": "What process powers main sequence stars?", "options": ["Nuclear fission", "Nuclear fusion", "Chemical burning", "Gravitational collapse"], "correct": 1, "explanation": "Nuclear fusion converts hydrogen into helium in stellar cores, releasing the energy that makes stars shine."},
            {"question": "What is Sagittarius A*?", "options": ["A constellation", "A supermassive black hole", "A nebula", "A galaxy"], "correct": 1, "explanation": "Sagittarius A* is the supermassive black hole at the center of our Milky Way galaxy."},
            {"question": "What is cosmic microwave background radiation?", "options": ["Heat from stars", "Afterglow of the Big Bang", "Solar radiation", "Galactic radio waves"], "correct": 1, "explanation": "The CMB is the afterglow radiation from the Big Bang, discovered in 1965."},
            {"question": "What is redshift in astronomy?", "options": ["Light becoming red", "Doppler effect in space", "A type of star", "Planetary motion"], "correct": 1, "explanation": "Redshift occurs when objects move away from us, stretching light waves to longer (redder) wavelengths."},
            {"question": "What are neutron stars?", "options": ["Young stars", "Collapsed stellar cores", "Binary star systems", "Planetary nebulae"], "correct": 1, "explanation": "Neutron stars are incredibly dense remnants of massive stars that have undergone supernova explosions."},
            {"question": "What is the Chandrasekhar limit?", "options": ["Speed of light", "Maximum white dwarf mass", "Galaxy size limit", "Black hole boundary"], "correct": 1, "explanation": "The Chandrasekhar limit (~1.4 solar masses) is the maximum mass a white dwarf can have before collapsing."},
            {"question": "What causes gravitational lensing?", "options": ["Glass in space", "Curved spacetime", "Magnetic fields", "Dust clouds"], "correct": 1, "explanation": "Massive objects curve spacetime, bending light paths and creating gravitational lensing effects."},
            {"question": "What is the Hubble constant?", "options": ["Light speed", "Universe expansion rate", "Star formation rate", "Galaxy rotation speed"], "correct": 1, "explanation": "The Hubble constant measures how fast the universe is expanding, about 70 km/s/Mpc."}
        ]
    
    # Try to select questions that haven't been used recently
    available_questions = []
    for q in all_easy_questions:
        is_recently_used = False
        for used_q in used_questions[-10:]:  # Check last 10 questions
            if q['question'].lower() in used_q.lower() or used_q.lower() in q['question'].lower():
                is_recently_used = True
                break
        if not is_recently_used:
            available_questions.append(q)
    
    # If we don't have enough unused questions, use all questions
    if len(available_questions) < count:
        available_questions = all_easy_questions
    
    # Randomly select questions
    selected = random.sample(available_questions, min(count, len(available_questions)))
    
    # Track these questions too
    if 'used_questions' not in session:
        session['used_questions'] = []
    for q in selected:
        session['used_questions'].append(q['question'])
    
    print(f"🔄 Using {len(selected)} fallback questions (tried to avoid recent repeats)")
    return selected



def check_answer_with_ai(question, user_answer, correct_answer, explanation):
    """Use Gemini to provide personalized feedback on answers"""
    is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
    
    if is_correct:
        prompt = f"""
        The user answered the astronomy question correctly: "{question}"
        Their answer: "{user_answer}" (which is correct)
        
        Generate an encouraging response (1-2 sentences) that:
        - Congratulates them enthusiastically
        - Adds one interesting space fact related to their answer
        - Keeps it fun and engaging
        """
    else:
        prompt = f"""
        The user answered this astronomy question incorrectly: "{question}"
        Their answer: "{user_answer}"
        Correct answer: "{correct_answer}"
        Explanation: "{explanation}"
        
        Generate a supportive response (1-2 sentences) that:
        - Gently corrects them without being discouraging
        - Provides the correct answer with a brief interesting fact
        - Encourages them to keep learning
        """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating AI feedback: {e}")
        if is_correct:
            return f"Excellent! {explanation}"
        else:
            return f"Not quite right. The correct answer is {correct_answer}. {explanation}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    level = data.get('level')
    
    print(f"Starting game at {level} level...")
    
    # Generate questions using AI
    questions = generate_questions(level)
    
    print(f"Generated {len(questions)} questions for {level} level")
    for i, q in enumerate(questions):
        print(f"Q{i+1}: {q.get('question', 'No question')}")
    
    session['level'] = level
    session['score'] = 0
    session['current_question'] = 0
    session['attempts'] = 0
    session['questions'] = questions
    
    return jsonify({'success': True})

@app.route('/get_question')
def get_question():
    if 'current_question' not in session:
        return jsonify({'error': 'Game not started'})
    
    current_q = session['current_question']
    questions = session['questions']
    
    if current_q >= len(questions):
        return jsonify({'game_over': True, 'score': session['score'], 'total': len(questions)})
    
    question = questions[current_q]
    return jsonify({
        'question': question.get('question', question.get('q', '')),
        'options': question['options'],
        'question_number': current_q + 1,
        'total_questions': len(questions),
        'score': session['score'],
        'level': session['level']
    })

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    answer_index = data.get('answer')
    
    current_q = session['current_question']
    questions = session['questions']
    question_data = questions[current_q]
    correct_index = question_data['correct']
    
    user_answer = question_data['options'][answer_index]
    correct_answer = question_data['options'][correct_index]
    explanation = question_data.get('explanation', '')
    
    is_correct = answer_index == correct_index
    
    # Generate AI feedback
    ai_feedback = check_answer_with_ai(
        question_data.get('question', question_data.get('q', '')),
        user_answer,
        correct_answer,
        explanation
    )
    
    if is_correct:
        session['score'] += 1
        session['current_question'] += 1
        session['attempts'] = 0
        return jsonify({
            'correct': True,
            'message': ai_feedback,
            'score': session['score']
        })
    else:
        session['attempts'] += 1
        max_attempts = 3 if current_q == 4 else 2  # Last question gets 3 attempts
        
        if session['attempts'] >= max_attempts:
            session['current_question'] += 1
            session['attempts'] = 0
            return jsonify({
                'correct': False,
                'message': ai_feedback,
                'score': session['score'],
                'attempts_exhausted': True
            })
        else:
            return jsonify({
                'correct': False,
                'message': f"Not quite right! Try again. ({session['attempts']}/{max_attempts} attempts)",
                'score': session['score'],
                'attempts_remaining': max_attempts - session['attempts']
            })

@app.route('/reset_game')
def reset_game():
    session.clear()
    print("🔄 Game session reset - all data cleared")
    return jsonify({'success': True})

@app.route('/reset_questions')
def reset_questions():
    """Reset question history to allow for fresh questions"""
    if 'used_questions' in session:
        old_count = len(session['used_questions'])
        session['used_questions'] = []
        print(f"🔄 Question history reset - cleared {old_count} previously asked questions")
        return jsonify({'success': True, 'message': f'Question history cleared! {old_count} questions removed from memory.'})
    else:
        print("🔄 No question history to reset")
        return jsonify({'success': True, 'message': 'No question history found.'})

@app.route('/question_stats')
def question_stats():
    """Get statistics about questions asked"""
    used_questions = session.get('used_questions', [])
    return jsonify({
        'total_questions_asked': len(used_questions),
        'recent_questions': used_questions[-5:] if used_questions else [],
        'session_active': 'level' in session
    })

if __name__ == '__main__':
    app.run(debug=True)
