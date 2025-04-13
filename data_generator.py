import pandas as pd
import numpy as np
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define subjects
subjects = ["Maths", "Science", "English", "History", "Computer"]

# Function to generate a student record with more natural variability
def generate_student_record(student_id):
    # Generate marks with a normal distribution (mean ~70, std ~15), clipped to [30, 100]
    marks = {subject: int(np.clip(np.random.normal(70, 15), 30, 100)) for subject in subjects}
    
    # Generate attendance with a normal distribution (mean ~85, std ~10), clipped to [50, 100]
    attendance = int(np.clip(np.random.normal(85, 10), 50, 100))
    
    # Calculate average marks
    avg_marks = sum(marks.values()) / len(subjects)

    # Recommendation logic based on avg_marks and attendance
    if avg_marks >= 75 and attendance >= 85:
        recommendation = "Eligible for Advanced Courses"
    elif avg_marks >= 50:
        recommendation = "Needs Improvement"
    else:
        recommendation = "High Risk of Failure"

    return {
        "StudentID": f"S{student_id:04}",
        **marks,
        "Attendance(%)": attendance,
        "Recommendation": recommendation
    }

# Parameters for balanced dataset
total_rows = 100000
target_per_category = total_rows // 3
max_difference = 1

# Counters
counts = {
    "Eligible for Advanced Courses": 0,
    "Needs Improvement": 0,
    "High Risk of Failure": 0
}

data = []
student_id = 1

while True:
    student = generate_student_record(student_id)
    recommendation = student["Recommendation"]

    # Check if adding this will maintain balance
    if counts[recommendation] < target_per_category:
        data.append(student)
        counts[recommendation] += 1
        student_id += 1

    # Check stopping condition
    values = list(counts.values())
    if max(values) - min(values) <= max_difference and sum(values) >= target_per_category * 3:
        break

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv("balanced_student_data.csv", index=False)

print("Balanced synthetic dataset created and saved as 'balanced_student_data.csv'")
print("Final counts:", counts)