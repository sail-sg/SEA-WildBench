import os
import sys

from openai import OpenAI

API_PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "sail_api"

print(f"Cancel batch jobs on API provider: [{API_PROVIDER}]")

if API_PROVIDER == "sail_api":
    client = OpenAI(base_url="https://chatgpt.alpha.insea.io/openai/v1")
else:
    client = OpenAI()

existing_batches = client.batches.list(limit=100)
for batch in existing_batches:
    if batch.status not in ["completed", "failed", "finalizing", "cancelled"]:
        client.batches.cancel(batch.id)
        print(f"Canceled batch {batch.id}")