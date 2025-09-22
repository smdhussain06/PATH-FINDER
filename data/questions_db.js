// Psychometric Test Questions Database
const psychometricQuestions = [
    // Personality Traits (Big Five Model)
    {
        id: 1,
        text: "I enjoy solving complex problems and puzzles.",
        category: "openness",
        subcategory: "intellectual_curiosity",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 2,
        text: "I prefer working with others rather than working alone.",
        category: "extraversion",
        subcategory: "social_preference",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 3,
        text: "I always complete my tasks on time and meet deadlines.",
        category: "conscientiousness",
        subcategory: "reliability",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 4,
        text: "I tend to worry about things that might go wrong.",
        category: "neuroticism",
        subcategory: "anxiety",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 5,
        text: "I go out of my way to help others, even when it's inconvenient.",
        category: "agreeableness",
        subcategory: "altruism",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 6,
        text: "I enjoy being the center of attention in social situations.",
        category: "extraversion",
        subcategory: "assertiveness",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 7,
        text: "I prefer following established procedures rather than trying new approaches.",
        category: "openness",
        subcategory: "change_resistance",
        options: [
            { value: 5, text: "Strongly Disagree" },
            { value: 4, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 2, text: "Agree" },
            { value: 1, text: "Strongly Agree" }
        ]
    },
    {
        id: 8,
        text: "I keep my workspace and belongings very organized.",
        category: "conscientiousness",
        subcategory: "orderliness",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 9,
        text: "I find it easy to trust others with important tasks.",
        category: "agreeableness",
        subcategory: "trust",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 10,
        text: "I often feel stressed when facing tight deadlines.",
        category: "neuroticism",
        subcategory: "stress_response",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },

    // Work Style Preferences - 15 additional questions
    {
        id: 11,
        text: "I prefer working on multiple projects simultaneously rather than focusing on one.",
        category: "work_style",
        subcategory: "multitasking",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 12,
        text: "I thrive in fast-paced, high-pressure environments.",
        category: "work_style",
        subcategory: "pace_preference",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 13,
        text: "I prefer having clear instructions rather than figuring things out independently.",
        category: "work_style",
        subcategory: "autonomy",
        options: [
            { value: 5, text: "Strongly Disagree" },
            { value: 4, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 2, text: "Agree" },
            { value: 1, text: "Strongly Agree" }
        ]
    },
    {
        id: 14,
        text: "I enjoy mentoring and teaching others.",
        category: "work_style",
        subcategory: "leadership",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 15,
        text: "I prefer working with data and numbers rather than people.",
        category: "work_style",
        subcategory: "people_vs_data",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 16,
        text: "Having a high salary is more important to me than job satisfaction.",
        category: "values",
        subcategory: "financial_motivation",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 17,
        text: "I want my work to make a positive impact on society.",
        category: "values",
        subcategory: "social_impact",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 18,
        text: "Work-life balance is extremely important to me.",
        category: "values",
        subcategory: "work_life_balance",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 19,
        text: "I prefer jobs with job security over those with high growth potential.",
        category: "values",
        subcategory: "security_vs_growth",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 20,
        text: "Recognition and acknowledgment for my work is very important to me.",
        category: "values",
        subcategory: "recognition",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 21,
        text: "I have strong analytical and logical thinking skills.",
        category: "skills",
        subcategory: "analytical",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 22,
        text: "I excel at written and verbal communication.",
        category: "skills",
        subcategory: "communication",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 23,
        text: "I am skilled at managing my time and prioritizing tasks effectively.",
        category: "skills",
        subcategory: "time_management",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 24,
        text: "I have a natural talent for understanding and working with technology.",
        category: "skills",
        subcategory: "technical",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    },
    {
        id: 25,
        text: "I am creative and enjoy coming up with innovative solutions.",
        category: "skills",
        subcategory: "creativity",
        options: [
            { value: 1, text: "Strongly Disagree" },
            { value: 2, text: "Disagree" },
            { value: 3, text: "Neutral" },
            { value: 4, text: "Agree" },
            { value: 5, text: "Strongly Agree" }
        ]
    }
];