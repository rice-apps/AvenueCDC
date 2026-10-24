"""Validated data model for a caller interaction."""

from enum import Enum
from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, JsonValue


class APIModel(BaseModel):
    """Shared validation behavior for API data models."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )


class CallOutcome(str, Enum):
    """The final disposition of a call."""

    COMPLETED = "completed"
    FILTERED_OUT = "filtered_out"
    ROUTED_TO_STAFF = "routed_to_staff"
    HUNG_UP = "hung_up"


class TranscriptSpeaker(str, Enum):
    """A participant represented in a transcript entry."""

    CALLER = "caller"
    ASSISTANT = "assistant"
    STAFF = "staff"
    SYSTEM = "system"


class RoutingType(str, Enum):
    """The kind of destination to which a call was routed."""

    STAFF = "staff"
    DEPARTMENT = "department"
    PHONE_NUMBER = "phone_number"
    VOICEMAIL = "voicemail"


class IntakeItem(APIModel):
    """One intake question and its answer, if collected."""

    key: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=1)
    answer: JsonValue | None = None
    required: bool = True


class TranscriptEntry(APIModel):
    """One timestamped utterance or system message."""

    speaker: TranscriptSpeaker
    text: str = Field(min_length=1)
    timestamp: AwareDatetime


class Report(APIModel):
    """Structured summary produced after or during a call."""

    summary: str = Field(min_length=1)
    needs: list[str] = Field(default_factory=list)
    follow_up_required: bool = False


class RoutingDestination(APIModel):
    """Destination used when a call is transferred or escalated."""

    type: RoutingType
    identifier: str = Field(min_length=1)
    name: str | None = None


class ChatSession(APIModel):
    """Chat session associated with the call."""

    session_id: str = Field(min_length=1)


class CallRecord(APIModel):
    """Top-level record for one caller interaction."""

    schema_version: Literal["1.0"] = "1.0"
    call_id: str = Field(min_length=1)
    caller_number: str | None = Field(default=None, max_length=50)
    language: str | None = Field(default=None, max_length=35)
    started_at: AwareDatetime
    ended_at: AwareDatetime | None = None
    outcome: CallOutcome | None = None
    routed_to: RoutingDestination | None = None
    intake: list[IntakeItem] = Field(default_factory=list)
    transcript: list[TranscriptEntry] = Field(default_factory=list)
    report: Report | None = None
    chat_session: ChatSession | None = None

