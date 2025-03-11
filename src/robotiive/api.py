import httpx
from httpx_sse import connect_sse

from robotiive.models import (
    ExecutionResponse,
    ProjectsResponse,
    TaskProgressEvent,
)

__all__ = ["get_projects", "execute_task", "monitor_task_progress"]


def get_projects(client: httpx.Client) -> ProjectsResponse:
    url = "iscool/v3/projects"
    response = client.get(url, params={"start": 0, "count": 100})
    response.raise_for_status()
    return ProjectsResponse.model_validate_json(response.content)


def execute_task(
    client: httpx.Client, project_id: str, task_id: str
) -> ExecutionResponse:
    url = "iscool/v3/execute/task"
    data = {"projectID": project_id, "taskID": task_id}
    response = client.post(url, json=data)
    response.raise_for_status()
    return ExecutionResponse.model_validate_json(response.content)


def monitor_task_progress(client: httpx.Client, execute_id: str) -> None:
    url = f"iscool/v3/execute/task/{execute_id}/monitor"

    with connect_sse(client, "GET", url) as event_source:
        for sse in event_source.iter_sse():
            event = TaskProgressEvent.model_validate_json(sse.data)

            if event.type == 1:
                progress = event.progress
                result = progress["result"]
                message = progress["message"]

                if result == 1:
                    msg = f"task failed\n{message}"
                    raise ValueError(msg)

                if result == 6:
                    return

                if result == 10:
                    msg = "task stopped"
                    raise ValueError(msg)

    raise ValueError("no task progress event found")
