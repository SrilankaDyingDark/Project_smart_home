from pydantic import BaseModel
from datetime import datetime

# -------- User -------- #
class UserBase(BaseModel):
    name: str
    house_area: float

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

# -------- Device -------- #
class DeviceBase(BaseModel):
    name: str
    type: str

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    class Config:
        from_attributes = True

# -------- UsageLog -------- #
class UsageLogBase(BaseModel):
    user_id: int
    device_id: int
    start_time: datetime
    finish_time: datetime

class UsageLogCreate(UsageLogBase):
    pass

class UsageLog(UsageLogBase):
    id: int
    class Config:
        from_attributes = True

# -------- SecurityEvent -------- #
class SecurityEventBase(BaseModel):
    user_id: int
    event: str
    timestamp: datetime

class SecurityEventCreate(SecurityEventBase):
    pass

class SecurityEvent(SecurityEventBase):
    id: int
    class Config:
        from_attributes = True

class SecurityEventWithDetails(SecurityEventBase):
    id: int | None = None
    severity: str
    user_name: str
    device_name: str
    device_type: str
    start_time: datetime
    duration_minutes: float
    reasons: list[str]

    class Config:
        from_attributes = True

# -------- Feedback -------- #
class FeedbackBase(BaseModel):
    user_id: int
    message: str
    timestamp: datetime

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    class Config:
        from_attributes = True
