// Comprehensive Career Database
const careers = [
  // Technology Careers
  {
    id: "software-engineer",
    title: "Software Engineer",
    category: "Technology",
    description: "Design and develop software applications, systems, and solutions",
    requiredSkills: ["programming", "problem-solving", "algorithms", "software-design"],
    preferredTraits: ["analytical", "detail", "innovation"],
    education: ["Computer Science", "Software Engineering", "Information Technology"],
    experience: "0-2 years",
    salaryRange: {
      min: 70000,
      max: 150000,
      currency: "USD"
    },
    growthProjection: "22%",
    workEnvironment: "Office/Remote",
    industries: ["Technology", "Finance", "Healthcare", "E-commerce"],
    dayInLife: [
      "Write and review code",
      "Debug and troubleshoot applications",
      "Collaborate with team members",
      "Design software architecture",
      "Test and deploy applications"
    ],
    ikigaiMatch: {
      love: "Creating innovative solutions",
      good: "Programming and logical thinking",
      need: "Digital transformation solutions",
      paid: "High demand in tech industry"
    }
  },
  {
    id: "data-scientist",
    title: "Data Scientist",
    category: "Technology",
    description: "Analyze complex data to extract insights and drive business decisions",
    requiredSkills: ["statistics", "programming", "machine-learning", "data-visualization"],
    preferredTraits: ["analytical", "detail", "innovation"],
    education: ["Data Science", "Statistics", "Computer Science", "Mathematics"],
    experience: "1-3 years",
    salaryRange: {
      min: 80000,
      max: 180000,
      currency: "USD"
    },
    growthProjection: "35%",
    workEnvironment: "Office/Remote",
    industries: ["Technology", "Finance", "Healthcare", "Retail", "Government"],
    dayInLife: [
      "Collect and clean data",
      "Build predictive models",
      "Create data visualizations",
      "Present findings to stakeholders",
      "Collaborate with business teams"
    ],
    ikigaiMatch: {
      love: "Discovering patterns in data",
      good: "Statistical analysis and programming",
      need: "Data-driven decision making",
      paid: "High demand across industries"
    }
  },
  {
    id: "ux-designer",
    title: "UX/UI Designer",
    category: "Design",
    description: "Design user interfaces and experiences for digital products",
    requiredSkills: ["design-thinking", "prototyping", "user-research", "visual-design"],
    preferredTraits: ["creative", "social", "detail"],
    education: ["Design", "Psychology", "Human-Computer Interaction"],
    experience: "0-2 years",
    salaryRange: {
      min: 60000,
      max: 130000,
      currency: "USD"
    },
    growthProjection: "13%",
    workEnvironment: "Office/Remote",
    industries: ["Technology", "E-commerce", "Entertainment", "Healthcare"],
    dayInLife: [
      "Conduct user research",
      "Create wireframes and prototypes",
      "Design user interfaces",
      "Test usability with users",
      "Collaborate with developers"
    ],
    ikigaiMatch: {
      love: "Creating beautiful and functional designs",
      good: "Visual design and user empathy",
      need: "Better user experiences",
      paid: "Growing demand in digital space"
    }
  },

  // Healthcare Careers
  {
    id: "registered-nurse",
    title: "Registered Nurse",
    category: "Healthcare",
    description: "Provide patient care and support in various healthcare settings",
    requiredSkills: ["medical-knowledge", "patient-care", "communication", "critical-thinking"],
    preferredTraits: ["social", "stress", "detail"],
    education: ["Nursing", "Bachelor of Science in Nursing"],
    experience: "0-1 years",
    salaryRange: {
      min: 55000,
      max: 90000,
      currency: "USD"
    },
    growthProjection: "7%",
    workEnvironment: "Hospital/Clinic",
    industries: ["Healthcare", "Government", "Education"],
    dayInLife: [
      "Assess patient conditions",
      "Administer medications",
      "Provide emotional support",
      "Document patient information",
      "Collaborate with medical team"
    ],
    ikigaiMatch: {
      love: "Helping people heal",
      good: "Caring for others and medical skills",
      need: "Healthcare and patient support",
      paid: "Stable demand in healthcare"
    }
  },
  {
    id: "physical-therapist",
    title: "Physical Therapist",
    category: "Healthcare",
    description: "Help patients recover mobility and manage pain through therapeutic exercises",
    requiredSkills: ["anatomy", "rehabilitation", "patient-care", "exercise-science"],
    preferredTraits: ["social", "detail", "stress"],
    education: ["Doctor of Physical Therapy", "Exercise Science"],
    experience: "0-2 years",
    salaryRange: {
      min: 75000,
      max: 95000,
      currency: "USD"
    },
    growthProjection: "18%",
    workEnvironment: "Clinic/Hospital",
    industries: ["Healthcare", "Sports", "Rehabilitation"],
    dayInLife: [
      "Evaluate patient conditions",
      "Develop treatment plans",
      "Guide therapeutic exercises",
      "Monitor patient progress",
      "Educate patients and families"
    ],
    ikigaiMatch: {
      love: "Helping people regain mobility",
      good: "Understanding of human movement",
      need: "Rehabilitation and pain management",
      paid: "Growing aging population"
    }
  },

  // Business & Finance
  {
    id: "financial-analyst",
    title: "Financial Analyst",
    category: "Finance",
    description: "Analyze financial data to guide investment and business decisions",
    requiredSkills: ["financial-modeling", "data-analysis", "excel", "presentation"],
    preferredTraits: ["analytical", "detail", "stress"],
    education: ["Finance", "Economics", "Business Administration", "Accounting"],
    experience: "0-2 years",
    salaryRange: {
      min: 60000,
      max: 110000,
      currency: "USD"
    },
    growthProjection: "5%",
    workEnvironment: "Office",
    industries: ["Finance", "Investment", "Corporate", "Government"],
    dayInLife: [
      "Analyze financial statements",
      "Create financial models",
      "Prepare investment reports",
      "Monitor market trends",
      "Present findings to management"
    ],
    ikigaiMatch: {
      love: "Understanding financial markets",
      good: "Analytical and mathematical skills",
      need: "Financial planning and investment guidance",
      paid: "Well-compensated in finance sector"
    }
  },
  {
    id: "marketing-manager",
    title: "Marketing Manager",
    category: "Business",
    description: "Develop and execute marketing strategies to promote products and services",
    requiredSkills: ["digital-marketing", "strategy", "communication", "analytics"],
    preferredTraits: ["creative", "social", "leadership"],
    education: ["Marketing", "Business Administration", "Communications"],
    experience: "2-5 years",
    salaryRange: {
      min: 65000,
      max: 130000,
      currency: "USD"
    },
    growthProjection: "10%",
    workEnvironment: "Office/Remote",
    industries: ["Retail", "Technology", "Healthcare", "Entertainment"],
    dayInLife: [
      "Develop marketing campaigns",
      "Analyze market research",
      "Manage marketing budgets",
      "Coordinate with creative teams",
      "Track campaign performance"
    ],
    ikigaiMatch: {
      love: "Creating compelling brand stories",
      good: "Strategic thinking and creativity",
      need: "Brand awareness and customer engagement",
      paid: "Essential for business growth"
    }
  },

  // Education
  {
    id: "elementary-teacher",
    title: "Elementary School Teacher",
    category: "Education",
    description: "Educate and nurture young students in fundamental subjects",
    requiredSkills: ["teaching", "curriculum-development", "classroom-management", "communication"],
    preferredTraits: ["social", "detail", "communication"],
    education: ["Education", "Teaching Certification", "Subject-specific degree"],
    experience: "0-1 years",
    salaryRange: {
      min: 40000,
      max: 70000,
      currency: "USD"
    },
    growthProjection: "4%",
    workEnvironment: "School",
    industries: ["Education", "Government", "Private Schools"],
    dayInLife: [
      "Plan and deliver lessons",
      "Assess student progress",
      "Manage classroom behavior",
      "Communicate with parents",
      "Attend professional development"
    ],
    ikigaiMatch: {
      love: "Inspiring young minds",
      good: "Teaching and mentoring",
      need: "Quality education for children",
      paid: "Stable employment in education"
    }
  },

  // Creative Fields
  {
    id: "graphic-designer",
    title: "Graphic Designer",
    category: "Creative",
    description: "Create visual concepts and designs for various media and platforms",
    requiredSkills: ["design-software", "visual-design", "typography", "branding"],
    preferredTraits: ["creative", "detail", "innovation"],
    education: ["Graphic Design", "Visual Arts", "Fine Arts"],
    experience: "0-2 years",
    salaryRange: {
      min: 45000,
      max: 85000,
      currency: "USD"
    },
    growthProjection: "3%",
    workEnvironment: "Office/Freelance",
    industries: ["Advertising", "Publishing", "Technology", "Entertainment"],
    dayInLife: [
      "Meet with clients",
      "Create design concepts",
      "Use design software",
      "Review and revise designs",
      "Prepare final deliverables"
    ],
    ikigaiMatch: {
      love: "Creating visual art",
      good: "Artistic and technical skills",
      need: "Visual communication",
      paid: "Demand in creative industries"
    }
  },

  // Engineering
  {
    id: "mechanical-engineer",
    title: "Mechanical Engineer",
    category: "Engineering",
    description: "Design and develop mechanical systems and devices",
    requiredSkills: ["cad-software", "engineering-principles", "problem-solving", "project-management"],
    preferredTraits: ["analytical", "detail", "innovation"],
    education: ["Mechanical Engineering", "Engineering Technology"],
    experience: "0-2 years",
    salaryRange: {
      min: 65000,
      max: 120000,
      currency: "USD"
    },
    growthProjection: "4%",
    workEnvironment: "Office/Manufacturing",
    industries: ["Manufacturing", "Automotive", "Aerospace", "Energy"],
    dayInLife: [
      "Design mechanical systems",
      "Create technical drawings",
      "Test prototypes",
      "Analyze system performance",
      "Collaborate with manufacturing"
    ],
    ikigaiMatch: {
      love: "Building mechanical solutions",
      good: "Engineering and mathematics",
      need: "Innovative mechanical systems",
      paid: "Strong demand in manufacturing"
    }
  },

  // Sales & Customer Service
  {
    id: "sales-representative",
    title: "Sales Representative",
    category: "Sales",
    description: "Sell products or services to businesses or consumers",
    requiredSkills: ["sales-techniques", "communication", "negotiation", "customer-service"],
    preferredTraits: ["social", "communication", "stress"],
    education: ["Business", "Marketing", "Communications", "Any field"],
    experience: "0-1 years",
    salaryRange: {
      min: 40000,
      max: 100000,
      currency: "USD"
    },
    growthProjection: "2%",
    workEnvironment: "Office/Field",
    industries: ["Retail", "Technology", "Pharmaceutical", "Insurance"],
    dayInLife: [
      "Prospect for new customers",
      "Present products/services",
      "Negotiate contracts",
      "Follow up with clients",
      "Meet sales targets"
    ],
    ikigaiMatch: {
      love: "Building relationships",
      good: "Persuasion and communication",
      need: "Connecting customers with solutions",
      paid: "Commission-based earning potential"
    }
  },

  // Human Resources
  {
    id: "hr-specialist",
    title: "Human Resources Specialist",
    category: "Human Resources",
    description: "Manage employee relations, recruitment, and HR policies",
    requiredSkills: ["recruitment", "employee-relations", "hr-policies", "communication"],
    preferredTraits: ["social", "detail", "communication"],
    education: ["Human Resources", "Psychology", "Business Administration"],
    experience: "1-3 years",
    salaryRange: {
      min: 50000,
      max: 85000,
      currency: "USD"
    },
    growthProjection: "7%",
    workEnvironment: "Office",
    industries: ["Corporate", "Government", "Healthcare", "Education"],
    dayInLife: [
      "Screen job candidates",
      "Handle employee concerns",
      "Maintain HR records",
      "Conduct training sessions",
      "Ensure policy compliance"
    ],
    ikigaiMatch: {
      love: "Supporting employee success",
      good: "People skills and organization",
      need: "Effective human resource management",
      paid: "Essential corporate function"
    }
  }
];

// Career categories for filtering
const careerCategories = [
  "Technology",
  "Healthcare",
  "Finance",
  "Business",
  "Education",
  "Creative",
  "Engineering",
  "Sales",
  "Human Resources",
  "Science",
  "Government",
  "Non-Profit"
];

// Industry growth trends
const industryTrends = {
  "Technology": {
    growth: "Very High",
    outlook: "Excellent",
    description: "Continued digital transformation and AI adoption"
  },
  "Healthcare": {
    growth: "High",
    outlook: "Excellent",
    description: "Aging population and medical advances"
  },
  "Finance": {
    growth: "Moderate",
    outlook: "Good",
    description: "Fintech innovation and digital banking"
  },
  "Education": {
    growth: "Moderate",
    outlook: "Stable",
    description: "Online learning and educational technology"
  },
  "Creative": {
    growth: "Moderate",
    outlook: "Good",
    description: "Digital media and content creation"
  },
  "Engineering": {
    growth: "Moderate",
    outlook: "Good",
    description: "Infrastructure and renewable energy"
  }
};

// Skill requirements by proficiency level
const skillLevels = {
  beginner: "0-1 years experience",
  intermediate: "1-3 years experience",
  advanced: "3-5 years experience",
  expert: "5+ years experience"
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    careers,
    careerCategories,
    industryTrends,
    skillLevels
  };
}