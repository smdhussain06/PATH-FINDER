// Psychometric Assessment JavaScript
class PsychometricAssessment {
    constructor() {
        this.questions = psychometricQuestions || [];
        this.currentQuestionIndex = 0;
        this.answers = {};
        this.results = {};
        this.startTime = null;
        
        this.init();
    }

    init() {
        this.loadPreviousAnswers();
        this.setupEventListeners();
        this.updateProgressBar();
    }

    setupEventListeners() {
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.previousQuestion();
            if (e.key === 'ArrowRight') this.nextQuestion();
            if (e.key >= '1' && e.key <= '5') {
                this.selectOption(parseInt(e.key) - 1);
            }
        });
    }

    loadPreviousAnswers() {
        const saved = localStorage.getItem('pathfinder_psychometric');
        if (saved) {
            const data = JSON.parse(saved);
            this.answers = data.answers || {};
            this.currentQuestionIndex = data.currentIndex || 0;
        }
    }

    saveProgress() {
        const data = {
            answers: this.answers,
            currentIndex: this.currentQuestionIndex,
            timestamp: Date.now()
        };
        localStorage.setItem('pathfinder_psychometric', JSON.stringify(data));
    }

    startAssessment() {
        this.startTime = Date.now();
        this.showScreen('questionScreen');
        this.displayQuestion();
    }

    showScreen(screenId) {
        document.querySelectorAll('.assessment-screen').forEach(screen => {
            screen.classList.remove('active');
        });
        document.getElementById(screenId).classList.add('active');
    }

    displayQuestion() {
        const question = this.questions[this.currentQuestionIndex];
        if (!question) return;

        // Update question info
        document.getElementById('currentQuestionNum').textContent = this.currentQuestionIndex + 1;
        document.getElementById('totalQuestions').textContent = this.questions.length;
        document.getElementById('questionText').textContent = question.text;
        document.getElementById('questionCategory').textContent = this.formatCategory(question.category);

        // Create options
        this.createOptions(question);
        
        // Update navigation
        this.updateNavigation();
        
        // Update progress
        this.updateProgressBar();
        
        // Restore previous answer if exists
        if (this.answers[question.id]) {
            this.selectOption(this.answers[question.id] - 1);
        }
    }

    formatCategory(category) {
        const categoryMap = {
            'openness': 'Openness to Experience',
            'conscientiousness': 'Conscientiousness',
            'extraversion': 'Extraversion',
            'agreeableness': 'Agreeableness',
            'neuroticism': 'Emotional Stability',
            'work_style': 'Work Style',
            'values': 'Values & Motivations',
            'skills': 'Skills Assessment'
        };
        return categoryMap[category] || category;
    }

    createOptions(question) {
        const container = document.getElementById('optionsContainer');
        container.innerHTML = '';

        question.options.forEach((option, index) => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'option';
            optionDiv.innerHTML = `
                <input type="radio" 
                       id="option${index}" 
                       name="answer" 
                       value="${option.value}"
                       onchange="psychometricTest.selectOption(${index})">
                <label for="option${index}">
                    <span class="option-number">${index + 1}</span>
                    <span class="option-text">${option.text}</span>
                </label>
            `;
            container.appendChild(optionDiv);
        });
    }

    selectOption(optionIndex) {
        const question = this.questions[this.currentQuestionIndex];
        const option = question.options[optionIndex];
        
        // Update answers
        this.answers[question.id] = option.value;
        
        // Update UI
        document.querySelectorAll('.option').forEach((opt, idx) => {
            opt.classList.toggle('selected', idx === optionIndex);
        });
        
        // Check the radio button
        document.getElementById(`option${optionIndex}`).checked = true;
        
        // Enable next button
        document.getElementById('nextBtn').disabled = false;
        
        // Save progress
        this.saveProgress();
        
        // Auto-advance after a short delay (optional)
        setTimeout(() => {
            if (this.currentQuestionIndex < this.questions.length - 1) {
                // Uncomment for auto-advance
                // this.nextQuestion();
            }
        }, 500);
    }

    nextQuestion() {
        if (this.currentQuestionIndex < this.questions.length - 1) {
            this.currentQuestionIndex++;
            this.displayQuestion();
        } else {
            this.completeAssessment();
        }
    }

    previousQuestion() {
        if (this.currentQuestionIndex > 0) {
            this.currentQuestionIndex--;
            this.displayQuestion();
        }
    }

    updateNavigation() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        
        prevBtn.disabled = this.currentQuestionIndex === 0;
        
        const currentQuestion = this.questions[this.currentQuestionIndex];
        const hasAnswer = this.answers[currentQuestion.id];
        nextBtn.disabled = !hasAnswer;
        
        // Update next button text for last question
        if (this.currentQuestionIndex === this.questions.length - 1) {
            nextBtn.innerHTML = '<i class="fas fa-check"></i> Complete Assessment';
        } else {
            nextBtn.innerHTML = 'Next <i class="fas fa-arrow-right"></i>';
        }
    }

    updateProgressBar() {
        const progress = ((this.currentQuestionIndex + 1) / this.questions.length) * 100;
        document.getElementById('progressBar').style.width = `${progress}%`;
        document.getElementById('progressText').textContent = `${Math.round(progress)}% Complete`;
    }

    completeAssessment() {
        this.calculateResults();
        this.displayResults();
        this.showScreen('resultsScreen');
        
        // Save completion time
        const completionTime = Date.now() - this.startTime;
        this.saveResults(completionTime);
    }

    calculateResults() {
        this.results = {
            personality: this.calculatePersonalityScores(),
            workStyle: this.calculateWorkStyleScores(),
            values: this.calculateValuesScores(),
            skills: this.calculateSkillsScores(),
            completionTime: Date.now() - this.startTime,
            completedAt: new Date().toISOString()
        };
    }

    calculatePersonalityScores() {
        const scores = {};
        
        // Big Five personality dimensions
        const dimensions = {
            openness: [1, 7],
            conscientiousness: [3, 8],
            extraversion: [2, 6],
            agreeableness: [5, 9],
            neuroticism: [4, 10]
        };

        for (const [dimension, questionIds] of Object.entries(dimensions)) {
            let total = 0;
            let count = 0;
            
            questionIds.forEach(id => {
                if (this.answers[id]) {
                    total += this.answers[id];
                    count++;
                }
            });
            
            scores[dimension] = count > 0 ? Math.round((total / count) * 20) : 0; // Scale to 0-100
        }
        
        return scores;
    }

    calculateWorkStyleScores() {
        const scores = {};
        const workStyleQuestions = {
            multitasking: [11],
            pace_preference: [12],
            autonomy: [13],
            leadership: [14],
            people_vs_data: [15]
        };

        for (const [style, questionIds] of Object.entries(workStyleQuestions)) {
            let total = 0;
            let count = 0;
            
            questionIds.forEach(id => {
                if (this.answers[id]) {
                    total += this.answers[id];
                    count++;
                }
            });
            
            scores[style] = count > 0 ? Math.round((total / count) * 20) : 0;
        }
        
        return scores;
    }

    calculateValuesScores() {
        const scores = {};
        const valuesQuestions = {
            financial_motivation: [16],
            social_impact: [17],
            work_life_balance: [18],
            security_vs_growth: [19],
            recognition: [20]
        };

        for (const [value, questionIds] of Object.entries(valuesQuestions)) {
            let total = 0;
            let count = 0;
            
            questionIds.forEach(id => {
                if (this.answers[id]) {
                    total += this.answers[id];
                    count++;
                }
            });
            
            scores[value] = count > 0 ? Math.round((total / count) * 20) : 0;
        }
        
        return scores;
    }

    calculateSkillsScores() {
        const scores = {};
        const skillsQuestions = {
            analytical: [21],
            communication: [22],
            time_management: [23],
            technical: [24],
            creativity: [25]
        };

        for (const [skill, questionIds] of Object.entries(skillsQuestions)) {
            let total = 0;
            let count = 0;
            
            questionIds.forEach(id => {
                if (this.answers[id]) {
                    total += this.answers[id];
                    count++;
                }
            });
            
            scores[skill] = count > 0 ? Math.round((total / count) * 20) : 0;
        }
        
        return scores;
    }

    displayResults() {
        this.displayPersonalityResults();
        this.displayWorkStyleResults();
        this.displayValuesResults();
        this.displaySkillsResults();
    }

    displayPersonalityResults() {
        const container = document.getElementById('personalityResults');
        const personality = this.results.personality;
        
        const personalityLabels = {
            openness: { name: 'Openness to Experience', icon: 'fas fa-lightbulb' },
            conscientiousness: { name: 'Conscientiousness', icon: 'fas fa-tasks' },
            extraversion: { name: 'Extraversion', icon: 'fas fa-users' },
            agreeableness: { name: 'Agreeableness', icon: 'fas fa-handshake' },
            neuroticism: { name: 'Emotional Stability', icon: 'fas fa-brain' }
        };

        container.innerHTML = '';
        
        Object.entries(personality).forEach(([trait, score]) => {
            const label = personalityLabels[trait];
            const level = this.getScoreLevel(score);
            
            const resultCard = document.createElement('div');
            resultCard.className = 'result-card';
            resultCard.innerHTML = `
                <div class="result-icon">
                    <i class="${label.icon}"></i>
                </div>
                <h3>${label.name}</h3>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${score}%"></div>
                </div>
                <div class="score-info">
                    <span class="score-value">${score}/100</span>
                    <span class="score-level ${level.toLowerCase()}">${level}</span>
                </div>
            `;
            container.appendChild(resultCard);
        });
    }

    displayWorkStyleResults() {
        const container = document.getElementById('workstyleResults');
        const workStyle = this.results.workStyle;
        
        const workStyleLabels = {
            multitasking: { name: 'Multitasking Preference', icon: 'fas fa-layer-group' },
            pace_preference: { name: 'Fast-Paced Environment', icon: 'fas fa-tachometer-alt' },
            autonomy: { name: 'Independent Work', icon: 'fas fa-user' },
            leadership: { name: 'Leadership Interest', icon: 'fas fa-crown' },
            people_vs_data: { name: 'Data vs People Focus', icon: 'fas fa-chart-bar' }
        };

        container.innerHTML = '';
        
        Object.entries(workStyle).forEach(([style, score]) => {
            const label = workStyleLabels[style];
            const level = this.getScoreLevel(score);
            
            const resultCard = document.createElement('div');
            resultCard.className = 'result-card';
            resultCard.innerHTML = `
                <div class="result-icon">
                    <i class="${label.icon}"></i>
                </div>
                <h3>${label.name}</h3>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${score}%"></div>
                </div>
                <div class="score-info">
                    <span class="score-value">${score}/100</span>
                    <span class="score-level ${level.toLowerCase()}">${level}</span>
                </div>
            `;
            container.appendChild(resultCard);
        });
    }

    displayValuesResults() {
        const container = document.getElementById('valuesResults');
        const values = this.results.values;
        
        const valuesLabels = {
            financial_motivation: { name: 'Financial Motivation', icon: 'fas fa-dollar-sign' },
            social_impact: { name: 'Social Impact', icon: 'fas fa-heart' },
            work_life_balance: { name: 'Work-Life Balance', icon: 'fas fa-balance-scale' },
            security_vs_growth: { name: 'Security Preference', icon: 'fas fa-shield-alt' },
            recognition: { name: 'Recognition Need', icon: 'fas fa-trophy' }
        };

        container.innerHTML = '';
        
        Object.entries(values).forEach(([value, score]) => {
            const label = valuesLabels[value];
            const level = this.getScoreLevel(score);
            
            const resultCard = document.createElement('div');
            resultCard.className = 'result-card';
            resultCard.innerHTML = `
                <div class="result-icon">
                    <i class="${label.icon}"></i>
                </div>
                <h3>${label.name}</h3>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${score}%"></div>
                </div>
                <div class="score-info">
                    <span class="score-value">${score}/100</span>
                    <span class="score-level ${level.toLowerCase()}">${level}</span>
                </div>
            `;
            container.appendChild(resultCard);
        });
    }

    displaySkillsResults() {
        const container = document.getElementById('skillsResults');
        const skills = this.results.skills;
        
        const skillsLabels = {
            analytical: { name: 'Analytical Thinking', icon: 'fas fa-search' },
            communication: { name: 'Communication', icon: 'fas fa-comments' },
            time_management: { name: 'Time Management', icon: 'fas fa-clock' },
            technical: { name: 'Technical Skills', icon: 'fas fa-cogs' },
            creativity: { name: 'Creativity', icon: 'fas fa-palette' }
        };

        container.innerHTML = '';
        
        Object.entries(skills).forEach(([skill, score]) => {
            const label = skillsLabels[skill];
            const level = this.getScoreLevel(score);
            
            const resultCard = document.createElement('div');
            resultCard.className = 'result-card';
            resultCard.innerHTML = `
                <div class="result-icon">
                    <i class="${label.icon}"></i>
                </div>
                <h3>${label.name}</h3>
                <div class="score-bar">
                    <div class="score-fill" style="width: ${score}%"></div>
                </div>
                <div class="score-info">
                    <span class="score-value">${score}/100</span>
                    <span class="score-level ${level.toLowerCase()}">${level}</span>
                </div>
            `;
            container.appendChild(resultCard);
        });
    }

    getScoreLevel(score) {
        if (score >= 80) return 'Very High';
        if (score >= 60) return 'High';
        if (score >= 40) return 'Medium';
        if (score >= 20) return 'Low';
        return 'Very Low';
    }

    saveResults(completionTime) {
        // Save to main PathFinder data structure
        PathFinder.updateProgress('psychometric', this.results);
        
        // Save detailed results separately
        const detailedResults = {
            answers: this.answers,
            results: this.results,
            completionTime: completionTime,
            completedAt: new Date().toISOString()
        };
        
        localStorage.setItem('pathfinder_psychometric_complete', JSON.stringify(detailedResults));
    }

    retakeAssessment() {
        if (confirm('Are you sure you want to retake the assessment? This will clear your current results.')) {
            this.currentQuestionIndex = 0;
            this.answers = {};
            this.results = {};
            localStorage.removeItem('pathfinder_psychometric');
            localStorage.removeItem('pathfinder_psychometric_complete');
            this.showScreen('welcomeScreen');
        }
    }

    proceedToIkigai() {
        window.location.href = 'ikigai.html';
    }
}

// Global functions for HTML event handlers
function startAssessment() {
    psychometricTest.startAssessment();
}

function nextQuestion() {
    psychometricTest.nextQuestion();
}

function previousQuestion() {
    psychometricTest.previousQuestion();
}

function retakeAssessment() {
    psychometricTest.retakeAssessment();
}

function proceedToIkigai() {
    psychometricTest.proceedToIkigai();
}

// Initialize assessment when page loads
let psychometricTest;

document.addEventListener('DOMContentLoaded', () => {
    psychometricTest = new PsychometricAssessment();
});
