# 🚀 Astroventure - AI-Powered Space Quiz Adventure

> An immersive, AI-driven astronomy quiz game that generates unique questions every time you play!

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini%20AI-Powered-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

### 🤖 **AI-Powered Question Generation**
- **Gemini AI Integration**: Every question is dynamically generated using Google's Gemini AI
- **Truly Unique Questions**: No two game sessions will have the same questions
- **Smart Question Tracking**: Prevents repetition across sessions
- **Adaptive Difficulty**: AI tailors questions to your selected skill level

### 🎮 **Immersive Gaming Experience**
- **3 Difficulty Levels**: Rookie (Easy), Explorer (Medium), Commander (Hard)
- **Animated Space Environment**: Moving planets, comets, and twinkling stars
- **Celebration System**: Fireworks, confetti, and animated rewards
- **Interactive Feedback**: AI-generated personalized responses to your answers
- **Sound Effects**: Engaging audio feedback for correct/incorrect answers

### 🎨 **Modern Web Interface**
- **Glassmorphism Design**: Beautiful translucent UI elements
- **Responsive Layout**: Works perfectly on desktop and mobile
- **Smooth Animations**: CSS animations and transitions throughout
- **Space Theme**: Immersive cosmic visuals and typography

### 📊 **Advanced Features**
- **Question Statistics**: Track how many questions you've seen
- **Session Management**: Reset question history for fresh experiences
- **Achievement System**: Earn cosmic badges and ranks
- **Share Achievements**: Share your space exploration success
- **Multiple Attempts**: Get 2-3 chances per question

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.8+**
- **Google Gemini API Key** (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/astroventure-quiz.git
   cd astroventure-quiz
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   **How to get your Gemini API Key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key (it's free!)
   - Copy the key to your `.env` file

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Open Your Browser**
   
   Navigate to `http://127.0.0.1:5000` and start your cosmic adventure! 🌌

## 🎯 How to Play

### Game Flow
1. **Choose Your Mission**: Select from Rookie, Explorer, or Commander difficulty
2. **AI Question Generation**: Gemini AI creates unique questions just for you
3. **Answer Challenges**: Tackle 5 astronomy questions with multiple attempts
4. **Get AI Feedback**: Receive personalized explanations for each answer
5. **Celebrate Success**: Enjoy animated rewards and share your achievements

### Difficulty Levels

| Level | Description | Topics |
|-------|-------------|---------|
| 🌟 **Rookie** | Perfect for beginners | Solar system basics, planets, stars, basic space facts |
| ☄️ **Explorer** | Intermediate challenges | Space missions, satellites, galaxies, space technology |
| 🛰️ **Commander** | Expert-level questions | Black holes, astrophysics, cosmology, advanced concepts |

### Scoring System
- **Correct Answer**: +1 point
- **Multiple Attempts**: 2-3 chances per question
- **Final Score**: X/5 with percentage and cosmic rank
- **Achievements**: Unlock space-themed badges and titles

## 🔧 Technical Architecture

### Backend (`app.py`)
- **Flask Web Framework**: Handles routing and session management
- **Gemini AI Integration**: Dynamic question generation with fallback systems
- **Question Uniqueness**: Tracks and prevents question repetition
- **Smart Fallbacks**: Multiple layers of question generation for reliability

### Frontend
- **`templates/index.html`**: Main game interface with modern HTML5
- **`static/style.css`**: Advanced CSS with animations and glassmorphism
- **`static/script.js`**: Interactive game logic and UI management

### Key Features
```python
# AI-Powered Question Generation
generate_questions(level, count=5)  # Creates unique questions per session
generate_alternative_questions()    # Backup generation method
create_minimal_questions()          # Fallback questions if AI fails

# Question Tracking
session['used_questions']           # Prevents repetition
reset_questions()                   # Clears question history
question_stats()                    # Shows usage statistics
```

## 🚀 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main game interface |
| `/start_game` | POST | Initialize new game session |
| `/get_question` | GET | Fetch current question |
| `/submit_answer` | POST | Submit answer and get AI feedback |
| `/reset_game` | GET | Clear entire game session |
| `/reset_questions` | GET | Clear question history only |
| `/question_stats` | GET | Get question usage statistics |

## 🔒 Environment Variables

Create a `.env` file with:

```env
# Required: Your Google Gemini API Key
GEMINI_API_KEY=your_api_key_here

# Optional: Flask configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

## 📱 Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🐛 Troubleshooting

### Common Issues

**"Questions are repeating"**
- Use the "Reset Questions" button in the main menu
- Check if your Gemini API key is working properly

**"AI questions not generating"**
- Verify your `.env` file contains a valid Gemini API key
- Check your internet connection
- The app will use fallback questions if AI fails

**"Game won't start"**
- Ensure Python 3.8+ is installed
- Install all requirements: `pip install -r requirements.txt`
- Check that Flask is running on port 5000

### Debug Mode
Run with debug output:
```bash
FLASK_DEBUG=True python app.py
```

## 📦 Project Structure

```
astroventure-quiz/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── README.md             # This file
├── PROJECT_OVERVIEW.md   # Detailed project documentation
├── templates/
│   └── index.html        # Main game interface
├── static/
│   ├── style.css         # Game styling and animations
│   └── script.js         # Frontend game logic
└── legacy/
    ├── Astroverse.py.txt # Original text-based version
    └── Astroverse_gui.py # Original GUI version
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Areas for Contribution
- 🎨 New visual effects and animations
- 🤖 Enhanced AI prompts for better questions
- 🌍 Internationalization and multiple languages
- 📱 Mobile app version
- 🎵 Sound effects and background music
- 🏆 More achievement types and leaderboards

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for powering the dynamic question generation
- **Font Awesome** for the beautiful space-themed icons
- **Google Fonts** for the Orbitron and Exo 2 typefaces
- **Flask Community** for the excellent web framework
- **Astronomy Community** for inspiring this educational tool

## 🌟 Star History

If you find this project helpful, please consider giving it a star! ⭐

---

<div align="center">

**🚀 Ready to explore the cosmos? Start your Astroventure today! 🌌**

[🎮 Play Now](http://127.0.0.1:5000) | [📝 Report Issues](https://github.com/yourusername/astroventure-quiz/issues) | [💡 Suggest Features](https://github.com/yourusername/astroventure-quiz/discussions)

Made with ❤️ and lots of ☕ for space enthusiasts everywhere

</div>


