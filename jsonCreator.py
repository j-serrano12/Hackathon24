# import spacy
# import json
# # Load English NLP model
# nlp = spacy.load("en_core_web_sm")
# # Process the text
# input_string = "John Doe is 30 years old and lives in New York."
# doc = nlp(input_string)
# # Dictionary to hold the extracted information
# data_dict = {}
# # Extract named entities (e.g., persons, dates, locations)
# for ent in doc.ents:
#     if ent.label_ == "PERSON":
#         data_dict["Name"] = ent.text
#     elif ent.label_ == "DATE":
#         data_dict["Age"] = ent.text
#     elif ent.label_ == "GPE":  # Geo-political entity (countries, cities)
#         data_dict["City"] = ent.text
# # Convert dictionary to JSON
# json_data = json.dumps(data_dict, indent=4)
# print(json_data)