# Application Credentials Guide

## What is `application_credentials.py`?

This component handles OAuth2 authorization flows for cloud-based integrations. It allows users to authenticate with external services using OAuth.

## When Do You Need It?

**Use application_credentials if:**
- Your integration connects to a cloud API that uses OAuth2
- Users need to authorize your integration with their account
- The service provider requires OAuth flow (Google, Spotify, Ring, Nest, etc.)

**Don't use application_credentials if:**
- Your integration uses API keys (use config_flow to collect the key)
- Your integration uses username/password (use config_flow with authentication)
- Your integration connects to local devices (no cloud authentication needed)
- Your integration doesn't require authentication

## Common OAuth Providers

Services that typically use OAuth2:
- Google services (Calendar, Drive, etc.)
- Spotify
- GitHub
- Fitbit
- Ring
- Nest
- Most modern cloud APIs

## Usage Pattern

```bash
# For OAuth-based cloud integration:
python scripts/scaffold.py api
python scripts/scaffold.py application_credentials
python scripts/scaffold.py sensor
```

Then:
1. Edit `application_credentials.py`:
   - Update `OAUTH_AUTHORIZE_URL`
   - Update `OAUTH_TOKEN_URL`
   - Update help URLs in `async_get_description_placeholders`

2. Update your `config_flow.py` to use OAuth:
   - Import OAuth helpers
   - Implement OAuth flow in config flow

3. Users authenticate via Settings -> Devices & Services -> Add Integration

## What the Template Provides

The `application_credentials.py.jinja` template includes:
- `async_get_authorization_server()` - Returns OAuth server endpoints
- `async_get_description_placeholders()` - Provides help links for users
- TODO comments for customization

## Additional Requirements

Your integration will need:
1. `application_credentials` in `manifest.json` dependencies
2. OAuth configuration in `config_flow.py`
3. Client ID and Client Secret from the service provider
4. Proper redirect URI configuration with the provider

## Example Flow

1. User adds your integration
2. Home Assistant redirects to OAuth provider
3. User authorizes the integration
4. Provider redirects back with authorization code
5. Your integration exchanges code for access token
6. Integration uses token to make API calls

## Learn More

- [Home Assistant Application Credentials Documentation](https://www.home-assistant.io/integrations/application_credentials/)
- [OAuth2 Flow Documentation](https://developers.home-assistant.io/docs/api/oauth/)
