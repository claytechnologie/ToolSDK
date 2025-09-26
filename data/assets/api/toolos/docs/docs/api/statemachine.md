# State Machine API

The State Machine API provides application flow control with predefined states for managing application lifecycle.

## Class Reference

::: toolos.api.StateMachineAPI

## Predefined States

| State | Description |
|-------|-------------|
| `FIRST_ENTRY` | Initial application state |
| `MAINMENU` | Main menu state |
| `STEP_1` to `STEP_5` | Generic workflow steps |
| `EXIT` | Application exit state |

## Basic Usage

```python
from toolos.api import StateMachineAPI

# Initialize state machine
state_machine = StateMachineAPI()

# Check current state (starts with FIRST_ENTRY)
if state_machine.IsState(state_machine.FIRST_ENTRY):
    print("First time running")
    state_machine.SetState(state_machine.MAINMENU)

# State-based logic
if state_machine.IsState(state_machine.MAINMENU):
    show_main_menu()
elif state_machine.IsState(state_machine.EXIT):
    cleanup_and_exit()
```

## Methods

### `SetState(new_state)`
Changes the current state to the specified state.

### `GetState()`
Returns the current state string.

### `IsState(check_state)`
Checks if the current state matches the specified state.

## Application Flow Example

```python
class Application:
    def __init__(self):
        self.state_machine = StateMachineAPI()
        self.running = True
        
    def run(self):
        while self.running:
            if self.state_machine.IsState(self.state_machine.FIRST_ENTRY):
                self.initialize_app()
                self.state_machine.SetState(self.state_machine.MAINMENU)
                
            elif self.state_machine.IsState(self.state_machine.MAINMENU):
                choice = self.show_menu()
                self.handle_menu_choice(choice)
                
            elif self.state_machine.IsState(self.state_machine.EXIT):
                self.running = False
```