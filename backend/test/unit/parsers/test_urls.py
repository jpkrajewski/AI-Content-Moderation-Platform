from moderation.parsers.urls import extract_urls
import pytest


@pytest.mark.parametrize(
    "text_blob, expected_urls",
    [
        # Test case 1: Single URL
        ("Visit our website at https://example.com for more details.", ["https://example.com"]),

        # Test case 2: Multiple URLs
        ("Check out https://example.com and http://test.com for more information.",
         ["https://example.com", "http://test.com"]),

        # Test case 3: No URLs
        ("This text has no URLs.", []),

        # Test case 4: URLs with query parameters
        ("Visit https://example.com?query=123&sort=asc for more info.",
         ["https://example.com"]),

        # Test case 5: URLs with subdomains
        ("Check https://sub.example.com and https://blog.test.com for updates.",
         ["https://sub.example.com", "https://blog.test.com"]),

        # Test case 6: Mixed content with URLs
        ("Here is a link: https://example.com. And some text.",
         ["https://example.com"]),

        # Test case 7: Invalid URLs (should not extract)
        ("This is not a URL: example.com/test.", []),

        # Test case 8: URLs with different protocols
        ("Visit https://secure-site.com and http://insecure-site.com.",
         ["https://secure-site.com", "http://insecure-site.com"]),

        # Test case 9: URLs with trailing punctuation
        ("Check this out: https://example.com!. It's great.",
         ["https://example.com"]),

        # Test case 10: URLs embedded in parentheses
        ("Visit our site (https://example.com) for details.",
         ["https://example.com"]),
    ]
)
def test_extract_urls(text_blob, expected_urls):
    # Call the function and compare the result with the expected output
    assert extract_urls(text_blob) == expected_urls