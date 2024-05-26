import streamlit as st  # Import Streamlit for building the web app
import pandas as pd  # Import pandas for data manipulation
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML
from fpdf import FPDF, HTMLMixin  # Import FPDF and HTMLMixin for PDF generation
import io  # Import io for in-memory file handling

# Function to load data from a CSV file
def load_data(file):
    data = pd.read_csv(file)  # Read the CSV file into a DataFrame
    return data  # Return the loaded data

# Function to clean equipment HTML content and extract the equipment name
def clean_equipment(equipment_html):
    soup = BeautifulSoup(equipment_html, "html.parser")  # Parse the HTML content using BeautifulSoup
    for tag in soup.find_all(["a", "span"]):  # Find all 'a' and 'span' tags
        tag.decompose()  # Remove the tags from the HTML content
    return soup.get_text().strip()  # Return the cleaned text

# PDF generation class
class PDF(FPDF, HTMLMixin):
    def header(self):
        if self.page == 1:  # Check if it's the first page
            self.set_font("Arial", 'B', 14)  # Set the font to Arial, bold, size 14
            self.cell(0, 10, "Workout Plan", ln=True, align='C')  # Add a centered cell with the title
            self.ln(10)  # Add a line break

# Function to generate the PDF
def generate_pdf(selected_exercises, goal_exercise_details):
    pdf = PDF()  # Create a PDF object
    pdf.add_page()  # Add a new page to the PDF
    
    for exercise, details in selected_exercises.items():  # Loop through the selected exercises
        muscle_group = details['muscle_group']  # Get the muscle group of the exercise
        goal = details['goal']  # Get the goal associated with the exercise
        male_link = details['male_link']  # Get the link to the male video
        female_link = details['female_link']  # Get the link to the female video
        equipment_name = details['equipment_name']  # Get the name of the equipment used
        reps, sets = goal_exercise_details[goal][exercise]['reps_sets']  # Get the reps and sets for the exercise
        rest = goal_exercise_details[goal][exercise]['rest']  # Get the rest time for the exercise
        
        pdf.set_font("Arial", 'BU', 12)  # Set the font to Arial, bold and underlined, size 12
        pdf.cell(0, 10, f"{exercise} ({muscle_group})", ln=True, align='L')  # Add a cell with the exercise name and muscle group
        
        pdf.set_font("Arial", size=12)  # Set the font to Arial, size 12
        
        pdf.set_font("Arial", 'B', 12)  # Set the font to Arial, bold, size 12
        pdf.cell(40, 10, "Sets:", border=0)  # Add a cell with the text "Sets:"
        pdf.set_font("Arial", size=12)  # Set the font to Arial, size 12
        pdf.cell(0, 10, f"{sets}", ln=True, border=0)  # Add a cell with the number of sets
        
        pdf.set_font("Arial", 'B', 12)  # Set the font to Arial, bold, size 12
        pdf.cell(40, 10, "Reps:", border=0)  # Add a cell with the text "Reps:"
        pdf.set_font("Arial", size=12)  # Set the font to Arial, size 12
        pdf.cell(0, 10, f"{reps}", ln=True, border=0)  # Add a cell with the number of reps
        
        pdf.set_font("Arial", 'B', 12)  # Set the font to Arial, bold, size 12
        pdf.cell(40, 10, "Rest:", border=0)  # Add a cell with the text "Rest:"
        pdf.set_font("Arial", size=12)  # Set the font to Arial, size 12
        pdf.cell(0, 10, f"{rest}", ln=True, border=0)  # Add a cell with the rest time
        
        pdf.set_font("Arial", 'B', 12)  # Set the font to Arial, bold, size 12
        pdf.cell(40, 10, "Equipment:", border=0)  # Add a cell with the text "Equipment:"
        pdf.set_font("Arial", size=12)  # Set the font to Arial, size 12
        pdf.cell(0, 10, f"{equipment_name}", ln=True, border=0)  # Add a cell with the equipment name
        
        pdf.set_font("Arial", 'B', 12)  # Set the font to Arial, bold, size 12
        pdf.cell(40, 10, "Male Video:", border=0)  # Add a cell with the text "Male Video:"
        pdf.set_text_color(0, 0, 255)  # Set the text color to blue
        pdf.cell(0, 10, "Click Here", ln=True, border=0, link=male_link)  # Add a cell with the link to the male video
        
        pdf.set_text_color(0, 0, 0)  # Reset text color to black
        pdf.set_font("Arial", 'B', 12)  # Set the font to Arial, bold, size 12
        pdf.cell(40, 10, "Female Video:", border=0)  # Add a cell with the text "Female Video:"
        pdf.set_text_color(0, 0, 255)  # Set the text color to blue
        pdf.cell(0, 10, "Click Here", ln=True, border=0, link=female_link)  # Add a cell with the link to the female video
        
        pdf.set_text_color(0, 0, 0)  # Reset text color to black
        pdf.ln(10)  # Add a line break
        pdf.cell(0, 10, "-"*100, ln=True, align='L')  # Add a separator line
        pdf.ln(5)  # Add another line break
    
    return pdf.output(dest='S').encode('latin1')  # Return the PDF as a byte string

# Initialize session state for navigation and selections
if "page" not in st.session_state:  # Check if 'page' is not in session state
    st.session_state.page = "welcome"  # Initialize 'page' to "welcome"

if "ratings" not in st.session_state:  # Check if 'ratings' is not in session state
    st.session_state.ratings = {}  # Initialize 'ratings' as an empty dictionary

if "selected_exercises" not in st.session_state:  # Check if 'selected_exercises' is not in session state
    st.session_state.selected_exercises = {}  # Initialize 'selected_exercises' as an empty dictionary

if "goal_exercise_details" not in st.session_state:  # Check if 'goal_exercise_details' is not in session state
    st.session_state.goal_exercise_details = {  # Initialize 'goal_exercise_details' with empty dictionaries for each goal
        "Muscular Strength": {},
        "Muscular Hypertrophy": {},
        "Cardiovascular Development": {},
        "Stretching": {}
    }

if "selected_keys" not in st.session_state:  # Check if 'selected_keys' is not in session state
    st.session_state.selected_keys = {}  # Initialize 'selected_keys' as an empty dictionary

# Welcome page
if st.session_state.page == "welcome":  # Check if the current page is "welcome"
    st.markdown("<h1>Exercise Database</h1>", unsafe_allow_html=True)  # Display the main title
    st.markdown("<h2>Welcome to the Exercise Database</h2>", unsafe_allow_html=True)  # Display the welcome message
    st.markdown("<p>Find exercises for various muscle groups, rate them, and create your personalized workout plan.</p>", unsafe_allow_html=True)  # Display the description
    
    if st.button("Dive In"):  # Button to proceed to the next page
        st.session_state.page = "generator"  # Set the page to "generator"
        st.experimental_rerun()  # Refresh the page to load the generator

# Workout selector page
if st.session_state.page == "generator":  # Check if the current page is "generator"
    st.markdown("<h1 style='text-align: center;'>Workout Selector</h1>", unsafe_allow_html=True)  # Display the workout selector title

    st.sidebar.subheader("Upload CSV file:")  # Sidebar title for file upload
    uploaded_file = st.sidebar.file_uploader("Choose a file", type="csv")  # File uploader widget

    if uploaded_file:  # Check if a file has been uploaded
        data = load_data(uploaded_file)  # Load the uploaded CSV file
        
        st.sidebar.subheader("Muscle Groups:")  # Sidebar title for muscle groups
        selected_muscle_groups = st.sidebar.multiselect("Select Muscle Groups:", sorted(data["Muscle Group"].unique()))  # Multi-select widget for muscle groups

        st.sidebar.subheader("Equipment:")  # Sidebar title for equipment
        data["Cleaned Equipment"] = data["Equipment"].apply(clean_equipment)  # Clean the equipment HTML content
        equipment_options = ["All"] + sorted(data["Cleaned Equipment"].unique())  # List of equipment options
        selected_equipment = st.sidebar.selectbox("Select Equipment:", equipment_options)  # Dropdown for equipment selection

        st.sidebar.subheader("Difficulty:")  # Sidebar title for difficulty
        difficulty_options = ["All", "Beginner", "Intermediate", "Advanced", "Novice"]  # List of difficulty options
        selected_difficulty = st.sidebar.selectbox("Select Difficulty:", difficulty_options)  # Dropdown for difficulty selection

        st.sidebar.subheader("Goal:")  # Sidebar title for goals
        selected_goal = st.sidebar.selectbox("Select Goal:", ["Muscular Strength", "Muscular Hypertrophy", "Cardiovascular Development", "Stretching"], key="selected_goal")  # Dropdown for goal selection

        # Filter data based on user input
        filtered_data = data  # Initialize filtered_data with the original data
        if selected_muscle_groups:  # Check if any muscle groups are selected
            filtered_data = filtered_data[filtered_data["Muscle Group"].isin(selected_muscle_groups)]  # Filter by selected muscle groups
        if selected_equipment != "All":  # Check if a specific equipment is selected
            filtered_data = filtered_data[filtered_data["Cleaned Equipment"] == selected_equipment]  # Filter by selected equipment
        if selected_difficulty != "All":  # Check if a specific difficulty level is selected
            filtered_data = filtered_data[filtered_data["Difficulty"] == selected_difficulty]  # Filter by selected difficulty

        # Assign reps, sets, and rest based on the selected goal
        if selected_goal == "Muscular Strength":  # Check if the selected goal is "Muscular Strength"
            equipment_for_strength = ["Barbell", "Dumbbells", "Machine", "Medicine-Ball", "Kettlebells", "Cables", "Band", "Plate", "Vitruvian", "Smith-Machine"]  # List of equipment for strength
            filtered_data = filtered_data[filtered_data["Cleaned Equipment"].apply(lambda x: any(equip in x for equip in equipment_for_strength))]  # Filter data for strength equipment
            reps_sets = ("[8, 6, 4]", 3)  # Reps and sets for strength
            rest = "[2-3min/Set]"  # Rest time for strength
        elif selected_goal == "Muscular Hypertrophy":  # Check if the selected goal is "Muscular Hypertrophy"
            equipment_for_hypertrophy = ["Barbell", "Dumbbells", "Bodyweight", "Machine", "Medicine-Ball", "Kettlebells", "Stretches", "Cables", "Band", "Plate", "TRX", "Bosu-Ball", "Vitruvian", "Smith-Machine"]  # List of equipment for hypertrophy
            filtered_data = filtered_data[filtered_data["Cleaned Equipment"].apply(lambda x: any(equip in x for equip in equipment_for_hypertrophy))]  # Filter data for hypertrophy equipment
            reps_sets = ("[12, 10, 8]", 3)  # Reps and sets for hypertrophy
            rest = "[2-3min/Set]"  # Rest time for hypertrophy
        elif selected_goal == "Cardiovascular Development":  # Check if the selected goal is "Cardiovascular Development"
            filtered_data = filtered_data[filtered_data["Cleaned Equipment"].str.contains("Cardio")]  # Filter data for cardio equipment
            reps_sets = ("[3-5min/Exercise]", 3)  # Reps and sets for cardio
            rest = "[1-2min/Set]"  # Rest time for cardio
        elif selected_goal == "Stretching":  # Check if the selected goal is "Stretching"
            filtered_data = filtered_data[filtered_data["Cleaned Equipment"].str.contains("Yoga")]  # Filter data for yoga equipment
            reps_sets = ("Hold 20 seconds", 3)  # Reps and sets for stretching
            rest = "[20-30sec]"  # Rest time for stretching
        else:
            reps_sets = []  # Initialize reps and sets as empty
            rest = ""  # Initialize rest as empty

        # Ensure that selected exercises are not lost when filters are changed
        filtered_exercises = {f"{row['Exercise']} ({row['Muscle Group']})": (row['Exercise'], row['Muscle Group'], selected_goal, row['Video Link (Male)'], row['Video Link (Female)'], row['Cleaned Equipment']) for idx, row in filtered_data.iterrows()}  # Dictionary of filtered exercises

        col1, col2, col3 = st.columns([4, 3, 4], gap="large")  # Create columns for layout

        with col1:
            st.markdown(f"<h5>Filtered Exercises: ({len(filtered_exercises)})</h5>", unsafe_allow_html=True)  # Display filtered exercises count
            if not selected_muscle_groups:  # Check if no muscle groups are selected
                st.info("Please select muscle groups to display exercises.")  # Prompt to select muscle groups
            elif filtered_data.empty:  # Check if no exercises are found
                st.warning("No exercises found. Please try different options.")  # Warning if no exercises are found
            else:
                for exercise_key, exercise_values in filtered_exercises.items():  # Loop through filtered exercises
                    exercise, muscle_group, goal, male_link, female_link, equipment_name = exercise_values  # Unpack exercise details
                    selected_key = f"{exercise_key}_selected"  # Generate key for the selected exercise

                    if selected_key not in st.session_state.selected_keys:  # Check if the exercise is not in the selected keys
                        st.session_state.selected_keys[selected_key] = False  # Initialize the selected key as False

                    selected = st.checkbox(exercise_key, key=selected_key, value=st.session_state.selected_keys[selected_key])  # Checkbox for exercise selection

                    st.write(f"**Male Video:** [Click Here]({male_link})")  # Display link to male video
                    st.write(f"**Female Video:** [Click Here]({female_link})")  # Display link to female video

                    rating_key = f"rating_{exercise_key}"  # Generate key for the exercise rating
                    rating = st.slider("Rate this exercise (out of 5):", 0, 5, st.session_state.ratings.get(rating_key, 0), key=rating_key)  # Slider for rating
                    st.session_state.ratings[rating_key] = rating  # Store the rating in session state

                    if selected:  # Check if the exercise is selected
                        if exercise not in st.session_state.selected_exercises:  # Check if the exercise is not already selected
                            st.session_state.selected_exercises[exercise] = {  # Add exercise details to selected exercises
                                'muscle_group': muscle_group,
                                'goal': goal,
                                'male_link': male_link,
                                'female_link': female_link,
                                'equipment_name': equipment_name
                            }
                        st.session_state.goal_exercise_details[goal][exercise] = {  # Add exercise details to goal exercise details
                            'reps_sets': reps_sets,
                            'rest': rest
                        }
                        st.session_state.selected_keys[selected_key] = True  # Set the selected key to True
                    else:
                        st.session_state.selected_exercises.pop(exercise, None)  # Remove the exercise from selected exercises
                        st.session_state.goal_exercise_details[goal].pop(exercise, None)  # Remove the exercise from goal exercise details
                        st.session_state.selected_keys[selected_key] = False  # Set the selected key to False

                    st.write(f"Equipment: {equipment_name}")  # Display the equipment name
                    st.write("---")  # Display a separator

        with col2:
            st.markdown("<h5>Recommended Exercises:</h5>", unsafe_allow_html=True)  # Display recommended exercises
            sorted_ratings = sorted(st.session_state.ratings.items(), key=lambda x: x[1], reverse=True)  # Sort the ratings in descending order
            if sorted_ratings:  # Check if there are any ratings
                for key, rating in sorted_ratings:  # Loop through the sorted ratings
                    if rating > 0:  # Check if the rating is greater than 0
                        exercise_name = key.replace("rating_", "").replace("_", " ")  # Format the exercise name
                        st.write(f"Rating ({exercise_name}): {rating}/5")  # Display the rating
            if not sorted_ratings or all(rating == 0 for _, rating in sorted_ratings):  # Check if there are no ratings or all ratings are 0
                st.info("Rate exercises to see your favorite ones.")  # Prompt to rate exercises

        with col3:
            st.markdown("<h5>Your Workout:</h5>", unsafe_allow_html=True)  # Display the user's workout
            for exercise, details in st.session_state.selected_exercises.items():  # Loop through the selected exercises
                muscle_group = details['muscle_group']  # Get the muscle group of the exercise
                goal = details['goal']  # Get the goal associated with the exercise
                male_link = details['male_link']  # Get the link to the male video
                female_link = details['female_link']  # Get the link to the female video
                equipment_name = details['equipment_name']  # Get the name of the equipment used
                reps, sets = st.session_state.goal_exercise_details[goal][exercise]['reps_sets']  # Get the reps and sets for the exercise
                rest = st.session_state.goal_exercise_details[goal][exercise]['rest']  # Get the rest time for the exercise
                st.write(f"**{exercise} ({muscle_group})**")  # Display the exercise name and muscle group
                st.write(f"    {sets} Sets || Reps {reps} || Rest {rest}")  # Display the sets, reps, and rest time
                st.write(f"**Male Video:** [Click Here]({male_link})")  # Display the link to the male video
                st.write(f"**Female Video:** [Click Here]({female_link})")  # Display the link to the female video
                st.write(f"**Equipment:** {equipment_name}")  # Display the equipment name
                st.write("---")  # Display a separator

            if st.session_state.selected_exercises:  # Check if there are any selected exercises
                if st.button("Download Workout as PDF"):  # Button to download the workout plan as a PDF
                    pdf_data = generate_pdf(st.session_state.selected_exercises, st.session_state.goal_exercise_details)  # Generate the PDF
                    pdf_data = io.BytesIO(pdf_data)  # Convert the PDF data to a BytesIO object
                    st.download_button(label="Download PDF", data=pdf_data, file_name="workout_plan.pdf", mime="application/pdf")  # Download button for the PDF
            else:
                st.info("Select exercises to enable PDF download.")  # Prompt to select exercises to enable PDF download
    else:
        st.info("Please upload the CSV file MuscleWiki_data_collection from the [Github repository](https://github.com/SimonKiflemariam/Simon-Kiflemariam-Interactive-EDA-Application/blob/main/Data/MuscleWiki_Data_Collection.csv) to proceed.")  # Prompt to upload the CSV file