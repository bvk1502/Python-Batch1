
### 6. CORS Middleware

**File:** `cors_middleware.py`

**Purpose:** Handles Cross-Origin Resource Sharing (CORS) requests.

**Features:**
- Configurable allowed origins
- Pre-flight request handling
- Credential support
- Custom headers support

**Configuration:**
```python
cors_config = CORSConfig(
    allowed_origins=["*"],  # Configure for production
    allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allowed_headers=["*"],
    allow_credentials=True,
    max_age=600
)
setup_cors_middleware(app, cors_config)
```

**Production CORS Configuration:**
```python
cors_config = CORSConfig(
    allowed_origins=[
        "https://yourdomain.com",
        "https://api.yourdomain.com"
    ],
    allowed_methods=["GET", "POST", "PUT", "DELETE"],
    allowed_headers=["Authorization", "Content-Type"],
    allow_credentials=True
)
```

## Configuration

### Environment Variables

Add these to your `.env` file:

```env
# JWT Configuration
SECRET_KEY=your-super-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
RATE_LIMIT_BURST=10

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
```

### Middleware Setup

```python
from app.middleware.config import setup_middlewares

app = FastAPI()
setup_middlewares(app)
```

## Usage Examples

### 1. Testing Authentication

```bash
# Create a JWT token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Use the token
curl -X GET "http://localhost:8000/protected" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 2. Testing Rate Limiting

```bash
# Make multiple requests to trigger rate limiting
for i in {1..70}; do
  echo "Request $i"
  curl -X GET "http://localhost:8000/health"
  sleep 0.1
done
```

### 3. Testing Security

```bash
# Test suspicious request (should be blocked)
curl -X GET "http://localhost:8000/.env"

# Test SQL injection attempt (should be blocked)
curl -X GET "http://localhost:8000/users/?id=1' OR '1'='1"
```

### 4. Testing CORS

```bash
# Test CORS pre-flight request
curl -X OPTIONS "http://localhost:8000/users/" \
  -H "Origin: https://yourdomain.com" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type"
```

### 5. Monitoring Logs

```bash
# Watch application logs
tail -f logs/app.log

# Filter by request ID
grep "req_1640995200000_12345" logs/app.log
```

## Best Practices

### 1. Security
- Always use HTTPS in production
- Configure CORS properly for production
- Use strong JWT secret keys
- Regularly rotate secrets
- Monitor for suspicious activity

### 2. Rate Limiting
- Set appropriate limits for your use case
- Monitor rate limit violations
- Consider different limits for different endpoints
- Implement user-based rate limiting for authenticated endpoints

### 3. Logging
- Use structured logging
- Don't log sensitive information
- Implement log rotation
- Monitor log levels in production

### 4. Error Handling
- Don't expose internal errors to clients
- Log all errors with context
- Implement proper error codes
- Provide helpful error messages

### 5. Performance
- Monitor middleware performance impact
- Use async operations where possible
- Implement caching for expensive operations
- Profile your application regularly

## Troubleshooting

### Common Issues

#### 1. Rate Limiting Too Aggressive
**Problem:** Legitimate users getting blocked
**Solution:** Adjust rate limits in configuration

```python
app.add_middleware(
    RateLimitingMiddleware,
    requests_per_minute=120,  # Increase limit
    requests_per_hour=2000,   # Increase limit
    burst_limit=20           # Increase burst limit
)
```

#### 2. CORS Issues
**Problem:** Frontend can't access API
**Solution:** Configure CORS properly

```python
cors_config = CORSConfig(
    allowed_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True
)
```

#### 3. Authentication Token Issues
**Problem:** Valid tokens being rejected
**Solution:** Check token format and secret key

```python
# Verify token manually
import jwt
try:
    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    print("Token is valid:", payload)
except jwt.ExpiredSignatureError:
    print("Token has expired")
except jwt.InvalidTokenError:
    print("Token is invalid")
```

#### 4. Logging Too Verbose
**Problem:** Too many log entries
**Solution:** Adjust logging configuration

```python
app.add_middleware(
    LoggingMiddleware,
    log_headers=False,  # Disable header logging
    log_body=False     # Disable body logging
)
```

### Debug Mode

Enable debug mode for detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

app.add_middleware(
    LoggingMiddleware,
    log_headers=True,
    log_body=True
)
```

### Monitoring

Monitor middleware performance:

```python
# Add timing middleware
@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Conclusion

This middleware stack provides a robust foundation for your FastAPI application. Each middleware serves a specific purpose and can be configured independently. Remember to:

1. Configure middlewares according to your needs
2. Monitor performance and adjust settings
3. Keep security configurations up to date
4. Implement proper logging and monitoring
5. Test thoroughly in development before deploying

For production deployments, ensure all security settings are properly configured and monitor the application for any issues.