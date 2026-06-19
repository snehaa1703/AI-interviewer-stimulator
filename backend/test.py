from ai_service import generate_questions

questions = generate_questions(
    role="Backend Developer",
    difficulty="Medium",
    num_questions=5
)

print(questions)