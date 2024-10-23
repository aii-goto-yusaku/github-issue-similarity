# GitHub Webhook Setup Guide

This guide provides detailed instructions for setting up the webhook integration between your GitHub repository and the Issue Similarity Detector.

## Prerequisites

Before setting up the webhook, ensure you have:

1. Administrator access to the GitHub repository
2. The Issue Similarity Detector server running and accessible from the internet
3. A secure HTTPS endpoint (recommended for production) or ngrok for development

## Setup Steps

### 1. Start the Webhook Server

Ensure your server is running and accessible:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For development, you can use ngrok to create a temporary public URL:

```bash
ngrok http 8000
```

### 2. Configure GitHub Webhook

1. Go to your repository settings on GitHub
2. Click on "Webhooks" in the left sidebar
3. Click "Add webhook"
4. Configure the webhook:
   - Payload URL: `https://your-server:8000/webhook`
   - Content type: `application/json`
   - Secret: (Optional but recommended for production - Note: Secret verification is not yet implemented in the current version)
   - SSL verification: Enable for production
   - Events: Select "Issues"
5. Click "Add webhook"

### 3. Verify the Setup

1. Create a new issue in your repository
2. Check the webhook's "Recent Deliveries" section in GitHub
3. Verify that the server receives the webhook and processes it
4. Confirm that the bot comments on similar issues

## Security Considerations

1. **Use HTTPS**: Always use HTTPS in production environments
2. **Webhook Secret**: Configure a webhook secret to verify requests
3. **Access Control**: Limit server access using firewalls
4. **Rate Limiting**: Implement rate limiting for the webhook endpoint
5. **Logging**: Enable logging for debugging and security monitoring

## Troubleshooting

### Common Issues

1. **Webhook Not Triggering**
   - Check if the server is accessible
   - Verify the webhook URL is correct
   - Review GitHub webhook logs

2. **Authentication Failed**
   - Verify the GitHub token has correct permissions
   - Check if the token is properly configured in .env

3. **Server Errors**
   - Check server logs for error messages
   - Verify all dependencies are installed
   - Ensure the server has sufficient resources

## Advanced Configuration

### Webhook Payload Example

```json
{
  "action": "opened",
  "issue": {
    "number": 1,
    "title": "Example Issue",
    "body": "Issue description"
  }
}
```

### Environment Variables

Additional configuration options:

```env
WEBHOOK_SECRET=your_webhook_secret
LOG_LEVEL=INFO
MAX_SIMILAR_ISSUES=5
```

## Monitoring

Consider monitoring these aspects:

1. Webhook delivery success rate
2. Response time for similarity analysis
3. Number of similar issues found
4. Server resource usage
5. Error rates and types

## Best Practices

1. Implement retry logic for failed webhook deliveries
2. Set up alerts for webhook failures
3. Regularly rotate security credentials
4. Monitor system performance
5. Keep dependencies updated