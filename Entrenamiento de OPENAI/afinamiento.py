import os
import json
import openai


training_data = [{
    "prompt": "Where is the billing ->",
    "completion": " You find the billing in the left-hand side menu.\n"
},{
    "prompt":"How do I upgrade my account ->",
    "completion": " Visit you user settings in the left-hand side menu, then click 'upgrade account' button at the top.\n"
}]

file_name = "training_data.jsonl"

with open(file_name, "w") as output_file:
 for entry in training_data:
  json.dump(entry, output_file)
  output_file.write("\n")

api_key =""
openai.api_key = api_key

upload_response = openai.File.create(
  file=open(file_name, "rb"),
  purpose='fine-tune'
)

file_id = upload_response.id
upload_response


fine_tune_response = openai.FineTune.create(training_file=file_id)
fine_tune_response

openai.FineTune.create(training_file=file_id, model="ada")

fine_tune_events = openai.FineTune.list_events(id=fine_tune_response.id)


retrieve_response = openai.FineTune.retrieve(id=fine_tune_response.id)
