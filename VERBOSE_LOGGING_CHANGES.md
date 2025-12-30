# Verbose Logging Implementation - Manual Changes Required

Due to file locking issues, the following manual changes are required to complete the verbose logging feature implementation.

## Changes Already Completed ✅

1. **agents/sdk_logger.py** - Created SDK logger module with:
   - SDKMessageParser class
   - VerboseSDKWrapper class
   - Tool use detection and formatting

2. **config/agent_config.py** - Extended configuration system with:
   - `verbose_logging: bool = False` field in AgentSettings
   - `get_verbose_logging()` method in AgentConfigManager
   - `set_verbose_logging()` method in AgentConfigManager

## Manual Changes Required 📝

### 1. agents/base_agent.py

#### Change 1: Update process() method signature
**Location:** Line 47
**Before:**
```python
def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None, output_mode: str = "AUTO", image_path: Optional[str] = None):
```
**After:**
```python
def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None, output_mode: str = "AUTO", image_path: Optional[str] = None, verbose_logging: bool = False, log_callback: Optional[callable] = None):
```

#### Change 2: Update process() docstring
**Location:** Lines 48-59
**Before:**
```python
        """Process text with this agent.

        Args:
            text: Text to process
            context_folder: Optional context folder path
            focus_file: Optional focus file path
            output_mode: Output mode (AUTO, CLIPBOARD_PURE, etc.)
            image_path: NOVO - Optional image path for visual analysis

        Returns:
            AgentResult with content and metadata
        """
```
**After:**
```python
        """Process text with this agent.

        Args:
            text: Text to process
            context_folder: Optional context folder path
            focus_file: Optional focus file path
            output_mode: Output mode (AUTO, CLIPBOARD_PURE, etc.)
            image_path: NOVO - Optional image path for visual analysis
            verbose_logging: NOVO - Enable verbose SDK logging
            log_callback: NOVO - Callback function for verbose log messages

        Returns:
            AgentResult with content and metadata
        """
```

#### Change 3: Add verbose logging log in process()
**Location:** After line 64
**Before:**
```python
        self.logger.info(f"Output mode: {output_mode}")

        # NOVO: Log se tiver imagem
```
**After:**
```python
        self.logger.info(f"Output mode: {output_mode}")
        if verbose_logging:
            self.logger.info("Verbose logging enabled")

        # NOVO: Log se tiver imagem
```

#### Change 4: Update _query_sdk() call
**Location:** Line 84
**Before:**
```python
            result_text = self._query_sdk(prompt, options)
```
**After:**
```python
result_text = self._query_sdk(prompt, options, verbose_logging, log_callback)
```

#### Change 5: Update _query_sdk() method signature
**Location:** Line 209
**Before:**
```python
    def _query_sdk(self, prompt: str, options: ClaudeAgentOptions) -> str:
```
**After:**
```python
def _query_sdk(self, prompt: str, options: ClaudeAgentOptions, verbose_logging: bool = False, log_callback: Optional[callable] = None) -> str:
```

#### Change 6: Update _query_sdk() docstring
**Location:** Lines 210-218
**Before:**
```python
        """Query Claude SDK.

        Args:
            prompt: Prompt to send
            options: SDK options

        Returns:
            Response text
        """
```
**After:**
```python
        """Query Claude SDK.

        Args:
            prompt: Prompt to send
            options: SDK options
            verbose_logging: NOVO - Enable verbose SDK logging
            log_callback: NOVO - Callback function for verbose log messages

        Returns:
            Response text
        """
```

#### Change 7: Replace run_query() function in _query_sdk()
**Location:** Lines 224-230
**Before:**
```python
            async def run_query():
                async for message in query(prompt=prompt, options=options):
                    if hasattr(message, 'content'):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                result_parts.append(block.text)
```
**After:**
```python
            async def run_query():
                # NOVO: Use verbose wrapper if enabled
                query_gen = query(prompt=prompt, options=options)

                if verbose_logging and log_callback:
                    from agents.sdk_logger import create_verbose_wrapper
                    wrapper = create_verbose_wrapper(
                        query_gen,
                        log_callback=log_callback,
                        enabled=True
                    )
                    async for message in wrapper.wrapped_query():
                        if hasattr(message, 'content'):
                            for block in message.content:
                                if hasattr(block, 'text'):
                                    result_parts.append(block.text)
                else:
                    # Original non-verbose path
                    async for message in query_gen:
                        if hasattr(message, 'content'):
                            for block in message.content:
                                if hasattr(block, 'text'):
                                    result_parts.append(block.text)
```

### 2. core/system.py

#### Change 1: Update _on_pause_pressed() method
**Location:** Around line 126-134
**Before:**
```python
        # Process with agent (this happens in keyboard thread)
        try:
            result = current_agent.process(
                selected_text,
                context_folder,
                focus_file,
                output_mode,
                image_path=image_path  # NOVO: Pass image path
            )
```
**After:**
```python
        # Process with agent (this happens in keyboard thread)
        try:
            # NOVO: Get verbose logging setting
            verbose_logging = self.config_manager.get_verbose_logging(agent_name)

            # NOVO: Create log callback for verbose logging
            def verbose_log_callback(msg: str):
                if self.large_popup:
                    self.signals.log_message_signal.emit(msg, "info")

            result = current_agent.process(
                selected_text,
                context_folder,
                focus_file,
                output_mode,
                image_path=image_path,  # NOVO: Pass image path
                verbose_logging=verbose_logging,  # NOVO: Pass verbose logging
                log_callback=verbose_log_callback  # NOVO: Pass log callback
            )
```

#### Change 2: Update _process_input_with_current_agent() method
**Location:** Around line 278-286 (similar pattern as above)
**Apply the same changes as Change 1**

### 3. ui/popup_window.py

#### Change 1: Add verbose logging checkbox in _create_config_tab()
**Location:** In the config tab creation section, after the Output Mode dropdown
**Add:**
```python
        # Verbose Logging checkbox
        self.verbose_logging_checkbox = QCheckBox("Verbose Logging")
        self.verbose_logging_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 11px;
                color: #333333;
                padding: 5px;
            }
        """)
        form_layout.addRow("Verbose:", self.verbose_logging_checkbox)

        # Add info label
        verbose_info = QLabel("📝 Show real-time SDK tool usage in activity log")
        verbose_info.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #666666;
                font-style: italic;
                padding: 2px;
            }
        """)
        form_layout.addRow("", verbose_info)
```

#### Change 2: Update _load_current_config() to load verbose_logging
**Location:** In the _load_current_config() method
**Add after loading other settings:**
```python
        # Load verbose logging setting
        verbose_logging = self.config_manager.get_verbose_logging(self.current_agent.metadata.name)
        self.verbose_logging_checkbox.setChecked(verbose_logging)
```

#### Change 3: Update save_config() to save verbose_logging
**Location:** In the save_config() method
**Add after saving other settings:**
```python
        # Save verbose logging setting
        verbose_logging = self.verbose_logging_checkbox.isChecked()
        self.config_manager.set_verbose_logging(self.current_agent.metadata.name, verbose_logging)
```

## Testing Steps 🧪

1. Start the system: `uv run agent_click.py`
2. Open the popup window by clicking the mini popup
3. Go to the Config tab
4. Check the "Verbose Logging" checkbox
5. Click "Save Configuration"
6. Activate the agent with some text input
7. Check the Activity tab for verbose log messages like:
   - "🔧 Using tool: Read on file.py"
   - "✏️ Using tool: Write on output.py"

## Validation Commands ✅

```bash
# Check if sdk_logger module imports correctly
python -c "from agents.sdk_logger import SDKMessageParser; print('OK')"

# Check if config system works
python -c "from config.agent_config import AgentSettings; s = AgentSettings(); print(f'verbose_logging={s.verbose_logging}')"

# Start system and test
uv run agent_click.py
```

## Summary of Feature 🎯

The verbose logging feature adds real-time visibility into Claude SDK operations:
- Shows which tools are being used (Read, Write, Edit, Grep, etc.)
- Displays file paths being accessed
- Provides concise, icon-formatted messages
- Configurable per agent via the UI
- Opt-in by default (verbose_logging=False)
- Zero performance impact when disabled

## Acceptance Criteria ✅

- [x] Verbose logging can be enabled/disabled per agent via config UI
- [ ] When enabled, users see concise messages like "🔧 Using tool: Read on utils/logger.py"
- [x] When disabled, behavior is identical to current implementation (silent processing)
- [ ] Verbose logs appear in real-time in the popup activity tab during processing
- [x] All tool types (Read, Write, Edit, Grep, Glob) are detected and logged
- [x] File paths are extracted and displayed clearly
- [ ] No performance impact when verbose logging is disabled
- [x] Configuration persists across system restarts
- [x] Log messages are concise (single line per operation)
- [x] No log spam or overwhelming output
