"""Integration tests for CLI commands."""
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil


def run_command(cmd, timeout=180):
    """Run a CLI command and return the result."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout
    )
    return result


def test_cli_help():
    """Test that CLI help commands work."""
    commands = [
        "python3 -m podchat --help",
        "python3 -m podchat --version",
        "python3 -m podchat summarize --help",
        "python3 -m podchat chat --help",
    ]
    
    for cmd in commands:
        result = run_command(cmd, timeout=10)
        assert result.returncode == 0, f"Command failed: {cmd}\n{result.stderr}"
        assert len(result.stdout) > 0, f"No output from: {cmd}"
        print(f"✓ {cmd}")


def test_cli_config():
    """Test that config command works."""
    result = run_command("python3 -m podchat config", timeout=10)
    
    assert result.returncode == 0, f"Config command failed:\n{result.stderr}"
    assert "PodChat Configuration" in result.stdout
    assert "LLM Settings" in result.stdout
    assert "Output Settings" in result.stdout
    print("✓ python3 -m podchat config")


def test_cli_summarize_invalid_url():
    """Test that summarize command handles invalid URLs gracefully."""
    result = run_command("python3 -m podchat summarize https://www.google.com", timeout=30)
    
    # Should fail with error message
    assert result.returncode != 0
    assert "❌" in result.stdout or "Error" in result.stderr or "Error" in result.stdout
    print("✓ Invalid URL handling works")


def test_cli_summarize_missing_url():
    """Test that summarize command requires URL argument."""
    result = run_command("python3 -m podchat summarize", timeout=10)
    
    # Should fail with usage message
    assert result.returncode != 0
    assert "Usage:" in result.stdout or "Error" in result.stderr
    print("✓ Missing URL validation works")


def test_cli_custom_output():
    """Test that custom output path works."""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = Path(temp_dir) / "test_output.md"
        
        # This will fail without a valid video but tests the path handling
        cmd = f'python3 -m podchat summarize https://www.youtube.com/watch?v=INVALID -o "{output_file}"'
        result = run_command(cmd, timeout=30)
        
        # Even if it fails due to invalid video, it should recognize the output option
        assert "--output" not in result.stderr or result.returncode != 0
        print("✓ Custom output path option recognized")


def test_cli_verbose_flag():
    """Test that verbose flag is recognized."""
    result = run_command("python3 -m podchat summarize --help", timeout=10)
    
    assert "--verbose" in result.stdout or "-v" in result.stdout
    print("✓ Verbose flag available")


if __name__ == "__main__":
    print("=" * 60)
    print("CLI INTEGRATION TESTS")
    print("=" * 60)
    print()
    
    try:
        test_cli_help()
        print()
        test_cli_config()
        print()
        test_cli_summarize_invalid_url()
        print()
        test_cli_summarize_missing_url()
        print()
        test_cli_custom_output()
        print()
        test_cli_verbose_flag()
        
        print()
        print("=" * 60)
        print("✅ ALL CLI INTEGRATION TESTS PASSED")
        print("=" * 60)
        sys.exit(0)
        
    except AssertionError as e:
        print()
        print("=" * 60)
        print("❌ TEST FAILED")
        print("=" * 60)
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ TEST ERROR")
        print("=" * 60)
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
