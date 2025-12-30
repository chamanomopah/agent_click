import re

# Read the file
with open('agents/base_agent.py', 'r') as f:
    content = f.read()

# Update process method signature
content = re.sub(
    r'def process\(self, text: str, context_folder: Optional\[str\] = None, focus_file: Optional\[str\] = None, output_mode: str = "AUTO", image_path: Optional\[str\] = None\):',
    'def process(self, text: str, context_folder: Optional[str] = None, focus_file: Optional[str] = None, output_mode: str = "AUTO", image_path: Optional[str] = None, verbose_logging: bool = False, log_callback: Optional[callable] = None):',
    content
)

# Update process docstring
old_docstring = '            image_path: NOVO - Optional image path for visual analysis\n\n        Returns:'
new_docstring = '            image_path: NOVO - Optional image path for visual analysis\n            verbose_logging: NOVO - Enable verbose SDK logging\n            log_callback: NOVO - Callback function for verbose log messages\n\n        Returns:'
content = content.replace(old_docstring, new_docstring)

# Add verbose logging log
old_log = '        self.logger.info(f"Output mode: {output_mode}")\n\n        # NOVO: Log se tiver imagem'
new_log = '        self.logger.info(f"Output mode: {output_mode}")\n        if verbose_logging:\n            self.logger.info("Verbose logging enabled")\n\n        # NOVO: Log se tiver imagem'
content = content.replace(old_log, new_log)

# Update _query_sdk call
old_call = '            result_text = self._query_sdk(prompt, options)'
new_call = 'result_text = self._query_sdk(prompt, options, verbose_logging, log_callback)'
content = content.replace(old_call, new_call)

# Update _query_sdk signature
old_sig = '    def _query_sdk(self, prompt: str, options: ClaudeAgentOptions) -> str:'
new_sig = 'def _query_sdk(self, prompt: str, options: ClaudeAgentOptions, verbose_logging: bool = False, log_callback: Optional[callable] = None) -> str:'
content = content.replace(old_sig, new_sig)

# Update _query_sdk docstring
old_query_doc = '        Args:\n            prompt: Prompt to send\n            options: SDK options\n\n        Returns:'
new_query_doc = 'Args:\n            prompt: Prompt to send\n            options: SDK options\n            verbose_logging: NOVO - Enable verbose SDK logging\n            log_callback: NOVO - Callback function for verbose log messages\n\n        Returns:'
content = content.replace(old_query_doc, new_query_doc)

# Rewrite run_query function
old_run_query = '''            async def run_query():
                async for message in query(prompt=prompt, options=options):
                    if hasattr(message, 'content'):
                        for block in message.content:
                            if hasattr(block, 'text'):
                                result_parts.append(block.text)'''

new_run_query = '''            async def run_query():
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
                                    result_parts.append(block.text)'''

content = content.replace(old_run_query, new_run_query)

# Write the file
with open('agents/base_agent.py', 'w') as f:
    f.write(content)

print('File updated successfully')
