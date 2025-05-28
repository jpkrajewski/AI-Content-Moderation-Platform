import pytest
from connexion.exceptions import ClientProblem
from moderation.auth.common import check_scopes


@pytest.mark.parametrize(
    "scopes, required_scopes, should_raise",
    [
        (None, None, False),
        ([], [], False),
        ([], ["scope1"], True),
        (["scope1"], [], False),
        (["scope1", "scope2"], ["scope1"], False),
        (["scope1"], ["scope2"], True),
    ],
)
def test_check_scopes(scopes, required_scopes, should_raise):
    if should_raise:
        with pytest.raises(ClientProblem):
            check_scopes(scopes, required_scopes)
    else:
        assert check_scopes(scopes, required_scopes) is None


def test_xdxd():
    import requests

    def check_url_with_google_safe_browsing(api_key, url_to_check):
        api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "client": {
                "clientId": "yourcompanyname",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                                "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [
                    {"url": url_to_check}
                ]
            }
        }

        response = requests.post(api_url, headers=headers, json=payload, params={"key": api_key})
        if response.status_code == 200:
            result = response.json()
            if "matches" in result:
                return f"Unsafe URL detected: {result['matches']}"
            else:
                return "The URL is safe."
        else:
            return f"Error: {response.status_code}, {response.text}"

    # Replace with your Google API key and the URL you want to check
    api_key = "AIzaSyCLj3R8WC0a2olN6pXkO55dCTg2KN4586M"
    url = "https://acessonetpj.com/componenteSeguranca.php?hash=10455267456835e6850f1647.30480167"
    print(check_url_with_google_safe_browsing(api_key, url))



def test_url():
    import spacy

    def extract_urls_with_spacy(text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        urls = [ent.text for ent in doc.ents if ent.label_ == "URL"]
        return urls

    # Example usage
    text_blob = """
    Check out  and  for more information. https://www.dsdsd.com
    """
    urls = extract_urls_with_spacy(text_blob)
    print(urls)