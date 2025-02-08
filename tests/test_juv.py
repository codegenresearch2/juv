import pytest

# Example test function
def test_example():
    assert 1 == 1  # Simple assertion to check if the test is working

# Example fixture
@pytest.fixture
def example_fixture():
    return 42

# Test class example
class TestExampleClass:
    def test_example_method(self, example_fixture):
        assert example_fixture == 42  # Using fixture in a test