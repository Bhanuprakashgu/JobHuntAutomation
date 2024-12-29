# JobHuntAutomation
# LinkedIn Auto Job Search and Application Bot

This Python-based bot automates the process of searching for jobs on LinkedIn based on the keywords extracted from your resume and specified location. The bot is under development to eventually support automatic job applications, including submitting resumes and cover letters.

---

## 🚀 Features

### Currently Implemented:
1. **Keyword Extraction from Resume**: Automatically extracts keywords from your resume using OpenAI's GPT API to tailor job searches.
2. **Job Search Automation**: Searches for jobs on LinkedIn based on keywords and location, with an "Easy Apply" filter.
3. **Database Logging**: Saves job search results in an SQLite database for easy tracking.

### Planned Improvements:
- **Automated Job Application**: Automatically apply to jobs by filling out forms, uploading resumes, and submitting tailored cover letters.
- **Enhanced Error Handling**: Improve resilience and user notifications for failed steps.
- **Customizable Search Criteria**: Add options to refine searches with filters like job type, experience level, and industry.

---

## 🛠️ Technologies Used
- **Python**: Core programming language.
- **Selenium**: Automates LinkedIn navigation.
- **SQLite**: Stores job search logs.
- **PyMuPDF (fitz)**: Extracts text from PDF resumes.
- **OpenAI GPT**: Generates keywords and tailored cover letters.
- **ChromeDriver Manager**: Manages Chrome WebDriver.

---

## 📂 Project Structure
```
├── linkedin automate job hunt.py               # Main script for the bot
├── config.py            # Configuration file for user credentials and paths
├── applications.db      # SQLite database to log job searches and applications
├── README.md            # Project documentation
```

---

## 📋 Setup Instructions

### Prerequisites
- Python 3.8+
- Google Chrome installed
- LinkedIn account credentials
- OpenAI API key

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure `config.py` with your credentials and paths:
   ```python
   LINKEDIN_EMAIL = "your-email@example.com"
   LINKEDIN_PASSWORD = "your-password"
   OPENAI_API_KEY = "your-openai-api-key"
   RESUME_PATH = r"path-to-your-resume.pdf"
   ```

---

## 🚦 How to Use
1. **Run the Bot**: 
   Execute the script:
   ```bash
   python bot.py
   ```

2. **Behavior**:
   - Extracts keywords from your resume.
   - Searches for jobs on LinkedIn based on extracted keywords and location.
   - Logs job search results in the database.

3. **Check the Database**:
   View logged job searches and details in `applications.db`.

---

## 🤝 Future Contributions
We welcome contributions to improve the bot! Potential areas of contribution:
- Automating the "Easy Apply" process.
- Adding support for multiple job boards.
- Improving keyword extraction accuracy.

---

## 🔒 Security Notes
- Ensure your credentials in `config.py` are secure and not exposed in public repositories.
- Use a separate LinkedIn account for testing if possible.

---

## 🛠️ Current Limitations
- Fully automated job applications are under development.
- Relies heavily on Selenium for LinkedIn navigation, which may break if LinkedIn updates its UI.

---

## 📞 Support
Email:bhanuprakashguddeti@gmail.com
Phone Number: +91 8096009638
For questions or support, reach out via email or submit an issue on the repository.
```  
Let me know if you need a specific name for the repository, or further tweaks!
