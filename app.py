"""
PATH-FINDER: Complete Career Discovery Platform
A comprehensive 3-layer career guidance system combining:
- Layer 1: Psychometric Personality Assessment  
- Layer 2: Ikigai Discovery & Analysis
- Layer 3: Career Navigation & Action Planning

Created by combining Streamlit Ikigai app + HTML/CSS/JS Career Navigation app
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import io
import os
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocDocument, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# Configure page
st.set_page_config(
    page_title="PATH-FINDER: Complete Career Discovery",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Psychometric Questions Database
PSYCHOMETRIC_QUESTIONS = [
    {
        "id": 1,
        "category": "problem_solving",
        "question": "When faced with a complex problem at work, what is your typical approach?",
        "options": [
            {
                "text": "I break it down into smaller, manageable parts and tackle each systematically",
                "traits": {"conscientiousness": 4, "openness": 3, "analytical_thinking": 5}
            },
            {
                "text": "I brainstorm multiple creative solutions before choosing the best one", 
                "traits": {"openness": 5, "creativity": 4, "extraversion": 3}
            },
            {
                "text": "I research similar problems and adapt proven solutions",
                "traits": {"conscientiousness": 3, "analytical_thinking": 4, "stability": 3}
            },
            {
                "text": "I collaborate with others to find the best solution together",
                "traits": {"agreeableness": 5, "extraversion": 4, "teamwork": 5}
            }
        ]
    },
    {
        "id": 2,
        "category": "work_environment",
        "question": "Your ideal work environment would be:",
        "options": [
            {
                "text": "A quiet, organized space where I can focus deeply on complex tasks",
                "traits": {"conscientiousness": 5, "introversion": 4, "depth_focus": 5}
            },
            {
                "text": "A dynamic, collaborative space with lots of interaction and energy",
                "traits": {"extraversion": 5, "agreeableness": 4, "social_energy": 5}
            },
            {
                "text": "A flexible environment where I can choose when and how to work",
                "traits": {"openness": 4, "autonomy": 5, "adaptability": 4}
            },
            {
                "text": "A structured environment with clear expectations and processes",
                "traits": {"conscientiousness": 5, "stability": 4, "structure_preference": 5}
            }
        ]
    },
    {
        "id": 3,
        "category": "decision_making",
        "question": "How do you typically make important decisions?",
        "options": [
            {
                "text": "I gather extensive data and analyze all possible outcomes",
                "traits": {"conscientiousness": 5, "analytical_thinking": 5, "neuroticism": 2}
            },
            {
                "text": "I trust my intuition and past experiences",
                "traits": {"openness": 4, "confidence": 4, "intuitive_thinking": 5}
            },
            {
                "text": "I seek advice from trusted colleagues or mentors",
                "traits": {"agreeableness": 4, "humility": 4, "social_intelligence": 4}
            },
            {
                "text": "I make quick decisions and adjust as I learn more",
                "traits": {"extraversion": 4, "adaptability": 5, "risk_tolerance": 4}
            }
        ]
    },
    {
        "id": 4,
        "category": "teamwork",
        "question": "In team projects, you naturally tend to:",
        "options": [
            {
                "text": "Take charge and coordinate the team's efforts toward the goal",
                "traits": {"extraversion": 5, "leadership": 5, "results_oriented": 4}
            },
            {
                "text": "Contribute specialized expertise and high-quality individual work",
                "traits": {"conscientiousness": 5, "expertise": 5, "quality_focus": 5}
            },
            {
                "text": "Facilitate communication and ensure everyone's voice is heard",
                "traits": {"agreeableness": 5, "empathy": 4, "social_intelligence": 5}
            },
            {
                "text": "Generate creative ideas and alternative approaches",
                "traits": {"openness": 5, "creativity": 5, "innovation": 4}
            }
        ]
    },
    {
        "id": 5,
        "category": "motivation",
        "question": "What motivates you most in your work?",
        "options": [
            {
                "text": "Solving complex challenges and achieving mastery in my field",
                "traits": {"openness": 4, "achievement": 5, "expertise": 5}
            },
            {
                "text": "Making a positive impact on others and contributing to society",
                "traits": {"agreeableness": 5, "social_impact": 5, "purpose_driven": 5}
            },
            {
                "text": "Leading teams and driving organizational success",
                "traits": {"extraversion": 5, "leadership": 5, "ambition": 4}
            },
            {
                "text": "Creating innovative solutions and exploring new possibilities",
                "traits": {"openness": 5, "creativity": 5, "innovation": 5}
            }
        ]
    }
]

# Big Five Traits for analysis
BIG_FIVE_TRAITS = {
    "openness": {
        "name": "Openness to Experience",
        "description": "Creativity, curiosity, and willingness to try new experiences",
        "high_description": "Creative, curious, open to new ideas and experiences",
        "low_description": "Practical, conventional, prefers familiar approaches"
    },
    "conscientiousness": {
        "name": "Conscientiousness", 
        "description": "Organization, discipline, and goal-directed behavior",
        "high_description": "Organized, disciplined, reliable, and goal-oriented",
        "low_description": "Flexible, spontaneous, adaptable to changing situations"
    },
    "extraversion": {
        "name": "Extraversion",
        "description": "Energy from social interaction and external stimulation",
        "high_description": "Outgoing, energetic, enjoys social interaction and leadership",
        "low_description": "Reserved, thoughtful, prefers deep work and smaller groups"
    },
    "agreeableness": {
        "name": "Agreeableness",
        "description": "Cooperation, empathy, and concern for others",
        "high_description": "Cooperative, empathetic, values harmony and helping others", 
        "low_description": "Direct, competitive, focused on results and efficiency"
    },
    "neuroticism": {
        "name": "Emotional Stability",
        "description": "Emotional resilience and stress management",
        "high_description": "May experience stress under pressure, sensitive to criticism",
        "low_description": "Emotionally stable, calm under pressure, resilient"
    }
}

# Enhanced career database
CAREER_DATABASE = {
    "Data Scientist": {
        "skills": ["programming", "mathematics", "analytical_thinking", "statistics", "machine_learning"],
        "growth_rate": "Very High",
        "salary_range": "$80,000 - $160,000",
        "description": "Analyze complex datasets to help organizations make data-driven decisions",
        "ikigai_intersections": ["Profession", "Vocation"],
        "psychometric_fit": {
            "openness": 4, "conscientiousness": 5, "extraversion": 2, 
            "agreeableness": 3, "neuroticism": 2
        },
        "what_you_love": ["analyzing_data", "learning_new_things", "creative_problem_solving"],
        "what_youre_good_at": ["programming", "mathematics", "analytical_thinking"],
        "what_world_needs": ["data_driven_decisions", "business_insights", "predictive_analytics"],
        "what_you_can_be_paid_for": ["data_analysis", "machine_learning_models", "business_intelligence"]
    },
    "UX/UI Designer": {
        "skills": ["design", "creativity", "user_research", "prototyping", "communication"],
        "growth_rate": "High",
        "salary_range": "$60,000 - $130,000",
        "description": "Create user-centered digital experiences and interfaces",
        "ikigai_intersections": ["Passion", "Mission"],
        "psychometric_fit": {
            "openness": 5, "conscientiousness": 3, "extraversion": 3,
            "agreeableness": 4, "neuroticism": 2
        },
        "what_you_love": ["artistic_expression", "helping_others", "creative_problem_solving"],
        "what_youre_good_at": ["design_thinking", "prototyping", "user_research"],
        "what_world_needs": ["intuitive_interfaces", "accessible_design", "better_user_experiences"],
        "what_you_can_be_paid_for": ["user_interface_design", "user_experience_consulting", "design_systems"]
    },
    "Product Manager": {
        "skills": ["strategic_planning", "communication", "leadership", "market_analysis", "project_management"],
        "growth_rate": "High",
        "salary_range": "$85,000 - $170,000",
        "description": "Guide product development from conception to market success",
        "ikigai_intersections": ["Passion", "Vocation"],
        "psychometric_fit": {
            "openness": 4, "conscientiousness": 4, "extraversion": 5,
            "agreeableness": 4, "neuroticism": 2
        },
        "what_you_love": ["strategic_thinking", "building_solutions", "leading_teams"],
        "what_youre_good_at": ["strategic_thinking", "communication", "project_management"],
        "what_world_needs": ["innovative_products", "user_solutions", "market_driven_development"],
        "what_you_can_be_paid_for": ["product_strategy", "product_development", "market_analysis"]
    },
    "Software Engineer": {
        "skills": ["programming", "problem_solving", "system_design", "algorithms", "debugging"],
        "growth_rate": "Very High", 
        "salary_range": "$70,000 - $150,000",
        "description": "Design, develop, and maintain software applications and systems",
        "ikigai_intersections": ["Profession", "Vocation"],
        "psychometric_fit": {
            "openness": 4, "conscientiousness": 5, "extraversion": 2,
            "agreeableness": 3, "neuroticism": 2
        },
        "what_you_love": ["building_solutions", "creative_problem_solving", "learning_new_things"],
        "what_youre_good_at": ["programming", "analytical_thinking", "problem_solving"],
        "what_world_needs": ["digital_transformation", "automation", "technical_solutions"],
        "what_you_can_be_paid_for": ["software_development", "technical_consulting", "system_architecture"]
    },
    "Digital Marketing Manager": {
        "skills": ["marketing", "communication", "analytical_thinking", "creativity", "strategic_planning"],
        "growth_rate": "High",
        "salary_range": "$50,000 - $110,000",
        "description": "Develop and execute marketing strategies across digital channels",
        "ikigai_intersections": ["Passion", "Profession"],
        "psychometric_fit": {
            "openness": 4, "conscientiousness": 3, "extraversion": 4,
            "agreeableness": 4, "neuroticism": 2
        },
        "what_you_love": ["creative_storytelling", "connecting_with_audiences", "brand_building"],
        "what_youre_good_at": ["marketing_strategy", "content_creation", "data_analysis"],
        "what_world_needs": ["brand_awareness", "customer_engagement", "digital_presence"],
        "what_you_can_be_paid_for": ["marketing_campaigns", "brand_strategy", "digital_advertising"]
    }
}

def add_custom_css():
    """Add modern dark theme CSS"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary-bg: #0e1117;
            --secondary-bg: #262730;
            --accent-color: #667eea;
            --accent-secondary: #764ba2;
            --text-primary: #fafafa;
            --text-secondary: #a0a0a0;
        }
        
        .main .block-container {
            padding: 2rem 1rem;
            max-width: 1200px;
        }
        
        .main-header {
            text-align: center;
            padding: 3rem 0 2rem 0;
        }
        
        .main-header h1 {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        
        .main-header p {
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }
        
        .progress-container {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 2rem 0;
            padding: 1rem;
            background: rgba(102, 126, 234, 0.05);
            border-radius: 12px;
            border: 1px solid rgba(102, 126, 234, 0.2);
        }
        
        .progress-step {
            text-align: center;
            padding: 1rem;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .progress-step.active {
            background: rgba(102, 126, 234, 0.1);
            border: 1px solid var(--accent-color);
        }
        
        .step-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .step-label {
            font-size: 0.9rem;
            font-weight: 500;
            color: var(--text-secondary);
        }
        
        .question-container {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 2rem;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .question-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--accent-color);
            margin-bottom: 1.5rem;
        }
        
        .stRadio > div[role="radiogroup"] > label {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .stRadio > div[role="radiogroup"] > label:hover {
            background: rgba(102, 126, 234, 0.1);
            border-color: var(--accent-color);
            transform: translateY(-2px);
        }
        
        .result-card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 2rem;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        
        .result-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        }
        
        .trait-bar {
            width: 100%;
            height: 8px;
            background: rgba(102, 126, 234, 0.2);
            border-radius: 4px;
            overflow: hidden;
            margin: 0.5rem 0;
        }
        
        .trait-fill {
            height: 100%;
            background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
            transition: width 0.5s ease;
        }
        
        .ikigai-section {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 2rem;
            margin: 2rem 0;
            border: 1px solid rgba(102, 126, 234, 0.2);
        }
        
        .ikigai-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .ikigai-header h2 {
            color: var(--accent-color);
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
            border: none;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }
        
        .metric-container {
            background: rgba(102, 126, 234, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(102, 126, 234, 0.2);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--accent-color);
            margin-bottom: 0.5rem;
        }
        
        .metric-label {
            font-size: 1rem;
            color: var(--text-secondary);
            font-weight: 500;
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in { animation: fadeInUp 0.6s ease; }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def main():
    add_custom_css()
    
    # Main header
    st.markdown("""
    <div class="main-header fade-in">
        <h1>🧭 PATH-FINDER</h1>
        <p>Complete Career Discovery Platform</p>
        <p style="font-size: 1rem; margin-top: 1rem;">
            3-Layer Analysis: Personality → Ikigai → Career Navigation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_layer' not in st.session_state:
        st.session_state.current_layer = 1
    if 'psychometric_answers' not in st.session_state:
        st.session_state.psychometric_answers = {}
    if 'psychometric_results' not in st.session_state:
        st.session_state.psychometric_results = None
    if 'ikigai_data' not in st.session_state:
        st.session_state.ikigai_data = None
    if 'final_recommendations' not in st.session_state:
        st.session_state.final_recommendations = None
    
    # Progress indicator
    display_progress_indicator()
    
    # Layer routing
    if st.session_state.current_layer == 1:
        layer_1_psychometric_assessment()
    elif st.session_state.current_layer == 2:
        layer_2_ikigai_discovery()
    elif st.session_state.current_layer == 3:
        layer_3_career_navigation()

def display_progress_indicator():
    """Display 3-layer progress indicator"""
    col1, col2, col3 = st.columns(3)
    
    layers = [
        {"num": 1, "label": "Personality Analysis", "icon": "🧠"},
        {"num": 2, "label": "Ikigai Discovery", "icon": "🌸"},
        {"num": 3, "label": "Career Navigation", "icon": "🎯"}
    ]
    
    for i, (col, layer) in enumerate(zip([col1, col2, col3], layers)):
        with col:
            is_active = st.session_state.current_layer == layer["num"]
            is_complete = st.session_state.current_layer > layer["num"]
            
            status_class = "active" if is_active else ("complete" if is_complete else "")
            
            st.markdown(f"""
            <div class="progress-step {status_class}" style="text-align: center;">
                <div class="step-icon">{layer["icon"]}</div>
                <div style="font-weight: 600; color: {'var(--accent-color)' if is_active else 'var(--text-secondary)'};">
                    Layer {layer["num"]}
                </div>
                <div class="step-label">{layer["label"]}</div>
            </div>
            """, unsafe_allow_html=True)

def layer_1_psychometric_assessment():
    """Layer 1: Comprehensive personality assessment"""
    st.markdown("""
    <div class="ikigai-section fade-in">
        <div class="ikigai-header">
            <h2>🧠 Personality Assessment</h2>
            <p style="color: var(--text-secondary); font-size: 1.1rem;">
                Discover your psychological profile through our comprehensive questionnaire
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Track progress
    total_questions = len(PSYCHOMETRIC_QUESTIONS)
    answered_questions = len(st.session_state.psychometric_answers)
    progress = answered_questions / total_questions if total_questions > 0 else 0
    
    st.progress(progress, f"Progress: {answered_questions}/{total_questions} questions completed")
    
    # Display questions
    for question in PSYCHOMETRIC_QUESTIONS:
        with st.container():
            st.markdown(f"""
            <div class="question-container fade-in">
                <div class="question-title">
                    Question {question['id']}: {question['question']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Radio button options
            options = [opt["text"] for opt in question["options"]]
            
            current_answer = st.session_state.psychometric_answers.get(question["id"])
            current_index = None
            if current_answer:
                try:
                    current_index = next(i for i, opt in enumerate(question["options"]) 
                                       if opt["text"] == current_answer["text"])
                except StopIteration:
                    current_index = None
            
            selected_option = st.radio(
                f"Select your answer for Question {question['id']}:",
                options,
                index=current_index,
                key=f"q_{question['id']}",
                label_visibility="collapsed"
            )
            
            # Store answer
            if selected_option:
                selected_option_data = next(opt for opt in question["options"] 
                                          if opt["text"] == selected_option)
                st.session_state.psychometric_answers[question["id"]] = {
                    "question": question["question"],
                    "text": selected_option,
                    "traits": selected_option_data["traits"],
                    "category": question["category"]
                }
    
    st.markdown("---")
    
    # Analysis button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Analyze My Personality", use_container_width=True):
            if len(st.session_state.psychometric_answers) >= len(PSYCHOMETRIC_QUESTIONS):
                with st.spinner("🧠 Analyzing your personality profile..."):
                    analyze_psychometric_results()
                    st.session_state.current_layer = 2
                    st.rerun()
            else:
                st.warning(f"Please answer all {len(PSYCHOMETRIC_QUESTIONS)} questions to continue.")

def analyze_psychometric_results():
    """Analyze psychometric assessment results"""
    trait_scores = {}
    
    # Initialize trait scores
    for trait in BIG_FIVE_TRAITS.keys():
        trait_scores[trait] = []
    
    # Collect trait scores from answers
    for answer in st.session_state.psychometric_answers.values():
        for trait, score in answer["traits"].items():
            if trait in trait_scores:
                trait_scores[trait].append(score)
    
    # Calculate average scores (safer calculation)
    final_scores = {}
    for trait, scores in trait_scores.items():
        if scores:
            final_scores[trait] = sum(scores) / len(scores)
        else:
            final_scores[trait] = 2.5  # Default neutral score
    
    # Generate personality analysis
    analysis = generate_personality_analysis(final_scores)
    
    # Store results
    st.session_state.psychometric_results = {
        "trait_scores": final_scores,
        "analysis": analysis,
        "completed_at": datetime.now().isoformat()
    }

def generate_personality_analysis(trait_scores):
    """Generate detailed personality analysis"""
    analysis = {
        "summary": "",
        "trait_details": {},
        "strengths": [],
        "development_areas": [],
        "work_style": ""
    }
    
    # Generate summary
    summary = "Based on your responses, you demonstrate "
    if trait_scores.get("openness", 0) >= 4:
        summary += "high creativity and openness to new experiences. "
    if trait_scores.get("conscientiousness", 0) >= 4:
        summary += "strong organizational skills and attention to detail. "
    if trait_scores.get("extraversion", 0) >= 4:
        summary += "natural leadership abilities and social energy. "
    if trait_scores.get("agreeableness", 0) >= 4:
        summary += "excellent interpersonal skills and empathy. "
    if trait_scores.get("neuroticism", 0) <= 2:
        summary += "emotional stability and resilience under pressure. "
    
    analysis["summary"] = summary
    
    # Trait details
    for trait, score in trait_scores.items():
        trait_info = BIG_FIVE_TRAITS.get(trait, {})
        if not trait_info:
            continue
            
        scaled_score = min(5, max(1, score))
        
        if scaled_score >= 4:
            description = trait_info.get("high_description", "High level")
        elif scaled_score <= 2:
            description = trait_info.get("low_description", "Low level")
        else:
            description = f"Balanced {trait_info.get('name', trait).lower()}"
        
        analysis["trait_details"][trait] = {
            "score": scaled_score,
            "description": description,
            "name": trait_info.get("name", trait.title())
        }
    
    # Identify strengths
    for trait, score in trait_scores.items():
        if score >= 4 and trait in BIG_FIVE_TRAITS:
            trait_info = BIG_FIVE_TRAITS[trait]
            analysis["strengths"].append(trait_info.get("high_description", f"High {trait}"))
    
    # Identify development areas  
    for trait, score in trait_scores.items():
        if score <= 2.5 and trait != "neuroticism" and trait in BIG_FIVE_TRAITS:
            trait_info = BIG_FIVE_TRAITS[trait]
            analysis["development_areas"].append(f"Develop {trait_info.get('name', trait).lower()}")
    
    return analysis

def layer_2_ikigai_discovery():
    """Layer 2: Ikigai discovery and analysis"""
    
    # Show psychometric results first
    if st.session_state.psychometric_results:
        with st.expander("🧠 Your Personality Profile", expanded=True):
            results = st.session_state.psychometric_results
            
            st.markdown("### Personality Summary")
            st.write(results["analysis"]["summary"])
            
            st.markdown("### Trait Scores")
            cols = st.columns(len(results["trait_scores"]))
            for i, (trait, score) in enumerate(results["trait_scores"].items()):
                with cols[i]:
                    trait_info = BIG_FIVE_TRAITS.get(trait, {"name": trait.title()})
                    percentage = int((score / 5) * 100)
                    st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-value">{percentage}%</div>
                        <div class="metric-label">{trait_info['name']}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Ikigai Discovery Section
    st.markdown("""
    <div class="ikigai-section fade-in">
        <div class="ikigai-header">
            <h2>🌸 Ikigai Discovery</h2>
            <p style="color: var(--text-secondary); font-size: 1.1rem;">
                Find your purpose by exploring what you love, what you're good at, what the world needs, and what you can be paid for
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Ikigai quadrants
    ikigai_quadrants = {
        "What You Love": {
            "icon": "💝",
            "items": [
                "Creative Problem Solving", "Helping Others", "Learning New Things",
                "Building Solutions", "Artistic Expression", "Leading Teams",
                "Analyzing Data", "Strategic Thinking", "Teaching Others", "Innovation"
            ]
        },
        "What You're Good At": {
            "icon": "💪", 
            "items": [
                "Communication", "Analytical Thinking", "Programming", "Design Thinking",
                "Project Management", "Research", "Leadership", "Mathematics",
                "Writing", "Marketing"
            ]
        },
        "What World Needs": {
            "icon": "🌍",
            "items": [
                "Digital Transformation", "Climate Solutions", "Education Access",
                "Healthcare Innovation", "Social Equality", "Economic Opportunity",
                "Mental Health Support", "Data Privacy", "Smart Cities", "Elderly Care"
            ]
        },
        "What You Can Be Paid For": {
            "icon": "💰",
            "items": [
                "Software Development", "Consulting Services", "Content Creation",
                "Product Design", "Data Analysis", "Marketing", "Financial Services",
                "Healthcare Services", "Education", "Engineering"
            ]
        }
    }
    
    # Initialize ikigai data
    if st.session_state.ikigai_data is None:
        st.session_state.ikigai_data = {quadrant: {} for quadrant in ikigai_quadrants.keys()}
    
    # Display ikigai quadrants
    for quadrant, data in ikigai_quadrants.items():
        with st.container():
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.03); border-radius: 12px; padding: 2rem; margin: 1rem 0; border: 1px solid rgba(102, 126, 234, 0.2);">
                <h3 style="color: var(--accent-color); margin-bottom: 1rem;">
                    {data['icon']} {quadrant}
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            cols = st.columns(2)
            for i, item in enumerate(data["items"]):
                with cols[i % 2]:
                    value = st.slider(
                        item,
                        0, 10, 5,
                        key=f"{quadrant}_{item}",
                        help=f"Rate how much this applies to you (0 = not at all, 10 = extremely)"
                    )
                    st.session_state.ikigai_data[quadrant][item] = value
    
    st.markdown("---")
    
    # Analysis button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌸 Analyze My Ikigai", use_container_width=True):
            with st.spinner("🌸 Discovering your Ikigai and matching careers..."):
                analyze_ikigai_and_generate_recommendations()
                st.session_state.current_layer = 3
                st.rerun()

def analyze_ikigai_and_generate_recommendations():
    """Analyze Ikigai data and generate comprehensive career recommendations"""
    
    # Calculate Ikigai intersections
    intersections = calculate_ikigai_intersections(st.session_state.ikigai_data)
    
    # Generate career recommendations combining psychometric + ikigai
    recommendations = generate_comprehensive_recommendations(
        st.session_state.psychometric_results,
        st.session_state.ikigai_data,
        intersections
    )
    
    # Store results
    st.session_state.final_recommendations = {
        "ikigai_intersections": intersections,
        "career_recommendations": recommendations,
        "completed_at": datetime.now().isoformat()
    }

def calculate_ikigai_intersections(ikigai_data):
    """Calculate Ikigai intersection scores"""
    intersections = {}
    
    quadrants = list(ikigai_data.keys())
    if len(quadrants) < 4:
        return {"Ikigai_Center": {"score": 0.5, "description": "Incomplete data"}}
    
    love = ikigai_data[quadrants[0]]  # What You Love
    good_at = ikigai_data[quadrants[1]]  # What You're Good At  
    world_needs = ikigai_data[quadrants[2]]  # What World Needs
    paid_for = ikigai_data[quadrants[3]]  # What You Can Be Paid For
    
    # Calculate intersection scores (simplified)
    intersections["Passion"] = {
        "score": calculate_intersection_score(love, good_at),
        "description": "What you love and are good at"
    }
    
    intersections["Mission"] = {
        "score": calculate_intersection_score(love, world_needs),
        "description": "What you love and the world needs"
    }
    
    intersections["Profession"] = {
        "score": calculate_intersection_score(good_at, paid_for),
        "description": "What you're good at and can be paid for"
    }
    
    intersections["Vocation"] = {
        "score": calculate_intersection_score(world_needs, paid_for),
        "description": "What the world needs and you can be paid for"
    }
    
    # Overall Ikigai score
    total_score = sum([intersection["score"] for intersection in intersections.values()])
    intersections["Ikigai_Center"] = {
        "score": total_score / 4,
        "description": "Perfect balance of all four elements"
    }
    
    return intersections

def calculate_intersection_score(dict1, dict2):
    """Calculate overlap score between two dictionaries"""
    if not dict1 or not dict2:
        return 0.5
    
    # Simple correlation-based scoring with safe calculation
    values1 = [v for v in dict1.values() if isinstance(v, (int, float))]
    values2 = [v for v in dict2.values() if isinstance(v, (int, float))]
    
    if len(values1) != len(values2) or len(values1) == 0:
        return 0.5
    
    # Calculate correlation manually to avoid numpy warnings
    mean1 = sum(values1) / len(values1)
    mean2 = sum(values2) / len(values2)
    
    numerator = sum((v1 - mean1) * (v2 - mean2) for v1, v2 in zip(values1, values2))
    sum_sq1 = sum((v1 - mean1) ** 2 for v1 in values1)
    sum_sq2 = sum((v2 - mean2) ** 2 for v2 in values2)
    
    if sum_sq1 == 0 or sum_sq2 == 0:
        return 0.5
    
    correlation = numerator / (sum_sq1 * sum_sq2) ** 0.5
    
    # Convert to 0-1 scale
    return max(0, min(1, (correlation + 1) / 2))

def generate_comprehensive_recommendations(psychometric_results, ikigai_data, intersections):
    """Generate comprehensive career recommendations"""
    recommendations = []
    
    for career_name, career_data in CAREER_DATABASE.items():
        # Psychometric compatibility
        psych_score = calculate_psychometric_compatibility(
            psychometric_results["trait_scores"],
            career_data["psychometric_fit"]
        )
        
        # Ikigai alignment
        ikigai_score = calculate_career_ikigai_alignment(
            intersections,
            career_data["ikigai_intersections"]
        )
        
        # Combined score
        combined_score = (psych_score * 0.4) + (ikigai_score * 0.6)  # Weight Ikigai more
        
        recommendations.append({
            "career": career_name,
            "data": career_data,
            "psychometric_score": psych_score,
            "ikigai_score": ikigai_score,
            "combined_score": combined_score,
            "match_percentage": int(combined_score * 100)
        })
    
    # Sort by combined score
    recommendations.sort(key=lambda x: x["combined_score"], reverse=True)
    
    return recommendations[:5]  # Top 5 recommendations

def calculate_psychometric_compatibility(user_traits, career_traits):
    """Calculate compatibility between user and career traits"""
    if not user_traits or not career_traits:
        return 0.5
    
    compatibility_score = 0
    trait_count = 0
    
    for trait, ideal_score in career_traits.items():
        if trait in user_traits:
            user_score = user_traits[trait]
            # Calculate distance (lower is better)
            distance = abs(user_score - ideal_score)
            # Convert to compatibility (higher is better)
            trait_compatibility = 1 - (distance / 5)  # Normalize by max distance
            compatibility_score += max(0, trait_compatibility)
            trait_count += 1
    
    return compatibility_score / trait_count if trait_count > 0 else 0.5

def calculate_career_ikigai_alignment(intersections, career_intersections):
    """Calculate how well career aligns with user's Ikigai"""
    if not career_intersections:
        return 0.5
    
    total_score = 0
    for intersection in career_intersections:
        if intersection in intersections:
            total_score += intersections[intersection]["score"]
    
    return total_score / len(career_intersections)

def layer_3_career_navigation():
    """Layer 3: Career navigation and action planning"""
    
    st.markdown("""
    <div class="ikigai-section fade-in">
        <div class="ikigai-header">
            <h2>🎯 Your Career Navigation Results</h2>
            <p style="color: var(--text-secondary); font-size: 1.1rem;">
                Comprehensive analysis combining personality and purpose
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.final_recommendations:
        results = st.session_state.final_recommendations
        
        # Ikigai Summary
        st.markdown("### 🌸 Your Ikigai Profile")
        ikigai_cols = st.columns(4)
        intersection_names = ["Passion", "Mission", "Profession", "Vocation"]
        
        for i, (intersection, data) in enumerate(list(results["ikigai_intersections"].items())[:4]):
            with ikigai_cols[i]:
                score_percentage = int(data["score"] * 100)
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-value">{score_percentage}%</div>
                    <div class="metric-label">{intersection}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Overall Ikigai Score
        overall_score = int(results["ikigai_intersections"]["Ikigai_Center"]["score"] * 100)
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <div style="background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary)); 
                        border-radius: 50%; width: 150px; height: 150px; margin: 0 auto;
                        display: flex; flex-direction: column; align-items: center; justify-content: center;
                        color: white; font-weight: 700;">
                <div style="font-size: 2.5rem;">{overall_score}%</div>
                <div>Ikigai Score</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Career Recommendations
        st.markdown("### 🚀 Top Career Recommendations")
        
        for i, rec in enumerate(results["career_recommendations"][:3]):
            with st.container():
                st.markdown(f"""
                <div class="result-card fade-in">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h3 style="color: var(--accent-color); margin: 0;">
                            #{i+1} {rec['career']}
                        </h3>
                        <div style="background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
                                    color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
                            {rec['match_percentage']}% Match
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Description:** {rec['data']['description']}")
                    st.write(f"**Growth Rate:** {rec['data']['growth_rate']}")
                    st.write(f"**Salary Range:** {rec['data']['salary_range']}")
                    
                    # Skill requirements
                    skills = ", ".join(rec['data']['skills'][:5])
                    st.write(f"**Key Skills:** {skills}")
                
                with col2:
                    st.write("**Match Breakdown:**")
                    psych_percent = int(rec['psychometric_score'] * 100)
                    ikigai_percent = int(rec['ikigai_score'] * 100)
                    
                    st.markdown(f"""
                    <div style="margin: 0.5rem 0;">
                        <div>Personality: {psych_percent}%</div>
                        <div class="trait-bar">
                            <div class="trait-fill" style="width: {psych_percent}%"></div>
                        </div>
                    </div>
                    <div style="margin: 0.5rem 0;">
                        <div>Ikigai: {ikigai_percent}%</div>
                        <div class="trait-bar">
                            <div class="trait-fill" style="width: {ikigai_percent}%"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Action Planning
        st.markdown("### 📋 Your Action Plan")
        
        action_tabs = st.tabs(["🎯 Immediate Steps", "📚 Learning Plan", "🤝 Networking", "📊 Progress Tracking"])
        
        with action_tabs[0]:
            st.markdown("#### Next 30 Days")
            top_career = results["career_recommendations"][0]
            st.write(f"**Focus Career:** {top_career['career']}")
            
            immediate_steps = [
                f"Research {top_career['career']} job market in your area",
                f"Identify 3-5 companies hiring for {top_career['career']} roles", 
                "Update your resume highlighting relevant experience",
                "Join professional communities related to your target field",
                "Set up job alerts for relevant positions"
            ]
            
            for step in immediate_steps:
                st.checkbox(step, key=f"immediate_{hash(step)}")
        
        with action_tabs[1]:
            st.markdown("#### Skills Development (Next 3 Months)")
            top_career = results["career_recommendations"][0]
            skills_to_develop = top_career['data']['skills'][:3]
            
            for skill in skills_to_develop:
                st.write(f"**{skill.replace('_', ' ').title()}**")
                st.write(f"- Find online courses or certifications")
                st.write(f"- Practice through personal projects")
                st.write(f"- Join communities focused on {skill}")
                st.write("")
        
        with action_tabs[2]:
            st.markdown("#### Networking Strategy")
            st.write("**Professional Networks to Join:**")
            st.write("- LinkedIn groups in your target industry")
            st.write("- Local professional meetups and events") 
            st.write("- Industry conferences and webinars")
            st.write("- Alumni networks from your educational background")
            
            st.write("**People to Connect With:**")
            st.write("- Current professionals in your target roles")
            st.write("- Hiring managers at companies of interest")
            st.write("- Mentors who can guide your career transition")
            st.write("- Peers who are on similar career paths")
        
        with action_tabs[3]:
            st.markdown("#### Track Your Progress")
            st.write("**Weekly Check-ins:**")
            st.write("- Applications submitted")
            st.write("- New connections made") 
            st.write("- Skills practiced/learned")
            st.write("- Interview opportunities")
            
            st.write("**Monthly Reviews:**")
            st.write("- Progress toward learning goals")
            st.write("- Network expansion")
            st.write("- Market research findings")
            st.write("- Strategy adjustments needed")
        
        st.markdown("---")
        
        # Download Options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Download Complete Report", use_container_width=True):
                report_text = generate_text_report()
                st.download_button(
                    "💾 Download Text Report",
                    report_text,
                    "career_analysis_complete.txt",
                    "text/plain",
                    use_container_width=True
                )
        
        with col2:
            if st.button("🔄 Retake Assessment", use_container_width=True):
                # Reset session state
                for key in ['current_layer', 'psychometric_answers', 'psychometric_results', 'ikigai_data', 'final_recommendations']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        with col3:
            if st.button("💾 Save Progress", use_container_width=True):
                # Generate JSON export
                export_data = {
                    "psychometric_results": st.session_state.psychometric_results,
                    "ikigai_data": st.session_state.ikigai_data,
                    "final_recommendations": st.session_state.final_recommendations,
                    "exported_at": datetime.now().isoformat()
                }
                
                st.download_button(
                    "💾 Download JSON",
                    json.dumps(export_data, indent=2),
                    "career_analysis_data.json",
                    "application/json",
                    use_container_width=True
                )

def generate_text_report():
    """Generate comprehensive text report"""
    if not st.session_state.final_recommendations:
        return "No analysis data available"
    
    results = st.session_state.final_recommendations
    psychometric = st.session_state.psychometric_results
    
    report = """
PATH-FINDER: COMPLETE CAREER ANALYSIS REPORT
============================================

Generated on: {date}

EXECUTIVE SUMMARY
================
This comprehensive analysis combines personality assessment with Ikigai discovery 
to provide personalized career recommendations based on your psychological profile 
and life purpose alignment.

PERSONALITY PROFILE
==================
{personality_summary}

BIG FIVE TRAIT SCORES
====================
""".format(
        date=datetime.now().strftime("%B %d, %Y"),
        personality_summary=psychometric["analysis"]["summary"]
    )
    
    for trait, score in psychometric["trait_scores"].items():
        trait_info = BIG_FIVE_TRAITS.get(trait, {"name": trait.title()})
        percentage = int((score / 5) * 100)
        report += f"{trait_info['name']}: {percentage}%\n"
    
    report += f"""

IKIGAI ANALYSIS
===============
Overall Ikigai Score: {int(results["ikigai_intersections"]["Ikigai_Center"]["score"] * 100)}%

Intersection Scores:
"""
    
    for intersection, data in results["ikigai_intersections"].items():
        if intersection != "Ikigai_Center":
            score_percent = int(data["score"] * 100)
            report += f"- {intersection}: {score_percent}% - {data['description']}\n"
    
    report += """

TOP CAREER RECOMMENDATIONS
==========================
"""
    
    for i, rec in enumerate(results["career_recommendations"][:3], 1):
        report += f"""
{i}. {rec['career']} ({rec['match_percentage']}% Match)
   Description: {rec['data']['description']}
   Salary Range: {rec['data']['salary_range']}
   Growth Rate: {rec['data']['growth_rate']}
   Key Skills: {', '.join(rec['data']['skills'][:5])}
   Personality Match: {int(rec['psychometric_score'] * 100)}%
   Ikigai Alignment: {int(rec['ikigai_score'] * 100)}%

"""
    
    report += """
NEXT STEPS
==========
1. Focus on your top career match and research the industry
2. Develop skills highlighted in your recommendations
3. Network with professionals in your target field
4. Update your resume to highlight relevant experience
5. Set up job alerts and start applying to relevant positions

Remember: Career discovery is a journey. Use this analysis as a starting 
point for deeper self-reflection and professional growth.
"""
    
    return report

if __name__ == "__main__":
    main()