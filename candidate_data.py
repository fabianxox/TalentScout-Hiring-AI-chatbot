# candidate_data.py
class CandidateData:
    def __init__(self):
        self.data = {
            "name": None,
            "email": None,
            "phone": None,
            "years_of_experience": None,
            "desired_position": None,
            "location": None,
            "tech_stack": []
        }

    def update(self, key, value):
        if not value:
            return
        if key == "tech_stack":
            if isinstance(value, str):
                self.data[key] = [t.strip() for t in value.split(",") if t.strip()]
        else:
            self.data[key] = str(value).strip()

    def is_info_complete(self):
        required_fields = [
            "name", "email", "phone", "years_of_experience",
            "desired_position", "location", "tech_stack"
        ]
        return all(bool(self.data.get(f)) for f in required_fields)
