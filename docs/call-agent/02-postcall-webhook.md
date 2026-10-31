# ADR: ElevenLabs Post-Call Webhook API

## Status

Proposed

## Context

The HOC phone system uses ElevenLabs to handle caller conversations and Twilio for telephony.

After a conversation ends, ElevenLabs sends a `post_call_transcription` webhook containing the transcript, conversation metadata, and analysis.

We need a backend API endpoint to receive this information and coordinate post-call processing.

## Decision

We will expose a FastAPI endpoint for receiving ElevenLabs post-call transcription events.

**Endpoint:** `POST /webhooks/elevenlabs/post-call`

### Responsibilities

The endpoint will:

1. Receive and validate ElevenLabs `post_call_transcription` events.
2. Associate the event with the corresponding call using `conversation_id`.
3. Retrieve relevant Twilio call information, including call status and available transfer details.
4. Persist the combined call information in Supabase.

The endpoint will not participate in live conversations, control call routing, or initiate transfers.

## API Contract

### Request

**Method:** `POST`

**Path:** `/webhooks/elevenlabs/post-call`

**Content-Type:** `application/json`

**Event type:** `post_call_transcription`

The request follows ElevenLabs' webhook payload format.

Required information:

| Field | Purpose |
|---|---|
| `type` | Identifies the webhook event |
| `data.conversation_id` | Associates the event with an existing call |
| `data.transcript` | Conversation transcript |
| `data.metadata` | Conversation timing and metadata |
| `data.analysis` | Post-call analysis and collected information |

The endpoint will accept additional fields provided by ElevenLabs without requiring changes to the API contract.

### Response

| Status | Meaning |
|---|---|
| `200 OK` | Event successfully accepted |
| `400 Bad Request` | Invalid or unsupported payload |
| `401 Unauthorized` | Webhook authentication failed |
| `500 Internal Server Error` | Event could not be accepted due to a server error |

The response does not contain conversation data.

## API Boundaries

- **ElevenLabs → FastAPI:** ElevenLabs is responsible for delivering post-call conversation data. FastAPI receives it through the webhook.
- **FastAPI → Twilio:** FastAPI retrieves telephony status and available transfer information using the call association established during initialization.
- **FastAPI → Supabase:** FastAPI is responsible for persisting the combined call record.
- **Supabase → Employee Dashboard:** The dashboard consumes stored call records independently of the webhook API.

The webhook is a provider-facing API, not an endpoint intended for direct use by the employee dashboard.

## Out of Scope

- Conversation initiation webhook
- Live audio or transcript streaming
- Agent configuration and prompts
- Call routing and transfer execution
- Employee dashboard APIs
- Internal processing, database queries, retry strategies, and storage implementation details