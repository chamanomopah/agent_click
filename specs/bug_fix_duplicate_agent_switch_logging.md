# Bug: Duplicate Agent Switch Logging

## Bug Description
When the user switches agents by pressing `Ctrl+Pause`, the system logs the same message twice:
- Once from `AgentRegistry.next_agent()` at line 83 in `agents/agent_registry.py`
- Once from `AgentClickSystem._on_switch_pressed()` at line 160 in `core/system.py`

This creates redundant log output that clutters the console and the activity log in the popup window.

**Expected behavior:** Agent switch should be logged once when it occurs.

**Actual behavior:** Agent switch is logged twice with identical messages.

**Impact:** Confusing log output that makes it harder to track actual system behavior and understand the sequence of events.

## Problem Statement
The agent switching functionality has redundant logging in two separate components. When `AgentClickSystem._on_switch_pressed()` calls `AgentRegistry.next_agent()`, both methods log the same "Switched to agent:" message, creating duplicate log entries.

## Solution Statement
Remove the duplicate logging from `core/system.py` line 160, keeping only the log in `agents/agent_registry.py` line 83. This is the minimal surgical fix because:

1. The `AgentRegistry.next_agent()` method is the core implementation that actually performs the switch
2. Keeping the log in the registry layer ensures all switch operations are logged, regardless of who calls the method
3. Removing the duplicate log from the system layer eliminates the redundancy without losing any information
4. The system layer already has sufficient logging through the mini popup update and large popup update

## Steps to Reproduce
1. Start the AgentClick system with `uv run agent_click.py`
2. Wait for system to initialize and mini popup to appear
3. Press `Ctrl+Pause` to switch to the next agent
4. Observe the console output - you will see two identical log messages:
   ```
   [13:55:02] [INFO] [AgentRegistry] Switched to agent: Prompt Assistant
   [13:55:02] [INFO] [AgentClickSystem] Switched to agent: Prompt Assistant
   ```

## Root Cause Analysis
The bug occurs due to improper separation of concerns in logging responsibility:

1. **Location of bug:** Two files are involved:
   - `agents/agent_registry.py` line 83 in `next_agent()` method
   - `core/system.py` line 160 in `_on_switch_pressed()` method

2. **Why it occurs:**
   - `AgentRegistry.next_agent()` performs the actual agent switch and logs it
   - `AgentClickSystem._on_switch_pressed()` calls `next_agent()` and then logs the same information
   - This creates a duplicate log entry for every single agent switch

3. **What conditions trigger it:**
   - The bug manifests every time the user presses `Ctrl+Pause` to switch agents
   - It affects all agent switches, regardless of which agents are involved

4. **Why it wasn't caught earlier:**
   - The logging works correctly (just redundant), so functionality appears normal
   - The extra log entries may have been overlooked during manual testing
   - Automated tests may not check for specific log message counts

5. **Technical details:**
   - The `next_agent()` method in `AgentRegistry` updates `current_index` and returns the new agent
   - Before returning, it logs: `logger.info(f"Switched to agent: {agent.metadata.name}")`
   - The calling code in `_on_switch_pressed()` then logs the exact same message with the same information
   - This violates the DRY (Don't Repeat Yourself) principle and creates log noise

## Relevant Files
Use these files to fix the bug:

- `core/system.py` - Contains the duplicate log that should be removed (line 160)
- `agents/agent_registry.py` - Contains the authoritative log that should be kept (line 83)

No new files need to be created for this fix.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Verify Current Behavior
- Read `core/system.py` and locate line 160 in the `_on_switch_pressed()` method
- Read `agents/agent_registry.py` and locate line 83 in the `next_agent()` method
- Confirm both log the same "Switched to agent:" message
- Run the system and press Ctrl+Pause to observe the duplicate logging

### Step 2: Remove Duplicate Log Entry
- Open `core/system.py`
- Locate the `_on_switch_pressed()` method (starts at line 156)
- Find line 160: `logger.info(f"Switched to agent: {next_agent.metadata.name}")`
- **Delete this line** (the duplicate log)
- Ensure the rest of the method remains intact, including:
  - The call to `next_agent()`
  - The signal emission to update mini popup
  - The signal emission to update large popup (if open)
  - The log message emission to large popup
- Save the file

### Step 3: Verify Fix Works
- Run the system: `cd C:\.agent_click && uv run agent_click.py`
- Press `Ctrl+Pause` to switch agents
- Verify that only ONE log message appears: `[INFO] [AgentRegistry] Switched to agent: <name>`
- Verify the mini popup updates correctly
- Verify the large popup (if open) shows "🔄 Switched to <agent name>" message
- Switch agents multiple times to confirm consistent behavior

### Final Step: Validate Fix
- Run all validation commands listed below
- Verify the bug is fixed (only one log per switch)
- Ensure zero regressions (agent switching still works correctly)
- Test edge cases (switching with popup open/closed, multiple rapid switches)

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `cd C:\.agent_click && uv run agent_click.py` - Start the system to manually test the fix
- Press `Ctrl+Pause` multiple times - Verify only one log message per switch (not two)
- Click mini popup to open large popup - Verify config loads correctly for each agent
- With large popup open, press `Ctrl+Pause` - Verify switch happens with single log and popup updates
- Check activity log in large popup - Verify "🔄 Switched to..." message appears once per switch

## Notes
- No new libraries needed for this fix
- This is a minimal surgical fix - only removing one line of duplicate code
- The fix maintains all existing functionality while eliminating log redundancy
- The remaining log in `AgentRegistry.next_agent()` is sufficient because:
  - It's at the core implementation layer where the switch actually happens
  - It will catch switches from any caller (not just `_on_switch_pressed()`)
  - The system layer still logs other related activities (mini popup update, large popup update)
- Potential side effects: None - this only removes redundant logging
- Related issues that might exist but are out of scope:
  - Other potential duplicate logging in other parts of the codebase (not investigated)
  - No other issues identified in the agent switch flow
