
class Commands:
    pass

class Terminal:
    
    def __init__(self):
        
        import os
        self.os = os

        # Color codes for terminal output
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKCYAN = '\033[96m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

        # Terminal state variables
        self.commands = Commands()
        self.vRunning = False
        self.vStop = False
        self.vCase = False
        self.current_stage = 0
        
        # Command history
        self.command_history = []
        self.max_history = 100
        
        # Load commands from JSON
        import json as js
        try:
            with open("commands.json", "r") as file:
                self.commands = js.load(file)
        except FileNotFoundError:
            print(f"{self.FAIL}Warning: commands.json not found. Using default commands.{self.ENDC}")
            self.commands = {"commands": [{"help": {"action": "run:self:help()"}, "exit": {"action": "None"}}]}
        except js.JSONDecodeError as e:
            print(f"{self.FAIL}Error parsing commands.json: {str(e)}{self.ENDC}")
            self.commands = {"commands": [{"help": {"action": "run:self:help()"}, "exit": {"action": "None"}}]}


    def iFlush(self, case):
        """Clears the terminal if case is True."""
        if case:
            self.os.system('cls' if self.os.name == 'nt' else 'clear')

    def iGetTasks(self) -> list:
        """Returns a list of tasks to be executed."""
        return []
    
    def iExecuteUnknownTasks(self, tasks):
        """Recognizes Tasks and Send them to the right function."""
        # Implementation of executing unknown tasks
        pass
    
    def iGetInput(self):
        """Gets Input from User."""
        user_input = input(f"{self.OKGREEN}C.L.A.Y Terminal$ {self.ENDC}")
        
        # Add to history if not empty and not duplicate
        if user_input.strip() and (not self.command_history or user_input.strip() != self.command_history[-1]):
            self.command_history.append(user_input.strip())
            # Keep history size manageable
            if len(self.command_history) > self.max_history:
                self.command_history.pop(0)
                
        return user_input

    def iCurrentStage(self):
        """Returns the Current Stage of the Terminal."""
        return self.current_stage
    
    def iProcessInput(self, user_input, stage):
        """Processes the User Input."""
        user_input = user_input.strip()
        
        if not user_input:  # Empty input
            return None
            
        # Split command and arguments
        parts = user_input.split()
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if not self.hValidateCommand(command):
            print(f"{self.FAIL}Unknown command: '{command}'. Type 'help' for available commands.{self.ENDC}")
            return None
            
        # Execute the command
        return self.hExecuteCommand(command, args, stage)
        
    def hExecuteCommand(self, command, args, stage):
        """Executes a validated command."""
        try:
            # Handle built-in commands first
            built_in_commands = {
                "clear": self.clear,
                "history": self.history,
                "toggle-clear": self.toggle_clear,
                "help": self.help,
                "ls": self.ls,
                "pwd": self.pwd,
                "cd": self.cd,
                "version": self.version,
                "status": self.status
            }
            
            if command in built_in_commands:
                built_in_commands[command](args)
                return True
                
            # Handle commands from JSON file
            if self.commands and "commands" in self.commands:
                command_data = self.commands["commands"][0].get(command)
                if not command_data:
                    return None
                    
                action = command_data.get("action")
                if action == "None":
                    self.vRunning = False
                    print(f"{self.OKGREEN}Goodbye!{self.ENDC}")
                elif action.startswith("run:self:"):
                    method_name = action.split(":")[-1].replace("()", "")
                    if hasattr(self, method_name):
                        getattr(self, method_name)(args)
                    else:
                        print(f"{self.FAIL}Method {method_name} not found{self.ENDC}")
                elif action.startswith("run:"):
                    # Handle external module execution
                    self.hExecuteExternalCommand(action, args)
                else:
                    print(f"{self.OKBLUE}Executing: {command} with args: {args}{self.ENDC}")
                    
        except Exception as e:
            print(f"{self.FAIL}Error executing command '{command}': {str(e)}{self.ENDC}")
            return False
        
        return True

    def hExecuteExternalCommand(self, action, args):
        """Executes external commands from modules."""
        try:
            # Parse action format: "run:path/to/module.py:function()"
            parts = action.split(":")
            if len(parts) >= 3:
                module_path = parts[1].lstrip("/")  # Remove leading slash if present
                function_call = parts[2].replace("()", "")  # Remove parentheses
                
                print(f"{self.OKCYAN}Launching external application: {module_path}{self.ENDC}")
                print(f"{self.WARNING}Transferring control to external module...{self.ENDC}")
                
                # Check if file exists
                if not self.os.path.exists(module_path):
                    print(f"{self.FAIL}Module file not found: {module_path}{self.ENDC}")
                    return False
                
                # Execute as subprocess to give full control
                import subprocess
                import sys
                
                try:
                    # Run the external module as a separate process
                    result = subprocess.run([
                        sys.executable, 
                        module_path
                    ], cwd=self.os.getcwd())
                    
                    print(f"{self.OKGREEN}External application completed with exit code: {result.returncode}{self.ENDC}")
                    return True
                    
                except Exception as e:
                    print(f"{self.FAIL}Error executing external application: {str(e)}{self.ENDC}")
                    # Fallback to inline execution
                    return self._execute_module_inline(module_path, function_call)
                    
            else:
                print(f"{self.FAIL}Invalid action format. Expected 'run:path/to/module.py:function()'{self.ENDC}")
                return False
                
        except Exception as e:
            print(f"{self.FAIL}Error loading external module: {str(e)}{self.ENDC}")
            return False
            
    def _execute_module_inline(self, module_path, function_call):
        """Fallback method for inline module execution."""
        try:
            import sys
            import importlib.util
            
            # Add the module directory to Python path temporarily
            module_dir = self.os.path.dirname(module_path)
            if module_dir and module_dir not in sys.path:
                sys.path.insert(0, module_dir)
                path_added = True
            else:
                path_added = False
                
            try:
                # Create module spec and load module
                spec = importlib.util.spec_from_file_location("external_module", module_path)
                if spec is None:
                    print(f"{self.FAIL}Could not create module spec for {module_path}{self.ENDC}")
                    return False
                
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Execute the specified function
                if hasattr(module, function_call):
                    print(f"{self.OKGREEN}Executing {function_call} from {module_path}...{self.ENDC}")
                    
                    func = getattr(module, function_call)
                    if callable(func):
                        try:
                            # Execute the function and wait for it to complete
                            result = func()
                            print(f"{self.OKGREEN}Module execution completed with return code: {result if result is not None else 0}{self.ENDC}")
                            return True
                        except SystemExit as e:
                            print(f"{self.OKGREEN}Module exited with code: {e.code}{self.ENDC}")
                            return True
                        except Exception as func_e:
                            print(f"{self.FAIL}Error executing function {function_call}: {str(func_e)}{self.ENDC}")
                            return False
                    else:
                        print(f"{self.FAIL}{function_call} is not callable{self.ENDC}")
                        return False
                else:
                    print(f"{self.FAIL}Function {function_call} not found in module {module_path}{self.ENDC}")
                    
                    # Debug: Show available functions in module
                    available_funcs = [name for name in dir(module) if callable(getattr(module, name)) and not name.startswith('_')]
                    if available_funcs:
                        print(f"{self.WARNING}Available functions in module: {', '.join(available_funcs)}{self.ENDC}")
                    return False
                
            finally:
                # Clean up: remove from path if we added it
                if path_added and module_dir in sys.path:
                    sys.path.remove(module_dir)
                    
        except Exception as e:
            print(f"{self.FAIL}Error loading external module: {str(e)}{self.ENDC}")
            import traceback
            print(f"{self.WARNING}Traceback: {traceback.format_exc()}{self.ENDC}")
            return False

    def help(self, args=None):
        """Shows available commands and their descriptions."""
        print(f"\n{self.BOLD}{self.HEADER}C.L.A.Y Terminal - Available Commands{self.ENDC}")
        print("=" * 60)
        
        # Organize commands by category
        categories = {}
        
        # Add commands from JSON
        if self.commands and "commands" in self.commands:
            commands = self.commands["commands"][0]
            for cmd, data in commands.items():
                category = data.get("category", "misc")
                description = data.get("description", "No description available")
                
                if category not in categories:
                    categories[category] = []
                categories[category].append((cmd, description))
        
        # Add built-in commands
        built_in_cmds = [
            ("clear", "Clear the terminal screen", "system"),
            ("history", "Show command history", "system"),
            ("toggle-clear", "Toggle auto-clear mode", "system"),
            ("pwd", "Print current working directory", "filesystem"),
            ("cd", "Change current directory", "filesystem"),
            ("version", "Show version information", "system"),
            ("status", "Show terminal status", "system")
        ]
        
        for cmd, desc, cat in built_in_cmds:
            if cat not in categories:
                categories[cat] = []
            # Only add if not already present
            if not any(existing_cmd == cmd for existing_cmd, _ in categories[cat]):
                categories[cat].append((cmd, desc))
        
        # Display commands by category
        category_colors = {
            "system": self.OKBLUE,
            "filesystem": self.OKGREEN, 
            "modules": self.OKCYAN,
            "misc": self.WARNING
        }
        
        for category in sorted(categories.keys()):
            color = category_colors.get(category, self.ENDC)
            print(f"\n{self.BOLD}{color}{category.upper()} COMMANDS:{self.ENDC}")
            print("-" * 30)
            
            for cmd, desc in sorted(categories[category]):
                print(f"  {self.OKGREEN}{cmd:<15}{self.ENDC} {desc}")
        
        print(f"\n{self.OKCYAN}Tip: Use 'command --help' for detailed command help{self.ENDC}")
        print(f"{self.OKCYAN}Tip: Use 'history' to see your recent commands{self.ENDC}")

    def ls(self, args=None):
        """Lists the contents of the current directory."""
        try:
            import os
            current_dir = os.getcwd()
            print(f"\n{self.BOLD}Contents of {current_dir}:{self.ENDC}")
            
            items = os.listdir(current_dir)
            for item in sorted(items):
                path = os.path.join(current_dir, item)
                if os.path.isdir(path):
                    print(f"{self.OKBLUE}📁 {item}/{self.ENDC}")
                else:
                    print(f"{self.OKGREEN}📄 {item}{self.ENDC}")
        except Exception as e:
            print(f"{self.FAIL}Error listing directory: {str(e)}{self.ENDC}")

    def clear(self, args=None):
        """Clears the terminal screen."""
        self.iFlush(True)

    def history(self, args=None):
        """Shows command history."""
        if hasattr(self, 'command_history') and self.command_history:
            print(f"\n{self.BOLD}Command History:{self.ENDC}")
            for i, cmd in enumerate(self.command_history[-10:], 1):
                print(f"{self.OKCYAN}{i:2d}. {cmd}{self.ENDC}")
        else:
            print(f"{self.WARNING}No command history available{self.ENDC}")

    def toggle_clear(self, args=None):
        """Toggles auto-clear mode."""
        self.vCase = not self.vCase
        status = "enabled" if self.vCase else "disabled"
        print(f"{self.OKGREEN}Auto-clear mode {status}{self.ENDC}")

    def pwd(self, args=None):
        """Prints the current working directory."""
        try:
            current_dir = self.os.getcwd()
            print(f"{self.OKBLUE}{current_dir}{self.ENDC}")
        except Exception as e:
            print(f"{self.FAIL}Error getting current directory: {str(e)}{self.ENDC}")

    def cd(self, args=None):
        """Changes the current directory."""
        try:
            if not args:
                # Go to home directory if no argument
                home_dir = self.os.path.expanduser("~")
                self.os.chdir(home_dir)
                print(f"{self.OKGREEN}Changed to home directory: {home_dir}{self.ENDC}")
            else:
                target_dir = " ".join(args)  # Handle paths with spaces
                if target_dir == "..":
                    self.os.chdir("..")
                elif target_dir == ".":
                    pass  # Stay in current directory
                else:
                    if not self.os.path.exists(target_dir):
                        print(f"{self.FAIL}Directory not found: {target_dir}{self.ENDC}")
                        return
                    if not self.os.path.isdir(target_dir):
                        print(f"{self.FAIL}Not a directory: {target_dir}{self.ENDC}")
                        return
                    self.os.chdir(target_dir)
                
                new_dir = self.os.getcwd()
                print(f"{self.OKGREEN}Changed directory to: {new_dir}{self.ENDC}")
                
        except PermissionError:
            print(f"{self.FAIL}Permission denied accessing directory{self.ENDC}")
        except Exception as e:
            print(f"{self.FAIL}Error changing directory: {str(e)}{self.ENDC}")

    def version(self, args=None):
        """Shows version information."""
        try:
            metadata = self.commands.get("metadata", {})
            version = metadata.get("version", "1.0.0")
            author = metadata.get("author", "Unknown")
            description = metadata.get("description", "C.L.A.Y Terminal")
            
            print(f"\n{self.BOLD}{self.HEADER}C.L.A.Y Terminal{self.ENDC}")
            print(f"{self.OKBLUE}Version: {version}{self.ENDC}")
            print(f"{self.OKBLUE}Author: {author}{self.ENDC}")
            print(f"{self.OKCYAN}{description}{self.ENDC}")
            print(f"{self.OKGREEN}Python: {self.get_python_version()}{self.ENDC}")
        except Exception as e:
            print(f"{self.FAIL}Error displaying version: {str(e)}{self.ENDC}")

    def status(self, args=None):
        """Shows current terminal status."""
        print(f"\n{self.BOLD}Terminal Status:{self.ENDC}")
        print(f"{self.OKGREEN}Running: {self.vRunning}{self.ENDC}")
        print(f"{self.OKGREEN}Auto-clear: {'Enabled' if self.vCase else 'Disabled'}{self.ENDC}")
        print(f"{self.OKGREEN}Current Stage: {self.current_stage}{self.ENDC}")
        print(f"{self.OKGREEN}Commands in History: {len(self.command_history)}{self.ENDC}")
        
        # Show current directory
        try:
            current_dir = self.os.getcwd()
            print(f"{self.OKGREEN}Current Directory: {current_dir}{self.ENDC}")
        except:
            print(f"{self.WARNING}Current Directory: Unable to determine{self.ENDC}")

    def get_python_version(self):
        """Gets the Python version."""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def ThisIsThis(self, user_input, command):
        """Checks if the user input matches the given command."""
        return user_input.strip().lower() == command.strip().lower()
    
    def iSwitchCase(self):
        """Switches the case variable."""
        self.vCase = not self.vCase
        return self.vCase
    
    def hValidateCommand(self, command):
        """Validates if a command exists."""
        # Built-in commands
        built_in_commands = ["clear", "history", "toggle-clear", "help", "ls", "pwd", "cd", "version", "status"]
        if command in built_in_commands:
            return True
            
        # Commands from JSON file
        if self.commands and "commands" in self.commands:
            commands_dict = self.commands["commands"][0]
            return command in commands_dict
        return False
