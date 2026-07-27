import os
import httpx
from fastmcp import FastMCP

mcp = FastMCP("QuincyEntraSonarMCP")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Referer": "https://entrasonar.com/"
}

@mcp.tool(
    output_schema={
        "type": "object",
        "properties": {
            "domain_info": {
                "type": "object",
                "description": "Granular Microsoft Entra ID / Azure infrastructure identification parameters.",
                "properties": {
                    "tenantId": {"type": ["string", "null"], "description": "Microsoft Entra Directory Tenant UUID."},
                    "domain": {"type": ["string", "null"], "description": "The queried domain identity string."},
                    "domainType": {"type": ["string", "null"], "description": "E.g., Federated or Managed configuration."},
                    "state": {"type": ["integer", "null"], "description": "Internal status numeric code flag."},
                    "idp": {"type": ["string", "null"], "description": "Name designation of the primary identity provider (IDP)."},
                    "idpInfo": {
                        "type": "object",
                        "description": "Comprehensive reference metadata detailing the IDP endpoint.",
                        "properties": {
                            "name": {"type": ["string", "null"]},
                            "logo": {"type": ["string", "null"]},
                            "description": {"type": ["string", "null"]},
                            "website": {"type": ["string", "null"]},
                            "documentation": {"type": ["string", "null"]}
                        }
                    },
                    "displayName": {"type": ["string", "null"], "description": "Legal/Enterprise identity display name."},
                    "allDomains": {"type": ["array", "null"], "items": {"type": ["string", "null"]}, "description": "Inventory of domain variants under the tenant."},
                    "defaultDomainName": {"type": ["string", "null"]},
                    "region": {"type": ["string", "null"]},
                    "tenantRegionScope": {"type": ["string", "null"]},
                    "isChina": {"type": ["boolean", "null"]},
                    "isGovCloud": {"type": ["boolean", "null"]},
                    "cloudInstanceName": {"type": ["string", "null"]},
                    "federationBrandName": {"type": ["string", "null"]},
                    "isB2CTenant": {"type": ["boolean", "null"]}
                }
            },
            "m365_checks": {
                "type": "object",
                "description": "Microsoft 365 posture analysis matrix logs covering DNS security and multi-cloud services status.",
                "properties": {
                    "success": {"type": ["boolean", "null"]},
                    "domain": {"type": ["string", "null"]},
                    "emailSecurity": {
                        "type": "object",
                        "description": "DNS boundaries configurations mapping standard hygiene layers.",
                        "properties": {
                            "mx": {
                                "type": "object",
                                "properties": {
                                    "configured": {"type": ["boolean", "null"]},
                                    "servers": {"type": ["array", "null"], "items": {"type": ["string", "null"]}},
                                    "primaryServer": {"type": ["string", "null"]}
                                }
                            },
                            "spf": {
                                "type": "object",
                                "properties": {
                                    "configured": {"type": ["boolean", "null"]},
                                    "record": {"type": ["string", "null"]},
                                    "includes": {"type": ["array", "null"], "items": {"type": ["string", "null"]}},
                                    "all": {"type": ["string", "null"]}
                                }
                            },
                            "dmarc": {
                                "type": "object",
                                "properties": {
                                    "configured": {"type": ["boolean", "null"]},
                                    "policy": {"type": ["string", "null"]},
                                    "record": {"type": ["string", "null"]},
                                    "reportingEmails": {"type": ["array", "null"], "items": {"type": ["string", "null"]}}
                                }
                            },
                            "dkim": {
                                "type": "object",
                                "properties": {
                                    "configured": {"type": ["boolean", "null"]}
                                }
                            },
                            "mtaSts": {
                                "type": "object",
                                "properties": {
                                    "configured": {"type": ["boolean", "null"]}
                                }
                            },
                            "bimi": {
                                "type": "object",
                                "properties": {
                                    "configured": {"type": ["boolean", "null"]}
                                }
                            }
                        }
                    },
                    "m365Services": {
                        "type": "object",
                        "description": "M365 cloud infrastructure routing tracking.",
                        "properties": {
                            "autodiscover": {
                                "type": "object",
                                "properties": {
                                    "available": {"type": ["boolean", "null"]}
                                }
                            },
                            "teams": {"type": "object", "properties": {"available": {"type": ["boolean", "null"]}}},
                            "sharepoint": {"type": "object", "properties": {"available": {"type": ["boolean", "null"]}}},
                            "onedrive": {"type": "object", "properties": {"available": {"type": ["boolean", "null"]}}},
                            "azureServices": {
                                "type": "object",
                                "description": "Exposes infrastructure indicators tracking content processing nodes across Azure, AWS, and Cloudflare layers.",
                                "properties": {
                                    "webapp": {"type": ["boolean", "null"]},
                                    "storage": {"type": ["boolean", "null"]},
                                    "appProxy": {"type": ["boolean", "null"]},
                                    "frontDoor": {"type": ["boolean", "null"]},
                                    "apiManagement": {"type": ["boolean", "null"]},
                                    "cdn": {"type": ["boolean", "null"]},
                                    "trafficManager": {"type": ["boolean", "null"]},
                                    "containerApps": {"type": ["boolean", "null"]},
                                    "cloudflare": {"type": ["boolean", "null"]},
                                    "fastly": {"type": ["boolean", "null"]},
                                    "globalProtect": {"type": ["boolean", "null"]},
                                    "appGateway": {"type": ["boolean", "null"]},
                                    "azureStaticWebApp": {"type": ["boolean", "null"]},
                                    "awsS3": {"type": ["boolean", "null"]},
                                    "awsCloudFront": {"type": ["boolean", "null"]},
                                    "awsElasticBeanstalk": {"type": ["boolean", "null"]},
                                    "googleCloudRun": {"type": ["boolean", "null"]},
                                    "firebaseHosting": {"type": ["boolean", "null"]},
                                    "googleCloudStorage": {"type": ["boolean", "null"]},
                                    "googleCloudCDN": {"type": ["boolean", "null"]},
                                    "googleAppEngine": {"type": ["boolean", "null"]},
                                    "awsALB": {"type": ["boolean", "null"]},
                                    "vercel": {"type": ["boolean", "null"]},
                                    "netlify": {"type": ["boolean", "null"]},
                                    "githubPages": {"type": ["boolean", "null"]},
                                    "render": {"type": ["boolean", "null"]},
                                    "heroku": {"type": ["boolean", "null"]},
                                    "azureCloudServiceClassic": {"type": ["boolean", "null"]}
                                }
                            },
                            "intune": {
                                "type": "object",
                                "properties": {
                                    "configured": {"type": ["boolean", "null"]},
                                    "enrollment": {"type": ["boolean", "null"]},
                                    "registration": {"type": ["boolean", "null"]}
                                }
                            },
                            "verifiedId": {
                                "type": "object",
                                "properties": {
                                    "configured": {"type": ["boolean", "null"]},
                                    "hasDidDocument": {"type": ["boolean", "null"]},
                                    "hasConfiguration": {"type": ["boolean", "null"]}
                                }
                            },
                            "thirdPartyApps": {
                                "type": ["array", "null"],
                                "items": {"type": ["string", "null"]},
                                "description": "Inventory array tracking registered enterprise marketplace ecosystems."
                            }
                        }
                    },
                    "cached": {"type": ["boolean", "null"]}
                }
            }
        },
        "required": ["domain_info", "m365_checks"]
    }
)
async def analyze_domain(domain: str) -> dict:
    """Analyze a domain name using EntraSonar APIs to aggregate general and M365 data."""
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Fetch General Domain Info
        info_url = f"https://entrasonar.com/api/domain?domain={domain}"
        res1 = await client.get(info_url, headers=HEADERS)
        domain_info = res1.json() if res1.status_code == 200 else {"error": res1.status_code}
        
        # Dynamically extract tenant details
        is_dict = isinstance(domain_info, dict)
        tenant_name = domain_info.get("tenantName", domain.split('.')[0]) if is_dict else domain.split('.')[0]
        tenant_id = domain_info.get("tenantId", "ba8f4151-ab0e-4da6-862d-68b05906e887") if is_dict else "ba8f4151-ab0e-4da6-862d-68b05906e887"
        
        # 2. Fetch M365 Checks using the dynamic tenant info
        m365_url = f"https://entrasonar.com/api/domain/m365-checks?domain={domain}&tenantName={tenant_name}&tenantId={tenant_id}&cloudType=worldwide"
        res2 = await client.get(m365_url, headers=HEADERS)
        m365_checks = res2.json() if res2.status_code == 200 else {"error": res2.status_code}
        
        return {
            "domain_info": domain_info,
            "m365_checks": m365_checks
        }

if __name__ == "__main__":
    mcp.run(
        transport="http", 
        host="0.0.0.0", 
        port=8000,
        stateless_http=True
    )