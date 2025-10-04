from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.config import settings


class FilterParams(BaseModel):
    filters: dict[str, str] = Field(default_factory=dict)
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=settings.paging_limit, ge=1)
    sort_by: str | None = Field(default=None)

    @field_validator("filters")
    @classmethod
    def validate_filters(cls, v: dict[str, str]) -> dict[str, str]:
        """Remove empty or whitespace-only filters."""
        return {k: v for k, v in v.items() if v and v.strip()}

    def validate_against_model(self, model_class: type) -> None:
        """Validate that filter and sort fields exist in the model."""
        # This method can be removed or updated based on your specific needs
        # since you're not using a database model
        pass


# Workout API Schemas
class WorkoutValueUnit(BaseModel):
    value: float
    unit: str


class WorkoutSummary(BaseModel):
    avg_heart_rate: int
    max_heart_rate: int
    min_heart_rate: int
    total_calories: int


class Workout(BaseModel):
    id: str
    name: str
    location: str
    start: str
    end: str
    duration: int
    distance: WorkoutValueUnit
    active_energy_burned: WorkoutValueUnit
    intensity: WorkoutValueUnit
    temperature: WorkoutValueUnit
    humidity: WorkoutValueUnit
    source: str
    summary: WorkoutSummary


class WorkoutFilters(BaseModel):
    additionalProp1: dict = Field(default_factory=dict)


class WorkoutDateRange(BaseModel):
    start: str
    end: str
    duration_days: int


class WorkoutMeta(BaseModel):
    requested_at: str
    filters: WorkoutFilters
    result_count: int
    date_range: WorkoutDateRange


class WorkoutResponse(BaseModel):
    data: list[Workout]
    meta: WorkoutMeta


class WorkoutRequestParams(BaseModel):
    start_date: Optional[str] = Field(None, description="ISO 8601 format (e.g., '2023-12-01T00:00:00Z')")
    end_date: Optional[str] = Field(None, description="ISO 8601 format (e.g., '2023-12-31T23:59:59Z')")
    workout_type: Optional[str] = Field(None, description="e.g., 'Outdoor Walk', 'Indoor Walk'")
    location: Optional[str] = Field(None, description="Indoor or Outdoor")
    min_duration: Optional[int] = Field(None, description="in seconds")
    max_duration: Optional[int] = Field(None, description="in seconds")
    min_distance: Optional[float] = Field(None, description="in km")
    max_distance: Optional[float] = Field(None, description="in km")
    sort_by: str = Field("date", description="Sort field")
    sort_order: str = Field("desc", description="Sort order")
    limit: int = Field(20, ge=1, le=100, description="Number of results to return")
    offset: int = Field(0, ge=0, description="Number of results to skip")
