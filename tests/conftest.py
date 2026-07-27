"""
Pytest configuration and fixtures.
"""
import pytest
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_domain():
    """Provide a test domain."""
    return "example.com"


@pytest.fixture
def mock_tenant_id():
    """Provide a test tenant ID."""
    return "12345678-1234-1234-1234-123456789012"


@pytest.fixture
def mock_domain_response():
    """Provide a mock domain info response."""
    return {
        "tenantId": "12345678-1234-1234-1234-123456789012",
        "domain": "example.com",
        "domainType": "Managed",
        "displayName": "Example Corporation",
        "region": "US",
        "cloudInstanceName": "AzurePublic",
        "isChina": False,
        "isGovCloud": False,
        "isB2CTenant": False,
    }


@pytest.fixture
def mock_m365_response():
    """Provide a mock M365 checks response."""
    return {
        "success": True,
        "domain": "example.com",
        "emailSecurity": {
            "mx": {
                "configured": True,
                "servers": ["mx1.example.com", "mx2.example.com"],
                "primaryServer": "mx1.example.com"
            },
            "spf": {
                "configured": True,
                "record": "v=spf1 include:_spf.google.com ~all",
                "includes": ["_spf.google.com"],
                "all": "~all"
            },
            "dkim": {"configured": True},
            "dmarc": {
                "configured": True,
                "policy": "quarantine",
                "record": "v=DMARC1; p=quarantine"
            },
            "mtaSts": {"configured": True},
            "bimi": {"configured": False}
        },
        "m365Services": {
            "autodiscover": {"available": True},
            "teams": {"available": True},
            "sharepoint": {"available": True},
            "onedrive": {"available": True}
        },
        "cached": False
    }
