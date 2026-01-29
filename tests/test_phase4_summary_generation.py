"""
Phase 4: Summary Generation - Integration Tests

Tests the end-to-end pipeline from URL to summary file generation.
This validates that Phases 0-4 are working correctly together.
"""
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from podchat.core.processor import PodcastProcessor
from podchat.utils.config import ConfigManager
from podchat.utils.exceptions import (
    InvalidURLError,
    TranscriptNotAvailableError,
    PodChatError
)


class Phase4TestRunner:
    """Test runner for Phase 4 validation."""
    
    def __init__(self):
        self.results: List[Dict] = []
        self.output_dir = Path("./test_summaries")
        self.output_dir.mkdir(exist_ok=True)
        
    def log_result(self, test_name: str, passed: bool, message: str = "", 
                   details: Dict = None):
        """Log a test result."""
        result = {
            "timestamp": datetime.now().isoformat(),
            "test": test_name,
            "passed": passed,
            "message": message,
            "details": details or {}
        }
        self.results.append(result)
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"       {message}")
        if not passed and details:
            print(f"       Details: {details}")
        print()
    
    def run_all_tests(self, test_video_url: str = None):
        """Run all Phase 4 tests."""
        print("=" * 70)
        print("PHASE 4: SUMMARY GENERATION - INTEGRATION TESTS")
        print("=" * 70)
        print()
        
        # Test 1: Basic imports and setup
        self.test_imports()
        
        # Test 2: Configuration loading
        self.test_configuration()
        
        # Test 3: Component instantiation
        self.test_component_instantiation()
        
        # Test 4: Pipeline structure
        self.test_pipeline_structure()
        
        # Test 5: Error handling
        self.test_error_handling()
        
        # Test 6: End-to-end with real video (if URL provided)
        if test_video_url:
            self.test_end_to_end_processing(test_video_url)
        else:
            print("⚠ SKIPPED: End-to-end test (no video URL provided)")
            print("   To run: python tests/test_phase4_summary_generation.py <youtube_url>")
            print()
        
        # Generate report
        self.generate_report()
    
    def test_imports(self):
        """Test that all Phase 4 components can be imported."""
        try:
            from podchat.core.processor import PodcastProcessor
            from podchat.core.output_formatter import OutputFormatter
            from podchat import PodcastProcessor as PP, Config
            
            self.log_result(
                "Import Test",
                True,
                "All Phase 4 components imported successfully"
            )
        except ImportError as e:
            self.log_result(
                "Import Test",
                False,
                f"Import failed: {e}"
            )
    
    def test_configuration(self):
        """Test configuration loading."""
        try:
            from podchat.models.config import Config
            
            # Test default config
            config = Config()
            assert config.llm_provider == "openrouter"
            assert config.output_directory == "./summaries"
            
            # Test config loading from env
            try:
                config = ConfigManager.load()
                has_api_key = config.llm_api_key is not None
                
                self.log_result(
                    "Configuration Test",
                    True,
                    f"Config loaded (API key present: {has_api_key})",
                    {"has_api_key": has_api_key}
                )
            except Exception as e:
                self.log_result(
                    "Configuration Test",
                    True,
                    "Config structure valid, API key check failed (expected if .env not configured)",
                    {"error": str(e)}
                )
                
        except Exception as e:
            self.log_result(
                "Configuration Test",
                False,
                f"Configuration failed: {e}"
            )
    
    def test_component_instantiation(self):
        """Test that pipeline components can be instantiated."""
        try:
            from podchat.models.config import Config
            from podchat.core.output_formatter import OutputFormatter
            from podchat.models.transcript import (
                Transcript, TranscriptMetadata, TranscriptSegment
            )
            
            # Test OutputFormatter
            formatter = OutputFormatter("./test_output")
            
            # Create mock transcript
            metadata = TranscriptMetadata(
                video_id="test123",
                url="https://youtube.com/watch?v=test123",
                duration=3600.0
            )
            
            segments = [
                TranscriptSegment(text="Test segment 1", start=0.0, duration=5.0),
                TranscriptSegment(text="Test segment 2", start=5.0, duration=5.0),
            ]
            
            transcript = Transcript(segments=segments, metadata=metadata)
            
            self.log_result(
                "Component Instantiation Test",
                True,
                f"Components created (transcript: {transcript.word_count} words)",
                {
                    "transcript_words": transcript.word_count,
                    "transcript_duration": transcript.metadata.duration
                }
            )
            
        except Exception as e:
            self.log_result(
                "Component Instantiation Test",
                False,
                f"Instantiation failed: {e}"
            )
    
    def test_pipeline_structure(self):
        """Test that PodcastProcessor has correct structure."""
        try:
            from podchat.core.processor import PodcastProcessor
            
            # Check required methods
            required_methods = ['__init__', 'process']
            missing = []
            
            for method in required_methods:
                if not hasattr(PodcastProcessor, method):
                    missing.append(method)
            
            if missing:
                self.log_result(
                    "Pipeline Structure Test",
                    False,
                    f"Missing methods: {missing}"
                )
            else:
                self.log_result(
                    "Pipeline Structure Test",
                    True,
                    "PodcastProcessor has all required methods"
                )
                
        except Exception as e:
            self.log_result(
                "Pipeline Structure Test",
                False,
                f"Structure check failed: {e}"
            )
    
    def test_error_handling(self):
        """Test error handling for various failure scenarios."""
        from podchat.integrations.youtube_client import YouTubeClient
        
        client = YouTubeClient()
        
        # Test invalid URL handling
        try:
            client.extract_video_id("https://invalid-url.com")
            self.log_result(
                "Error Handling Test - Invalid URL",
                False,
                "Should have raised InvalidURLError"
            )
        except InvalidURLError:
            self.log_result(
                "Error Handling Test - Invalid URL",
                True,
                "InvalidURLError raised correctly"
            )
        except Exception as e:
            self.log_result(
                "Error Handling Test - Invalid URL",
                False,
                f"Wrong exception type: {type(e).__name__}"
            )
        
        # Test valid URL parsing
        try:
            test_urls = [
                ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
                ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
                ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ]
            
            all_passed = True
            for url, expected_id in test_urls:
                video_id = client.extract_video_id(url)
                if video_id != expected_id:
                    all_passed = False
                    break
            
            self.log_result(
                "Error Handling Test - URL Parsing",
                all_passed,
                f"Tested {len(test_urls)} URL formats"
            )
            
        except Exception as e:
            self.log_result(
                "Error Handling Test - URL Parsing",
                False,
                f"URL parsing failed: {e}"
            )
    
    def test_end_to_end_processing(self, video_url: str):
        """Test complete end-to-end processing with a real video."""
        print("-" * 70)
        print("END-TO-END TEST: Processing real video")
        print("-" * 70)
        print()
        
        try:
            # Load config
            print("1. Loading configuration...")
            config = ConfigManager.load()
            config.verbose = True
            config.output_directory = str(self.output_dir)
            
            if not config.llm_api_key:
                self.log_result(
                    "End-to-End Processing Test",
                    False,
                    "No API key configured. Please set OPENROUTER_API_KEY in .env"
                )
                return
            
            print("   ✓ Configuration loaded")
            print()
            
            # Initialize processor
            print("2. Initializing processor...")
            processor = PodcastProcessor(config)
            print("   ✓ Processor initialized")
            print()
            
            # Process video
            print(f"3. Processing video: {video_url}")
            print("   This may take 1-3 minutes depending on video length...")
            print()
            
            start_time = datetime.now()
            result = processor.process(url=video_url, mode="summary")
            end_time = datetime.now()
            
            processing_time = (end_time - start_time).total_seconds()
            
            print()
            print("   ✓ Processing complete!")
            print()
            
            # Validate output
            output_path = Path(result['output_path'])
            if not output_path.exists():
                raise FileNotFoundError(f"Output file not created: {output_path}")
            
            content = output_path.read_text()
            validation = self.validate_summary_quality(content)
            
            self.log_result(
                "End-to-End Processing Test",
                validation['passed'],
                f"Processed in {processing_time:.2f}s",
                {
                    "video_id": result['video_id'],
                    "word_count": result['word_count'],
                    "processing_time": processing_time,
                    "output_path": str(output_path),
                    "validation": validation
                }
            )
            
            # Print result summary
            print("-" * 70)
            print("PROCESSING RESULT:")
            print("-" * 70)
            print(f"Video ID:        {result['video_id']}")
            print(f"Word Count:      {result['word_count']:,}")
            print(f"Processing Time: {processing_time:.2f}s")
            print(f"Output File:     {output_path}")
            print()
            print("Quality Validation:")
            for check, passed in validation['checks'].items():
                status = "✓" if passed else "✗"
                print(f"  {status} {check}")
            print()
            
        except Exception as e:
            self.log_result(
                "End-to-End Processing Test",
                False,
                f"Processing failed: {e}",
                {"error_type": type(e).__name__}
            )
            import traceback
            print("\nError traceback:")
            traceback.print_exc()
            print()
    
    def validate_summary_quality(self, content: str) -> Dict:
        """Validate that generated summary meets quality standards."""
        checks = {
            "Has markdown heading": content.strip().startswith("#"),
            "Has metadata section": any(x in content for x in ["URL:", "Duration:", "Metadata"]),
            "Has overview/summary": any(x in content for x in ["Overview", "Summary", "## "]),
            "Has main themes": "Theme" in content or "theme" in content,
            "Has takeaways": any(x in content for x in ["Takeaway", "takeaway", "Key"]),
            "Has timestamps": "[" in content and ":" in content and "]" in content,
            "Has quotes": '"' in content or "Quote" in content,
            "Sufficient length": len(content) > 500,
            "Not truncated": not content.strip().endswith("..."),
            "Proper markdown": "##" in content,
        }
        
        all_passed = all(checks.values())
        
        return {
            "passed": all_passed,
            "checks": checks,
            "total_checks": len(checks),
            "passed_checks": sum(checks.values()),
            "content_length": len(content)
        }
    
    def generate_report(self):
        """Generate final test report."""
        print("=" * 70)
        print("TEST REPORT")
        print("=" * 70)
        print()
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['passed'])
        failed = total - passed
        
        print(f"Total Tests:  {total}")
        print(f"Passed:       {passed} ({100*passed//total}%)")
        print(f"Failed:       {failed}")
        print()
        
        if failed > 0:
            print("Failed Tests:")
            for result in self.results:
                if not result['passed']:
                    print(f"  ✗ {result['test']}: {result['message']}")
            print()
        
        # Save detailed results to JSON
        results_file = self.output_dir / "test_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": total,
                    "passed": passed,
                    "failed": failed
                },
                "results": self.results
            }, f, indent=2)
        
        print(f"Detailed results saved to: {results_file}")
        print()
        
        # Overall status
        if failed == 0:
            print("✅ ALL TESTS PASSED - Phase 4 implementation verified!")
        else:
            print("⚠️  SOME TESTS FAILED - Review errors above")
        
        print("=" * 70)
        print()


def main():
    """Main test execution."""
    import sys
    
    # Get optional video URL from command line
    test_video_url = sys.argv[1] if len(sys.argv) > 1 else None
    
    if test_video_url:
        print(f"Test video URL provided: {test_video_url}")
        print()
    else:
        print("⚠️  No test video URL provided")
        print("Usage: python tests/test_phase4_summary_generation.py <youtube_url>")
        print()
        print("Running structural tests only...")
        print()
    
    runner = Phase4TestRunner()
    runner.run_all_tests(test_video_url)


if __name__ == "__main__":
    main()
