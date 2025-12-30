I'll analyze the codebase to understand the project structure and create a comprehensive plan for the feature that reads the currently selected file in VSCode.Now let me look at more of the popup_window.py to understand the config tab structure:Now let me check if there's any VSCode integration already:Now let me understand what the user is asking for. Based on the Portuguese text "ter a opção de output (agent config) de arquivo que estiver selecionado no momento (pode ser o arquivo que esta selecionado no vscode ou o explorador de arquivos ou outro) dai o claude lê o arquivo", the user wants:

**A new input option that reads the currently selected file in VSCode (or file explorer) and provides it as input to the agent.**

Let me check if there are any examples of reading VSCode state:Perfect! Now I understand. The user wants a new input strategy that automatically reads the currently selected/open file in VSCode. Let me create a comprehensive plan:Now let me check if there's a way to detect VSCode's active file. Let me check the Windows-specific approaches:Now I have enough context to create a comprehensive plan. Let me create the detailed implementation plan:

# Feature: VSCode Active File Input Strategy

## Feature Description
Add a new input strategy that automatically reads the currently active/selected file in VSCode (or file explorer) and provides its content as input to agents. This allows users to quickly process files they are working on without manually selecting text or dragging files. When activated, the system will detect the active file in VSCode's window title, read its content, and pass it to the agent for processing.

## User Story
As a developer using AgentClick
I want to automatically read the file I'm currently viewing in VSCode
So that I can quickly analyze, refactor, or get help with the active file without manually selecting text or dragging files

## Problem Statement
Current input methods require users to:
- Manually select text in VSCode and copy it (requires multiple steps)
- Drag files to the mini popup (disrupts workflow)
- Take screenshots or use clipboard images (not ideal for code files)

This friction breaks the development workflow, especially when users want quick analysis or assistance with the file they're actively working on.

## Solution Statement
Create a new **VSCode Active File Input Strategy** that:
1. Detects VSCode as the active window
2. Extracts the active file path from VSCode's window title (format: "filename.ext - projectname - Visual Studio Code")
3. Reads the file content from disk
4. Provides it as input to the agent

This strategy integrates seamlessly with the existing InputManager system and follows the established Strategy Pattern. Users can select "VSCode Active File" from the Input dropdown in the Config tab, and pressing Pause will automatically read the active file.

## Relevant Files
Use these files to implement the feature:

- `core/input_strategy.py` - Add new InputType enum value: VSCODE_ACTIVE_FILE
- `core/input_strategies/vscode_active_file_strategy.py` - NEW FILE: Strategy implementation
- `core/input_strategies/__init__.py` - Export new strategy class
- `core/input_manager.py` - Register and use new strategy
- `ui/popup_window.py` - Add "VSCode Active File" option to Input dropdown
- `agents/base_agent.py` - Update _build_prompt to include file context if active file is used
- `config/agent_config.py` - Add to default allowed_inputs list

### New Files
- `core/input_strategies/vscode_active_file_strategy.py` - Detects VSCode window, extracts file path, reads file content

## Implementation Plan

### Phase 1: Foundation
- Create the new InputType enum value
- Implement VSCode window detection using Windows API
- Implement file path extraction from VSCode window title
- Set up basic file reading with error handling

### Phase 2: Core Implementation
- Create VSCodeActiveFileStrategy class following existing strategy pattern
- Implement capture_input() method with window title parsing
- Implement is_available() method to check if VSCode is active window
- Add comprehensive logging for debugging
- Handle edge cases (untitled files, remote files, binary files)

### Phase 3: Integration
- Register strategy in InputManager
- Add to Input dropdown in popup_window.py
- Update default allowed_inputs in agent_config.py
- Update README with new input type documentation
- Add tests and validation

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add New InputType to Enum
- Open `core/input_strategy.py`
- Add new enum value: `VSCODE_ACTIVE_FILE = "vscode_active_file"`
- Update `InputContent.get_text_for_agent()` to handle new type
- Add format: `[VSCODE ACTIVE FILE: {filename}]\n{content}`
- Write tests for: InputType enum has new value

### Step 2: Create VSCode Active File Strategy
- Create `core/input_strategies/vscode_active_file_strategy.py`
- Import required dependencies: `win32gui`, `win32con`, `win32process` (from pywin32)
- Implement `VSCodeActiveFileStrategy` class inheriting from `InputStrategy`
- Implement `get_input_type()` to return `InputType.VSCODE_ACTIVE_FILE`
- Write tests for: Strategy class instantiates correctly

### Step 3: Implement VSCode Window Detection
- In `VSCodeActiveFileStrategy`, create `_get_vscode_window()` method:
  - Use `win32gui.GetForegroundWindow()` to get active window
  - Use `win32gui.GetWindowText()` to get window title
  - Check if title contains "Visual Studio Code"
  - Return window handle or None
- Add error handling for when VSCode is not running
- Write tests for: Detects VSCode window correctly, returns None when VSCode not active

### Step 4: Implement File Path Extraction
- Create `_extract_file_path_from_title()` method:
  - Parse window title format: "filename.ext - foldername - Visual Studio Code"
  - Handle variations: "filename.ext - Visual Studio Code", "Untitled-*"
  - Extract filename from beginning of title
  - Search for file in common project locations or use OS file search
  - Return absolute file path or None
- Handle special cases:Untitled files, remote files (SSH, WSL), files without save
- Write tests for: Extracts correct path from various title formats

### Step 5: Implement File Content Reading
- Create `_read_file_content()` method:
  - Accept file path as parameter
  - Check if file exists and is readable
  - Try to read as UTF-8 text
  - Handle encoding errors (try UTF-16, latin-1 fallbacks)
  - Reject binary files
  - Return file content as string or None
- Add metadata collection: file size, line count, language/extension
- Write tests for: Reads text files correctly, handles binary files, handles encoding errors

### Step 6: Implement capture_input() Method
- Implement `capture_input()` method:
  - Call `_get_vscode_window()` to verify VSCode is active
  - Call `_extract_file_path_from_title()` to get file path
  - Call `_read_file_content()` to get file content
  - Return `InputContent` with:
    - `input_type`: VSCODE_ACTIVE_FILE
    - `text`: file content
    - `file_path`: extracted file path
    - `metadata`: filename, size, line count, extension
  - Return None if any step fails
- Add comprehensive logging at each step
- Write tests for: Returns InputContent when file available, returns None when errors

### Step 7: Implement is_available() Method
- Implement `is_available()` method:
  - Check if VSCode is active window
  - Verify window title contains extractable file path
  - Return True if both conditions met, False otherwise
- Make this a fast check without reading entire file
- Write tests for: Returns True when VSCode active with file, False otherwise

### Step 8: Register Strategy in InputManager
- Open `core/input_manager.py`
- Import `VSCodeActiveFileStrategy` from `core.input_strategies`
- Add to strategies list in `__init__()`:
  ```python
  VSCodeActiveFileStrategy(),
  ```
- Add to priority_order in `capture_input()` (after SELECTED_TEXT, before FILE_UPLOAD)
- Test that strategy is registered and available

### Step 9: Update Input Dropdown UI
- Open `ui/popup_window.py`
- Find `input_options` list in `_create_config_tab()` (around line 367)
- Add new option:
  ```python
  ("VSCode Active File", InputType.VSCODE_ACTIVE_FILE.value),
  ```
- Verify dropdown displays new option correctly
- Test selection in UI

### Step 10: Update Default Configuration
- Open `config/agent_config.py`
- Update `AgentSettings.__post_init__()` method
- Add `"vscode_active_file"` to default `allowed_inputs` list
- Ensure new agents have this input enabled by default
- Test that new agents include VSCode input in defaults

### Step 11: Update Documentation
- Open `README.md`
- Add new input type section in "Input Types" chapter:
  - Title: "### 5. 📝 VSCode Active File (NEW)"
  - How to use: "Have VSCode open with file → Press Pause"
  - Use case examples
  - Supported file types
- Update "Input Type Priority" section to include VSCode Active File
- Add workflow example showing usage
- Update "Per-Agent Input Filtering" section

### Step 12: Add PyWin32 Dependency
- Check if `pywin32` is in dependencies (PEP 723 section in README)
- Add installation instruction:
  ```bash
  uv add pywin32
  ```
- Document in "New Libraries Needed" section below

### Final Step: Validate Feature
- Run all validation commands listed below
- Ensure all acceptance criteria are met
- Verify zero regressions
- Test edge cases:
  - VSCode not running
  - VSCode open but no file active
  - Binary file active in VSCode
  - Untitled/new file in VSCode
  - Remote file (SSH/WSL) in VSCode
  - Very large files (>1MB)
  - Files with special characters in name
  - Files with unusual encodings

## Testing Strategy

### Unit Tests
- Test: `InputType.VSCODE_ACTIVE_FILE` enum value exists
- Test: `VSCodeActiveFileStrategy.get_input_type()` returns correct type
- Test: `_get_vscode_window()` detects VSCode correctly
- Test: `_get_vscode_window()` returns None when VSCode not active
- Test: `_extract_file_path_from_title()` parses various title formats
- Test: `_extract_file_path_from_title()` handles untitled files
- Test: `_read_file_content()` reads text files correctly
- Test: `_read_file_content()` rejects binary files
- Test: `_read_file_content()` handles encoding errors
- Test: `is_available()` returns True when VSCode active with file
- Test: `is_available()` returns False when VSCode not active
- Test: `capture_input()` returns InputContent when successful
- Test: `capture_input()` returns None on errors
- Test: InputContent contains correct metadata (filename, size, line count)

### Integration Tests
- Test: VSCodeActiveFileStrategy registered in InputManager
- Test: Strategy appears in Input dropdown in Config tab
- Test: Strategy can be selected as allowed input for agents
- Test: Pressing Pause with VSCode active reads the file
- Test: Agent receives file content and processes correctly
- Test: File path appears in agent context/focus_file
- Test: Integration with output modes (clipboard, file, editor)
- Test: Strategy priority order in auto-detection

### Edge Cases
- Edge case: VSCode not running - Strategy returns None, logs warning
- Edge case: VSCode active but no file open (welcome screen) - Returns None, logs info
- Edge case: Untitled/new file (not saved) - Returns None, suggests user saves first
- Edge case: Remote file (SSH/WSL) - Returns None, logs that remote files not supported
- Edge case: Binary file active in VSCode - Returns None, logs that binary files not supported
- Edge case: Very large file (>5MB) - Reads but logs warning about size
- Edge case: File with special characters in name - Handles correctly with proper path escaping
- Edge case: File with unusual encoding (UTF-16, Latin-1) - Tries multiple encodings
- Edge case: File deleted but still open in VSCode - Returns None, logs file not found
- Edge case: Multiple VSCode windows - Uses foreground window (active one)

## Acceptance Criteria
- [ ] New input strategy "VSCode Active File" available in Input dropdown
- [ ] Strategy detects VSCode as active window correctly
- [ ] Strategy extracts file path from VSCode window title
- [ ] Strategy reads file content and provides to agent
- [ ] Strategy handles errors gracefully (VSCode not running, no file, etc.)
- [ ] Strategy can be enabled/disabled per agent via Allowed Inputs
- [ ] Strategy appears in correct priority order for auto-detection
- [ ] File metadata (name, size, line count, extension) included in InputContent
- [ ] Agent receives file with proper context label "[VSCODE ACTIVE FILE]"
- [ ] README updated with documentation for new input type
- [ ] Zero regressions - existing input strategies still work correctly
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Edge cases handled without crashes

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `uv run agent_click.py` - Start the system and verify no import errors
- `python -c "from core.input_strategies.vscode_active_file_strategy import VSCodeActiveFileStrategy; print('Strategy imports successfully')"` - Verify strategy imports
- `python -c "from core.input_strategy import InputType; print([t.value for t in InputType])"` - Verify VSCODE_ACTIVE_FILE in enum
- Manual test: Open VSCode with a Python file → Select "VSCode Active File" in Config → Press Pause → Verify file content is processed
- Manual test: Try with VSCode closed → Verify graceful error handling
- Manual test: Try with untitled file → Verify appropriate error message
- Manual test: Try with binary file → Verify rejection with log message
- Check that existing input types (Text Selection, File Upload, etc.) still work correctly
- Verify Input dropdown shows new option in Config tab

## Notes
- **New libraries needed**: 
  - `uv add pywin32` - Required for Windows API access (GetForegroundWindow, GetWindowText)
  - This library provides access to win32gui, win32con, win32process modules
  - Only ~5MB install, widely used and stable
  - Alternative: use `ctypes` with windll but more complex and less reliable

- **Future considerations or potential improvements**:
  - Support for other editors (Sublime Text, Notepad++, JetBrains IDEs)
  - Use VSCode extension API for more reliable file detection (requires extension development)
  - Cache recently used files for faster access
  - Add file size limit warning for very large files
  - Support for reading specific line ranges instead of entire file

- **Breaking changes or migration notes**:
  - None - this is a new feature, doesn't change existing behavior
  - Existing configurations continue to work without modification
  - New input type added to default allowed_inputs for new agents only

- **Performance considerations**:
  - Window detection is fast (~1-2ms)
  - File reading depends on file size (typical dev files <100KB load instantly)
  - Large files (>1MB) may cause slight delay, consider adding size limit
  - Strategy check in is_available() is lightweight, no file I/O

- **Security considerations**:
  - Only reads files from disk, doesn't modify anything
  - Follows OS file permissions (can't read files user doesn't have access to)
  - No network access or external dependencies
  - File paths validated before reading

- **Dependencies or prerequisites**:
  - Requires VSCode to be installed and running
  - Requires Windows OS (uses Windows API)
  - Requires file to be saved on disk (not unsaved/untitled)
  - pywin32 library must be installed