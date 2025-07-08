# Astroventure Project Overview

## Folder Structure

- `Astroverse.py.txt`: Original text-based Python quiz game
- `Astroverse_gui.py`: Tkinter-based GUI version of the game
- `app.py`: Modern Flask web application (main game)
- `templates/index.html`: Main HTML template for the web version
- `static/style.css`: Modern CSS with animations and space theme
- `static/script.js`: Interactive JavaScript for game functionality
- `requirements.txt`: Python dependencies for the web version
- `README.md`: Instructions and description of the game

## Game Description

Astroventure is a cutting-edge, AI-powered space-themed quiz game that generates dynamic questions using Google's Gemini AI. It features an immersive cosmic environment with animated planets, stars, and comets, creating a truly modern gaming experience.

### Game Features

- **AI-Powered Questions**: Gemini AI generates unique, personalized questions for each game session
- **Intelligent Feedback**: AI provides contextual, encouraging responses to both correct and incorrect answers
- **Immersive Space Environment**: 
  - Animated starfield with twinkling effects
  - Moving planets with realistic orbits
  - Comet trails across the screen
  - Deep space black background
- **Three Difficulty Levels**: 
  - 🌟 **ROOKIE** (Easy): Basic astronomy questions suitable for beginners
  - ☄️ **EXPLORER** (Medium): Intermediate space knowledge and missions
  - 🛰️ **COMMANDER** (Hard): Advanced astrophysics and cosmology concepts
- **Modern UI/UX**: 
  - Glassmorphism design with blur effects
  - Smooth animations and transitions
  - Responsive design for all devices
  - Loading screens with AI-themed animations
- **Interactive Elements**: Hover effects, sound feedback, and visual responses
- **Achievement System**: AI-generated personalized congratulations based on performance

## How to Run the AI-Powered Web Version

1. **Install Python** (3.7 or higher)

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**:
   - The `.env` file contains your Gemini API key
   - Make sure the key is valid and has proper permissions

4. **Run the Flask Application**:
   ```bash
   python app.py
   ```

5. **Open Your Browser** and go to:
   ```
   http://localhost:5000
   ```

### First Time Setup
- Questions are generated dynamically by Gemini AI
- If AI generation fails, the app falls back to curated questions
- Loading screen appears while AI generates questions (2-3 seconds)

## How to Run Other Versions

### GUI Version (Tkinter):
```bash
python Astroverse_gui.py
```

### Original Text Version:
1. Rename `Astroverse.py.txt` to `Astroverse.py`
2. Run: `python Astroverse.py`

## Technical Features

- **Google Gemini AI Integration**: Dynamic question generation and intelligent feedback
- **Flask Backend**: RESTful API endpoints with AI-powered game logic
- **Environment Variables**: Secure API key management with python-dotenv
- **Session Management**: Tracks game state across requests
- **Advanced CSS3**: 
  - Animated planets with orbital mechanics
  - Particle systems for stars and comets
  - Glassmorphism effects with backdrop blur
  - Gradient animations and glow effects
- **Responsive Design**: Mobile-friendly interface with touch support
- **Sound Effects**: Generated audio feedback for interactions
- **Error Handling**: Graceful fallbacks when AI services are unavailable
- **Loading States**: Smooth transitions with AI-themed loading animations

## Game Mechanics

- **5 Questions per Level**: Each difficulty has unique questions
- **Multiple Attempts**: 2 attempts per question (3 for the final "trick" question)
- **Real-time Scoring**: Score updates instantly with visual feedback
- **Achievement Levels**: Different congratulatory messages based on performance
- **Replay System**: Easy navigation between games and difficulty levels

---
For more details, see