import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors


class MLBasedTutorRecommender:

    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)

        # Encode categorical columns
        self.subject_encoder = LabelEncoder()
        self.location_encoder = LabelEncoder()
        self.level_encoder = LabelEncoder()

        self.df["subject_encoded"] = self.subject_encoder.fit_transform(self.df["subject"])
        self.df["location_encoded"] = self.location_encoder.fit_transform(self.df["location"])
        self.df["level_encoded"] = self.level_encoder.fit_transform(self.df["teaching_level"])

        # Feature matrix
        self.features = self.df[[
            "subject_encoded",
            "experience_years",
            "price_per_hour",
            "location_encoded",
            "level_encoded"
        ]]

        # Train KNN model
        self.model = NearestNeighbors(n_neighbors=5, metric="cosine")
        self.model.fit(self.features)

    def recommend(self, subject, location, level, experience_preference, price_preference):
        """
        Recommend tutors based on student preference
        """

        # Encode input
        subject_encoded = self.subject_encoder.transform([subject])[0]
        location_encoded = self.location_encoder.transform([location])[0]
        level_encoded = self.level_encoder.transform([level])[0]

        # Create query vector
        query = np.array([[
            subject_encoded,
            experience_preference,
            price_preference,
            location_encoded,
            level_encoded
        ]])

        # Find nearest tutors
        distances, indices = self.model.kneighbors(query)

        recommended_tutors = self.df.iloc[indices[0]]

        return recommended_tutors


if __name__ == "__main__":

    recommender = MLBasedTutorRecommender("synthetic_tutor_dataset.csv")

    recommendations = recommender.recommend(
        subject="Maths",
        location="CityA",
        level="Intermediate",
        experience_preference=3,
        price_preference=500
    )

    print("\nTop Recommended Tutors:\n")
    print(recommendations[[
        "tutor_id",
        "subject",
        "experience_years",
        "price_per_hour",
        "location",
        "teaching_level"
    ]])