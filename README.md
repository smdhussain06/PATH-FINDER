# Career Guidance with Ikigai Framework

This project integrates the **Ikigai model** into a psychometric and job market analysis web application.

## 🌸 What is Ikigai?

**Ikigai (生き甲斐)** is a Japanese concept meaning "reason for being." It represents the intersection of four fundamental elements:

- **What you love** (your passion and interests)
- **What you are good at** (your skills and talents)  
- **What the world needs** (problems you can solve)
- **What you can be paid for** (marketable skills and opportunities)

## 🔹 Workflow

1. **User Segmentation** – Choose Student, Graduate, Professional, or Career Changer.
2. **Ikigai Quadrant Assessment** – Complete detailed forms for each quadrant:
   - What you love (passions and interests)
   - What you are good at (skills and talents)
   - What the world needs (social problems and market needs)
   - What you can be paid for (monetizable skills)
3. **Ikigai Analysis Engine** – Rule-based scoring maps answers to Ikigai intersections:
   - **Passion** (Love ∩ Good At)
   - **Mission** (Love ∩ World Needs)
   - **Profession** (Good At ∩ Paid For)
   - **Vocation** (World Needs ∩ Paid For)
4. **Career Suggestions** – Top 2–3 careers aligned with your Ikigai intersections
5. **Personalized Roadmap** – 12-week development plan targeting weak quadrants
6. **Export Options** – Download as PDF or text file

## 🔹 Features

- **Ikigai-Centered Assessment**: Move beyond generic skills tests to purpose-driven analysis
- **Intersection Analysis**: Discover your unique combinations of passion, skill, purpose, and market value
- **Career Alignment**: Recommendations based on authentic Ikigai methodology
- **Visual Quadrant Display**: Clear visualization of your Ikigai strengths and gaps
- **Personalized Development**: Targeted roadmaps for strengthening weak quadrants
- **Professional Reports**: Download comprehensive analysis as PDF or text

## 🔹 User Types Supported

- **Students**: Academic performance and interest-based guidance with future-focused assessment
- **Graduates**: Degree-based career path recommendations aligned with personal purpose
- **Professionals**: Experience-driven role transitions focusing on authentic career alignment  
- **Career Changers**: Industry transition support through Ikigai-based self-discovery

## 🔹 Tech Stack

- **Frontend/UI**: Streamlit (fast, free, hackathon-friendly)
- **Backend Logic**: Python (rule-based, extendable with ML)
- **Analysis Engine**: Scikit-learn for similarity matching
- **Data Storage**: CSV files (user profiles, career mapping)
- **Export**: ReportLab for PDF generation
- **Hosting**: Streamlit Community Cloud (free)

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the displayed URL (typically http://localhost:8501)

3. Select your user type and complete the Ikigai assessment

4. Discover your purpose intersections and aligned career recommendations

5. Download your personalized analysis and development roadmap

## 🔹 Why Ikigai?

The Ikigai model helps users align **what they love, what they are good at, what the world needs, and what they can be paid for** into a meaningful career path. This project turns self-reflection into **practical, market-driven career suggestions** with skill development roadmaps.

Unlike traditional career assessments that focus solely on skills or interests, our Ikigai approach ensures:

- **Authentic alignment** between personal values and career choices
- **Sustainable motivation** through purpose-driven work
- **Market relevance** by considering real-world needs and opportunities
- **Holistic development** addressing passion, skill, purpose, and practical considerations

## Demo Data

The application includes sample user data in `sampleusers.csv` for testing purposes, showcasing different Ikigai profiles and career alignments.

## Project Structure

- `app.py` - Main Streamlit application with Ikigai framework
- `sampleusers.csv` - Demo user profiles with Ikigai mappings
- `requirements.txt` - Python dependencies including ReportLab
- `README.md` - This file

## Career Database

Includes 8 careers mapped to Ikigai intersections:
- **Data Scientist** (Profession + Vocation)
- **Web Developer** (Passion + Profession)  
- **UX/UI Designer** (Passion + Mission)
- **Business Consultant** (Mission + Vocation)
- **Product Manager** (Passion + Vocation)
- **Digital Marketing Manager** (Passion + Profession)
- **AI/ML Engineer** (Profession + Vocation)
- **Technical Writer** (Mission + Vocation)

Each career includes detailed Ikigai quadrant mappings for authentic alignment assessment.

---

*Discover your Ikigai and find work that truly matters.* 🌸