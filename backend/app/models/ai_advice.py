from sqlalchemy import Column, String, Text, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.base import Base

class AIAdvice(Base):
    __tablename__ = "ai_advice"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    symbol = Column(String, nullable=False, index=True)
    recommendation = Column(String, nullable=False) # BUY, SELL, HOLD
    summary = Column(Text, nullable=False)
    details = Column(JSONB)
    confidence = Column(Numeric(3, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    user = relationship("User", backref="ai_advice")
