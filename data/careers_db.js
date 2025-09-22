// Career Paths Database
const careerPaths = [
    {
        id: 1,
        title: "Software Developer",
        category: "Technology",
        description: "Design, develop, and maintain software applications and systems",
        requiredSkills: ["technical", "analytical", "creativity", "time_management"],
        personalityMatch: {
            openness: "high",
            conscientiousness: "medium",
            extraversion: "low",
            agreeableness: "medium",
            neuroticism: "low"
        },
        workStyle: {
            multitasking: "medium",
            pace_preference: "medium",
            autonomy: "high",
            leadership: "low",
            people_vs_data: "high"
        },
        values: {
            financial_motivation: "high",
            social_impact: "medium",
            work_life_balance: "medium",
            security_vs_growth: "low",
            recognition: "medium"
        },
        salaryRange: "$70,000 - $150,000",
        jobGrowth: "22% (Much faster than average)",
        education: "Bachelor's degree in Computer Science or related field",
        workEnvironment: "Office, remote work options available",
        dailyTasks: [
            "Writing and testing code",
            "Debugging software issues",
            "Collaborating with team members",
            "Documenting code and processes"
        ],
        careerPath: [
            "Junior Developer",
            "Software Developer",
            "Senior Developer",
            "Lead Developer/Team Lead",
            "Engineering Manager"
        ]
    },
    {
        id: 2,
        title: "Marketing Manager",
        category: "Business",
        description: "Develop and execute marketing strategies to promote products or services",
        requiredSkills: ["communication", "creativity", "analytical", "time_management"],
        personalityMatch: {
            openness: "high",
            conscientiousness: "high",
            extraversion: "high",
            agreeableness: "medium",
            neuroticism: "low"
        },
        workStyle: {
            multitasking: "high",
            pace_preference: "high",
            autonomy: "medium",
            leadership: "high",
            people_vs_data: "low"
        },
        values: {
            financial_motivation: "high",
            social_impact: "medium",
            work_life_balance: "medium",
            security_vs_growth: "medium",
            recognition: "high"
        },
        salaryRange: "$65,000 - $120,000",
        jobGrowth: "10% (Faster than average)",
        education: "Bachelor's degree in Marketing, Business, or related field",
        workEnvironment: "Office, some travel required",
        dailyTasks: [
            "Developing marketing campaigns",
            "Analyzing market trends",
            "Managing marketing budgets",
            "Coordinating with creative teams"
        ],
        careerPath: [
            "Marketing Assistant",
            "Marketing Specialist",
            "Marketing Manager",
            "Senior Marketing Manager",
            "Director of Marketing"
        ]
    },
    {
        id: 3,
        title: "Data Scientist",
        category: "Technology",
        description: "Analyze complex data to help organizations make informed decisions",
        requiredSkills: ["analytical", "technical", "communication", "time_management"],
        personalityMatch: {
            openness: "high",
            conscientiousness: "high",
            extraversion: "low",
            agreeableness: "medium",
            neuroticism: "low"
        },
        workStyle: {
            multitasking: "medium",
            pace_preference: "medium",
            autonomy: "high",
            leadership: "low",
            people_vs_data: "high"
        },
        values: {
            financial_motivation: "high",
            social_impact: "high",
            work_life_balance: "medium",
            security_vs_growth: "low",
            recognition: "medium"
        },
        salaryRange: "$85,000 - $165,000",
        jobGrowth: "35% (Much faster than average)",
        education: "Bachelor's/Master's in Data Science, Statistics, or related field",
        workEnvironment: "Office, remote work options available",
        dailyTasks: [
            "Collecting and cleaning data",
            "Performing statistical analysis",
            "Creating data visualizations",
            "Presenting findings to stakeholders"
        ],
        careerPath: [
            "Data Analyst",
            "Junior Data Scientist",
            "Data Scientist",
            "Senior Data Scientist",
            "Chief Data Officer"
        ]
    },
    {
        id: 4,
        title: "Psychologist",
        category: "Healthcare",
        description: "Study human behavior and mental processes to help people improve their lives",
        requiredSkills: ["communication", "analytical", "time_management"],
        personalityMatch: {
            openness: "high",
            conscientiousness: "high",
            extraversion: "medium",
            agreeableness: "high",
            neuroticism: "low"
        },
        workStyle: {
            multitasking: "medium",
            pace_preference: "low",
            autonomy: "medium",
            leadership: "medium",
            people_vs_data: "low"
        },
        values: {
            financial_motivation: "medium",
            social_impact: "high",
            work_life_balance: "high",
            security_vs_growth: "high",
            recognition: "medium"
        },
        salaryRange: "$80,000 - $120,000",
        jobGrowth: "3% (Average)",
        education: "Doctoral degree in Psychology",
        workEnvironment: "Private practice, hospitals, clinics",
        dailyTasks: [
            "Conducting therapy sessions",
            "Psychological assessments",
            "Developing treatment plans",
            "Maintaining patient records"
        ],
        careerPath: [
            "Psychology Intern",
            "Licensed Psychologist",
            "Senior Psychologist",
            "Clinical Director",
            "Private Practice Owner"
        ]
    },
    {
        id: 5,
        title: "Financial Advisor",
        category: "Finance",
        description: "Help individuals and organizations make informed financial decisions",
        requiredSkills: ["communication", "analytical", "time_management"],
        personalityMatch: {
            openness: "medium",
            conscientiousness: "high",
            extraversion: "high",
            agreeableness: "high",
            neuroticism: "low"
        },
        workStyle: {
            multitasking: "high",
            pace_preference: "medium",
            autonomy: "medium",
            leadership: "medium",
            people_vs_data: "medium"
        },
        values: {
            financial_motivation: "high",
            social_impact: "medium",
            work_life_balance: "medium",
            security_vs_growth: "medium",
            recognition: "high"
        },
        salaryRange: "$55,000 - $200,000+",
        jobGrowth: "4% (Average)",
        education: "Bachelor's degree in Finance, Economics, or related field",
        workEnvironment: "Office, client meetings",
        dailyTasks: [
            "Meeting with clients",
            "Analyzing financial data",
            "Creating investment strategies",
            "Monitoring market trends"
        ],
        careerPath: [
            "Financial Analyst",
            "Junior Financial Advisor",
            "Financial Advisor",
            "Senior Financial Advisor",
            "Wealth Manager"
        ]
    }
];