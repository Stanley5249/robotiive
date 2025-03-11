import httpx
import rich
import typer

from robotiive.api import (
    execute_task,
    get_projects,
    monitor_task_progress,
)
from robotiive.models import Project, ProjectsResponse, Task

__all__ = ["app", "run", "run_all"]

# ==============================================================================
# utility functions
# ==============================================================================


def get_default_client() -> httpx.Client:
    return httpx.Client(verify=False, timeout=10.0, base_url="https://localhost:16888/")


def select_project(projects_response: ProjectsResponse, project_name: str) -> Project:
    for project in projects_response.data:
        if project["name"] == project_name:
            return project

    raise ValueError(f"project name {project_name!r} not found")


def select_project_task(project: Project, task_name: str) -> Task:
    for task in project["tasks"]:
        if task["name"] == task_name:
            return task

    raise ValueError(f"task name {task_name!r} not found")


# ==============================================================================
# CLI
# ==============================================================================

console = rich.get_console()

app = typer.Typer(
    help="Robotiive CLI",
    add_completion=False,
    pretty_exceptions_show_locals=False,
)


@app.command()
def run(project_name: str, task_name: str) -> None:
    """Run a task in a project."""

    with get_default_client() as client:
        projects_response = get_projects(client)
        project = select_project(projects_response, project_name)
        task = select_project_task(project, task_name)

        console.log(f"Running task {task_name!r} in project {project_name!r}...")

        execution_response = execute_task(client, project["id"], task["id"])
        monitor_task_progress(client, execution_response.execute_id)

    console.log(f"Task {task_name!r} completed successfully.")


@app.command()
def run_all(project_name: str) -> None:
    """Run all tasks in a project sequentially."""

    console.log(f"Running all tasks in project {project_name!r} ...")

    with get_default_client() as client:
        projects_response = get_projects(client)
        project = select_project(projects_response, project_name)
        project_id = project["id"]

        for task in project["tasks"]:
            task_name = task["name"]
            task_id = task["id"]

            console.log(f"Running task {task_name!r} ...")

            execution_response = execute_task(client, project_id, task_id)
            monitor_task_progress(client, execution_response.execute_id)

            console.log(f"Task {task_name!r} completed successfully.")

    console.log("All tasks completed successfully.")
