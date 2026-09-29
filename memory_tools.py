import json 
from pathlib import Path
from datetime import datetime
# folder name where persistent memory is stored

MEMORY_DIR = Path(__file__).resolve().parent.parent / "projectmemory"

# task_state.json file 

TASK_STATE_FILE= MEMORY_DIR/"task_state.json"

# Only these project statuses are allowed
VALID_STATUSES = {
    "pending",
    "in_progress",
    "pending_validation",
    "completed",
    "blocked",
    # Detailed Workflow Statuses
    "planning",
    "implementation",
     "pending_testing",
     "testing_failed",
     "pending_review",
     "review_failed",
     
}

def get_project_state():
    """
       Read the current project state from task_state.json.
    """
    with open(TASK_STATE_FILE,"r",encoding="utf-8") as file:
        state=json.load(file)
    return state


def update_project_state(
    current_task=None,
    status=None,
    last_completed_task=None,
    next_task=None,
    reset_task=False
):
    """
    Update selected fields in task_state.json.
    Fields that are not provided remain unchanged.
    """
    # read  existing project state 
    state=get_project_state()
    
    if reset_task:
        state["last_completed_task"]=None
        state["next_task"]=None
    # Validate status if a new stauses was provided
    if status is not None and  status not in VALID_STATUSES:
        raise ValueError(f"Invalid status:{status}")
    
    # update only  the fields that are provided   
    if current_task is not None: # type: ignore
        state["current_task"]=current_task   # type: ignore
    
    if status is not None:                      # type: ignore
        state["status"]=status                  # type: ignore
    if last_completed_task is not None:         #  type: ignore
        state["last_completed_task"]=last_completed_task   #  type: ignore
    if next_task is not None:                              #  type: ignore
        state["next_task"]=next_task                       #  type: ignore
    # Time stamp should update whenevr project sate changes 
    state["updated_at"] = datetime.now().isoformat(timespec="seconds")
    
    with open(TASK_STATE_FILE,"w",encoding="utf-8")as file:
        json.dump(state,file,indent=2)
        return state

if __name__ == "__main__":
    updated_state = update_project_state(
        status="pending_validation"
    )

    print(updated_state)


