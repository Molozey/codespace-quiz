from pydantic import BaseModel


class ReceiverResult(BaseModel):
    status: int
    reason: str | None
