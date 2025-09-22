import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import io
import os
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# Configure page
st.set_page_config(
    page_title="Ikigai Career Guidance",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ikigai-focused career database with intersection mappings
CAREER_DATABASE = {
    "Data Scientist": {
        "skills": ["programming", "mathematics", "analytical_thinking", "statistics", "machine_learning"],
        "growth_rate": "High",
        "salary_range": "$70,000 - $150,000",
        "description": "Analyze complex data to help organizations make decisions",
        "ikigai_intersections": ["Profession", "Vocation"],  # Good at + Paid for, World needs + Paid for
        "what_you_love": ["solving puzzles", "discovering patterns", "working with data"],
        "what_youre_good_at": ["mathematics", "programming", "analytical thinking"],
        "what_world_needs": ["data-driven decisions", "business insights", "predictive analytics"],
        "what_you_can_be_paid_for": ["data analysis", "machine learning models", "business intelligence"]
    },
    "Web Developer": {
        "skills": ["programming", "web_technologies", "design", "problem_solving", "teamwork"],
        "growth_rate": "Very High",
        "salary_range": "$50,000 - $120,000", 
        "description": "Build and maintain websites and web applications",
        "ikigai_intersections": ["Passion", "Profession"],
        "what_you_love": ["creating digital experiences", "building applications", "visual design"],
        "what_youre_good_at": ["programming", "web technologies", "problem solving"],
        "what_world_needs": ["digital presence", "online services", "user-friendly interfaces"],
        "what_you_can_be_paid_for": ["website development", "application building", "digital solutions"]
    },
    "UX/UI Designer": {
        "skills": ["design", "creativity", "user_research", "prototyping", "communication"],
        "growth_rate": "High",
        "salary_range": "$55,000 - $130,000",
        "description": "Design user interfaces and improve user experiences",
        "ikigai_intersections": ["Passion", "Mission"],
        "what_you_love": ["creative problem solving", "user empathy", "visual aesthetics"],
        "what_youre_good_at": ["design thinking", "prototyping", "user research"],
        "what_world_needs": ["intuitive interfaces", "accessible design", "better user experiences"],
        "what_you_can_be_paid_for": ["user interface design", "user experience consulting", "design systems"]
    },
    "Business Consultant": {
        "skills": ["analytical_thinking", "communication", "strategic_planning", "leadership", "problem_solving"],
        "growth_rate": "Medium",
        "salary_range": "$60,000 - $140,000",
        "description": "Advise organizations on business strategy and operations",
        "ikigai_intersections": ["Mission", "Vocation"],
        "what_you_love": ["helping organizations grow", "strategic thinking", "problem solving"],
        "what_youre_good_at": ["analysis", "communication", "strategic planning"],
        "what_world_needs": ["business optimization", "strategic guidance", "organizational improvement"],
        "what_you_can_be_paid_for": ["consulting services", "strategic planning", "business analysis"]
    },
    "Product Manager": {
        "skills": ["strategic_planning", "communication", "leadership", "market_analysis", "project_management"],
        "growth_rate": "High",
        "salary_range": "$70,000 - $160,000",
        "description": "Guide product development from conception to launch",
        "ikigai_intersections": ["Passion", "Vocation"],
        "what_you_love": ["bringing ideas to life", "user-centered solutions", "innovation"],
        "what_youre_good_at": ["strategic thinking", "communication", "project management"],
        "what_world_needs": ["innovative products", "user solutions", "market-driven development"],
        "what_you_can_be_paid_for": ["product strategy", "product development", "market analysis"]
    },
    "Digital Marketing Manager": {
        "skills": ["marketing", "communication", "analytical_thinking", "creativity", "strategic_planning"],
        "growth_rate": "High",
        "salary_range": "$45,000 - $100,000",
        "description": "Plan and execute digital marketing campaigns",
        "ikigai_intersections": ["Passion", "Profession"],
        "what_you_love": ["creative storytelling", "connecting with audiences", "brand building"],
        "what_youre_good_at": ["marketing strategy", "content creation", "data analysis"],
        "what_world_needs": ["brand awareness", "customer engagement", "digital presence"],
        "what_you_can_be_paid_for": ["marketing campaigns", "brand strategy", "digital advertising"]
    },
    "AI/ML Engineer": {
        "skills": ["programming", "machine_learning", "mathematics", "analytical_thinking", "research"],
        "growth_rate": "Very High",
        "salary_range": "$80,000 - $180,000",
        "description": "Develop artificial intelligence and machine learning systems",
        "ikigai_intersections": ["Profession", "Vocation"],
        "what_you_love": ["cutting-edge technology", "solving complex problems", "innovation"],
        "what_youre_good_at": ["programming", "mathematics", "algorithmic thinking"],
        "what_world_needs": ["intelligent automation", "predictive systems", "AI solutions"],
        "what_you_can_be_paid_for": ["AI development", "machine learning models", "automation systems"]
    },
    "Technical Writer": {
        "skills": ["technical_writing", "communication", "research", "attention_to_detail", "adaptability"],
        "growth_rate": "Medium",
        "salary_range": "$45,000 - $90,000",
        "description": "Create technical documentation and instructional materials",
        "ikigai_intersections": ["Mission", "Vocation"],
        "what_you_love": ["clear communication", "helping others learn", "simplifying complexity"],
        "what_youre_good_at": ["writing", "research", "technical understanding"],
        "what_world_needs": ["clear documentation", "knowledge transfer", "technical education"],
        "what_you_can_be_paid_for": ["technical documentation", "instructional design", "content creation"]
    }
}

# Skills mapping for normalization
SKILLS_MAPPING = {
    "programming": ["programming", "coding", "software_development"],
    "mathematics": ["mathematics", "math", "statistics", "calculus"],
    "analytical_thinking": ["analytical_thinking", "analysis", "critical_thinking"],
    "communication": ["communication", "presentation", "writing"],
    "leadership": ["leadership", "management", "team_building"],
    "creativity": ["creativity", "design", "innovation"],
    "problem_solving": ["problem_solving", "troubleshooting"],
    "teamwork": ["teamwork", "collaboration", "interpersonal"],
    "strategic_planning": ["strategic_planning", "strategy", "planning"],
    "marketing": ["marketing", "advertising", "branding"],
    "project_management": ["project_management", "organization"],
    "adaptability": ["adaptability", "flexibility", "learning_agility"],
    "technical_writing": ["technical_writing", "documentation"],
    "research": ["research", "investigation"],
    "design": ["design", "visual_design", "graphic_design"],
    "machine_learning": ["machine_learning", "ai", "artificial_intelligence"],
    "web_technologies": ["web_technologies", "html", "css", "javascript"],
    "user_research": ["user_research", "ux_research"],
    "prototyping": ["prototyping", "wireframing"],
    "market_analysis": ["market_analysis", "market_research"],
    "attention_to_detail": ["attention_to_detail", "detail_oriented"]
}

def load_sample_users():
    """Load sample users data from CSV"""
    try:
        if os.path.exists("sampleusers.csv"):
            return pd.read_csv("sampleusers.csv")
        else:
            # Return empty dataframe if file doesn't exist
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading sample users: {str(e)}")
        return pd.DataFrame()

def normalize_skills(skills_dict):
    """Normalize skills to match career database format"""
    normalized = {}
    for skill, value in skills_dict.items():
        # Find the canonical skill name
        canonical_skill = skill.lower().replace(" ", "_")
        for canonical, variants in SKILLS_MAPPING.items():
            if canonical_skill in variants or canonical_skill == canonical:
                normalized[canonical] = value
                break
        else:
            # Keep original if no mapping found
            normalized[canonical_skill] = value
    return normalized

def calculate_career_match(user_skills, career_requirements):
    """Calculate how well user skills match career requirements"""
    user_skills_norm = normalize_skills(user_skills)
    
    # Create vectors for comparison
    all_skills = set(user_skills_norm.keys()) | set(career_requirements)
    
    user_vector = [user_skills_norm.get(skill, 0) for skill in all_skills]
    career_vector = [3 if skill in career_requirements else 0 for skill in all_skills]  # 3 as baseline requirement
    
    # Calculate cosine similarity
    if sum(user_vector) == 0 or sum(career_vector) == 0:
        return 0
    
    similarity = cosine_similarity([user_vector], [career_vector])[0][0]
    
    # Boost score if user has high ratings in required skills
    boost = sum(user_skills_norm.get(skill, 0) for skill in career_requirements) / (len(career_requirements) * 5)
    
    return min(similarity + boost, 1.0)

def calculate_ikigai_intersections(ikigai_data):
    """Calculate Ikigai intersections based on user responses"""
    love = ikigai_data.get("what_you_love", {})
    good_at = ikigai_data.get("what_youre_good_at", {})
    world_needs = ikigai_data.get("what_world_needs", {})
    paid_for = ikigai_data.get("what_you_can_be_paid_for", {})
    
    intersections = {}
    
    # Passion: What you love ∩ What you're good at
    passion_score = calculate_intersection_score_improved(love, good_at)
    passion_elements = find_common_elements_improved(love, good_at)
    intersections["Passion"] = {
        "score": passion_score,
        "description": "What you love and are good at",
        "elements": passion_elements
    }
    
    # Mission: What you love ∩ What the world needs
    mission_score = calculate_intersection_score_improved(love, world_needs)
    mission_elements = find_common_elements_improved(love, world_needs)
    intersections["Mission"] = {
        "score": mission_score,
        "description": "What you love and the world needs",
        "elements": mission_elements
    }
    
    # Profession: What you're good at ∩ What you can be paid for
    profession_score = calculate_intersection_score_improved(good_at, paid_for)
    profession_elements = find_common_elements_improved(good_at, paid_for)
    intersections["Profession"] = {
        "score": profession_score,
        "description": "What you're good at and can be paid for",
        "elements": profession_elements
    }
    
    # Vocation: What the world needs ∩ What you can be paid for
    vocation_score = calculate_intersection_score_improved(world_needs, paid_for)
    vocation_elements = find_common_elements_improved(world_needs, paid_for)
    intersections["Vocation"] = {
        "score": vocation_score,
        "description": "What the world needs and you can be paid for",
        "elements": vocation_elements
    }
    
    # Ikigai center: combination of all quadrants
    ikigai_center_score = (passion_score + mission_score + profession_score + vocation_score) / 4
    intersections["Ikigai_Center"] = {
        "score": ikigai_center_score,
        "description": "Perfect balance of all four elements",
        "elements": []
    }
    
    return intersections

def calculate_intersection_score_improved(dict1, dict2):
    """Improved calculation of overlap score between two dictionaries"""
    if not dict1 or not dict2:
        return 0.0
    
    # Create semantic mappings for related concepts
    semantic_mappings = {
        "creative_problem_solving": ["design_thinking", "creative_content", "artistic_expression"],
        "technology_innovation": ["software_development", "digital_transformation", "data_analysis"],
        "helping_others": ["education_access", "social_impact", "training_programs"],
        "strategic_thinking": ["strategic_planning", "business_optimization", "project_management"],
        "communication": ["content_creation", "marketing_campaigns", "technical_writing"],
        "leadership": ["project_management", "strategic_planning", "training_programs"],
        "programming": ["software_development", "technical_writing", "data_analysis"],
        "mathematical_analysis": ["data_analysis", "research_projects"],
        "design_thinking": ["design_services", "better_user_experiences"],
        "marketing": ["marketing_campaigns", "content_creation"],
        "research": ["research_projects", "technical_writing"],
        "analytical_thinking": ["data_analysis", "consulting_services", "research_projects"]
    }
    
    total_score = 0
    matches_found = 0
    
    # Direct matches
    for key1, value1 in dict1.items():
        if key1 in dict2:
            # Direct key match
            avg_score = (value1 + dict2[key1]) / 2
            total_score += avg_score
            matches_found += 1
        else:
            # Check for semantic matches
            related_keys = semantic_mappings.get(key1, [])
            for related_key in related_keys:
                if related_key in dict2:
                    # Semantic match with slight penalty
                    avg_score = (value1 + dict2[related_key]) / 2 * 0.8
                    total_score += avg_score
                    matches_found += 1
                    break
    
    # If no matches found, check for high-scoring items in both categories
    if matches_found == 0:
        high_scores_1 = [k for k, v in dict1.items() if v >= 4]
        high_scores_2 = [k for k, v in dict2.items() if v >= 4]
        
        if high_scores_1 and high_scores_2:
            # Give partial score for having high ratings in both areas
            total_score = 2.0  # Base compatibility score
            matches_found = 1
    
    if matches_found == 0:
        return 0.0
    
    # Normalize to 0-1 scale
    normalized_score = total_score / (matches_found * 5)
    return min(normalized_score, 1.0)

def find_common_elements_improved(dict1, dict2):
    """Find elements that exist in both dictionaries with high scores"""
    common_elements = []
    
    # Direct matches
    common_keys = set(dict1.keys()) & set(dict2.keys())
    for key in common_keys:
        if dict1[key] >= 3 and dict2[key] >= 3:
            common_elements.append(key.replace("_", " ").title())
    
    # Semantic matches for high-scoring items
    semantic_mappings = {
        "creative_problem_solving": ["design_thinking", "creative_content"],
        "technology_innovation": ["software_development", "digital_transformation"],
        "helping_others": ["education_access", "social_impact"],
        "strategic_thinking": ["strategic_planning", "business_optimization"],
        "communication": ["content_creation", "marketing_campaigns"],
        "programming": ["software_development", "data_analysis"],
        "design_thinking": ["design_services", "better_user_experiences"]
    }
    
    for key1, value1 in dict1.items():
        if value1 >= 4:  # High score in first category
            related_keys = semantic_mappings.get(key1, [])
            for related_key in related_keys:
                if related_key in dict2 and dict2[related_key] >= 3:
                    element_name = f"{key1.replace('_', ' ').title()} → {related_key.replace('_', ' ').title()}"
                    if element_name not in common_elements:
                        common_elements.append(element_name)
    
    return common_elements if common_elements else ["Areas for development identified"]

def calculate_career_match_ikigai(ikigai_intersections, career_name):
    """Calculate career match based on Ikigai intersections"""
    career_info = CAREER_DATABASE[career_name]
    career_intersections = career_info.get("ikigai_intersections", [])
    
    if not career_intersections:
        return 0.0
    
    total_score = 0
    intersection_count = 0
    
    # Calculate score based on relevant intersections
    for intersection in career_intersections:
        if intersection in ikigai_intersections:
            intersection_score = ikigai_intersections[intersection]["score"]
            total_score += intersection_score
            intersection_count += 1
    
    if intersection_count == 0:
        return 0.0
    
    # Base score from intersection alignment
    base_score = total_score / intersection_count
    
    # Bonus for multiple intersection alignment
    if intersection_count > 1:
        base_score *= 1.3
    
    # Bonus for high overall Ikigai center score
    ikigai_center_score = ikigai_intersections.get("Ikigai_Center", {}).get("score", 0)
    if ikigai_center_score > 0.5:
        base_score += (ikigai_center_score * 0.2)
    
    # Ensure we have a minimum score for any career if user has some alignment
    if base_score == 0 and ikigai_center_score > 0.3:
        base_score = 0.15  # Minimum viable score
    
    return min(base_score, 1.0)

def generate_skill_gap_analysis(user_skills, recommended_careers):
    """Generate skill gap analysis for recommended careers"""
    gaps = {}
    
    for career in recommended_careers:
        career_info = CAREER_DATABASE[career]
        required_skills = career_info["skills"]
        
        user_skills_norm = normalize_skills(user_skills)
        gap_analysis = []
        
        for skill in required_skills:
            user_level = user_skills_norm.get(skill, 0)
            if user_level < 3:  # Below proficient level
                gap_analysis.append({
                    "skill": skill.replace("_", " ").title(),
                    "current_level": user_level,
                    "target_level": 4,
                    "gap": 4 - user_level
                })
        
        gaps[career] = gap_analysis
    
    return gaps

def generate_learning_roadmap(skill_gaps, user_type):
    """Generate a 12-week learning roadmap"""
    roadmap = []
    
    # Base roadmap structure
    weeks = 12
    skills_to_develop = []
    
    # Collect all skills that need improvement
    for career, gaps in skill_gaps.items():
        for gap in gaps:
            if gap["gap"] > 0:
                skills_to_develop.append(gap["skill"])
    
    # Remove duplicates and prioritize
    unique_skills = list(set(skills_to_develop))
    
    # Create weekly plan
    skills_per_week = max(1, len(unique_skills) // weeks) if unique_skills else 1
    
    for week in range(1, weeks + 1):
        week_plan = {
            "week": week,
            "focus_area": "",
            "learning_goals": [],
            "resources": [],
            "milestones": []
        }
        
        if week <= 4:  # Foundation phase
            week_plan["focus_area"] = "Foundation Building"
            if unique_skills:
                skill = unique_skills[(week - 1) % len(unique_skills)]
                week_plan["learning_goals"] = [f"Learn basics of {skill}"]
                week_plan["resources"] = [f"Online courses for {skill}", f"{skill} tutorials and documentation"]
                week_plan["milestones"] = [f"Complete introductory {skill} course"]
        elif week <= 8:  # Skill development phase
            week_plan["focus_area"] = "Skill Development"
            if unique_skills:
                skill = unique_skills[(week - 5) % len(unique_skills)]
                week_plan["learning_goals"] = [f"Practice intermediate {skill}"]
                week_plan["resources"] = [f"Hands-on {skill} projects", f"{skill} practice platforms"]
                week_plan["milestones"] = [f"Complete 2-3 {skill} projects"]
        else:  # Application phase
            week_plan["focus_area"] = "Application & Portfolio"
            week_plan["learning_goals"] = ["Build portfolio projects", "Apply learned skills"]
            week_plan["resources"] = ["Portfolio platforms", "Project showcases", "Professional networks"]
            week_plan["milestones"] = ["Complete portfolio project", "Get feedback from professionals"]
        
        roadmap.append(week_plan)
    
    return roadmap

def main():
    st.title("� Ikigai Career Guidance Platform")
    st.markdown("### Discover your purpose through the ancient Japanese concept of Ikigai")
    st.markdown("*Find your reason for being at the intersection of what you love, what you're good at, what the world needs, and what you can be paid for.*")
    
    # Sidebar for user type selection
    st.sidebar.title("🎯 Career Discovery Setup")
    
    # Load demo data option
    sample_users = load_sample_users()
    if not sample_users.empty:
        use_demo = st.sidebar.checkbox("📊 Use Demo Data", help="Load sample user profile for testing")
        if use_demo:
            demo_user = st.sidebar.selectbox("Select Demo User", sample_users['name'].tolist())
            selected_demo = sample_users[sample_users['name'] == demo_user].iloc[0]
    else:
        use_demo = False
    
    user_type = st.sidebar.selectbox(
        "👤 Select Your Profile Type",
        ["Student", "Graduate", "Professional", "Career Changer"],
        help="Choose the category that best describes your current situation"
    )
    
    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(f"🌸 Ikigai Assessment for {user_type}")
        st.markdown("*Complete each quadrant to discover your career purpose*")
        
        # Ikigai-focused form
        with st.form("ikigai_assessment"):
            # Basic information
            name = st.text_input("Full Name", value=selected_demo['name'] if use_demo else "")
            age = st.number_input("Age", min_value=16, max_value=70, value=int(selected_demo['age']) if use_demo else 25)
            
            # Ikigai Quadrant 1: What You Love
            st.subheader("💝 What You Love")
            st.markdown("*Your passions, interests, and what energizes you*")
            
            what_you_love = {}
            love_options = [
                "Creative Problem Solving", "Helping Others", "Technology Innovation", 
                "Artistic Expression", "Learning New Things", "Leading Teams",
                "Analyzing Data", "Building Solutions", "Teaching Others", "Strategic Thinking"
            ]
            
            for i, option in enumerate(love_options):
                if i % 2 == 0:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        what_you_love[option.lower().replace(" ", "_")] = st.slider(
                            f"{option}", 1, 5, 3, key=f"love_{option}"
                        )
                else:
                    with col_b:
                        what_you_love[option.lower().replace(" ", "_")] = st.slider(
                            f"{option}", 1, 5, 3, key=f"love_{option}"
                        )
            
            # Ikigai Quadrant 2: What You're Good At
            st.subheader("💪 What You're Good At")
            st.markdown("*Your skills, talents, and natural abilities*")
            
            what_youre_good_at = {}
            skills_options = [
                "Programming", "Communication", "Mathematical Analysis", "Design Thinking",
                "Project Management", "Research", "Writing", "Leadership",
                "Marketing", "Problem Solving", "Data Analysis", "Creativity"
            ]
            
            for i, skill in enumerate(skills_options):
                if i % 2 == 0:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        what_youre_good_at[skill.lower().replace(" ", "_")] = st.slider(
                            f"{skill}", 1, 5, 2, key=f"skill_{skill}"
                        )
                else:
                    with col_b:
                        what_youre_good_at[skill.lower().replace(" ", "_")] = st.slider(
                            f"{skill}", 1, 5, 2, key=f"skill_{skill}"
                        )
            
            # Ikigai Quadrant 3: What the World Needs
            st.subheader("🌍 What the World Needs")
            st.markdown("*Problems you want to solve and impact you want to make*")
            
            what_world_needs = {}
            world_needs_options = [
                "Digital Transformation", "Sustainable Solutions", "Education Access", "Healthcare Innovation",
                "Better User Experiences", "Data-Driven Decisions", "Creative Content", "Business Optimization",
                "Technology Accessibility", "Social Impact", "Environmental Protection", "Economic Growth"
            ]
            
            for i, need in enumerate(world_needs_options):
                if i % 2 == 0:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        what_world_needs[need.lower().replace(" ", "_")] = st.slider(
                            f"{need}", 1, 5, 3, key=f"need_{need}"
                        )
                else:
                    with col_b:
                        what_world_needs[need.lower().replace(" ", "_")] = st.slider(
                            f"{need}", 1, 5, 3, key=f"need_{need}"
                        )
            
            # Ikigai Quadrant 4: What You Can Be Paid For
            st.subheader("💰 What You Can Be Paid For")
            st.markdown("*Market demands and monetizable skills*")
            
            what_you_can_be_paid_for = {}
            paid_for_options = [
                "Software Development", "Consulting Services", "Content Creation", "Design Services",
                "Data Analysis", "Marketing Campaigns", "Training Programs", "Research Projects",
                "Product Development", "Strategic Planning", "Technical Writing", "Project Management"
            ]
            
            for i, paid_skill in enumerate(paid_for_options):
                if i % 2 == 0:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        what_you_can_be_paid_for[paid_skill.lower().replace(" ", "_")] = st.slider(
                            f"{paid_skill}", 1, 5, 3, key=f"paid_{paid_skill}"
                        )
                else:
                    with col_b:
                        what_you_can_be_paid_for[paid_skill.lower().replace(" ", "_")] = st.slider(
                            f"{paid_skill}", 1, 5, 3, key=f"paid_{paid_skill}"
                        )
            
            # User type specific questions
            additional_info = {}
            
            if user_type == "Student":
                st.subheader("🎓 Academic Context")
                additional_info["field_of_study"] = st.text_input("Field of Study", "")
                additional_info["academic_year"] = st.selectbox("Academic Year", ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduate"])
                
            elif user_type == "Graduate":
                st.subheader("🎓 Recent Graduate Info")
                additional_info["degree"] = st.text_input("Degree", "")
                additional_info["graduation_year"] = st.number_input("Graduation Year", min_value=2020, max_value=2025, value=2024)
                
            elif user_type == "Professional":
                st.subheader("💼 Professional Background")
                additional_info["years_experience"] = st.number_input("Years of Experience", min_value=0, max_value=50, value=5)
                additional_info["current_role"] = st.text_input("Current Role", "")
                additional_info["industry"] = st.text_input("Current Industry", "")
                
            elif user_type == "Career Changer":
                st.subheader("🔄 Career Transition")
                additional_info["previous_field"] = st.text_input("Previous Field/Industry", "")
                additional_info["years_in_previous"] = st.number_input("Years in Previous Field", min_value=0, max_value=50, value=5)
                additional_info["reason_for_change"] = st.text_area("Reason for Career Change", "")
            
            submitted = st.form_submit_button("🌸 Discover My Ikigai", type="primary")
            
            if submitted:
                # Store Ikigai data in session state
                st.session_state.ikigai_data = {
                    "name": name,
                    "age": age,
                    "user_type": user_type,
                    "what_you_love": what_you_love,
                    "what_youre_good_at": what_youre_good_at,
                    "what_world_needs": what_world_needs,
                    "what_you_can_be_paid_for": what_you_can_be_paid_for,
                    "additional_info": additional_info
                }
                st.session_state.analysis_complete = True
                st.rerun()
    
    with col2:
        st.header("🌸 About Ikigai")
        st.info("""
        **Ikigai (生き甲斐)** is a Japanese concept meaning "reason for being."
        
        � **Passion** = Love ∩ Good At
        🔹 **Mission** = Love ∩ World Needs  
        🔹 **Profession** = Good At ∩ Paid For
        🔹 **Vocation** = World Needs ∩ Paid For
        
        Your **Ikigai** lies at the center where all four elements intersect.
        """)
        
        if not sample_users.empty:
            st.header("👥 Demo Users")
            st.dataframe(sample_users[['name', 'user_type', 'suggested_career']].head(), width='stretch')
    
    # Results section
    if st.session_state.analysis_complete and 'ikigai_data' in st.session_state:
        st.markdown("---")
        display_ikigai_results(st.session_state.ikigai_data)

def display_ikigai_results(ikigai_data):
    """Display Ikigai-based analysis results"""
    st.header("🌸 Your Ikigai Analysis Results")
    
    # Debug information to help identify issues
    with st.expander("🔍 Debug Information", expanded=False):
        st.write("**Input Data Summary:**")
        for quadrant in ["what_you_love", "what_youre_good_at", "what_world_needs", "what_you_can_be_paid_for"]:
            data = ikigai_data.get(quadrant, {})
            high_scores = [f"{k}: {v}" for k, v in data.items() if v >= 4]
            st.write(f"**{quadrant.replace('_', ' ').title()}:** {len(high_scores)} high scores (4+)")
            if high_scores:
                st.write(", ".join(high_scores[:5]))
    
    # Calculate Ikigai intersections
    intersections = calculate_ikigai_intersections(ikigai_data)
    
    # Calculate career matches using Ikigai methodology
    career_scores = {}
    for career_name in CAREER_DATABASE.keys():
        score = calculate_career_match_ikigai(intersections, career_name)
        career_scores[career_name] = score
    
    # Sort careers by Ikigai alignment
    recommended_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Display Ikigai intersections
    st.subheader("🎯 Your Ikigai Intersections")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Passion quadrant
        passion = intersections["Passion"]
        with st.expander(f"🔥 Passion (Score: {passion['score']:.2f})", expanded=True):
            st.write("**What you love AND are good at**")
            if passion['elements']:
                for element in passion['elements']:
                    st.write(f"• {element}")
            else:
                st.write("Consider developing skills in areas you're passionate about")
        
        # Profession quadrant  
        profession = intersections["Profession"]
        with st.expander(f"💼 Profession (Score: {profession['score']:.2f})", expanded=True):
            st.write("**What you're good at AND can be paid for**")
            if profession['elements']:
                for element in profession['elements']:
                    st.write(f"• {element}")
            else:
                st.write("Focus on monetizing your existing skills")
    
    with col2:
        # Mission quadrant
        mission = intersections["Mission"]
        with st.expander(f"� Mission (Score: {mission['score']:.2f})", expanded=True):
            st.write("**What you love AND the world needs**")
            if mission['elements']:
                for element in mission['elements']:
                    st.write(f"• {element}")
            else:
                st.write("Explore how your passions can address world problems")
        
        # Vocation quadrant
        vocation = intersections["Vocation"]
        with st.expander(f"🌍 Vocation (Score: {vocation['score']:.2f})", expanded=True):
            st.write("**What the world needs AND you can be paid for**")
            if vocation['elements']:
                for element in vocation['elements']:
                    st.write(f"• {element}")
            else:
                st.write("Look for market opportunities in areas of social need")
    
    # Ikigai Center
    ikigai_center = intersections["Ikigai_Center"]
    if ikigai_center['score'] > 0.6:
        st.success(f"🌸 **Strong Ikigai Alignment!** (Score: {ikigai_center['score']:.2f})")
        st.write("You have a well-balanced foundation for finding your purpose.")
    elif ikigai_center['score'] > 0.4:
        st.warning(f"🌱 **Developing Ikigai** (Score: {ikigai_center['score']:.2f})")
        st.write("You're on the right path. Focus on strengthening weaker quadrants.")
    else:
        st.info(f"🌿 **Exploring Ikigai** (Score: {ikigai_center['score']:.2f})")
        st.write("Take time to explore and develop each quadrant of your Ikigai.")
    
    st.markdown("---")
    
    # Career recommendations based on Ikigai
    st.subheader("🎯 Ikigai-Aligned Career Recommendations")
    
    if all(score == 0 for _, score in recommended_careers):
        st.warning("⚠️ **Limited Career Alignment Detected**")
        st.write("Your current responses show limited direct alignment with our career database. This doesn't mean you lack direction - it may indicate:")
        st.write("• Unique combination of interests that could lead to innovative career paths")
        st.write("• Need for more exploration and self-reflection")
        st.write("• Potential for creating your own career path")
        
        # Show all careers with basic info for exploration
        st.write("**Career Paths to Explore:**")
        for career, info in CAREER_DATABASE.items():
            with st.expander(f"{career} - {info['growth_rate']} Growth Potential"):
                st.write(f"**Description:** {info['description']}")
                st.write(f"**Salary Range:** {info['salary_range']}")
                st.write(f"**Key Skills:** {', '.join(info['skills'][:4])}")
                st.write(f"**Ikigai Focus:** {', '.join(info['ikigai_intersections'])}")
    else:
        for i, (career, score) in enumerate(recommended_careers):
            with st.expander(f"#{i+1} {career} ({score:.1%} Ikigai match)", expanded=(i==0)):
                career_info = CAREER_DATABASE[career]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Description:** {career_info['description']}")
                st.write(f"**Growth Rate:** {career_info['growth_rate']}")
                st.write(f"**Salary Range:** {career_info['salary_range']}")
                
                # Show Ikigai alignment
                st.write("**Ikigai Alignment:**")
                for intersection in career_info['ikigai_intersections']:
                    intersection_score = intersections[intersection]['score']
                    st.write(f"• {intersection}: {intersection_score:.1%}")
            
            with col2:
                st.write("**Key Skills:**")
                for skill in career_info['skills'][:5]:
                    st.write(f"• {skill.replace('_', ' ').title()}")
                
                # Progress bar for Ikigai match
                st.metric("Ikigai Match", f"{score:.1%}")
                st.progress(score)
    
    # Skill development recommendations
    st.markdown("---")
    st.subheader("� Ikigai Development Roadmap")
    
    # Generate personalized roadmap based on Ikigai gaps
    roadmap = generate_ikigai_roadmap(intersections, recommended_careers)
    
    # Display roadmap in phases
    tab1, tab2, tab3, tab4 = st.tabs(["� Strengthen Passion", "🎯 Clarify Mission", "� Build Profession", "🌍 Find Vocation"])
    
    with tab1:
        passion_roadmap = roadmap.get("Passion", [])
        if passion_roadmap:
            for week, activity in enumerate(passion_roadmap, 1):
                st.write(f"**Week {week}:** {activity}")
        else:
            st.success("Your passion quadrant is strong! Focus on other areas.")
    
    with tab2:
        mission_roadmap = roadmap.get("Mission", [])
        if mission_roadmap:
            for week, activity in enumerate(mission_roadmap, 1):
                st.write(f"**Week {week}:** {activity}")
        else:
            st.success("Your mission quadrant is strong! Focus on other areas.")
    
    with tab3:
        profession_roadmap = roadmap.get("Profession", [])
        if profession_roadmap:
            for week, activity in enumerate(profession_roadmap, 1):
                st.write(f"**Week {week}:** {activity}")
        else:
            st.success("Your profession quadrant is strong! Focus on other areas.")
    
    with tab4:
        vocation_roadmap = roadmap.get("Vocation", [])
        if vocation_roadmap:
            for week, activity in enumerate(vocation_roadmap, 1):
                st.write(f"**Week {week}:** {activity}")
        else:
            st.success("Your vocation quadrant is strong! Focus on other areas.")
    
    # Download functionality
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("� Download as PDF", type="secondary", use_container_width=True):
            if PDF_AVAILABLE:
                pdf_buffer = generate_ikigai_pdf(ikigai_data, intersections, recommended_careers, roadmap)
                st.download_button(
                    label="💾 Download PDF Report",
                    data=pdf_buffer,
                    file_name=f"ikigai_analysis_{ikigai_data['name'].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    width='stretch'
                )
            else:
                st.error("PDF generation not available. Please install reportlab: pip install reportlab")
    
    with col2:
        if st.button("📥 Download as Text", type="primary", width='stretch'):
            analysis_text = generate_ikigai_analysis_text(ikigai_data, intersections, recommended_careers, roadmap)
            st.download_button(
                label="💾 Download Text File",
                data=analysis_text,
                file_name=f"ikigai_analysis_{ikigai_data['name'].replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with col3:
        if st.button("🌸 Retake Assessment", type="secondary", width='stretch'):
            # Clear session state to allow retaking the assessment
            for key in ['ikigai_data', 'analysis_complete']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

def generate_ikigai_roadmap(intersections, recommended_careers):
    """Generate development roadmap based on Ikigai gaps"""
    roadmap = {
        "Passion": [],
        "Mission": [],
        "Profession": [],
        "Vocation": []
    }
    
    # Identify weak quadrants (score < 0.5)
    for quadrant, data in intersections.items():
        if quadrant == "Ikigai_Center":
            continue
            
        score = data['score']
        if score < 0.5:
            if quadrant == "Passion":
                roadmap["Passion"] = [
                    "Explore activities that combine your interests with skill-building",
                    "Take personality assessments to better understand your motivations",
                    "Try new hobbies related to your career interests",
                    "Join communities of people doing work you admire"
                ]
            elif quadrant == "Mission":
                roadmap["Mission"] = [
                    "Research social problems you care about",
                    "Volunteer for causes aligned with your values",
                    "Connect with organizations making social impact",
                    "Define your personal mission statement"
                ]
            elif quadrant == "Profession":
                roadmap["Profession"] = [
                    "Identify marketable skills you can develop",
                    "Take online courses in high-demand areas",
                    "Build a portfolio showcasing your abilities",
                    "Network with professionals in your target field"
                ]
            elif quadrant == "Vocation":
                roadmap["Vocation"] = [
                    "Research job market trends and opportunities",
                    "Identify skills gaps in areas of social need",
                    "Explore careers that solve important problems",
                    "Connect with professionals in purpose-driven roles"
                ]
    
    return roadmap

def generate_ikigai_pdf(ikigai_data, intersections, recommended_careers, roadmap):
    """Generate PDF version of Ikigai analysis"""
    if not PDF_AVAILABLE:
        return None
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=20, spaceAfter=30, textColor=colors.darkblue)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=14, spaceAfter=12, textColor=colors.darkgreen)
    normal_style = styles['Normal']
    
    # Build story
    story = []
    
    # Title
    story.append(Paragraph("🌸 Ikigai Career Analysis Report", title_style))
    story.append(Spacer(1, 20))
    
    # Personal Information
    story.append(Paragraph("Personal Information", heading_style))
    personal_info = [
        f"Name: {ikigai_data['name']}",
        f"Age: {ikigai_data['age']}",
        f"Profile Type: {ikigai_data['user_type']}"
    ]
    for info in personal_info:
        story.append(Paragraph(info, normal_style))
    story.append(Spacer(1, 20))
    
    # Ikigai Intersection Scores
    story.append(Paragraph("Ikigai Intersection Analysis", heading_style))
    
    intersection_data = []
    intersection_data.append(['Intersection', 'Score', 'Description'])
    
    for quadrant, data in intersections.items():
        if quadrant != "Ikigai_Center":
            score_text = f"{data['score']:.2f}"
            intersection_data.append([quadrant, score_text, data['description']])
    
    intersection_data.append(['Overall Ikigai', f"{intersections['Ikigai_Center']['score']:.2f}", "Balance of all elements"])
    
    intersection_table = Table(intersection_data, colWidths=[2*inch, 1*inch, 3*inch])
    intersection_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(intersection_table)
    story.append(Spacer(1, 20))
    
    # Career Recommendations
    story.append(Paragraph("Recommended Careers (Ikigai-Aligned)", heading_style))
    
    for i, (career, score) in enumerate(recommended_careers):
        career_info = CAREER_DATABASE[career]
        story.append(Paragraph(f"{i+1}. {career} ({score:.1%} Ikigai match)", normal_style))
        story.append(Paragraph(f"Description: {career_info['description']}", normal_style))
        story.append(Paragraph(f"Growth Rate: {career_info['growth_rate']} | Salary: {career_info['salary_range']}", normal_style))
        story.append(Paragraph(f"Ikigai Intersections: {', '.join(career_info['ikigai_intersections'])}", normal_style))
        story.append(Spacer(1, 10))
    
    story.append(Spacer(1, 20))
    
    # Development Roadmap
    story.append(Paragraph("Ikigai Development Roadmap", heading_style))
    
    for quadrant, activities in roadmap.items():
        if activities:
            story.append(Paragraph(f"{quadrant} Development:", normal_style))
            for i, activity in enumerate(activities, 1):
                story.append(Paragraph(f"Week {i}: {activity}", normal_style))
            story.append(Spacer(1, 10))
    
    # Next Steps
    story.append(Spacer(1, 20))
    story.append(Paragraph("Next Steps", heading_style))
    next_steps = [
        "1. Focus on strengthening your weakest Ikigai quadrant",
        "2. Pursue careers that align with multiple intersections", 
        "3. Continuously reassess and refine your Ikigai",
        "4. Connect your work to your deeper purpose",
        "5. Seek mentorship in your chosen field"
    ]
    
    for step in next_steps:
        story.append(Paragraph(step, normal_style))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("Remember: Ikigai is a journey, not a destination. 🌸", normal_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def generate_ikigai_analysis_text(ikigai_data, intersections, recommended_careers, roadmap):
    """Generate text version of Ikigai analysis for download"""
    text = f"""
IKIGAI CAREER ANALYSIS REPORT
=============================

Personal Information:
- Name: {ikigai_data['name']}
- Age: {ikigai_data['age']}
- Profile Type: {ikigai_data['user_type']}

IKIGAI INTERSECTION SCORES:
===========================
"""
    
    for quadrant, data in intersections.items():
        if quadrant != "Ikigai_Center":
            text += f"\n{quadrant}: {data['score']:.2f}\n"
            text += f"Description: {data['description']}\n"
            if data['elements']:
                text += "Strong Areas:\n"
                for element in data['elements']:
                    text += f"  • {element}\n"
            text += "\n"
    
    text += f"Overall Ikigai Center Score: {intersections['Ikigai_Center']['score']:.2f}\n"
    
    text += f"""

RECOMMENDED CAREERS (Ikigai-Aligned):
====================================
"""
    
    for i, (career, score) in enumerate(recommended_careers):
        career_info = CAREER_DATABASE[career]
        text += f"""
{i+1}. {career} ({score:.1%} Ikigai match)
   Description: {career_info['description']}
   Growth Rate: {career_info['growth_rate']}
   Salary Range: {career_info['salary_range']}
   Ikigai Intersections: {', '.join(career_info['ikigai_intersections'])}
"""
    
    text += f"""

IKIGAI DEVELOPMENT ROADMAP:
===========================
"""
    
    for quadrant, activities in roadmap.items():
        if activities:
            text += f"\n{quadrant} Development:\n"
            for i, activity in enumerate(activities, 1):
                text += f"  Week {i}: {activity}\n"
    
    text += """

NEXT STEPS:
===========
1. Focus on strengthening your weakest Ikigai quadrant
2. Pursue careers that align with multiple intersections
3. Continuously reassess and refine your Ikigai
4. Connect your work to your deeper purpose
5. Seek mentorship in your chosen field

Remember: Ikigai is a journey, not a destination. 🌸
"""
    
    return text

def generate_roadmap_text(user_data, recommended_careers, ikigai, roadmap):
    """Generate text version of the roadmap for download"""
    text = f"""
CAREER ANALYSIS & LEARNING ROADMAP
===================================

Personal Information:
- Name: {user_data['name']}
- Age: {user_data['age']}
- Profile Type: {user_data['user_type']}

TOP CAREER RECOMMENDATIONS:
===========================
"""
    
    for i, (career, score) in enumerate(recommended_careers):
        career_info = CAREER_DATABASE[career]
        text += f"""
{i+1}. {career} ({score:.1%} match)
   Description: {career_info['description']}
   Growth Rate: {career_info['growth_rate']}
   Salary Range: {career_info['salary_range']}
   Key Skills: {', '.join(career_info['skills'])}
"""
    
    text += f"""

IKIGAI MAPPING:
===============
"""
    for quadrant, items in ikigai.items():
        text += f"\n{quadrant}:\n"
        for item in items:
            text += f"  • {item.replace('_', ' ').title()}\n"
    
    text += f"""

12-WEEK LEARNING ROADMAP:
=========================
"""
    
    for week_data in roadmap:
        text += f"""
Week {week_data['week']}: {week_data['focus_area']}
{"=" * (len(f"Week {week_data['week']}: {week_data['focus_area']}"))}

Learning Goals:
"""
        for goal in week_data['learning_goals']:
            text += f"  • {goal}\n"
        
        text += "\nRecommended Resources:\n"
        for resource in week_data['resources']:
            text += f"  • {resource}\n"
        
        text += "\nMilestones:\n"
        for milestone in week_data['milestones']:
            text += f"  ✅ {milestone}\n"
        
        text += "\n"
    
    text += """
NEXT STEPS:
===========
1. Start with Week 1 activities immediately
2. Join online communities related to your target career
3. Network with professionals in your chosen field
4. Consider informational interviews
5. Update your resume and LinkedIn profile
6. Track your progress weekly

Good luck on your career journey! 🚀
"""
    
    return text

if __name__ == "__main__":
    main()