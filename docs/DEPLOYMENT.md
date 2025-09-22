# 🚀 Deployment Guide for PATH-FINDER

## Quick Deployment Options

### 1. Streamlit Community Cloud (Recommended)

**Step 1:** Fork or have access to this repository
**Step 2:** Visit [share.streamlit.io](https://share.streamlit.io)
**Step 3:** Connect your GitHub account
**Step 4:** Select this repository (`smdhussain06/PATH-FINDER`)
**Step 5:** Set main file path to `app.py`
**Step 6:** Click "Deploy!"

Your app will be live at: `https://[your-app-name].streamlit.app`

### 2. Heroku Deployment

Create these additional files:

**Procfile:**
```
web: sh setup.sh && streamlit run app.py
```

**setup.sh:**
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = \$PORT\n\
" > ~/.streamlit/config.toml
```

**runtime.txt:**
```
python-3.13.0
```

Then deploy using Heroku CLI:
```bash
heroku create your-app-name
git push heroku master
```

### 3. Railway Deployment

**Step 1:** Visit [railway.app](https://railway.app)
**Step 2:** Connect GitHub repository
**Step 3:** Railway will auto-detect Python and install dependencies
**Step 4:** Set start command to: `streamlit run app.py --server.port $PORT`

### 4. Google Cloud Run

**Step 1:** Create `Dockerfile`:
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080
CMD streamlit run app.py --server.port 8080 --server.enableCORS false --server.enableXsrfProtection false
```

**Step 2:** Deploy with Cloud Run:
```bash
gcloud run deploy --source .
```

### 5. Local Development

```bash
# Clone the repository
git clone https://github.com/smdhussain06/PATH-FINDER.git
cd PATH-FINDER

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Environment Variables

For production deployment, consider setting:

- `STREAMLIT_THEME_PRIMARY_COLOR`: Customize primary color
- `STREAMLIT_THEME_BACKGROUND_COLOR`: Set background color
- `STREAMLIT_SERVER_PORT`: Custom port (if needed)

## Performance Tips

1. **Caching**: The app uses `@st.cache_data` for performance
2. **Memory**: Monitor memory usage for large datasets
3. **Loading**: Add loading spinners for better UX

## Troubleshooting

### Common Issues:

**Import Errors:**
- Ensure all dependencies in `requirements.txt` are installed
- Check Python version compatibility (3.8+)

**Memory Issues:**
- Reduce sample data size
- Implement pagination for large datasets

**Slow Loading:**
- Use `@st.cache_data` decorator
- Optimize data processing functions

## Support

For deployment issues:
- Check [Streamlit Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- Review platform-specific deployment guides
- Open an issue in this repository

## Live Demo

🌟 **Try the live application:** [PATH-FINDER Demo](https://your-deployed-app-url.streamlit.app)

---

*Built with ❤️ using Streamlit and the power of Ikigai philosophy*