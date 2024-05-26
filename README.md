# Simon Kiflemariam - Interactive EDA Application

## Project Description
This project is an interactive exploratory data analysis (EDA) application designed to help users create personalized workout plans based on various muscle groups, equipment, and fitness goals. The application utilizes data collected from MuscleWiki.com to provide a comprehensive database of exercises, allowing users to filter, rate, and generate customized workout plans.

## Relevant Files
### 1. Data Collection Process
- **Notebook:** [MuscleWiki.com - Data Collection.ipynb](https://github.com/SimonKiflemariam/Simon-Kiflemariam-Interactive-EDA-Application/blob/main/Data/MuscleWiki.com_Data_Collection.ipynb)
- **Description:** This Jupyter Notebook contains the Python code used to scrape exercise data from MuscleWiki.com. It details the process of setting up the web scraper, extracting the data, and saving it into a CSV file.

### 2. Collected Data
- **CSV File:** [MuscleWiki_Data_Collection.csv](https://github.com/SimonKiflemariam/Simon-Kiflemariam-Interactive-EDA-Application/blob/main/Data/MuscleWiki_Data_Collection.csv)
- **Description:** This CSV file contains the dataset collected from MuscleWiki.com, including exercise names, muscle groups, video links, equipment, and difficulty levels.

### 3. Streamlit Application
- **Python Script:** [streamlit_app.py](https://github.com/SimonKiflemariam/Simon-Kiflemariam-Interactive-EDA-Application/blob/main/streamlit_app.py)
- **Description:** This Python script contains the code for the Streamlit web application. It provides an interactive user interface for filtering exercises, rating them, and generating a personalized workout plan. The application also includes functionality for downloading the workout plan as a PDF.

## Deployed Application
- **URL:** [Workout Selector Streamlit App](https://workout-selector.streamlit.app/)
- **Description:** The Streamlit application has been deployed to the cloud, allowing users to access and interact with the workout selector tool online.

## How to Run the Project
1. Clone the repository: `git clone https://github.com/SimonKiflemariam/Simon-Kiflemariam-Interactive-EDA-Application.git`
2. Navigate to the project directory: `cd Simon-Kiflemariam-Interactive-EDA-Application`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run the Streamlit application: `streamlit run streamlit_app.py`
