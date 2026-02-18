from db import get_db_connection

def get_recommended_tutors(subject=None):
    conn = get_db_connection()

    if subject:
        tutors = conn.execute("""
            SELECT users.id, users.name,
                   tutor_profiles.subject,
                   tutor_profiles.experience,
                   tutor_profiles.price_per_hour
            FROM users
            JOIN tutor_profiles
            ON users.id = tutor_profiles.user_id
            WHERE tutor_profiles.subject = ?
        """, (subject,)).fetchall()
    else:
        tutors = conn.execute("""
            SELECT users.id, users.name,
                   tutor_profiles.subject,
                   tutor_profiles.experience,
                   tutor_profiles.price_per_hour
            FROM users
            JOIN tutor_profiles
            ON users.id = tutor_profiles.user_id
        """).fetchall()

    conn.close()
    return tutors

