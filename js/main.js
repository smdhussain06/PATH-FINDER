// Main JavaScript for PATH-FINDER
// Global state management
const PathFinder = {
    currentUser: null,
    currentStep: 'landing',
    assessmentData: {
        psychometric: {},
        ikigai: {},
        preferences: {}
    },
    
    init() {
        this.loadUserData();
        this.initEventListeners();
        this.checkRoute();
    },

    // Load user data from localStorage
    loadUserData() {
        const saved = localStorage.getItem('pathfinder_data');
        if (saved) {
            const data = JSON.parse(saved);
            this.currentUser = data.currentUser;
            this.assessmentData = data.assessmentData || this.assessmentData;
        }
    },

    // Save user data to localStorage
    saveUserData() {
        const data = {
            currentUser: this.currentUser,
            assessmentData: this.assessmentData,
            timestamp: Date.now()
        };
        localStorage.setItem('pathfinder_data', JSON.stringify(data));
    },

    // Initialize event listeners
    initEventListeners() {
        // Navigation menu toggle for mobile
        const navToggle = document.querySelector('.nav-toggle');
        const navMenu = document.querySelector('.nav-menu');
        
        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                navToggle.classList.toggle('active');
            });
        }

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Close modal when clicking outside
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal(e.target.id);
            }
        });

        // Escape key to close modals
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const activeModal = document.querySelector('.modal.active');
                if (activeModal) {
                    this.closeModal(activeModal.id);
                }
            }
        });
    },

    // Check current route and initialize appropriate page
    checkRoute() {
        const path = window.location.pathname;
        if (path.includes('psychometric')) {
            this.currentStep = 'psychometric';
        } else if (path.includes('ikigai')) {
            this.currentStep = 'ikigai';
        } else if (path.includes('jobmarket')) {
            this.currentStep = 'jobmarket';
        } else if (path.includes('roadmap')) {
            this.currentStep = 'roadmap';
        }
    },

    // Open modal
    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    },

    // Close modal
    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    },

    // Set user type and redirect to assessment
    selectUserType(userType) {
        this.currentUser = {
            type: userType,
            startTime: Date.now(),
            progress: 0
        };
        this.saveUserData();
        this.closeModal('userTypeModal');
        
        // Redirect to psychometric test
        window.location.href = 'pages/psychometric.html';
    },

    // Navigate to specific section
    navigateToSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    },

    // Update progress across the platform
    updateProgress(step, data) {
        if (!this.currentUser) return;
        
        this.assessmentData[step] = { ...this.assessmentData[step], ...data };
        
        // Calculate overall progress
        const steps = ['psychometric', 'ikigai', 'jobmarket', 'roadmap'];
        const completed = steps.filter(s => 
            this.assessmentData[s] && Object.keys(this.assessmentData[s]).length > 0
        ).length;
        
        this.currentUser.progress = Math.round((completed / steps.length) * 100);
        this.saveUserData();
        
        // Update UI if progress indicator exists
        this.updateProgressUI();
    },

    // Update progress UI elements
    updateProgressUI() {
        const progressBar = document.querySelector('.progress-bar');
        const progressText = document.querySelector('.progress-text');
        
        if (progressBar && this.currentUser) {
            progressBar.style.width = `${this.currentUser.progress}%`;
        }
        
        if (progressText && this.currentUser) {
            progressText.textContent = `${this.currentUser.progress}% Complete`;
        }
    },

    // Generate career recommendations based on assessments
    generateRecommendations() {
        if (!this.assessmentData.psychometric || !this.assessmentData.ikigai) {
            return [];
        }

        // This would typically involve complex algorithms
        // For now, we'll use a simplified matching system
        const recommendations = [];
        
        // Add logic to match user profile with careers
        // This would be implemented with the career data
        
        return recommendations;
    },

    // Export user data as JSON
    exportData() {
        const data = {
            user: this.currentUser,
            assessments: this.assessmentData,
            recommendations: this.generateRecommendations(),
            exportDate: new Date().toISOString()
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], {
            type: 'application/json'
        });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `pathfinder-results-${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    },

    // Reset all data
    resetData() {
        if (confirm('Are you sure you want to reset all your data? This action cannot be undone.')) {
            localStorage.removeItem('pathfinder_data');
            this.currentUser = null;
            this.assessmentData = {
                psychometric: {},
                ikigai: {},
                preferences: {}
            };
            window.location.href = '/';
        }
    }
};

// Global functions for HTML onclick handlers
function openUserTypeModal() {
    PathFinder.openModal('userTypeModal');
}

function closeUserTypeModal() {
    PathFinder.closeModal('userTypeModal');
}

function selectUserType(userType) {
    PathFinder.selectUserType(userType);
}

function scrollToSection(sectionId) {
    PathFinder.navigateToSection(sectionId);
}

function exportResults() {
    PathFinder.exportData();
}

function resetAllData() {
    PathFinder.resetData();
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    PathFinder.init();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
        PathFinder.saveUserData();
    }
});

// Auto-save data before page unload
window.addEventListener('beforeunload', () => {
    PathFinder.saveUserData();
});
