from db import get_db_connection


def get_recommended_tutors(subject=None):

    conn = get_db_connection()

    base_query = """
        SELECT users.id,
               users.name,
               users.email,
               tutor_profiles.subject,
               tutor_profiles.experience,
               tutor_profiles.price_per_hour,
               tutor_profiles.demo_link,
               AVG(ratings.rating) AS avg_rating
        FROM users
        JOIN tutor_profiles
            ON users.id = tutor_profiles.user_id
        LEFT JOIN ratings
            ON users.id = ratings.tutor_id
    """

    if subject:
        base_query += " WHERE tutor_profiles.subject = ?"

    base_query += " GROUP BY users.id, tutor_profiles.subject"

    if subject:
        tutors = conn.execute(base_query, (subject,)).fetchall()
    else:
        tutors = conn.execute(base_query).fetchall()

    conn.close()
    return tutors