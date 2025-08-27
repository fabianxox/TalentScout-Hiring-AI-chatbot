def get_candidate_prompt(user_input, candidate_data):
    """
    Minimal reference of candidate input and missing field.
    No LLM needed for validations, only for tech questions.
    """
    field_order = [
        "name","email","phone","years of experience",
        "desired_position","location","tech_stack"
    ]
    current_field = next((f for f in field_order if not candidate_data.data.get(f)), None)

    if not current_field:
        return "All candidate info collected! Move on to technical questions."

    return f"""
Candidate input: "{user_input}"

Candidate data so far:
- Name: {candidate_data.data.get('name')}
- Email: {candidate_data.data.get('email')}
- Phone: {candidate_data.data.get('phone')}
- Years of experience: {candidate_data.data.get('years of experience')}
- Desired role: {candidate_data.data.get('desired_position')}
- Location: {candidate_data.data.get('location')}
- Tech stack: {candidate_data.data.get('tech_stack')}

Current field to validate: "{current_field}"
"""
