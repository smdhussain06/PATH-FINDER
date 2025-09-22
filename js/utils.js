// Utility Functions for PATH-FINDER

// Animation and UI utilities
const Utils = {
    // Smooth scroll to element
    scrollToElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    },

    // Format time duration
    formatDuration(milliseconds) {
        const minutes = Math.floor(milliseconds / 60000);
        const seconds = Math.floor((milliseconds % 60000) / 1000);
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    },

    // Format date
    formatDate(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Generate unique ID
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    },

    // Validate email
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    // Calculate percentage match
    calculateMatch(userProfile, careerRequirements) {
        if (!userProfile || !careerRequirements) return 0;
        
        let totalScore = 0;
        let weightedScore = 0;
        
        // Compare personality traits
        if (userProfile.personality && careerRequirements.personalityMatch) {
            Object.keys(careerRequirements.personalityMatch).forEach(trait => {
                const userScore = userProfile.personality[trait] || 0;
                const requiredLevel = careerRequirements.personalityMatch[trait];
                
                let match = 0;
                if (requiredLevel === 'high' && userScore >= 60) match = 100;
                else if (requiredLevel === 'medium' && userScore >= 40 && userScore < 80) match = 100;
                else if (requiredLevel === 'low' && userScore < 60) match = 100;
                else match = Math.max(0, 100 - Math.abs(userScore - this.getRequiredScore(requiredLevel)));
                
                totalScore += match;
                weightedScore += 100;
            });
        }
        
        return weightedScore > 0 ? Math.round(totalScore / weightedScore * 100) : 0;
    },

    getRequiredScore(level) {
        switch(level) {
            case 'high': return 80;
            case 'medium': return 50;
            case 'low': return 20;
            default: return 50;
        }
    },

    // Local storage helpers
    storage: {
        set(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
                return true;
            } catch (e) {
                console.error('Storage set error:', e);
                return false;
            }
        },

        get(key) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : null;
            } catch (e) {
                console.error('Storage get error:', e);
                return null;
            }
        },

        remove(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (e) {
                console.error('Storage remove error:', e);
                return false;
            }
        },

        clear() {
            try {
                localStorage.clear();
                return true;
            } catch (e) {
                console.error('Storage clear error:', e);
                return false;
            }
        }
    },

    // DOM helpers
    createElement(tag, className, content) {
        const element = document.createElement(tag);
        if (className) element.className = className;
        if (content) element.innerHTML = content;
        return element;
    },

    // Show/hide loading spinner
    showLoading(container) {
        const spinner = this.createElement('div', 'loading-spinner', 
            '<i class="fas fa-spinner fa-spin"></i><span>Loading...</span>'
        );
        container.appendChild(spinner);
        return spinner;
    },

    hideLoading(spinner) {
        if (spinner && spinner.parentNode) {
            spinner.parentNode.removeChild(spinner);
        }
    },

    // Show notification
    showNotification(message, type = 'info') {
        const notification = this.createElement('div', `notification ${type}`,
            `<i class="fas fa-${this.getNotificationIcon(type)}"></i>
             <span>${message}</span>
             <button class="close-btn" onclick="this.parentNode.remove()">
                <i class="fas fa-times"></i>
             </button>`
        );
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
        
        return notification;
    },

    getNotificationIcon(type) {
        switch(type) {
            case 'success': return 'check-circle';
            case 'error': return 'exclamation-triangle';
            case 'warning': return 'exclamation-circle';
            default: return 'info-circle';
        }
    }
};

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Utils;
}