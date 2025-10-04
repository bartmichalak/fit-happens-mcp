import httpx
from fastmcp import FastMCP

from app.config import settings
from app.schemas import WorkoutRequestParams, WorkoutResponse

workouts_router = FastMCP(name="Workouts MCP")


@workouts_router.tool
def get_workouts(
    start_date: str | None = None,
    end_date: str | None = None,
    workout_type: str | None = None,
    location: str | None = None,
    min_duration: int | None = None,
    max_duration: int | None = None,
    min_distance: float | None = None,
    max_distance: float | None = None,
    sort_by: str = "date",
    sort_order: str = "desc",
    limit: int = 20,
    offset: int = 0,
) -> dict:
    """
    Get workouts with filtering, sorting, and pagination from the external API.
    
    Args:
        start_date: ISO 8601 format (e.g., '2023-12-01T00:00:00Z')
        end_date: ISO 8601 format (e.g., '2023-12-31T23:59:59Z')
        workout_type: e.g., 'Outdoor Walk', 'Indoor Walk'
        location: Indoor or Outdoor
        min_duration: in seconds
        max_duration: in seconds
        min_distance: in km
        max_distance: in km
        sort_by: Sort field (default: date)
        sort_order: Sort order (default: desc)
        limit: Number of results to return (1-100, default: 20)
        offset: Number of results to skip (default: 0)
    
    Returns:
        Dictionary containing workout data and metadata
    """
    # Validate parameters
    params = WorkoutRequestParams(
        start_date=start_date,
        end_date=end_date,
        workout_type=workout_type,
        location=location,
        min_duration=min_duration,
        max_duration=max_duration,
        min_distance=min_distance,
        max_distance=max_distance,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )
    
    # Prepare query parameters, excluding None values
    query_params = {
        key: value for key, value in params.model_dump().items() 
        if value is not None
    }
    
    # Make HTTP request to external API
    try:
        with httpx.Client(timeout=settings.external_api_timeout) as client:
            response = client.get(
                f"{settings.external_api_base_url}/api/v1/workouts",
                params=query_params,
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            
            # Parse and return the response
            workout_data = response.json()
            return workout_data
            
    except httpx.HTTPStatusError as e:
        return {
            "error": f"HTTP error {e.response.status_code}",
            "message": e.response.text,
            "data": [],
            "meta": {
                "requested_at": "",
                "filters": {},
                "result_count": 0,
                "date_range": {"start": "", "end": "", "duration_days": 0}
            }
        }
    except httpx.RequestError as e:
        return {
            "error": f"Request error: {str(e)}",
            "message": "Failed to connect to external API",
            "data": [],
            "meta": {
                "requested_at": "",
                "filters": {},
                "result_count": 0,
                "date_range": {"start": "", "end": "", "duration_days": 0}
            }
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "message": "An unexpected error occurred",
            "data": [],
            "meta": {
                "requested_at": "",
                "filters": {},
                "result_count": 0,
                "date_range": {"start": "", "end": "", "duration_days": 0}
            }
        }
