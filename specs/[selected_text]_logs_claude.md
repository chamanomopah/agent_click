I'll analyze the codebase to understand the project structure and create a detailed implementation plan for adding verbose logging to the Claude Code SDK.Now let me search for how the SDK query is being used to understand where we need to add verbose logging:Perfect! Now I have a clear understanding of the codebase. Let me create a comprehensive implementation plan for adding verbose logging to the Claude Code SDK integration.

# Feature: Verbose Logging for Claude Code SDK

## Feature Description
Add verbose, real-time logging to the Claude Code SDK integration that shows the agent's thinking process, tools being used, and files being modified in a concise, summarized format. The current implementation only shows final results after processing completes. This feature will provide visibility into Claude's actions during processing without overwhelming the logs with excessive detail.

## User Story
As a developer using the AgentClick system
I want to see summarized real-time logs of Claude's actions (tools used, files modified, current operation)
So that I can understand what's happening during processing and debug issues more effectively

## Problem Statement
The current Claude Code SDK integration in `agents/base_agent.py` uses an async generator (`async for message in query()`) but only collects text content silently. Users see nothing during processing and only get the final result, making it difficult to:
- Understand what Claude is doing during long operations
- Debug when something goes wrong
- See which tools are being used
- Track which files are being read/modified
- Get feedback on processing progress

## Solution Statement
Implement a verbose logging wrapper around the Claude SDK query that:
1. Intercepts SDK messages to extract tool usage, file operations, and progress information
2. Emits summarized, concise log messages through the existing signal system for GUI display
3. Formats messages clearly without overwhelming detail (e.g., "🔧 Using tool: Read on file.py" instead of full JSON)
4. Maintains backward compatibility with existing functionality
5. Provides a toggle option in agent configuration to enable/disable verbose logging

## Relevant Files
Use these files to implement the feature:

- `agents/base_agent.py` - Contains `_query_sdk()` method that wraps the SDK query (main integration point)
- `core/system.py` - Contains signal system for thread-safe GUI updates (log_message_signal)
- `ui/popup_window.py` - Contains activity log display that will show verbose messages
- `config/agent_config.py` - Configuration system to store verbose logging preference
- `utils/logger.py` - Logging utilities for console output

### New Files
- `agents/sdk_logger.py` - New module to handle SDK message parsing and verbose logging

## Implementation Plan

### Phase 1: Foundation
- Create SDK message parser that extracts tool usage, file operations, and progress from SDK messages
- Create verbose logging toggle in agent configuration system
- Define concise message format standards (avoid log spam)

### Phase 2: Core Implementation
- Implement SDK message interceptor that wraps the query generator
- Add tool usage detection (Read, Write, Edit, Grep, Glob, etc.)
- Add file operation tracking (which files are being accessed/modified)
- Integrate with existing signal system for GUI updates

### Phase 3: Integration
- Update BaseAgent._query_sdk() to use verbose logging wrapper
- Add configuration option to enable/disable verbose logging per agent
- Update popup UI to show verbose logs in activity tab
- Test with all agents to ensure no performance degradation

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create SDK Logger Module
- Create `agents/sdk_logger.py` with SDKMessageParser class
- Implement message type detection (content blocks, tool use, tool results)
- Implement tool name extraction (Read, Write, Edit, Grep, Glob, etc.)
- Implement file path extraction from tool parameters
- Implement concise message formatting with icons
- Write tests for: parsing different message types, extracting tool names, formatting messages

### Step 2: Extend Configuration System
- Update `config/agent_config.py` to add `verbose_logging` boolean field to AgentSettings
- Update default settings to include `verbose_logging: False` (opt-in to avoid log spam)
- Update `ui/popup_window.py` config tab to add checkbox for "Verbose Logging"
- Update save/load logic to persist verbose_logging setting
- Write tests for: saving/loading verbose_logging config, default value is False

### Step 3: Create Verbose Logging Wrapper
- Create `VerboseSDKWrapper` class in `agents/sdk_logger.py`
- Implement async wrapper that yields messages while emitting log callbacks
- Add callback parameter for log emission (function called with formatted messages)
- Implement message interception logic in wrapper
- Implement progress tracking (e.g., "Processing step 1/3...")
- Write tests for: wrapper correctly forwards messages, callbacks are triggered

### Step 4: Integrate with BaseAgent
- Update `agents/base_agent.py` to import SDK logger
- Modify `process()` method to accept `verbose_logging` parameter
- Pass `verbose_logging` config setting from system to agent
- Modify `_query_sdk()` to use VerboseSDKWrapper when enabled
- Wire up log callback to use agent's logger and system signals
- Write tests for: verbose mode shows logs, non-verbose mode is silent

### Step 5: Update System Orchestrator
- Update `core/system.py` to pass verbose_logging config to agent.process()
- Retrieve verbose_logging setting from AgentConfigManager
- Add log_message_signal emission for SDK verbose logs
- Ensure thread-safe signal emission from keyboard handler thread
- Write tests for: verbose setting correctly passed to agent, signals emitted safely

### Step 6: Update UI for Verbose Display
- Update `ui/popup_window.py` to handle verbose log messages
- Add visual distinction for verbose messages (different color/icon)
- Ensure auto-scroll works for verbose logs
- Add "Clear Log" button for better UX
- Write tests for: verbose messages display correctly, colors are distinct

### Final Step: Validate Feature
- Run all validation commands listed below
- Ensure all acceptance criteria are met
- Test with Prompt Assistant agent (verify logs appear)
- Test with verbose logging disabled (verify no extra logs)
- Test with multiple rapid activations (verify no signal/sync issues)
- Verify zero performance impact when verbose logging is disabled

## Testing Strategy

### Unit Tests
- Test SDKMessageParser correctly identifies tool use messages
- Test SDKMessageParser extracts tool names (Read, Write, Edit, etc.)
- Test SDKMessageParser extracts file paths from parameters
- Test VerboseSDKWrapper yields all messages correctly
- Test VerboseSDKWrapper triggers callbacks at appropriate times
- Test AgentSettings correctly saves/loads verbose_logging field

### Integration Tests
- Test verbose logs appear in popup window when enabled
- Test no logs appear when verbose logging disabled
- Test multiple tool uses generate multiple log lines
- Test long-running operations show progress
- Test verbose setting persists across agent switches
- Test thread-safe signal emission doesn't crash UI

### Edge Cases
- Edge case: SDK returns messages without content (handle gracefully)
- Edge case: Tool use without file path (show tool name only)
- Edge case: Very long file paths (truncate to avoid UI overflow)
- Edge case: Rapid tool usage (debounce to avoid UI freeze)
- Edge case: Verbose logging enabled during active query (apply on next query)

## Acceptance Criteria
- [ ] Verbose logging can be enabled/disabled per agent via config UI
- [ ] When enabled, users see concise messages like "🔧 Using tool: Read on utils/logger.py"
- [ ] When disabled, behavior is identical to current implementation (silent processing)
- [ ] Verbose logs appear in real-time in the popup activity tab during processing
- [ ] All tool types (Read, Write, Edit, Grep, Glob) are detected and logged
- [ ] File paths are extracted and displayed clearly
- [ ] No performance impact when verbose logging is disabled
- [ ] Configuration persists across system restarts
- [ ] Log messages are concise (single line per operation)
- [ ] No log spam or overwhelming output

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd C:\.agent_click && python -m pytest tests/ -v -k "sdk_logger or verbose"` - Run SDK logger tests
- `cd C:\.agent_click && python -m pytest tests/ -v -k "config"` - Verify configuration system works
- `cd C:\.agent_click && python agents/base_agent.py` - Quick syntax check (will fail but shows import errors)
- `cd C:\.agent_click && uv run agent_click.py` - Start system and manually test with verbose enabled
- `cd C:\.agent_click && uv run python -c "from agents.sdk_logger import SDKMessageParser; print('OK')"` - Verify module imports

## Notes
- No new libraries needed (uses existing claude_agent_sdk, PyQt6)
- Future consideration: Add progress bar for multi-step operations
- Breaking changes: None (backward compatible, opt-in feature)
- Performance consideration: Minimal overhead when disabled (simple boolean check)
- Security consideration: No sensitive data logged (only file paths and tool names)
- Dependencies: Requires claude_agent_sdk to expose message structure (already available)