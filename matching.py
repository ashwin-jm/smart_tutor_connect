# matching.py

# External / mock tutor data (Phase 1)
external_tutor_data = [
    {"id": 1, "name": "Anjali", "subject": "Maths", "experience": 5},
    {"id": 2, "name": "Rahul", "subject": "Physics", "experience": 3},
    {"id": 3, "name": "Sneha", "subject": "Maths", "experience": 2},
]


def get_recommended_tutors(subject):
    """
    Phase 1: Rule-based matching using external data
    Phase 2: This function will be replaced by an ML model
    """
    matched = [t for t in external_tutor_data if t["subject"] == subject]
    matched.sort(key=lambda x: x["experience"], reverse=True)
    return matched
