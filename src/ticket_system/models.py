from enum import Enum
from pydantic import BaseModel

class Department(str, Enum):
    INFRASTRUCTURE = "Infrastructure"
    BILLING = "Billing"
    SECURITY = "Security"
    SUPPORT = "Support"

class Urgency(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class classificationOutput(BaseModel):
    urgency: Urgency