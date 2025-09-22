// Psychometric Test Questions Dataset
const psychometricQuestions = [
  // Analytical Thinking
  {
    id: 1,
    text: "I enjoy solving complex problems that require logical thinking.",
    category: "analytical",
    trait: "openness",
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
    text: "I prefer to analyze data before making decisions.",
    category: "analytical",
    trait: "conscientiousness",
    options: [
      { value: 1, text: "Strongly Disagree" },
      { value: 2, text: "Disagree" },
      { value: 3, text: "Neutral" },
      { value: 4, text: "Agree" },
      { value: 5, text: "Strongly Agree" }
    ]
  },
  
  // Social Interaction
  {
    id: 3,
    text: "I feel energized when working with large groups of people.",
    category: "social",
    trait: "extraversion",
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
    text: "I prefer collaborative work environments over working alone.",
    category: "social",
    trait: "extraversion",
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
    text: "I enjoy helping others solve their problems.",
    category: "social",
    trait: "agreeableness",
    options: [
      { value: 1, text: "Strongly Disagree" },
      { value: 2, text: "Disagree" },
      { value: 3, text: "Neutral" },
      { value: 4, text: "Agree" },
      { value: 5, text: "Strongly Agree" }
    ]
  },
  
  // Creative Thinking
  {
    id: 6,
    text: "I often come up with innovative solutions to problems.",
    category: "creative",
    trait: "openness",
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
    text: "I enjoy artistic and creative activities.",
    category: "creative",
    trait: "openness",
    options: [
      { value: 1, text: "Strongly Disagree" },
      { value: 2, text: "Disagree" },
      { value: 3, text: "Neutral" },
      { value: 4, text: "Agree" },
      { value: 5, text: "Strongly Agree" }
    ]
  },
  {
    id: 8,
    text: "I like to think outside the box and challenge conventional methods.",
    category: "creative",
    trait: "openness",
    options: [
      { value: 1, text: "Strongly Disagree" },
      { value: 2, text: "Disagree" },
      { value: 3, text: "Neutral" },
      { value: 4, text: "Agree" },
      { value: 5, text: "Strongly Agree" }
    ]
  },
  
  // Leadership
  {
    id: 9,
    text: "I naturally take charge in group situations.",
    category: "leadership",
    trait: "extraversion",
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
    text: "I enjoy motivating and inspiring others.",
    category: "leadership",
    trait: "extraversion",
    options: [
      { value: 1, text: "Strongly Disagree" },
      { value: 2, text: "Disagree" },
      { value: 3, text: "Neutral" },
      { value: 4, text: "Agree" },
      { value: 5, text: "Strongly Agree" }
    ]
  },
  {
    id: 11,
    text: "I am comfortable making important decisions.",
    category: "leadership",
    trait: "conscientiousness",
    options: [
      { value: 1, text: "Strongly Disagree" },
      { value: 2, text: "Disagree" },
      { value: 3, text: "Neutral" },
      { value: 4, text: "Agree" },
      { value: 5, text: "Strongly Agree" }
    ]
  },
  
  // Detail Orientation
  {
    id: 12,
    text: "I pay close attention to details in my work.",
    category: "detail",
    trait: "conscientiousness",
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
    text: "I prefer structured and organized work environments.",
    category: "detail",
    trait: "conscientiousness",
    options: [
      { value: 1, text: "Strongly Disagree" },
      { value: 2, text: "Disagree" },
      { value: 3, text: "Neutral" },
      { value: 4, text: "Agree" },
      { value: 5, text: "Strongly Agree" }
    ]
  },
  {
    id: 14,
    text: "I like to follow established procedures and guidelines.",
    category: "detail",
    trait: "conscientiousness",
    options: [
      { value: 1, text: "Strongly Disagree" },
      { value: 2, text: "Disagree" },
      { value: 3, text: "Neutral" },
      { value: 4, text: "Agree" },
      { value: 5, text: "Strongly Agree" }
    ]
  },
  
  // Stress Management
  {
    id: 15,
    text: "I remain calm under pressure.",
    category: "stress",
    trait: "neuroticism",
    reverse: true,
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
    text: "I work well in fast-paced environments.",
    category: "stress",
    trait: "neuroticism",
    reverse: true,
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
    text: "I can handle multiple tasks simultaneously without feeling overwhelmed.",
    category: "stress",
    trait: "neuroticism",
    reverse: true,
    options: [
      { value: 1, text: "Strongly Disagree" },
      { value: 2, text: "Disagree" },
      { value: 3, text: "Neutral" },
      { value: 4, text: "Agree" },
      { value: 5, text: "Strongly Agree" }
    ]
  },
  
  // Communication
  {
    id: 18,
    text: "I enjoy presenting ideas to others.",
    category: "communication",
    trait: "extraversion",
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
    text: "I am good at explaining complex concepts in simple terms.",
    category: "communication",
    trait: "agreeableness",
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
    text: "I prefer written communication over verbal communication.",
    category: "communication",
    trait: "extraversion",
    reverse: true,
    options: [
      { value: 1, text: "Strongly Disagree" },
      { value: 2, text: "Disagree" },
      { value: 3, text: "Neutral" },
      { value: 4, text: "Agree" },
      { value: 5, text: "Strongly Agree" }
    ]
  },
  
  // Innovation
  {
    id: 21,
    text: "I enjoy exploring new technologies and methods.",
    category: "innovation",
    trait: "openness",
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
    text: "I am comfortable with change and uncertainty.",
    category: "innovation",
    trait: "openness",
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
    text: "I like to experiment with new approaches to problem-solving.",
    category: "innovation",
    trait: "openness",
    options: [
      { value: 1, text: "Strongly Disagree" },
      { value: 2, text: "Disagree" },
      { value: 3, text: "Neutral" },
      { value: 4, text: "Agree" },
      { value: 5, text: "Strongly Agree" }
    ]
  },
  
  // Work Style
  {
    id: 24,
    text: "I prefer working independently rather than in teams.",
    category: "workstyle",
    trait: "extraversion",
    reverse: true,
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
    text: "I am motivated by achieving measurable results.",
    category: "workstyle",
    trait: "conscientiousness",
    options: [
      { value: 1, text: "Strongly Disagree" },
      { value: 2, text: "Disagree" },
      { value: 3, text: "Neutral" },
      { value: 4, text: "Agree" },
      { value: 5, text: "Strongly Agree" }
    ]
  }
];

// Scoring weights for different categories
const categoryWeights = {
  analytical: {
    engineering: 0.9,
    dataScience: 0.95,
    research: 0.85,
    finance: 0.8,
    consulting: 0.75
  },
  social: {
    humanResources: 0.95,
    socialWork: 0.9,
    teaching: 0.85,
    healthcare: 0.8,
    sales: 0.75
  },
  creative: {
    design: 0.95,
    marketing: 0.8,
    entertainment: 0.9,
    writing: 0.85,
    architecture: 0.8
  },
  leadership: {
    management: 0.95,
    entrepreneurship: 0.9,
    consulting: 0.8,
    politics: 0.85,
    executive: 0.9
  },
  detail: {
    accounting: 0.95,
    law: 0.85,
    engineering: 0.8,
    research: 0.8,
    quality: 0.9
  },
  stress: {
    emergency: 0.95,
    surgery: 0.9,
    finance: 0.8,
    journalism: 0.75,
    aviation: 0.85
  },
  communication: {
    teaching: 0.95,
    sales: 0.9,
    journalism: 0.85,
    publicRelations: 0.9,
    counseling: 0.85
  },
  innovation: {
    technology: 0.95,
    research: 0.9,
    design: 0.85,
    entrepreneurship: 0.8,
    consulting: 0.75
  },
  workstyle: {
    freelance: 0.8,
    remote: 0.75,
    corporate: 0.7,
    startup: 0.85,
    academic: 0.8
  }
};

// Big Five personality traits mapping
const personalityTraits = {
  openness: {
    description: "Openness to experience - creativity, curiosity, and willingness to try new things",
    careers: ["researcher", "artist", "entrepreneur", "consultant", "designer"]
  },
  conscientiousness: {
    description: "Conscientiousness - organization, dependability, and attention to detail",
    careers: ["accountant", "project manager", "engineer", "lawyer", "administrator"]
  },
  extraversion: {
    description: "Extraversion - sociability, assertiveness, and energetic approach to social situations",
    careers: ["sales representative", "teacher", "manager", "public relations", "politician"]
  },
  agreeableness: {
    description: "Agreeableness - cooperation, trust, and empathy towards others",
    careers: ["counselor", "nurse", "social worker", "teacher", "human resources"]
  },
  neuroticism: {
    description: "Emotional stability - ability to handle stress and remain calm under pressure",
    careers: ["surgeon", "pilot", "emergency responder", "crisis manager", "military officer"]
  }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    psychometricQuestions,
    categoryWeights,
    personalityTraits
  };
}
