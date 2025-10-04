import httpx
from fastmcp import FastMCP

from app.config import settings
from app.schemas import HeartRateRequestParams, HeartRateResponse

heart_rate_router = FastMCP(name="Heart Rate MCP")


@heart_rate_router.tool
def get_heart_rate(
    start_date: str | None = None,
    end_date: str | None = None,
    workout_id: str | None = None,
    source: str | None = None,
    min_avg: float | None = None,
    max_avg: float | None = None,
    min_max: float | None = None,
    max_max: float | None = None,
    min_min: float | None = None,
    max_min: float | None = None,
    sort_by: str = "date",
    sort_order: str = "desc",
    limit: int = 20,
    offset: int = 0,
) -> dict:
    """
    Get heart rate data with filtering, sorting, and pagination from the external API.
    
    Args:
        start_date: ISO 8601 format (e.g., '2023-12-01T00:00:00Z')
        end_date: ISO 8601 format (e.g., '2023-12-31T23:59:59Z')
        workout_id: Filter by specific workout ID
        source: Filter by data source (e.g., 'Apple Health')
        min_avg: Minimum average heart rate
        max_avg: Maximum average heart rate
        min_max: Minimum maximum heart rate
        max_max: Maximum maximum heart rate
        min_min: Minimum minimum heart rate
        max_min: Maximum minimum heart rate
        sort_by: Sort field (default: date)
        sort_order: Sort order (default: desc)
        limit: Number of results to return (1-100, default: 20)
        offset: Number of results to skip (default: 0)
    
    Returns:
        Dictionary containing heart rate data, recovery data, summary, and metadata
    """
    # Validate parameters
    params = HeartRateRequestParams(
        start_date=start_date,
        end_date=end_date,
        workout_id=workout_id,
        source=source,
        min_avg=min_avg,
        max_avg=max_avg,
        min_max=min_max,
        max_max=max_max,
        min_min=min_min,
        max_min=max_min,
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
                f"{settings.external_api_base_url}/api/v1/heart-rate",
                params=query_params,
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            
            # Parse and return the response
            heart_rate_data = response.json()
            return heart_rate_data
            
    except httpx.HTTPStatusError as e:
        return {
            "error": f"HTTP error {e.response.status_code}",
            "message": e.response.text,
            "data": [],
            "recovery_data": [],
            "summary": {
                "total_records": 0,
                "avg_heart_rate": 0,
                "max_heart_rate": 0,
                "min_heart_rate": 0,
                "avg_recovery_rate": 0,
                "max_recovery_rate": 0,
                "min_recovery_rate": 0
            },
            "meta": {
                "requested_at": "",
                "filters": {},
                "result_count": 0,
                "date_range": {}
            }
        }
    except httpx.RequestError as e:
        return {
            "error": f"Request error: {str(e)}",
            "message": "Failed to connect to external API",
            "data": [],
            "recovery_data": [],
            "summary": {
                "total_records": 0,
                "avg_heart_rate": 0,
                "max_heart_rate": 0,
                "min_heart_rate": 0,
                "avg_recovery_rate": 0,
                "max_recovery_rate": 0,
                "min_recovery_rate": 0
            },
            "meta": {
                "requested_at": "",
                "filters": {},
                "result_count": 0,
                "date_range": {}
            }
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "message": "An unexpected error occurred",
            "data": [],
            "recovery_data": [],
            "summary": {
                "total_records": 0,
                "avg_heart_rate": 0,
                "max_heart_rate": 0,
                "min_heart_rate": 0,
                "avg_recovery_rate": 0,
                "max_recovery_rate": 0,
                "min_recovery_rate": 0
            },
            "meta": {
                "requested_at": "",
                "filters": {},
                "result_count": 0,
                "date_range": {}
            }
        }
