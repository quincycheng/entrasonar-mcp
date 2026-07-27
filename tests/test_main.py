"""
Test cases for the EntraSonar MCP server.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
from main import analyze_domain, mcp, HEADERS


class TestHeaders:
    """Test HTTP headers configuration."""
    
    def test_headers_exist(self):
        """Test that HEADERS are defined."""
        assert HEADERS is not None
        assert isinstance(HEADERS, dict)
    
    def test_headers_user_agent(self):
        """Test that User-Agent header is set."""
        assert "User-Agent" in HEADERS
        assert len(HEADERS["User-Agent"]) > 0
    
    def test_headers_referer(self):
        """Test that Referer header is set."""
        assert "Referer" in HEADERS
        assert "entrasonar.com" in HEADERS["Referer"]


class TestMCPServer:
    """Test MCP server initialization."""
    
    def test_mcp_server_created(self):
        """Test that MCP server is initialized."""
        assert mcp is not None
        assert mcp.name == "QuincyEntraSonarMCP"
    
    def test_analyze_domain_tool_registered(self):
        """Test that analyze_domain tool is registered."""
        # Check if the tool is in the list of tools
        assert any(tool.name == "analyze_domain" for tool in mcp.tools)


class TestAnalyzeDomain:
    """Test the analyze_domain function."""
    
    @pytest.mark.asyncio
    async def test_analyze_domain_success(self):
        """Test successful domain analysis with mocked HTTP responses."""
        domain = "example.com"
        
        mock_domain_info = {
            "tenantId": "12345678-1234-1234-1234-123456789012",
            "domain": "example.com",
            "domainType": "Managed",
            "displayName": "Example Corporation"
        }
        
        mock_m365_checks = {
            "success": True,
            "domain": "example.com",
            "emailSecurity": {
                "spf": {"configured": True},
                "dkim": {"configured": True},
                "dmarc": {"configured": True}
            }
        }
        
        mock_response_1 = MagicMock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = mock_domain_info
        
        mock_response_2 = MagicMock()
        mock_response_2.status_code = 200
        mock_response_2.json.return_value = mock_m365_checks
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client
            
            # Mock sequential get calls
            mock_client.get.side_effect = [mock_response_1, mock_response_2]
            
            result = await analyze_domain(domain)
            
            assert result is not None
            assert "domain_info" in result
            assert "m365_checks" in result
    
    @pytest.mark.asyncio
    async def test_analyze_domain_with_error_response(self):
        """Test domain analysis with error responses."""
        domain = "invalid.com"
        
        mock_response_1 = MagicMock()
        mock_response_1.status_code = 404
        
        mock_response_2 = MagicMock()
        mock_response_2.status_code = 404
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client
            
            mock_client.get.side_effect = [mock_response_1, mock_response_2]
            
            result = await analyze_domain(domain)
            
            assert result is not None
            assert "domain_info" in result
            assert "m365_checks" in result
    
    @pytest.mark.asyncio
    async def test_analyze_domain_extracts_tenant_name(self):
        """Test that tenant name is extracted correctly."""
        domain = "contoso.com"
        
        mock_domain_info = {
            "tenantName": "contoso",
            "tenantId": "12345678-1234-1234-1234-123456789012"
        }
        
        mock_m365_checks = {"success": True}
        
        mock_response_1 = MagicMock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = mock_domain_info
        
        mock_response_2 = MagicMock()
        mock_response_2.status_code = 200
        mock_response_2.json.return_value = mock_m365_checks
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client
            
            mock_client.get.side_effect = [mock_response_1, mock_response_2]
            
            result = await analyze_domain(domain)
            
            # Verify the second call (M365 checks) includes the tenant name
            second_call = mock_client.get.call_args_list[1]
            assert "tenantName=contoso" in str(second_call)


class TestDomainValidation:
    """Test domain input validation."""
    
    @pytest.mark.asyncio
    async def test_analyze_domain_with_empty_string(self):
        """Test handling of empty domain string."""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client
            
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            
            mock_client.get.side_effect = [mock_response, mock_response]
            
            result = await analyze_domain("")
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_analyze_domain_with_special_characters(self):
        """Test handling of domains with special characters."""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client
            
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            
            mock_client.get.side_effect = [mock_response, mock_response]
            
            result = await analyze_domain("test-domain.co.uk")
            assert result is not None


class TestOutputSchema:
    """Test the output schema validation."""
    
    def test_output_schema_defined(self):
        """Test that output schema is defined for analyze_domain."""
        tool = next((t for t in mcp.tools if t.name == "analyze_domain"), None)
        assert tool is not None
        assert tool.outputSchema is not None
    
    def test_output_schema_contains_required_fields(self):
        """Test that output schema has required fields."""
        tool = next((t for t in mcp.tools if t.name == "analyze_domain"), None)
        assert tool is not None
        schema = tool.outputSchema
        
        # Check for required fields
        assert "properties" in schema
        assert "domain_info" in schema["properties"]
        assert "m365_checks" in schema["properties"]
