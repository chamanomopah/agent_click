# Feature: Fix and Enhance SDK Verbose Logging

## Feature Description
Fixes the Claude SDK verbose logging functionality that is not working properly. The verbose logging feature is configured and enabled in the agent settings, but tool usage messages (Read, Write, Edit, Grep, Glob, etc.) are not being displayed in the Activity Log during agent processing. This feature provides real-time feedback showing which files the agent is accessing and which tools it's using, which is essential for transparency and debugging.

## User Story
As a developer using the AgentClick system
I want to see real-time verbose logs of SDK tool usage during agent processing
So that I can understand what the agent is doing, which files it's accessing, and debug any issues

## Problem Statement
The verbose logging system is fully implemented (configuration, UI controls, SDK wrapper, message parser, callback mechanism), but it's not displaying tool usage messages in the Activity Log. The configuration shows `verbose_logging: true` for all agents, and the code correctly passes this flag to the agent's `process()` method, but no tool usage messages (like "📖 Using Read: file.py") appear in the Activity Log during processing. This indicates one of the following issues:

1. **SDK message structure mismatch**: The parser might be looking for the wrong message structure (block.type, block.name, etc.)
2. **Tool use detection failing**: The parser's logic for detecting `tool_use` blocks might not be matching the actual SDK message format
3. **Callback not emitting**: The callback function might not be properly emitting signals to the GUI
4. **Async timing issue**: The async generator wrapper might not be yielding messages at the right time
5. **GUI not receiving signals**: The signal/slot connection might not be working correctly

## Solution Statement
We will fix the verbose logging by:

1. **Adding comprehensive debug logging** to trace exactly what's happening at each step
2. **Validating the SDK message structure** by logging the actual message objects received from the SDK
3. **Enhancing the SDK message parser** to handle different message formats and add fallback detection methods
4. **Improving error handling** to catch and log any parsing failures
5. **Adding a test mode** that logs raw message structures for analysis
6. **Verifying the callback mechanism** works correctly
7. **Adding visual indicators** in the GUI when verbose logging is active

The fix will be implemented incrementally with extensive logging at each step to identify exactly where the problem occurs.

## Relevant Files
Use these files to implement the feature:

- `C:/.agent_click/agents/sdk_logger.py` - SDK message parser and verbose wrapper (NEEDS DEBUG LOGGING)
- `C:/.agent_click/agents/base_agent.py` - Query SDK method that creates the verbose wrapper (NEEDS DEBUG LOGGING)
- `C:/.agent_click/core/system.py` - Creates callback and passes verbose_logging flag (NEEDS DEBUG LOGGING)
- `C:/.agent_click/config/agent_config.py` - Stores verbose_logging setting (NO CHANGES NEEDED)
- `C:/.agent_click/ui/popup_window.py` - Displays verbose log messages (NEEDS DEBUG LOGGING)

## Implementation Plan

### Phase 1: Foundation - Add Comprehensive Debug Logging
Add extensive debug logging throughout the verbose logging pipeline to trace the exact flow and identify where messages are being lost. This includes:
- Log when verbose logging is enabled/disabled
- Log when the wrapper is created
- Log each message received from the SDK
- Log the structure of each message (type, attributes, content)
- Log parser results
- Log callback invocations
- Log signal emissions

### Phase 2: Core Implementation - Enhanced Message Parser
Once we identify the issue through debug logs, enhance the SDKMessageParser to:
- Handle the actual SDK message structure correctly
- Add multiple detection methods for tool use blocks
- Add better error handling and logging
- Support both content blocks and direct message attributes
- Log raw message structure when parsing fails

### Phase 3: Integration - Verify End-to-End Flow
After fixing the parser, verify the complete flow:
- Configuration → Wrapper → Parser → Callback → Signal → GUI
- Add visual indicators when verbose logging is active
- Test with different agents and tool usage patterns
- Ensure error messages are displayed if parsing fails

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add Debug Logging to SDK Logger Module
- Add debug logging to `VerboseSDKWrapper.__init__()` to log when wrapper is created and enabled status
- Add debug logging to `VerboseSDKWrapper._log()` to log when messages are being logged
- Add debug logging to `VerboseSDKWrapper.wrapped_query()` to log when query starts and message count
- Add debug logging to `SDKMessageParser.extract_tool_use()` to log:
  - When extraction is attempted
  - Message structure (has content, content type, content length)
  - Each block's type and attributes
  - Whether tool_use was found
  - Final extraction result
- Add debug logging to catch and log any exceptions with full stack traces
- Write tests for: Verify debug logs appear when verbose logging is enabled

### Step 2: Add Debug Logging to Base Agent Query Method
- Add debug logging to `BaseAgent._query_sdk()` to log:
  - When verbose_logging is True/False
  - When wrapper is being created
  - When query starts
  - Number of messages received
  - Any exceptions
- Add logging to show the type of each message object received from SDK
- Add logging to show if message.content exists and its length
- Write tests for: Verify query method logs verbose logging status

### Step 3: Add Debug Logging to System Coordinator
- Add debug logging to `AgentClickSystem._on_pause_pressed()` to log:
  - Verbose logging setting value
  - When callback function is created
  - When callback is invoked with a message
- Add debug logging to verbose_log_callback to show messages being emitted
- Add logging to verify signal connections are working
- Write tests for: Verify system passes verbose logging correctly

### Step 4: Add Debug Logging to Popup Window
- Add debug logging to `PopupWindow.log()` to show:
  - When log messages are received
  - Message content and level
  - Whether they're being displayed
- Add debug logging to verify signal handler is receiving messages
- Write tests for: Verify popup receives and displays log messages

### Step 5: Run System with Verbose Logging and Analyze Logs
- Enable verbose logging for an agent (already enabled in config)
- Trigger agent processing with Pause key
- Collect all debug logs from console
- Analyze logs to identify:
  - Is verbose_logging flag True?
  - Is wrapper being created?
  - Are messages being received from SDK?
  - What is the structure of SDK messages?
  - Is parser detecting tool_use blocks?
  - Is callback being invoked?
  - Are signals being emitted?
  - Is GUI receiving signals?
- Write tests for: Verify complete flow works end-to-end

### Step 6: Fix the Identified Issue
Based on the analysis from Step 5, implement the appropriate fix:
- **If SDK message structure is different**: Update parser to match actual structure
- **If parser logic is wrong**: Fix the detection logic for tool_use blocks
- **If callback not working**: Fix callback mechanism
- **If signals not working**: Fix signal/slot connections
- **If timing issue**: Adjust async handling
- Add extensive error handling for the specific issue
- Write tests for: Verify the specific fix resolves the issue

### Step 7: Add Message Structure Fallback Detection
Enhance parser to handle multiple message formats:
- Check for both `block.type == 'tool_use'` and `message.type == 'tool_use'`
- Check for nested content structures
- Add support for direct message attributes vs content blocks
- Add fallback detection that looks for tool name patterns in different locations
- Log which detection method succeeded
- Write tests for: Verify parser handles different message formats

### Step 8: Add Visual Indicator for Verbose Logging
Add visual feedback when verbose logging is enabled:
- Show "🔊 Verbose logging ON" message when processing starts
- Add icon or badge in Activity Log when verbose mode is active
- Show "🔇 Verbose logging OFF" when disabled
- Write tests for: Verify visual indicators appear correctly

### Step 9: Test with Real Agent Operations
Test verbose logging with actual tool usage:
- Use an agent that reads files (should see "📖 Using Read: file.py")
- Use an agent that writes files (should see "✏️ Using Write: file.py")
- Use an agent that uses Grep (should see "🔍 Using Grep: pattern")
- Use an agent that uses multiple tools (should see all tool usage)
- Verify each tool usage appears in Activity Log with correct icon and file path
- Write tests for: Verify all common tools appear in logs correctly

### Final Step: Validate Feature
- Run all validation commands listed below
- Ensure all acceptance criteria are met
- Verify zero regressions (agents still work without verbose logging)
- Test with verbose logging both enabled and disabled
- Verify performance is not impacted significantly
- Clean up excessive debug logs (keep only essential ones)

## Testing Strategy

### Unit Tests
- Test `SDKMessageParser.extract_tool_use()` with various message structures
- Test `VerboseSDKWrapper` creation and message iteration
- Test callback function invocation and logging
- Test signal emission and reception
- Test configuration loading (verbose_logging flag)

### Integration Tests
- Test complete flow: config → agent → wrapper → parser → callback → GUI
- Test with different agents (Prompt Assistant, TAC agents, etc.)
- Test with different tool usage patterns (Read, Write, Grep, etc.)
- Test with verbose logging enabled vs disabled
- Test signal/slot communication between threads

### Edge Cases
- Edge case: SDK message has no content attribute
- Edge case: Message has empty content list
- Edge case: Tool use block has no name attribute
- Edge case: File path parameter has different names (path vs filepath vs file_path)
- Edge case: Callback function is None
- Edge case: GUI is closed (large_popup is None) when callback tries to emit
- Edge case: Multiple rapid tool uses in succession
- Edge case: Exception during message parsing (should log and continue)

## Acceptance Criteria
- [ ] Verbose logging shows tool usage messages in Activity Log when enabled
- [ ] Tool usage messages include icon, tool name, and file path (if applicable)
- [ ] Messages appear in real-time as agent processes
- [ ] Verbose logging can be toggled on/off per agent via config UI
- [ ] Disabling verbose logging hides tool usage messages (cleaner log)
-- [ ] Debug logs help identify any future issues
- [ ] No performance impact when verbose logging is disabled
- [ ] Works with all agent types
- [ ] Works with all common tools (Read, Write, Edit, Grep, Glob, Bash, Task, WebSearch)
- [ ] Gracefully handles unknown tools or malformed messages
- [ ] Visual indicator shows when verbose mode is active
- [ ] Zero regressions - agents work perfectly regardless of verbose logging setting

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd C:/.agent_click && uv run agent_click.py` - Start the system to verify it initializes without errors
- Open config popup for "Prompt Assistant" agent - Verify "Enable Verbose Logging" checkbox is checked
- Trigger agent processing with Pause key - Verify tool usage messages appear in Activity Log
- Disable verbose logging checkbox, save, trigger processing - Verify no tool usage messages appear
- Enable verbose logging again, trigger processing with file reading - Verify "📖 Using Read: <file>" appears
- Test with different agents - Verify verbose logging works for all agents
- Check console logs - Verify debug logs show the flow clearly
- Close system and restart - Verify verbose logging setting persists

## Notes
- **New libraries needed**: None (using existing libraries)
- **Important**: The actual SDK message structure is unknown - we must add extensive logging first to see what we're dealing with
- **Performance**: Debug logging should be disabled or minimal in production to avoid log spam
- **Future considerations**: Consider adding a "Debug Mode" that shows even more detailed information (raw SDK messages, timing, etc.)
- **Breaking changes**: None - this is a bug fix, not a feature change
- **Dependencies**: Requires claude-agent-sdk to be working correctly
- **Testing**: Must test with actual agent operations that use tools (not just simple text processing)
