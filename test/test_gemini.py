from gemini_parser import parse_event

query = "Kal 5 baje se 6 baje tak team meeting schedule karo"

result = parse_event(query)

print(result)
