import os
import json
import openai



file_name = "colores_prepared.jsonl"

api_key ="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"
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
