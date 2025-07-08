let currentScreen = 'main-menu';

// Screen management
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
    currentScreen = screenId;
}

// Start game with selected level
async function startGame(level) {
    showScreen('loading-screen');
    
    try {
        const response = await fetch('/start_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ level: level })
        });
        
        if (response.ok) {
            // Add a minimum loading time for better UX
            setTimeout(() => {
                showScreen('game-screen');
                loadQuestion();
            }, 2000);
        } else {
            showError('Failed to start game. Please try again.');
        }
    } catch (error) {
        console.error('Error starting game:', error);
        showError('Connection error. Please check your internet and try again.');
    }
}

// Load current question
async function loadQuestion() {
    try {
        const response = await fetch('/get_question');
        const data = await response.json();
        
        if (data.game_over) {
            showResults(data.score, data.total);
            return;
        }
        
        // Update game header
        document.getElementById('score').textContent = data.score;
        document.getElementById('current-level').textContent = data.level.toUpperCase();
        document.getElementById('question-progress').textContent = `${data.question_number}/${data.total_questions}`;
        
        // Update question
        document.getElementById('question-number').textContent = `Question ${data.question_number}`;
        document.getElementById('question').textContent = data.question;
        
        // Create options
        const optionsContainer = document.getElementById('options-container');
        optionsContainer.innerHTML = '';
        
        data.options.forEach((option, index) => {
            const button = document.createElement('button');
            button.className = 'option-btn';
            button.textContent = option;
            button.onclick = () => selectAnswer(index, button);
            optionsContainer.appendChild(button);
        });
        
        // Clear feedback
        document.getElementById('feedback').textContent = '';
        document.getElementById('feedback').className = 'feedback';
        
    } catch (error) {
        console.error('Error loading question:', error);
    }
}

// Handle answer selection
async function selectAnswer(answerIndex, buttonElement) {
    // Disable all option buttons
    const optionButtons = document.querySelectorAll('.option-btn');
    optionButtons.forEach(btn => {
        btn.disabled = true;
        btn.style.cursor = 'not-allowed';
    });
    
    try {
        const response = await fetch('/submit_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answer: answerIndex })
        });
        
        const data = await response.json();
        
        // Update feedback with AI styling
        displayAIResponse(data.message, data.correct);
        
        // Update score
        document.getElementById('score').textContent = data.score;
        
        // Visual feedback on buttons
        if (data.correct) {
            buttonElement.classList.add('correct');
            playSuccessSound();
            setTimeout(() => {
                loadQuestion();
            }, 1500);
        } else {
            buttonElement.classList.add('incorrect');
            playErrorSound();
            
            if (data.attempts_exhausted) {
                setTimeout(() => {
                    loadQuestion();
                }, 2500);
            } else {
                // Re-enable buttons for another attempt
                setTimeout(() => {
                    optionButtons.forEach(btn => {
                        btn.disabled = false;
                        btn.style.cursor = 'pointer';
                        btn.classList.remove('incorrect');
                    });
                }, 1500);
            }
        }
        
    } catch (error) {
        console.error('Error submitting answer:', error);
    }
}

// Show results screen
function showResults(score, total) {
    showScreen('results-screen');
    
    // Calculate percentage
    const percentage = Math.round((score / total) * 100);
    
    // Update basic score info
    document.getElementById('final-score').textContent = score;
    document.getElementById('total-questions').textContent = total;
    document.getElementById('score-percentage').textContent = `${percentage}%`;
    
    // Determine achievement level and customize appearance
    const achievementIcon = document.getElementById('achievement-icon');
    const achievementTitle = document.getElementById('achievement-title');
    const achievementText = document.getElementById('achievement-text');
    const missionStatus = document.getElementById('mission-status');
    const trophyIcon = document.getElementById('trophy-icon');
    const missionRank = document.getElementById('mission-rank');
    
    // Play celebration sound
    playCelebrationSound(score, total);
    
    if (score === total) {
        achievementIcon.innerHTML = '🏆';
        achievementTitle.textContent = 'Cosmic Champion!';
        achievementText.textContent = 'Perfect Score! You are a true master of the universe! Every question answered correctly with stellar precision!';
        missionStatus.textContent = 'MISSION PERFECTION!';
        trophyIcon.className = 'fas fa-crown';
        trophyIcon.style.color = '#ffd700';
        missionRank.textContent = 'Commander';
        
        // Add extra sparkle effects for perfect score
        addSparkleEffect();
        
    } else if (score >= total - 1) {
        achievementIcon.innerHTML = '🥇';
        achievementTitle.textContent = 'Space Ace!';
        achievementText.textContent = 'Outstanding performance! You\'re almost a cosmic champion! Your knowledge of the universe shines bright!';
        missionStatus.textContent = 'MISSION SUCCESS!';
        trophyIcon.className = 'fas fa-medal';
        trophyIcon.style.color = '#ffd93d';
        missionRank.textContent = 'Captain';
        
    } else if (score >= Math.floor(total / 2)) {
        achievementIcon.innerHTML = '🥈';
        achievementTitle.textContent = 'Star Explorer!';
        achievementText.textContent = 'Great work! Your space knowledge is developing well. Keep exploring the cosmic mysteries!';
        missionStatus.textContent = 'MISSION COMPLETE!';
        trophyIcon.className = 'fas fa-trophy';
        trophyIcon.style.color = '#c0c0c0';
        missionRank.textContent = 'Lieutenant';
        
    } else {
        achievementIcon.innerHTML = '🌟';
        achievementTitle.textContent = 'Cosmic Cadet!';
        achievementText.textContent = 'Every space journey begins with curiosity! Keep learning and reach for the stars!';
        missionStatus.textContent = 'MISSION STARTED!';
        trophyIcon.className = 'fas fa-rocket';
        trophyIcon.style.color = '#64ffda';
        missionRank.textContent = 'Cadet';
    }
    
    // Update fun stats
    updateFunStats(score, total);
    
    // Animate score circle based on percentage
    animateScoreCircle(percentage);
    
    // Trigger confetti for good scores
    if (percentage >= 60) {
        setTimeout(triggerConfetti, 1000);
    }
}

// Navigation functions
function playAgain() {
    resetGame();
    showScreen('main-menu');
}

function backToMenu() {
    resetGame();
    showScreen('main-menu');
}

// Reset game state
async function resetGame() {
    try {
        await fetch('/reset_game');
    } catch (error) {
        console.error('Error resetting game:', error);
    }
}

// Sound effects (simple beep sounds)
function playSuccessSound() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(1200, audioContext.currentTime + 0.1);
    
    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.3);
}

function playErrorSound() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.setValueAtTime(400, audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(200, audioContext.currentTime + 0.1);
    
    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.3);
}

// Error handling
function showError(message) {
    showScreen('main-menu');
    alert(message);
}

// Enhanced visual effects for AI responses
function displayAIResponse(message, isCorrect) {
    const feedback = document.getElementById('feedback');
    feedback.innerHTML = `
        <div class="ai-response ${isCorrect ? 'correct' : 'incorrect'}">
            <i class="fas fa-robot"></i>
            <span>${message}</span>
        </div>
    `;
}

// Add sparkle effect for perfect scores
function addSparkleEffect() {
    const resultsContent = document.querySelector('.results-content');
    const sparkles = document.createElement('div');
    sparkles.className = 'sparkle-overlay';
    sparkles.innerHTML = '✨ 🌟 ⭐ 💫 🌠 ✨ 🌟 ⭐ 💫 🌠';
    sparkles.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        font-size: 1.5rem;
        animation: sparkle-dance 3s infinite;
        z-index: 10;
    `;
    resultsContent.appendChild(sparkles);
    
    const style = document.createElement('style');
    style.textContent = `
        @keyframes sparkle-dance {
            0%, 100% { transform: rotate(0deg) scale(1); opacity: 0.7; }
            25% { transform: rotate(90deg) scale(1.2); opacity: 1; }
            50% { transform: rotate(180deg) scale(0.8); opacity: 0.5; }
            75% { transform: rotate(270deg) scale(1.1); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
}

// Update fun stats
function updateFunStats(score, total) {
    // Simulate time taken (you could track real time if needed)
    const timeMinutes = Math.floor(Math.random() * 3) + 2;
    const timeSeconds = Math.floor(Math.random() * 60);
    document.getElementById('time-taken').textContent = `${timeMinutes}:${timeSeconds.toString().padStart(2, '0')}`;
    
    // Knowledge points based on score
    const knowledgePoints = score * 10 + Math.floor(Math.random() * 5);
    document.getElementById('knowledge-gained').textContent = `+${knowledgePoints}`;
}

// Animate the score circle
function animateScoreCircle(percentage) {
    const circle = document.querySelector('.score-circle');
    circle.style.background = `conic-gradient(from 0deg, #64ffda 0deg, #64ffda ${percentage * 3.6}deg, rgba(255,255,255,0.1) ${percentage * 3.6}deg)`;
}

// Trigger confetti animation
function triggerConfetti() {
    const confetti = document.createElement('div');
    confetti.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1000;
    `;
    
    for (let i = 0; i < 50; i++) {
        const piece = document.createElement('div');
        piece.style.cssText = `
            position: absolute;
            width: 10px;
            height: 10px;
            background: ${['#ff6b9d', '#64ffda', '#ffd93d', '#8b5cf6', '#10b981'][Math.floor(Math.random() * 5)]};
            left: ${Math.random() * 100}%;
            animation: confetti-fall ${Math.random() * 3 + 2}s linear forwards;
            transform: rotate(${Math.random() * 360}deg);
        `;
        confetti.appendChild(piece);
    }
    
    document.body.appendChild(confetti);
    
    const style = document.createElement('style');
    style.textContent = `
        @keyframes confetti-fall {
            0% {
                transform: translateY(-100vh) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(100vh) rotate(720deg);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    setTimeout(() => {
        document.body.removeChild(confetti);
    }, 5000);
}

// Enhanced celebration sounds
function playCelebrationSound(score, total) {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const percentage = (score / total) * 100;
    
    if (percentage === 100) {
        // Perfect score - triumphant fanfare
        playTrumpetFanfare(audioContext);
    } else if (percentage >= 80) {
        // Great score - success melody
        playSuccessMelody(audioContext);
    } else if (percentage >= 60) {
        // Good score - encouraging chime
        playEncouragingChime(audioContext);
    } else {
        // Keep trying - gentle positive tone
        playPositiveTone(audioContext);
    }
}

function playTrumpetFanfare(audioContext) {
    const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
    notes.forEach((freq, index) => {
        setTimeout(() => {
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(freq, audioContext.currentTime);
            oscillator.type = 'square';
            
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        }, index * 200);
    });
}

function playSuccessMelody(audioContext) {
    const notes = [440, 523.25, 659.25]; // A4, C5, E5
    notes.forEach((freq, index) => {
        setTimeout(() => {
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(freq, audioContext.currentTime);
            oscillator.type = 'sine';
            
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.3);
        }, index * 150);
    });
}

function playEncouragingChime(audioContext) {
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.setValueAtTime(659.25, audioContext.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(1318.51, audioContext.currentTime + 0.2);
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.4);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.4);
}

function playPositiveTone(audioContext) {
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.setValueAtTime(523.25, audioContext.currentTime);
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.08, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.6);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.6);
}

// Share achievement function
function shareAchievement() {
    const score = document.getElementById('final-score').textContent;
    const total = document.getElementById('total-questions').textContent;
    const level = document.getElementById('current-level').textContent;
    const rank = document.getElementById('mission-rank').textContent;
    
    const shareText = `🚀 Just completed an Astroventure mission! 🌟\n` +
                     `Score: ${score}/${total} as a ${rank} on ${level} level!\n` +
                     `#Astroventure #SpaceQuiz #CosmicKnowledge`;
    
    if (navigator.share) {
        navigator.share({
            title: 'Astroventure Achievement',
            text: shareText,
            url: window.location.href
        });
    } else {
        // Fallback - copy to clipboard
        navigator.clipboard.writeText(shareText).then(() => {
            alert('Achievement copied to clipboard! Share it on your favorite social platform! 🚀');
        });
    }
}

// Reset questions functionality
async function resetQuestions() {
    if (confirm('This will clear all question history and allow you to see questions you\'ve seen before. Continue?')) {
        try {
            const response = await fetch('/reset_questions');
            const data = await response.json();
            
            if (data.success) {
                showNotification(`✅ ${data.message}`, 'success');
                
                // Update stats display if it's open
                if (document.getElementById('stats-display').style.display !== 'none') {
                    showQuestionStats();
                }
            }
        } catch (error) {
            console.error('Error resetting questions:', error);
            showNotification('❌ Error resetting questions. Please try again.', 'error');
        }
    }
}

// Show question statistics
async function showQuestionStats() {
    try {
        const response = await fetch('/question_stats');
        const data = await response.json();
        
        const statsContent = document.getElementById('stats-content');
        const statsDisplay = document.getElementById('stats-display');
        
        statsContent.innerHTML = `
            <div style="color: #fff; line-height: 1.6;">
                <p><strong>Total Questions Asked:</strong> ${data.total_questions_asked}</p>
                <p><strong>Session Active:</strong> ${data.session_active ? 'Yes' : 'No'}</p>
                ${data.recent_questions.length > 0 ? `
                    <p><strong>Recent Questions:</strong></p>
                    <ul style="margin-left: 20px; font-size: 0.9rem; opacity: 0.8;">
                        ${data.recent_questions.map(q => `<li>${q.length > 60 ? q.substring(0, 60) + '...' : q}</li>`).join('')}
                    </ul>
                ` : '<p><em>No questions asked yet.</em></p>'}
                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.3); text-align: center;">
                    <button class="control-btn reset" onclick="resetQuestions()" style="font-size: 0.8rem; padding: 8px 15px;">
                        <i class="fas fa-refresh"></i>
                        Clear Question History
                    </button>
                </div>
            </div>
        `;
        
        statsDisplay.style.display = 'block';
    } catch (error) {
        console.error('Error fetching stats:', error);
        showNotification('❌ Error loading stats. Please try again.', 'error');
    }
}

// Hide question statistics
function hideQuestionStats() {
    document.getElementById('stats-display').style.display = 'none';
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'rgba(76, 175, 80, 0.9)' : 'rgba(244, 67, 54, 0.9)'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        z-index: 10000;
        border: 2px solid ${type === 'success' ? '#4caf50' : '#f44336'};
        font-family: 'Exo 2', sans-serif;
        font-size: 0.9rem;
        max-width: 300px;
        animation: slideInRight 0.3s ease, fadeOut 0.3s ease 3s forwards;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3.5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3500);
}

// Add CSS for notification animations
if (!document.getElementById('notification-styles')) {
    const style = document.createElement('style');
    style.id = 'notification-styles';
    style.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}

// Initialize the game
document.addEventListener('DOMContentLoaded', function() {
    showScreen('main-menu');
    
    // Load initial stats to show if there's existing data
    fetch('/question_stats')
        .then(response => response.json())
        .then(data => {
            if (data.total_questions_asked > 0) {
                console.log(`📊 Found ${data.total_questions_asked} previously asked questions in session`);
            }
        })
        .catch(error => console.log('Stats not available yet'));
    
    // Add some interactive elements
    document.addEventListener('mousemove', function(e) {
        const stars = document.querySelector('.stars');
        const twinkling = document.querySelector('.twinkling');
        
        if (stars && twinkling) {
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            stars.style.transform = `translate(${x * 10}px, ${y * 10}px) rotate(-45deg)`;
            twinkling.style.transform = `translate(${x * 5}px, ${y * 5}px)`;
        }
    });
});
