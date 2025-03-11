from typing import TypedDict

from pydantic import BaseModel, ConfigDict, Field, with_config

__all__ = [
    "Task",
    "Project",
    "ProjectsResponse",
    "ExecutionResponse",
    "Progress",
    "TaskProgressEvent",
]


base_config: ConfigDict = {"extra": "ignore"}

# ==============================================================================
# get_projects
# ==============================================================================


@with_config(base_config)
class Task(TypedDict):
    name: str
    id: str
    # comment: str


@with_config(base_config)
class Project(TypedDict):
    id: str
    name: str
    # comment: str
    tasks: list[Task]


class ProjectsResponse(BaseModel):
    model_config = base_config
    # total: int
    data: list[Project]


# ==============================================================================
# execute_task
# ==============================================================================


class ExecutionResponse(BaseModel):
    model_config = base_config
    execute_id: str = Field(alias="executeID")


# ==============================================================================
# wait_task_result
# ==============================================================================


@with_config(base_config)
class Progress(TypedDict):
    result: int
    message: str


class TaskProgressEvent(BaseModel):
    model_config = base_config
    type: int
    progress: Progress
