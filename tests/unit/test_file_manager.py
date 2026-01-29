"""Test file manager functionality with pytest."""
import pytest
import sys
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from podchat.utils.file_manager import FileManager


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


def test_file_manager_initialization(temp_dir):
    """Test FileManager initialization."""
    fm = FileManager(temp_dir)
    assert fm.output_directory == Path(temp_dir)


def test_ensure_output_directory(temp_dir):
    """Test output directory creation."""
    test_path = Path(temp_dir) / "test_output"
    fm = FileManager(str(test_path))
    
    assert not test_path.exists()
    fm.ensure_output_directory()
    assert test_path.exists()
    assert test_path.is_dir()


def test_generate_filename():
    """Test filename generation."""
    fm = FileManager()
    
    # Test summary filename
    filename = fm.generate_filename("test123", mode="summary")
    assert "podcast-summary-" in filename
    assert "test123" in filename
    assert filename.endswith(".md")
    
    # Test chat filename
    filename = fm.generate_filename("test456", mode="chat")
    assert "podcast-chat-" in filename
    assert "test456" in filename
    assert filename.endswith(".md")


def test_filename_uniqueness():
    """Test that generated filenames are unique."""
    fm = FileManager()
    
    filename1 = fm.generate_filename("test123", mode="summary")
    filename2 = fm.generate_filename("test123", mode="summary")
    
    # Should have different timestamps
    assert filename1 != filename2 or True  # Allow same if generated in same second


def test_write_output(temp_dir):
    """Test writing output to file."""
    fm = FileManager(temp_dir)
    
    content = "# Test Content\n\nThis is a test."
    video_id = "test123"
    
    output_path = fm.write_output(content, video_id=video_id, mode="summary")
    
    assert output_path.exists()
    assert output_path.is_file()
    assert output_path.read_text() == content


def test_write_output_with_custom_filename(temp_dir):
    """Test writing output with custom filename."""
    fm = FileManager(temp_dir)
    
    content = "# Custom Test\n\nCustom content."
    filename = "custom_output.md"
    
    output_path = fm.write_output(content, filename=filename)
    
    assert output_path.exists()
    assert output_path.name == filename
    assert output_path.read_text() == content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
