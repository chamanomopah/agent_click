# Bug: SelectedTextStrategy Causes Unwanted Ctrl+C and Clipboard Interference

## Bug Description
When a user has text in clipboard and presses Pause to process it with an agent, `SelectedTextStrategy` incorrectly triggers a destructive Ctrl+C operation that interferes with the clipboard, even though the text is already available in clipboard via `TextSelectionStrategy`.

**Actual Behavior:**
- User selects text and copies it to clipboard (Ctrl+C)
- User presses Pause to activate agent
- System incorrectly uses `SelectedTextStrategy` which performs another Ctrl+C
- This causes unwanted clipboard interference and potential data loss
- Log shows: `[INFO] [SelectedTextStrategy] Captured selected text: 358 chars`
- Log shows: `[INFO] [InputManager] ✅ Auto-detected input: selected_text`

**Expected Behavior:**
- When text is in clipboard, `TextSelectionStrategy` should capture it non-destructively
- `SelectedTextStrategy` should only be used as a fallback when clipboard is empty
- No extra Ctrl+C should be performed when clipboard already has the desired text
- Log should show: `[INFO] [TextSelectionStrategy] Captured text selection: 358 chars`
- Log should show: `[INFO] [InputManager] ✅ Auto-detected input: text_selection`

**Symptoms:**
- Unwanted Ctrl+C keyboard simulation
- Clipboard being overwritten and restored unnecessarily
- Input type incorrectly identified as `selected_text` instead of `text_selection`
- Potential data loss if clipboard restore fails

**When/How Bug Manifests:**
- When user has text in clipboard and presses Pause
- When `TextSelectionStrategy` should work but `SelectedTextStrategy` is used instead
- Affects all agents that process text input

**Impact on Users:**
- Annoying Ctrl+C visual feedback in applications
- Clipboard interference in workflows
- Unnecessary keyboard simulation
- Confusion about why system isn't using clipboard directly

## Problem Statement
`SelectedTextStrategy.is_available()` always returns `True` without checking if text is actually selected on screen. This causes it to be attempted in priority order before checking if `TextSelectionStrategy` (non-destructive clipboard read) has already succeeded. The strategy uses destructive Ctrl+C operations that interfere with clipboard even when clipboard already contains the desired text.

## Solution Statement
Fix `SelectedTextStrategy.is_available()` to return `False` when clipboard already has text content, making it a true fallback strategy that only activates when `TextSelectionStrategy` fails. This ensures:

1. `TextSelectionStrategy` (non-destructive clipboard read) is always tried first
2. `SelectedTextStrategy` (destructive Ctrl+C) is only used when clipboard is empty
3. No unwanted Ctrl+C when clipboard already has the desired text
4. Minimal change - only fix the `is_available()` method

This is surgical: Only one method changed, no refactoring, no side effects.

## Steps to Reproduce
1. Start the AgentClick system: `cd C:\.agent_click && uv run agent_click.py`
2. In any application (e.g., Notepad, VSCode), select some text (e.g., 358 characters)
3. Copy the text to clipboard using Ctrl+C
4. Press Pause to activate the agent
5. Observe the console logs
6. **Bug**: System shows `[INFO] [SelectedTextStrategy] Captured selected text: 358 chars`
7. **Bug**: System shows `[INFO] [InputManager] ✅ Auto-detected input: selected_text`
8. **Bug**: Unwanted Ctrl+C operation is performed (visible in some applications)

**Expected Correct Behavior:**
- System should show `[INFO] [TextSelectionStrategy] Captured text selection: 358 chars`
- System should show `[INFO] [InputManager] ✅ Auto-detected input: text_selection`
- No Ctrl+C should be performed since clipboard already has the text

## Root Cause Analysis

**Where the Bug Occurs:**
File: `C:/.agent_click/core/input_strategies/selected_text_strategy.py`
Method: `is_available()` (lines 79-91)

**Why It Occurs:**
The `is_available()` method in `SelectedTextStrategy` always returns `True` without performing any actual check:

```python
def is_available(self) -> bool:
    """Check if text is currently selected.

    This is a non-destructive check - we always return True since we can't
    detect if text is selected without actually capturing it (which would
    interfere with the user's clipboard).

    The actual availability will be determined when capture_input() is called.

    Returns:
        True (always available to try)
    """
    return True
```

**What Conditions Trigger It:**
- When `TextSelectionStrategy` has text in clipboard (should succeed)
- When `InputManager` iterates through priority order (lines 101-106 in `input_manager.py`)
- Since `SelectedTextStrategy.is_available()` always returns True, it's considered available
- If `TextSelectionStrategy.capture_input()` fails for any reason (even transient clipboard issues), `SelectedTextStrategy` takes over with destructive Ctrl+C

**Why It Wasn't Caught Earlier:**
- The system appears to work (text is captured and processed)
- The bug is subtle - wrong strategy is used but result is the same
- Only visible in logs and unwanted Ctrl+C behavior
- Clipboard restore hides the interference in most cases

**Technical Details:**
The priority order in `InputManager.capture_input()` (lines 88-94) is:
1. `TEXT_SELECTION` - Should work when clipboard has text
2. `SELECTED_TEXT` - Should only work as fallback when clipboard empty

But because `SelectedTextStrategy.is_available()` always returns True, it causes the strategy to be considered even when `TextSelectionStrategy` should handle it. The destructive Ctrl+C in `SelectedTextStrategy.capture_input()` (line 49) then interferes with clipboard unnecessarily.

## Relevant Files
Use these files to fix the bug:

- `C:/.agent_click/core/input_strategies/selected_text_strategy.py` - **PRIMARY FILE** - Contains the buggy `is_available()` method that always returns True, causing unwanted Ctrl+C interference

- `C:/.agent_click/core/input_manager.py` - **CONTEXT FILE** - Shows how strategies are prioritized and selected; helps understand the priority order

- `C:/.agent_click/core/input_strategies/text_selection_strategy.py` - **REFERENCE FILE** - Shows correct implementation of `is_available()` that actually checks clipboard content

- `C:/.agent_click/core/selection_manager.py` - **UTILITY FILE** - Provides clipboard access methods used by both strategies

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Understand Current Behavior
- Read `C:/.agent_click/core/input_strategies/selected_text_strategy.py` lines 79-91
- Note that `is_available()` always returns `True` without any check
- Read `C:/.agent_click/core/input_strategies/text_selection_strategy.py` lines 57-68
- Note that it properly checks clipboard content in `is_available()`
- Understand the difference: `TextSelectionStrategy` checks, `SelectedTextStrategy` doesn't

### Step 2: Fix is_available() Method
- Edit `C:/.agent_click/core/input_strategies/selected_text_strategy.py`
- Change the `is_available()` method (lines 79-91) to check clipboard first
- New logic: Return `False` if clipboard already has text (let TextSelectionStrategy handle it)
- New logic: Return `True` only if clipboard is empty (act as true fallback)
- Implementation: Use `self.selection_manager.get_selected_text()` to check clipboard
- If clipboard has text: return `False` (TextSelectionStrategy should handle it)
- If clipboard is empty or None: return `True` (we'll try Ctrl+C as fallback)

**Specific code change:**
```python
def is_available(self) -> bool:
    """Check if this strategy should be used as fallback.

    Returns False if clipboard already has text (TextSelectionStrategy should handle it).
    Returns True only if clipboard is empty (we'll try Ctrl+C as fallback).

    Returns:
        True if clipboard is empty, False otherwise
    """
    try:
        # If clipboard already has text, let TextSelectionStrategy handle it
        text = self.selection_manager.get_selected_text()
        if text and len(text.strip()) > 0:
            self.logger.debug("Clipboard has text, letting TextSelectionStrategy handle it")
            return False
        # Clipboard is empty, we can try Ctrl+C as fallback
        return True
    except Exception as e:
        self.logger.error(f"Error checking availability: {e}")
        return True  # On error, allow trying as fallback
```

**Why this fixes the root cause:**
- Prevents `SelectedTextStrategy` from being used when clipboard has text
- Ensures `TextSelectionStrategy` (non-destructive) is prioritized
- Only uses destructive Ctrl+C as true fallback when clipboard is empty
- Minimal change: Only one method modified
- No side effects: Doesn't change capture logic, just availability check

### Step 3: Add Unit Test for Bug Fix
- Create new test file: `C:/.agent_click/tests/test_selected_text_strategy_fix.py`
- Test 1: Verify `is_available()` returns False when clipboard has text
- Test 2: Verify `is_available()` returns True when clipboard is empty
- Test 3: Verify priority order uses TextSelectionStrategy when clipboard has text
- Test 4: Verify priority order uses SelectedTextStrategy when clipboard is empty
- Ensure tests fail before fix and pass after fix

**Test implementation:**
```python
import unittest
from unittest.mock import Mock, patch
from core.input_strategies.selected_text_strategy import SelectedTextStrategy
from core.input_strategies.text_selection_strategy import TextSelectionStrategy
from core.selection_manager import SelectionManager

class TestSelectedTextStrategyFix(unittest.TestCase):
    """Test that SelectedTextStrategy only acts as fallback."""

    def test_is_available_returns_false_when_clipboard_has_text(self):
        """Test that is_available returns False when clipboard has text."""
        strategy = SelectedTextStrategy()

        # Mock clipboard to have text
        with patch.object(SelectionManager, 'get_selected_text', return_value='test text'):
            available = strategy.is_available()
            self.assertFalse(available, "Should return False when clipboard has text")

    def test_is_available_returns_true_when_clipboard_empty(self):
        """Test that is_available returns True when clipboard is empty."""
        strategy = SelectedTextStrategy()

        # Mock clipboard to be empty
        with patch.object(SelectionManager, 'get_selected_text', return_value=None):
            available = strategy.is_available()
            self.assertTrue(available, "Should return True when clipboard is empty")

    def test_text_selection_has_priority_when_clipboard_has_text(self):
        """Test that TextSelectionStrategy is prioritized when clipboard has text."""
        text_strategy = TextSelectionStrategy()
        selected_strategy = SelectedTextStrategy()

        # Mock clipboard to have text
        with patch.object(SelectionManager, 'get_selected_text', return_value='test text'):
            text_available = text_strategy.is_available()
            selected_available = selected_strategy.is_available()

            self.assertTrue(text_available, "TextSelectionStrategy should be available")
            self.assertFalse(selected_available, "SelectedTextStrategy should NOT be available")

if __name__ == '__main__':
    unittest.main()
```

### Step 4: Manual Testing Verification
- Start the system: `cd C:/.agent_click && uv run agent_click.py`
- Test Case 1: Text in clipboard
  - Select text in Notepad
  - Press Ctrl+C to copy to clipboard
  - Press Pause to activate agent
  - **Verify**: Log shows `[INFO] [TextSelectionStrategy] Captured text selection: X chars`
  - **Verify**: Log shows `[INFO] [InputManager] ✅ Auto-detected input: text_selection`
  - **Verify**: No unwanted Ctrl+C is performed

- Test Case 2: Text selected but not copied (fallback scenario)
  - Select text in Notepad (don't press Ctrl+C)
  - Press Pause to activate agent
  - **Verify**: Log shows `[INFO] [SelectedTextStrategy] Captured selected text: X chars` (or TextSelectionStrategy if clipboard somehow has text)
  - **Verify**: Agent processes the text successfully

- Test Case 3: Empty clipboard, no selection
  - Clear clipboard
  - Don't select anything
  - Press Pause to activate agent
  - **Verify**: Log shows `[WARNING] ⚠️  No input available from any source`

### Final Step: Validate Fix
- Run all validation commands listed below
- Verify the bug is fixed (clipboard no longer interfered with when it has text)
- Ensure zero regressions (all tests pass, all scenarios work)
- Test edge cases (very long text, special characters, unicode)
- Monitor logs to confirm correct strategy selection

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `cd C:/.agent_click && python -m pytest tests/test_selected_text_strategy_fix.py -v` - Run the new unit tests to verify the fix works

- `cd C:/.agent_click && python -m pytest tests/ -v` - Run all existing tests to ensure no regressions (if test suite exists)

- `cd C:/.agent_click && uv run agent_click.py` - Manual test: Start system, copy text to clipboard, press Pause, verify logs show `TextSelectionStrategy` not `SelectedTextStrategy`

- `cd C:/.agent_click && python -c "from core.input_strategies.selected_text_strategy import SelectedTextStrategy; from unittest.mock import patch; from core.selection_manager import SelectionManager; s = SelectedTextStrategy(); print('With text:', patch.object(SelectionManager, 'get_selected_text', return_value='test')(lambda: s.is_available())()); print('Empty:', patch.object(SelectionManager, 'get_selected_text', return_value=None)(lambda: s.is_available())())"` - Quick inline test to verify is_available() logic

## Notes
- **No new libraries needed** - This fix uses existing dependencies only
- **Minimal and surgical** - Only one method in one file is changed
- **No refactoring** - Keep existing structure, just fix the availability check
- **No side effects** - Change only affects when SelectedTextStrategy is considered available
- **Why this approach**:
  - Solves root cause: Prevents unwanted Ctrl+C when clipboard has text
  - Maintains fallback functionality: SelectedTextStrategy still works when clipboard empty
  - Non-breaking: Doesn't change capture logic, just prioritizes non-destructive method
  - Simple: Single method change, easy to understand and test
- **Potential side effects to watch for**:
  - If clipboard is temporarily empty when user expects SelectedTextStrategy to work, it won't be tried
  - This is acceptable because it's better to fail than to interfere destructively
- **Performance considerations**:
  - Adds one extra clipboard check in is_available()
  - Negligible performance impact (clipboard access is fast)
  - Prevents unnecessary Ctrl+C operations (net performance gain)
- **Why certain solutions were avoided**:
  - Removing SelectedTextStrategy entirely: Too drastic, it has valid use cases as fallback
  - Complex clipboard detection logic: Overkill, simple check is sufficient
  - Adding configuration option: Unnecessary complexity for clear bug
  - Refactoring priority system: Scope creep, not needed for this fix
