"""Test script for new input types."""

import sys
sys.path.insert(0, r'C:\.agent_click')

from core.input_manager import InputManager
from core.input_strategy import InputType
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def test_text_selection():
    """Test text selection input."""
    print("\n" + "="*60)
    print("TEST 1: Text Selection")
    print("="*60)

    manager = InputManager()

    # Copy some text to clipboard first
    import pyperclip
    test_text = "This is a test text for AgentClick input system."
    pyperclip.copy(test_text)
    print(f"✅ Text copied to clipboard: {test_text[:50]}...")

    # Capture
    content = manager.capture_input(preferred_type=InputType.TEXT_SELECTION)

    if content:
        print(f"✅ Input captured!")
        print(f"   Type: {content.input_type.value}")
        print(f"   Text: {content.text[:50]}...")
        print(f"   Metadata: {content.metadata}")
    else:
        print("❌ Failed to capture text selection")


def test_file_upload():
    """Test file upload input."""
    print("\n" + "="*60)
    print("TEST 2: File Upload")
    print("="*60)

    manager = InputManager()

    # Create test file
    test_file = Path("test_input.txt")
    test_content = "This is test content from a file.\nLine 2\nLine 3"

    test_file.write_text(test_content, encoding='utf-8')
    print(f"✅ Test file created: {test_file}")

    # Configure file upload
    manager.set_file_upload(str(test_file))

    # Capture
    content = manager.capture_input(preferred_type=InputType.FILE_UPLOAD)

    if content:
        print(f"✅ Input captured!")
        print(f"   Type: {content.input_type.value}")
        print(f"   File: {content.file_path}")
        print(f"   Text: {content.text[:50]}...")
        print(f"   Metadata: {content.metadata}")
    else:
        print("❌ Failed to capture file upload")

    # Cleanup
    test_file.unlink()
    print("🧹 Test file cleaned up")


def test_clipboard_image():
    """Test clipboard image input."""
    print("\n" + "="*60)
    print("TEST 3: Clipboard Image")
    print("="*60)

    manager = InputManager()

    # Check availability first
    available = manager.check_available_inputs()
    print(f"Clipboard image available: {available[InputType.CLIPBOARD_IMAGE]}")

    if available[InputType.CLIPBOARD_IMAGE]:
        # Capture
        content = manager.capture_input(preferred_type=InputType.CLIPBOARD_IMAGE)

        if content:
            print(f"✅ Input captured!")
            print(f"   Type: {content.input_type.value}")
            print(f"   Image: {content.image_path}")
            print(f"   Metadata: {content.metadata}")
        else:
            print("❌ Failed to capture clipboard image")
    else:
        print("⚠️  No image in clipboard - copy an image first (Ctrl+C on any image)")
        print("   Then run this test again.")


def test_screenshot():
    """Test screenshot input."""
    print("\n" + "="*60)
    print("TEST 4: Screenshot")
    print("="*60)

    manager = InputManager()

    print("Taking screenshot in 3 seconds...")
    print("Switch to the window you want to capture!")

    import time
    time.sleep(3)

    # Capture
    content = manager.take_screenshot()

    if content:
        print(f"✅ Input captured!")
        print(f"   Type: {content.input_type.value}")
        print(f"   Image: {content.image_path}")
        print(f"   Metadata: {content.metadata}")
    else:
        print("❌ Failed to capture screenshot")


def test_auto_detect():
    """Test auto-detection of best input."""
    print("\n" + "="*60)
    print("TEST 5: Auto-Detect Best Input")
    print("="*60)

    manager = InputManager()

    # Show status
    print("\nAvailable inputs:")
    print(manager.get_status_summary())

    # Auto-detect
    content = manager.capture_input()

    if content:
        print(f"\n✅ Auto-detected and captured!")
        print(f"   Type: {content.input_type.value}")
        print(f"   Text: {content.text[:50]}...")
    else:
        print("❌ No input available")


def test_allowed_inputs_filter():
    """Test filtering by allowed inputs."""
    print("\n" + "="*60)
    print("TEST 6: Filter by Allowed Inputs")
    print("="*60)

    manager = InputManager()

    # Copy text to clipboard
    import pyperclip
    test_text = "Test text for filtering"
    pyperclip.copy(test_text)
    print(f"✅ Text copied to clipboard")

    # Test 1: Allow only text_selection
    print("\nTest 6a: Allow only text_selection")
    content = manager.capture_input(allowed_inputs=["text_selection"])
    if content and content.input_type == InputType.TEXT_SELECTION:
        print(f"✅ Captured with filter: {content.input_type.value}")
    else:
        print("❌ Failed to capture with filter")

    # Test 2: Allow only file_upload (should fail since no file configured)
    print("\nTest 6b: Allow only file_upload (no file configured)")
    content = manager.capture_input(allowed_inputs=["file_upload"])
    if content is None:
        print("✅ Correctly returned None (no file available)")
    else:
        print(f"❌ Unexpectedly captured: {content.input_type.value}")

    # Test 3: Auto-detect with multiple allowed
    print("\nTest 6c: Auto-detect with multiple allowed")
    content = manager.capture_input(allowed_inputs=["text_selection", "file_upload"])
    if content:
        print(f"✅ Auto-detected: {content.input_type.value}")
    else:
        print("❌ Failed to auto-detect")


def test_config_integration():
    """Test integration with AgentConfigManager."""
    print("\n" + "="*60)
    print("TEST 7: AgentConfigManager Integration")
    print("="*60)

    from config.agent_config import AgentConfigManager

    config_manager = AgentConfigManager()

    # Test getting/setting allowed inputs
    print("\nTest 7a: Get allowed inputs for agent")
    allowed = config_manager.get_allowed_inputs("Diagnostic Agent")
    print(f"✅ Allowed inputs for Diagnostic Agent: {allowed}")

    print("\nTest 7b: Set custom allowed inputs")
    config_manager.set_allowed_inputs(
        "Diagnostic Agent",
        ["text_selection", "file_upload"]
    )
    allowed = config_manager.get_allowed_inputs("Diagnostic Agent")
    print(f"✅ Updated allowed inputs: {allowed}")

    print("\nTest 7c: Check if specific input is allowed")
    is_allowed = config_manager.is_input_allowed("Diagnostic Agent", "text_selection")
    print(f"✅ text_selection allowed: {is_allowed}")

    is_allowed = config_manager.is_input_allowed("Diagnostic Agent", "screenshot")
    print(f"✅ screenshot allowed: {is_allowed}")

    print("\nTest 7d: Toggle input")
    config_manager.toggle_input("Diagnostic Agent", "screenshot")
    allowed = config_manager.get_allowed_inputs("Diagnostic Agent")
    print(f"✅ After toggle screenshot: {allowed}")

    # Restore defaults
    config_manager.set_allowed_inputs(
        "Diagnostic Agent",
        ["text_selection", "file_upload", "clipboard_image", "screenshot"]
    )
    print("\n✅ Restored defaults")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("AgentClick Input System Tests")
    print("="*60)

    test_text_selection()
    test_file_upload()
    test_clipboard_image()
    # test_screenshot()  # Uncomment to test screenshot
    test_auto_detect()
    test_allowed_inputs_filter()
    test_config_integration()

    print("\n" + "="*60)
    print("Tests completed!")
    print("="*60)


if __name__ == "__main__":
    main()
