import sqlite3
import time
import openai
import fitz  # PyMuPDF for reading PDFs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Import webdriver-manager
import config

# Set OpenAI API key
openai.api_key = config.OPENAI_API_KEY

# SQLite Database Setup
db_path = "applications.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create applications table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT,
    company_name TEXT,
    application_status TEXT,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    job_link TEXT
)
""")
conn.commit()

# Function to log applications
def log_application(job_title, company_name, status="Submitted", job_link=""):
    cursor.execute("""
    INSERT INTO applications (job_title, company_name, application_status, job_link)
    VALUES (?, ?, ?, ?)""",
                   (job_title, company_name, status, job_link))
    conn.commit()

# Function to read the resume
def read_resume(file_path):
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        print(f"Error reading resume: {e}")
        return ""

# Function to generate a cover letter using OpenAI
def generate_cover_letter(job_title, company_name, job_description, resume_text):
    prompt = f"""
    Write a professional and tailored cover letter for the following job:
    Job Title: {job_title}
    Company Name: {company_name}
    Job Description: {job_description}
    Resume Details: {resume_text}
    Make it engaging, concise, and aligned with industry standards.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating cover letter: {e}")
        return ""

# Selenium Setup using webdriver-manager
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver_service = Service(ChromeDriverManager().install())  # Automatically manage ChromeDriver
driver = webdriver.Chrome(service=driver_service, options=options)

# Login to LinkedIn
def linkedin_login(email, password):
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
    time.sleep(5)
    print("Logged in successfully.")

# Job Search
def search_jobs(job_title, location="India"):
    # Construct the search URL with Easy Apply filter
    job_title_encoded = job_title.replace(" ", "%20")
    location_encoded = location.replace(" ", "%20")
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={job_title_encoded}&location={location_encoded}&f_E=2"  # f_E=2 filters for "Easy Apply" jobs
    
    driver.get(search_url)
    time.sleep(5)  # Wait for the results to load
    print(f"Job search initiated for '{job_title}' in {location} with 'Easy Apply' filter.")

# Apply for Jobs
def apply_jobs():
    resume_path = config.RESUME_PATH  # Use the resume path from config
    resume_text = read_resume(resume_path)

    try:
        # Wait for job cards to load
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-list__title")))
        
        # Select all job titles
        job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-card-list__title")
        
        for job_card in job_cards:
            job_link = job_card.get_attribute("href")
            print(f"Applying for job: {job_link}")

            # Navigate to the job link
            driver.get(job_link)
            time.sleep(3)  # Wait for the job page to load

            try:
                # Click the Easy Apply button using a flexible XPath
                easy_apply_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "artdeco-button") and contains(@aria-label, "Easy Apply")]'))
                )
                easy_apply_button.click()
                time.sleep(2)

                # Fill in the cover letter
                job_description = driver.find_element(By.CLASS_NAME, "jobs-description").text
                job_title = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__job-title").text
                company_name = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__company-name").text
                cover_letter = generate_cover_letter(job_title, company_name, job_description, resume_text)

                cover_letter_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//textarea[@name="coverLetter"]'))
                )
                cover_letter_field.send_keys(cover_letter)

                # Submit the application
                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
                )
                submit_button.click()

                # Log the application
                log_application(job_title, company_name, "Submitted", job_link)
                print(f"Applied to {job_title} at {company_name}")

            except Exception as e:
                print(f"Error applying for job: {e}")
                continue  # Continue to the next job if there's an error

    except Exception as e:
        print(f"Error retrieving job links: {e}")

# Main Execution
if __name__ == "__main__":
    email = config.LINKEDIN_EMAIL
    password = config.LINKEDIN_PASSWORD

    linkedin_login(email, password)
    search_jobs("Data Scientist")
    apply_jobs()

    # Close the driver and database connection
    driver.quit()
    conn.close()
