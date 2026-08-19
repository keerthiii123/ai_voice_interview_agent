from crew_agents import evaluate_answer

question = "What is a Python list?"
answer = "A list is a collection of values in Python."

result = evaluate_answer(question, answer)

print("\n📊 Evaluation:")
print(result)