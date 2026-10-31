"""Local test server that receives ElevenLabs post-call webhooks.

Prints the conversation ID and transcript after each conversation ends.

Setup:
    Add ELEVENLABS_WEBHOOK_SECRET to .env. It is generated when the webhook is
    created in ElevenLabs.

Run from the repo root, in two terminals:
    ngrok http 8080 --url https://dumpling-qualm-ferocious.ngrok-free.dev
    uv run --env-file .env uvicorn scripts.test_server:app --reload --port 8080

Webhook URL (set in ElevenLabs under Post-call webhooks):
    https://dumpling-qualm-ferocious.ngrok-free.dev/webhooks/post_call

To test, end a conversation in the agent's Preview. Incoming requests can be
inspected at http://localhost:4040.
"""

import os

from elevenlabs.client import ElevenLabs
from elevenlabs.errors import BadRequestError
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()
elevenlabs = ElevenLabs()
WEBHOOK_SECRET = os.environ['ELEVENLABS_WEBHOOK_SECRET']


@app.post('/webhooks/post_call')
async def post_call(request: Request):
    raw_body = (await request.body()).decode('utf-8')

    try:
        event = elevenlabs.webhooks.construct_event(
            rawBody=raw_body,
            sig_header=request.headers.get('elevenlabs-signature'),
            secret=WEBHOOK_SECRET,
        )
    except BadRequestError:
        raise HTTPException(status_code=401, detail='Invalid signature')

    if event['type'] == 'post_call_transcription':
        data = event['data']
        print(f"Conversation: {data['conversation_id']}")
        for turn in data['transcript']:
            print(f"{turn['role']}: {turn.get('message')}")

    return {'status': 'ok'}