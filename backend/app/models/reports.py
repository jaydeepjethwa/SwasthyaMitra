from pydantic import BaseModel


class Report(BaseModel):
    title: str
    description: str = "There was no serious disease found from the XRay."
    symptoms: str = None
    treatment: str = None
    user_id: int
    image_id: str
