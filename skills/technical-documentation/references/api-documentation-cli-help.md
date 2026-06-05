# Technical Documentation Methodology Reference

> **Comprehensive reference on API documentation patterns and CLI help text design.**
> Compiled from industry standards (OpenAPI/Swagger, Google, Stripe, GitHub, GNU, POSIX, Linux man-pages, clig.dev, Microsoft Azure Architecture).

---

## Table of Contents

1. [API Documentation Patterns](#1-api-documentation-patterns)
   - [1.1 Endpoint Reference Structure](#11-endpoint-reference-structure)
   - [1.2 HTTP Methods & Status Codes](#12-http-methods--status-codes)
   - [1.3 Parameter Documentation Conventions](#13-parameter-documentation-conventions)
   - [1.4 Request/Response Documentation](#14-requestresponse-documentation)
   - [1.5 Error Documentation](#15-error-documentation)
   - [1.6 Example Design](#16-example-design)
   - [1.7 Authentication Documentation Patterns](#17-authentication-documentation-patterns)
   - [1.8 OpenAPI/Swagger Specification Patterns](#18-openapiswagger-specification-patterns)
   - [1.9 Doc Generation Workflows](#19-doc-generation-workflows)
2. [CLI Help Text Design](#2-cli-help-text-design)
   - [2.1 Help Text Structure](#21-help-text-structure)
   - [2.2 Usage Line Conventions](#22-usage-line-conventions)
   - [2.3 Flag Naming Conventions](#23-flag-naming-conventions)
   - [2.4 Subcommand Help Hierarchy](#24-subcommand-help-hierarchy)
   - [2.5 Exit Codes](#25-exit-codes)
   - [2.6 Environment Variables](#26-environment-variables)
   - [2.7 Output Format Documentation](#27-output-format-documentation)
   - [2.8 Man Page Structure](#28-man-page-structure)
3. [Additional Patterns & Standards](#3-additional-patterns--standards)

---

## 1. API Documentation Patterns

### 1.1 Endpoint Reference Structure

Every endpoint reference should document these fields in a consistent order:

```
ENDPOINT
  METHOD         HTTP method (GET, POST, PUT, PATCH, DELETE)
  PATH           Canonical URI path (e.g., /v2/customers/{id})
  SUMMARY        One-line description of the operation
  DESCRIPTION    Extended description of what the endpoint does
  AUTH           Required authentication / scopes
  PARAMETERS     Path, query, header, and cookie parameters
  REQUEST BODY   Schema for POST/PUT/PATCH (if applicable)
  RESPONSES      One block per status code (200, 201, 204, 400, 404, etc.)
  ERRORS         Specific error conditions and codes
  EXAMPLES       Happy path and error-case examples (curl, SDK snippets)
```

**Recommended ordering within a doc set:**

1. **Overview / Authentication** (first page)
2. **Resources grouped by domain** (e.g., Customers, Orders, Payments)
3. **Within each resource group:**
   - List (GET) — collection
   - Retrieve (GET) — single item
   - Create (POST)
   - Update (PUT/PATCH)
   - Delete (DELETE)
4. **Webhooks** (if applicable)
5. **Errors / API Reference Appendix**

**URI design rules (REST):**

| Rule | Good | Bad |
|------|------|-----|
| Use nouns, not verbs | `/orders` | `/create-order` |
| Plural for collections | `/customers` | `/customer` |
| Singular for single resource | `/customers/5` | `/customers/5` (acceptable) |
| Keep nesting shallow | `/customers/5/orders` | `/customers/5/orders/99/products` |
| Don't mirror DB structure | `/invoices` | `/tbl_invoices` |
| Version in URI path | `/v2/customers` | `?version=2` or `/customers` (unversioned) |

---

### 1.2 HTTP Methods & Status Codes

#### Standard HTTP Method Mapping

| Method | CRUD | Idempotent | Safe | Request Body |
|--------|------|------------|------|-------------|
| GET | Read | Yes | Yes | No |
| POST | Create | No | No | Yes |
| PUT | Replace | Yes | No | Yes |
| PATCH | Partial update | No* | No | Yes |
| DELETE | Delete | Yes | No | No (body discouraged) |

*\*PATCH is not guaranteed idempotent unless using a strategy like JSON Merge Patch (RFC 7396).*

#### Common HTTP Status Codes

| Code | Name | When to Use |
|------|------|-------------|
| `200 OK` | Success | GET, PUT, PATCH completed |
| `201 Created` | Created | POST creates a resource; include `Location` header |
| `202 Accepted` | Accepted | Async operation accepted for processing |
| `204 No Content` | No Content | DELETE succeeds, or GET with no body |
| `301 Moved Permanently` | Redirect | Resource relocated |
| `304 Not Modified` | Not Modified | Conditional GET (ETag/If-Modified-Since) |
| `400 Bad Request` | Bad Request | Malformed syntax, missing required fields |
| `401 Unauthorized` | Unauthorized | Missing or invalid credentials |
| `403 Forbidden` | Forbidden | Authenticated but not authorized |
| `404 Not Found` | Not Found | Resource does not exist |
| `405 Method Not Allowed` | Method Not Allowed | Wrong HTTP method for the endpoint |
| `409 Conflict` | Conflict | Version conflict, duplicate resource |
| `422 Unprocessable Entity` | Unprocessable | Semantic validation failure (preferred over 400 for business logic) |
| `429 Too Many Requests` | Rate Limited | Rate limit exceeded; include `Retry-After` header |
| `500 Internal Server Error` | Server Error | Unexpected server failure |
| `502 Bad Gateway` | Bad Gateway | Upstream service failure |
| `503 Service Unavailable` | Service Unavailable | Temporary overload or maintenance |

#### Documentation Pattern for Status Codes

```yaml
responses:
  "200":
    description: "Customer retrieved successfully"
    content:
      application/json:
        schema:
          $ref: "#/components/schemas/Customer"
  "401":
    description: "Authentication credentials missing or invalid"
  "404":
    description: "Customer with the specified ID was not found"
  "429":
    description: "Rate limit exceeded. Retry after the time specified in the Retry-After header"
```

---

### 1.3 Parameter Documentation Conventions

#### Parameter Locations

| Location | `in` value | Description | Example |
|----------|-----------|-------------|---------|
| Path | `path` | URL path variable | `GET /users/{id}` |
| Query | `query` | URL query string | `?status=active&limit=10` |
| Header | `header` | HTTP header | `X-Request-Id: abc123` |
| Cookie | `cookie` | Cookie value | `session_id=xyz` |

#### Documentation Fields Per Parameter

```
name          — The parameter name (matches the URI template for path params)
in            — Location: path, query, header, cookie
description   — Human-readable explanation (required for every parameter)
required      — Boolean (true for path params, true for mandatory query/header params)
schema        — Type definition (type, format, enum, default, minimum, maximum, pattern)
example       — Single representative value
examples      — Multiple named examples
deprecated    — Boolean (default false)
allowEmptyValue — Boolean (false by default)
nullable      — Boolean (false by default)
style         — Serialization style for arrays/objects
explode       — Whether to explode array/object values
```

#### Query Parameter Documentation Patterns

```yaml
parameters:
  - name: limit
    in: query
    description: "Maximum number of results to return (1–100)"
    schema:
      type: integer
      minimum: 1
      maximum: 100
      default: 20
    required: false
  - name: offset
    in: query
    description: "Number of results to skip for pagination"
    schema:
      type: integer
      minimum: 0
      default: 0
    required: false
  - name: sort_by
    in: query
    description: "Field to sort results by"
    schema:
      type: string
      enum: [created_at, updated_at, name]
      default: created_at
    required: false
  - name: status
    in: query
    description: "Filter by status (comma-separated for multiple values)"
    schema:
      type: array
      items:
        type: string
        enum: [active, inactive, archived]
      style: form
      explode: false
    required: false
```

**Key rule:** Always document query parameters with type, constraints (min/max/enum), default values, and example values. Incomplete parameter documentation is one of the most common API doc gaps.

---

### 1.4 Request/Response Documentation

#### Request Body Schema

Document the full schema for POST, PUT, and PATCH requests:

```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        required:
          - email
          - name
        properties:
          email:
            type: string
            format: email
            description: "Customer email address"
            example: "user@example.com"
          name:
            type: string
            description: "Customer full name"
            minLength: 1
            maxLength: 255
            example: "Alice Johnson"
          phone:
            type: string
            description: "Customer phone number (optional)"
            nullable: true
            example: "+1-555-0123"
```

**Best practices for request body docs:**

- Mark required fields explicitly (both in a `required` array and via prose)
- Always include `example` values that are realistic (not `string` or `123`)
- Document format constraints: `minLength`, `maxLength`, `pattern`, `minimum`, `maximum`
- Document `nullable: true` explicitly — don't confuse nullable with optional
- Use `deprecated: true` on fields being phased out

#### Response Schema Documentation

```yaml
responses:
  "200":
    description: "Orders list with pagination metadata"
    content:
      application/json:
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                $ref: "#/components/schemas/Order"
            pagination:
              type: object
              properties:
                total:
                  type: integer
                  description: "Total number of records matching the query"
                limit:
                  type: integer
                  description: "Number of records per page"
                offset:
                  type: integer
                  description: "Offset used for this page"
                next_offset:
                  type: integer
                  nullable: true
                  description: "Offset for the next page, or null if no more records"
```

**Best practices for response docs:**

- Document every status code that can be returned (including error codes)
- Show the full response shape, not just the success case
- Document pagination metadata when returning lists
- Document rate limit headers for 429 responses
- Use `$ref` to shared components to avoid duplication

---

### 1.5 Error Documentation

#### Error Response Body Schema

Standardize on a consistent error envelope:

```yaml
Error:
  type: object
  required:
    - error
  properties:
    error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: "Machine-readable error code"
          example: "rate_limit_exceeded"
        message:
          type: string
          description: "Human-readable error description"
          example: "API rate limit exceeded. Please wait and retry your request."
        details:
          type: string
          description: "Additional information (optional)"
          example: "Limit: 100 requests/minute. Reset at 2025-06-05T14:00:00Z"
        request_id:
          type: string
          description: "Unique identifier for the failed request"
          example: "req_abc123def456"
        documentation_url:
          type: string
          format: uri
          description: "Link to relevant documentation"
          example: "https://api.example.com/docs/errors#rate_limit_exceeded"
```

**Mapping errors to status codes:**

| Error Category | HTTP Status | Error Code Example |
|---------------|-------------|-------------------|
| Validation | `400` | `validation_error` |
| Auth missing | `401` | `unauthorized` |
| Auth denied | `403` | `forbidden` |
| Not found | `404` | `not_found` |
| Conflict | `409` | `conflict`, `already_exists` |
| Rate limit | `429` | `rate_limit_exceeded` |
| Server error | `500` | `internal_error` |

**Documentation pattern per endpoint:**

```yaml
responses:
  "400":
    description: "Request validation failed"
    content:
      application/json:
        schema:
          $ref: "#/components/schemas/Error"
        example:
          error:
            code: "validation_error"
            message: "The 'email' field must be a valid email address"
            details: "email: user@example -> must be a valid email format"
            request_id: "req_abc123"
  "404":
    description: "Resource not found"
    content:
      application/json:
        schema:
          $ref: "#/components/schemas/Error"
        example:
          error:
            code: "not_found"
            message: "Customer with ID 'cus_999' not found"
            request_id: "req_def456"
```

---

### 1.6 Example Design

#### Happy Path Examples

Include `curl` examples and (preferably) code snippets in multiple languages:

```bash
# Create a new customer
curl -X POST https://api.example.com/v2/customers \
  -H "Authorization: Bearer sk_test_..." \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "name": "Alice Johnson",
    "phone": "+1-555-0123"
  }'
```

**Example structure:**

```
## Examples

### Create a customer

Creates a new customer record and returns the created object.

Request:
  POST /v2/customers
  Authorization: Bearer <your-secret-key>
  Content-Type: application/json

  {
    "email": "alice@example.com",
    "name": "Alice Johnson"
  }

Response: 201 Created

  {
    "id": "cus_01H2XYZ...",
    "email": "alice@example.com",
    "name": "Alice Johnson",
    "created_at": "2025-06-05T12:00:00Z"
  }
```

#### Error Case Examples

Always include at least one error example per endpoint:

```
### Create a customer — validation error

Attempting to create a customer with an invalid email address.

Request:
  POST /v2/customers

  {
    "email": "not-an-email",
    "name": "Alice Johnson"
  }

Response: 400 Bad Request

  {
    "error": {
      "code": "validation_error",
      "message": "The 'email' field must be a valid email address",
      "request_id": "req_abc123def456"
    }
  }
```

#### Example Design Rules

1. **Realistic data** — Use names like "Alice Johnson", not "John Doe" or "test"
2. **Realistic IDs** — Use example IDs that look like real IDs (e.g., `cus_01H2XYZ...`)
3. **Show request AND response** — Don't show one without the other
4. **Error examples > success examples** — Developers learn more from errors than from happy paths
5. **Include HTTP headers** — Show Authorization, Content-Type, etc.
6. **Machine-readable and human-readable** — Provide curl snippets alongside JSON
7. **Language SDK examples** — If available, show Python, JavaScript, Ruby, etc.

---

### 1.7 Authentication Documentation Patterns

#### API Key Authentication (Header)

```yaml
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: |
        API key authentication. Obtain your API key from the dashboard.
        
        All API requests must include your API key in the `X-API-Key` header:
        
            X-API-Key: YOUR_API_KEY_HERE
```

**Documentation text pattern:**

```
## Authentication

This API uses API keys for authentication. Include your API key in the
`X-API-Key` header of all requests:

    X-API-Key: YOUR_API_KEY_HERE

Your API key is available in the Dashboard. Keep it secret — do not share
it in client-side code, commit it to version control, or expose it in
browser-accessible contexts.

All API requests must be made over HTTPS. Calls made over plain HTTP will
fail. API requests without authentication will return a 401 error.

Type:        Bearer token transmitted as a custom header
Header name: X-API-Key
Required:    Yes
```

#### Bearer Token / JWT Authentication

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JSON Web Token (JWT) authentication. Obtain a JWT by authenticating
        through the OAuth 2.0 flow (see below).
        
        Include the JWT in the `Authorization` header:
        
            Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Documentation text pattern:**

```
## Authentication

The API uses Bearer tokens (JWT) for authentication. Include the token
in the `Authorization` header of all requests:

    Authorization: Bearer <your-jwt-token>

### Obtaining a Token

1. POST to /v2/auth/login with your credentials
2. The response includes an `access_token`, `refresh_token`, and `expires_in`
3. Use the `access_token` for subsequent requests
4. When the token expires (after `expires_in` seconds), use `refresh_token`
   to obtain a new access token

### Token Structure

Tokens are JSON Web Tokens (JWT) containing:

- `sub`: User or service account ID
- `iat`: Issued-at timestamp
- `exp`: Expiration timestamp
- `scope`: Space-delimited list of granted scopes
```

#### OAuth 2.0 Flows

```yaml
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/oauth/authorize
          tokenUrl: https://auth.example.com/oauth/token
          refreshUrl: https://auth.example.com/oauth/token
          scopes:
            read:   "Read access to customer data"
            write:  "Write access to customer data"
            admin:  "Administrative access"
```

**OAuth flow documentation pattern:**

```
## Authentication — OAuth 2.0

This API uses OAuth 2.0 with the Authorization Code grant type.

### 1. Get authorization

Redirect the user to:

    https://auth.example.com/oauth/authorize
      ?response_type=code
      &client_id={client_id}
      &redirect_uri={redirect_uri}
      &scope=read+write
      &state={random_string}

Parameters:
  client_id     (required) Your application's client ID
  redirect_uri  (required) Where to send the auth code
  scope          (required) Space-delimited scopes
  state          (required) CSRF protection token

### 2. Exchange code for token

    POST https://auth.example.com/oauth/token

    grant_type=authorization_code
    &code={code_from_step_1}
    &redirect_uri={redirect_uri}
    &client_id={client_id}
    &client_secret={client_secret}

Response:
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "rt_abc123def456",
    "scope": "read write"
  }

### 3. Use the access token

    Authorization: Bearer eyJhbGciOi...

### Scopes reference

| Scope   | Description                             |
|---------|-----------------------------------------|
| `read`  | Access to read-only endpoints           |
| `write` | Access to create/update/delete endpoints|
| `admin` | Full administrative access              |
```

#### Documentation for Each OAuth Flow

| OAuth Flow | When to Document | Key Parameters |
|-----------|-----------------|----------------|
| Authorization Code | Server-side apps with confidential clients | `client_id`, `redirect_uri`, `scope`, `state`, `code` |
| Implicit (deprecated) | Legacy public clients (use PKCE instead) | `client_id`, `redirect_uri`, `scope`, `state` |
| Client Credentials | Machine-to-machine / server-to-server | `client_id`, `client_secret` |
| Resource Owner Password (deprecated) | Legacy first-party apps | `username`, `password`, `client_id` |
| PKCE extension | Public clients (mobile, SPA) | `code_challenge`, `code_challenge_method`, `code_verifier` |

#### Combining Auth Methods (AND / OR)

```yaml
# AND: Both must be present
security:
  - ApiKeyAuth: []
    OAuth2: [read]

# OR: Either one suffices
security:
  - OAuth2: [read]
  - ApiKeyAuth: []

# Delete/unauthenticated endpoint
security: []
```

---

### 1.8 OpenAPI/Swagger Specification Patterns

#### Core OpenAPI 3.0 Document Structure

```yaml
openapi: 3.0.3
info:
  title: Example API
  description: |
    Multi-line description using Markdown.
    Supports **bold**, `code`, and [links](https://example.com).
  version: 2.1.0
  contact:
    name: API Support
    email: api@example.com
    url: https://example.com/support
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT
servers:
  - url: https://api.example.com/v2
    description: Production server
  - url: https://staging-api.example.com/v2
    description: Staging server
paths:
  /customers:
    $ref: "./paths/customers.yaml"
  /customers/{id}:
    $ref: "./paths/customers_id.yaml"
components:
  schemas:
    $ref: "./schemas/_index.yaml"
  securitySchemes:
    $ref: "./security.yaml"
  parameters:
    $ref: "./parameters/_index.yaml"
```

#### Annotation Patterns (Code-First)

**Python (FastAPI):**

```python
from fastapi import FastAPI, Query, Path, Body, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Example API",
    version="2.1.0",
    description="API for managing customers and orders",
)


class CreateCustomerRequest(BaseModel):
    email: str = Field(
        ...,  # ellipsis = required
        description="Customer email address",
        max_length=255,
        example="alice@example.com",
    )
    name: str = Field(
        ...,
        description="Customer full name",
        max_length=255,
        example="Alice Johnson",
    )
    phone: str | None = Field(
        None,
        description="Customer phone number (optional)",
        example="+1-555-0123",
    )


class CustomerResponse(BaseModel):
    id: str = Field(..., description="Unique customer identifier")
    email: str = Field(..., description="Customer email address")
    name: str = Field(..., description="Customer full name")
    created_at: str = Field(..., description="ISO 8601 creation timestamp")


@app.post(
    "/customers",
    response_model=CustomerResponse,
    status_code=201,
    summary="Create a new customer",
    description="Creates a customer record and returns the created object.",
    responses={
        400: {"description": "Validation error"},
        401: {"description": "Authentication required"},
        409: {"description": "Customer already exists"},
    },
)
async def create_customer(
    body: CreateCustomerRequest,
    x_api_key: str = Header(..., description="API key"),
):
    """Create a new customer."""
    ...
```

**Java (Spring Boot / SpringDoc):**

```java
@RestController
@RequestMapping("/v2/customers")
@Tag(name = "Customers", description = "Customer management API")
public class CustomerController {

    @PostMapping
    @Operation(
        summary = "Create a new customer",
        description = "Creates a customer record and returns the created object."
    )
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Customer created",
                     content = @Content(schema = @Schema(implementation = CustomerResponse.class))),
        @ApiResponse(responseCode = "400", description = "Validation error"),
        @ApiResponse(responseCode = "401", description = "Authentication required")
    })
    public ResponseEntity<CustomerResponse> createCustomer(
            @Valid @RequestBody @Schema(description = "Customer data") CreateCustomerRequest request,
            @RequestHeader("X-API-Key") @Schema(description = "API key") String apiKey) {
        ...
    }
}
```

**Node.js (Express + swagger-jsdoc / swagger-autogen):**

```javascript
/**
 * @openapi
 * /v2/customers:
 *   post:
 *     summary: Create a new customer
 *     description: Creates a customer record and returns the created object.
 *     tags: [Customers]
 *     security:
 *       - ApiKeyAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/CreateCustomerRequest'
 *     responses:
 *       201:
 *         description: Customer created successfully
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/CustomerResponse'
 *       400:
 *         description: Validation error
 *       401:
 *         description: Authentication required
 */
router.post("/v2/customers", async (req, res) => {
    ...
});
```

#### OpenAPI Design Rules

1. **Contract-first > Code-first** for API design maturity, but code-first via annotations is valid when well-maintained
2. **Use `$ref`** to components — never inline the same schema twice
3. **Use semantic versioning** in the `info.version` field
4. **Document all error responses** — don't skip 4xx/5xx codes
5. **Always include examples** for every schema property and every request/response
6. **Use `nullable: true`** explicitly rather than making fields optional and nullable (they're different)
7. **Mark deprecated fields** with `deprecated: true`
8. **Document rate limits** in the 429 response description
9. **Include `externalDocs`** pointing to detailed documentation
10. **Keep spec files modular** — split paths, schemas, and parameters into separate files for large APIs

---

### 1.9 Doc Generation Workflows

#### Swagger/OpenAPI Toolchain

```
Spec Authoring
  ├── Swagger Editor (browser)         — Visual spec editor with live preview
  ├── Stoplight Studio                 — GUI-based spec editor
  ├── Redocly CLI                      — CLI linting and bundling
  └── hand-written YAML/JSON           — Direct spec authoring

Code-First Generation
  ├── FastAPI (Python)                 — Auto-generates OpenAPI 3.0 from type hints
  ├── SpringDoc (Java)                 — OpenAPI 3.0 from annotations
  ├── swagger-jsdoc (Node.js)          — JSDoc annotations → OpenAPI
  ├── swagger-autogen (Node.js)        — Route introspection → OpenAPI
  ├── drf-spectacular (Django)         — DRF → OpenAPI 3.0
  └── NSwag (.NET)                     — Reflection-based spec generation

Doc Rendering
  ├── Swagger UI                       — Interactive API documentation
  ├── Redoc / Redocly                  — Clean, static API reference pages
  ├── Stoplight Elements               — React-based API doc components
  ├── ReadMe.io                        — Hosted API reference platform
  └── docusaurus-openapi               — OpenAPI plugin for Docusaurus

Code Generation
  ├── OpenAPI Generator                — Server stubs + client SDKs (40+ languages)
  ├── Swagger Codegen                  — Legacy code generator
  └── Kiota (Microsoft)                — SDK generator for OpenAPI

Testing & Validation
  ├── Spectral (Stoplight)             — OpenAPI linting / style rules
  ├── Vacuum (Redocly)                 — OpenAPI linting
  ├── Dredd                            — API spec vs implementation testing
  ├── Schemathesis                     — Property-based testing from OpenAPI spec
  └── Postman / Bruno                  — Manual API testing collections from spec
```

#### Workflow: Contract-First

```
1. Design spec (Swagger Editor / Stoplight / YAML)
2. Validate with Spectral (lint rules)
3. Commit spec to version control
4. CI validates spec on every PR (Spectral + schema validation)
5. CI generates:
   a. Swagger UI / Redoc static site (deploy to docs server)
   b. Server stubs (OpenAPI Generator)
   c. Client SDKs (OpenAPI Generator)
6. Implement server logic against generated stubs
7. Test with Dredd or Schemathesis against spec
8. Publish docs and SDKs
```

#### Workflow: Code-First

```
1. Add annotations/type hints to code
2. Run code-first generator (FastAPI auto, swagger-autogen, etc.)
3. Validate generated spec with Spectral
4. Commit spec alongside code
5. CI validates spec + renders docs
6. Generate clients from spec if needed
```

---

## 2. CLI Help Text Design

### 2.1 Help Text Structure

#### Standard Help Output Layout

```
PROGRAM(1)                 User Commands                 PROGRAM(1)

NAME
    mytool - Brief one-line description

SYNOPSIS
    mytool [options] [command] [arguments]

DESCRIPTION
    Longer description of the tool, what it does, and when to use it.
    Multi-line paragraphs are fine. Use clear, imperative language.

OPTIONS
    -f, --flag ARG      Description of the flag (default: value)
    --long-flag         Description of the long-form flag
    -v, --verbose       Enable verbose output

COMMANDS
    create              Create a new resource
        mytool create [options] <name>
    list                List existing resources
        mytool list [options]
    delete              Delete a resource
        mytool delete [options] <id>

ENVIRONMENT
    MYTOOL_HOME         Configuration directory (default: ~/.mytool)
    MYTOOL_DEBUG        Enable debug logging (default: false)
    NO_COLOR            Disable colored output

EXIT CODES
    0                   Success
    1                   General error
    2                   Invalid usage or parse error

EXAMPLES
    mytool create my-resource --description "A test resource"
    mytool list --format json --limit 10
    mytool delete 12345

SEE ALSO
    mytool-config(1), mytool-daemon(8)

AUTHOR
    Written by the MyTool Team.

BUGS
    Report bugs to https://github.com/example/mytool/issues
```

#### Quick Reference (Default, No Args)

When the user runs the tool with no arguments, show a compact overview:

```
Usage: mytool [OPTIONS] COMMAND [ARGS]...

  MyTool - Resource management for the Example Platform.

Commands:
  create    Create a new resource
  list      List existing resources
  delete    Delete a resource

Options:
  --help          Show this message and exit.
  --version       Show version and exit.
  -v, --verbose   Verbose output

Run 'mytool COMMAND --help' for more info on a command.
```

#### Principles for Help Text (from clig.dev)

1. **Lead with examples** — users scan for patterns they recognize
2. **Use formatting for scannability** — aligned columns, section headers
3. **Suggest corrections** for typos (e.g., "Did you mean `ps`?")
4. **Provide web, terminal, and man page documentation**
5. **Concise by default, extensive with --help**
6. **Show state feedback** (like `git status`)
7. **Show progress for long operations**

---

### 2.2 Usage Line Conventions

#### Standard Usage Line Pattern

```
usage: <program> [<global-options>] <command> [<command-options>] [<args>]
```

**POSIX/GNU conventions:**

| Notation | Meaning |
|----------|---------|
| `[ ]` | Optional item |
| `< >` | Variable / replaceable |
| `{ }` | Required choice |
| `( )` | Grouping |
| `\|` | Separator between choices |
| `...` | Repeatable |
| `-` | Standard input (in place of a filename) |

**Examples:**

```
mytool [options] <filename>
mytool [--force] <source> <destination>
mytool {create|list|delete} [options] [<name>]
mytool [-v | --verbose] <input>... [--output <file>]
mytool <command> [<args>]
```

#### Usage Line First Rule

The usage line should be the **first thing** the user sees when they run `--help` or `-h`. It should fit on one line (≤80 characters if possible).

**Good:**

```
usage: git clone [--template=<template_directory>] [-l] [-s] [--no-hardlinks] [--depth <depth>] <repository> [<directory>]
```

**Bad (needs reformatting):**

```
usage: mytool --config <config-file> --input <input-file> --output <output-file> --format <format> --verbose --debug --retries <n> --timeout <seconds> <name>
```

**Reformatted:**

```
usage: mytool [options] <name>

Options:
  --config <file>     Configuration file
  --input <file>      Input file (required)
  --output <file>     Output file (required)
  --format <fmt>      Output format (default: json)
  ...
```

---

### 2.3 Flag Naming Conventions

#### Standard Conventions

| Convention | Rule | Examples |
|-----------|------|---------|
| Short flags | Single letter, preceded by `-` | `-v`, `-o`, `-f` |
| Long flags | Multi-character, preceded by `--` | `--verbose`, `--output`, `--force` |
| Case | Lowercase for short flags; lowercase with hyphens for long | `--no-color`, `--dry-run` |
| Booleans | Present = true, absent = false | `--verbose` (enables), `--no-verbose` (disables) |
| Negation | Prefix with `no-` for negated booleans | `--no-color`, `--no-cache` |
| Value flags | Flag takes a value; show metavar in help | `--output <file>`, `-o <file>` |
| Repeatable | Documented with `...` in usage | `-I <path>` (multiple include paths) |

#### Common Short Flags and Their Meanings

| Flag | Meaning | Convention Level |
|------|---------|-----------------|
| `-h` | Help | Universal (POSIX/GNU/BSD) |
| `-V` | Version | Common (can conflict with `-v`) |
| `-v` | Verbose | Widespread |
| `-q` | Quiet | Widespread |
| `-o` | Output file | Widespread |
| `-f` | Force / file input | Widespread |
| `-n` | Dry run | Common |
| `-d` | Debug / directory | Common |
| `-r` | Recursive | Common |
| `-t` | Type / tag | Context-dependent |
| `-c` | Config | Common |
| `-D` | Define | Common in build tools |

#### Flag Documentation Template

```
  -f, --flag ARG         Description of what this flag does.
                         Second line if needed. (default: value)
  --no-flag              Disable the flag behavior.
  -v, --verbose          Increase verbosity. Repeat for more: -vvv.
  -q, --quiet            Suppress all output except errors.
      --json             Output in JSON format (implies --quiet).
```

**Rules:**

1. Short flag listed first, then long flag, separated by `, `
2. If the flag takes a value, show its metavar after the flag in angle brackets
3. Description starts with a capital letter, ends with a period
4. Default value shown in parentheses at the end
5. Long-only flags (no short form) indented with extra spaces

---

### 2.4 Subcommand Help Hierarchy

#### Multi-Level Help Pattern

```
# Top-level help
$ mytool --help
Usage: mytool [OPTIONS] COMMAND [ARGS]...

Commands:
  config    Manage configuration
  project   Manage projects
  task      Manage tasks

# Subcommand help
$ mytool project --help
Usage: mytool project [OPTIONS] COMMAND [ARGS]...

Commands:
  create    Create a new project
  list      List projects
  delete    Delete a project

# Sub-subcommand help
$ mytool project create --help
Usage: mytool project create [OPTIONS] <name>

Create a new project in the workspace.

Options:
  --description TEXT   Project description
  --team TEXT          Team to assign the project to
  --public             Make the project publicly visible
  --dry-run            Validate without creating
```

#### Hierarchy Rules

1. Each subcommand shows its **full ancestor chain** in the usage line
2. Each level has its own `--help` output
3. Parent commands show summary of children; children show full flag details
4. Maximum nesting depth: 3 levels recommended (`tool group action`)
5. Each level provides a brief description of what it does

#### Commands Section Layout

```
Commands:
  create    Create a new resource
            More detail about the create command displayed
            on a continuation line or description block.
  list      List existing resources
  delete    Delete a resource

Use 'mytool <command> --help' for more info on a specific command.
```

**Design pattern:**
- Command name left-aligned
- Short description at a consistent tab stop (usually 4+ spaces from the longest command name)
- Multiple subcommands sorted alphabetically

---

### 2.5 Exit Codes

#### Standard Exit Code Convention

| Code | Meaning | When Used |
|------|---------|-----------|
| `0` | Success | Command completed successfully |
| `1` | General error | Catch-all for unspecified failures |
| `2` | Misuse / parse error | Invalid syntax, unknown flag, missing argument |
| `64` | Usage error | Command-line usage error (sysexits.h) |
| `65` | Data format error | Data format error (sysexits.h) |
| `69` | Unavailable | Service/resource temporarily unavailable |
| `70` | Internal software error | Internal error (sysexits.h) |
| `75` | Temporary failure | Temporary OS-level failure |
| `77` | Permission denied | Permission denied (sysexits.h) |
| `78` | Configuration error | Configuration file error (sysexits.h) |
| `126` | Command invoked cannot execute | Permission problem or non-executable |
| `127` | Command not found | Command not found in PATH |
| `128+n` | Signal n | Killed by signal (e.g., 130 = Ctrl+C, SIGINT) |
| `130` | Terminated by Ctrl+C | SIGINT received |
| `255` | Exit status out of range | Error in exit() argument |

#### Exit Code Documentation Pattern

```
EXIT CODES
    Exit codes used by <program>:

    0         Successful completion
    1         General error (see stderr for details)
    2         Invalid usage or command-line parsing error
    64        Invalid input data
    70        Internal software error
    77        Permission denied

    For a complete list of exit codes, see <program>(1) or
    sysexits(3) for the standard BSD exit code convention.
```

**Rule:** Always document exit code 0 (success) and at least the common failure codes (1, 2). If using sysexits.h codes, reference `sysexits(3)`.

---

### 2.6 Environment Variables

#### Documentation Pattern

```
ENVIRONMENT

    <PROGRAM>_HOME
        Directory for program data and configuration files.
        If not set, the default is ~/.<program>. (since v2.0)

    <PROGRAM>_DEBUG
        Set to "1", "true", or "yes" to enable debug logging
        to stderr. Overrides --quiet. (default: unset)

    NO_COLOR
        If set, disable ANSI color escape codes in output.
        See https://no-color.org/ for the standard. (default: unset)

    EDITOR
        The text editor to use for interactive input.
        (default: vi, then nano, then EDITOR from the environment)

    HTTP_PROXY, HTTPS_PROXY, NO_PROXY
        Standard proxy environment variables for network requests.
```

#### Environment Variable Rules

1. **Naming:** `PROGRAMNAME_VARIABLE` — uppercase, underscores, program-specific prefix
2. **Precedence** (highest to lowest): CLI flags > Environment variables > Config file > System default
3. **Document defaults** — every variable's fallback must be stated
4. **Use established standards** — `NO_COLOR`, `EDITOR`, `PAGER`, `HTTP_PROXY`
5. **Don't store secrets in env vars** — use config files with restricted permissions instead
6. **Document the `--help` output** as the authoritative source for env var names

---

### 2.7 Output Format Documentation

#### Human-Readable vs Machine-Readable

```
OUTPUT FORMAT

    By default, output is formatted for human readability.

    --json
        Output in JSON format, suitable for programmatic consumption.
        Implies --quiet (suppresses progress and status messages).

    --yaml
        Output in YAML format (if supported).

    --plain
        Output as plain text with minimal formatting.

    --no-color
        Disable ANSI color codes in terminal output.
        Also respected via the NO_COLOR environment variable.
```

#### Table/List Output Conventions

```
# Tabular output
$ mytool list
ID        NAME            STATUS    CREATED
p_abc123  Alice Project   active    2025-06-01
p_def456  Bob Project     archived  2025-05-15

# --json output
$ mytool list --json
[
  {"id": "p_abc123", "name": "Alice Project", "status": "active", "created": "2025-06-01"},
  {"id": "p_def456", "name": "Bob Project", "status": "archived", "created": "2025-05-15"}
]
```

**Rules for output:**

1. Human-readable = default; machine-readable = opt-in via `--json` or `--format`
2. Tabular output: aligned columns, headers, consistent spacing
3. Use pipe-through-pager for long output (respect `PAGER` env var)
4. Send data to stdout, logs/errors to stderr
5. Show progress bars for long operations (use stderr, not stdout)
6. Confirm destructive actions with a prompt before executing

---

### 2.8 Man Page Structure

#### Standard Man Page Sections (man-pages(7))

| # | Section | Mandatory | Used For |
|---|---------|-----------|----------|
| 1 | NAME | Yes | Title and one-line description |
| 2 | SYNOPSIS | Yes | Usage summary |
| 3 | CONFIGURATION | No | Configuration file format |
| 4 | DESCRIPTION | Yes | Full description of behavior |
| 5 | OPTIONS | Yes (Sections 1, 8) | Command-line flags |
| 6 | EXIT STATUS | Yes | Exit codes |
| 7 | RETURN VALUE | No | Library function return values |
| 8 | ERRORS | No | Error values / errno |
| 9 | ENVIRONMENT | No | Environment variables |
| 10 | FILES | No | Files used by the program |
| 11 | VERSIONS | No | Version compatibility info |
| 12 | STANDARDS | No | Standards conformance |
| 13 | HISTORY | No | Historical notes |
| 14 | NOTES | No | Miscellaneous notes |
| 15 | CAVEATS | No | Warnings / gotchas |
| 16 | BUGS | No | Known issues |
| 17 | EXAMPLES | No | Usage examples |
| 18 | AUTHORS | No | Author credit |
| 19 | REPORTING BUGS | No | Bug reporting info |
| 20 | COPYRIGHT | No | License information |
| 21 | SEE ALSO | No | Cross-references |

#### Groff Man Page Template

```groff
.TH MYTOOL 1 "2025-06-05" "MyTool v2.1" "User Commands"
.SH NAME
mytool \- Manage resources on the Example Platform
.SH SYNOPSIS
\fBmytool\fR [\fIoptions\fR] \fIcommand\fR [\fIargs\fR]
.SH DESCRIPTION
\fBMyTool\fR is a command-line utility for managing resources
on the Example Platform. It supports creating, listing, and
deleting resources in your workspace.
.P
The tool reads configuration from \fImytool.conf\fR(5) if present,
then from environment variables, and finally applies CLI flags
with the highest precedence.
.SH OPTIONS
.TP
\fB\-h\fR, \fB\-\-help\fR
Display this help message and exit.
.TP
\fB\-v\fR, \fB\-\-verbose\fR
Increase verbosity. Repeat for more verbose output (e.g., \-vvv).
.TP
\fB\-\-json\fR
Output in JSON format.
.SH EXIT STATUS
.TP
0
Successful completion.
.TP
1
General error.
.TP
2
Invalid usage or syntax error.
.SH ENVIRONMENT
.TP
\fBMYTOOL_HOME\fR
Configuration directory. Default: \fI~/.mytool\fR.
.TP
\fBNO_COLOR\fR
If set, disables colored output.
.SH FILES
.TP
\fI~/.mytool/mytool.conf\fR
User configuration file.
.SH EXAMPLES
.TP
Create a resource:
\fBmytool create my-resource \-\-description "A test resource"\fR
.TP
List resources in JSON format:
\fBmytool list \-\-json \-\-limit 10\fR
.SH SEE ALSO
.BR mytool.conf (5),
.BR mytool-daemon (8)
.SH AUTHOR
Written by the MyTool Team.
```

#### Man Page Formatting Conventions

| Element | Groff Markup | Rendered |
|---------|-------------|----------|
| Italic (variable) | `\fI...\fR` | `replaceable` |
| Bold (literal) | `\fB...\fR` | **literal** |
| Bold+Italic | `\fB\fI...\fR\fR` | ***combo*** |
| Minus sign | `\-` | `-` (not hyphen) |
| Em-dash | `\\(em` | — |
| Apostrophe | `\\(aq` | ' |
| Caret | `\\(ha` | ^ |
| Tilde | `\\(ti` | ~ |
| Tagged paragraph | `.TP` | Indented definition list |
| Paragraph break | `.P` | Blank line + new paragraph |
| Code block | `.EX` / `.EE` | Example/code block |
| Bullet list | `.IP \\(bu 2` | Bullet point |
| No-fill mode | `.nf` / `.fi` | Preserve line breaks |

---

## 3. Additional Patterns & Standards

### Richardson Maturity Model (RMM)

| Level | Name | Description |
|-------|------|-------------|
| 0 | The Swamp of POX | Single URI, all POST requests |
| 1 | Resources | Separate URIs for different resources |
| 2 | HTTP Verbs | HTTP methods define operations (GET, POST, PUT, DELETE) |
| 3 | Hypermedia (HATEOAS) | Resources contain links to related actions |

### OpenAPI / Swagger File Organization

```
api/
  openapi.yaml          # Root: openapi, info, servers, externalDocs
  paths/
    _index.yaml         # or include in root
    customers.yaml
    customers_id.yaml
    orders.yaml
    orders_id.yaml
  schemas/
    _index.yaml         # Refs to all schemas
    Customer.yaml
    Order.yaml
    Error.yaml
  parameters/
    _index.yaml
    resource_id.yaml
    pagination.yaml
  security.yaml         # securitySchemes definition
  responses.yaml        # Shared response components
```

### CLI Configuration Precedence

```
(Override)  CLI Flags                          # Highest precedence
            Environment Variables
            Project-local Config (.env)
            User Config (~/.config/program/)
            System Config (/etc/program/)
(Default)   Built-in Defaults                  # Lowest precedence
```

### Documentation Linting (Spectral Rules for OpenAPI)

Essential Spectral rules for API documentation quality:

| Rule | Description |
|------|-------------|
| `oas3-valid-schema-example` | Example values must match schema types |
| `oas3-operation-summary` | Every operation must have a summary |
| `oas3-parameter-description` | Every parameter must have a description |
| `operation-description` | Every operation should have a description |
| `operation-tag-defined` | Tags must be defined in the global tags list |
| `no-$ref-siblings` | No sibling keys alongside `$ref` |
| `openapi-tags` | Must have at least one tag |
| `oas3-api-servers` | Must define at least one server URL |

### Key References

| Resource | URL |
|----------|-----|
| OpenAPI 3.0 Specification | https://spec.openapis.org/oas/v3.0.3 |
| Swagger Tools & Docs | https://swagger.io/docs/ |
| CLI Guidelines (clig.dev) | https://clig.dev/ |
| Man Page Conventions (man-pages(7)) | https://man7.org/linux/man-pages/man7/man-pages.7.html |
| POSIX Utility Conventions | https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html |
| GNU Coding Standards | https://www.gnu.org/prep/standards/ |
| Heroku CLI Style Guide | https://devcenter.heroku.com/articles/cli-style-guide |
| Stripe API Reference | https://stripe.com/docs/api |
| GitHub REST API Docs | https://docs.github.com/en/rest |
| Google API Design Guide | https://google.aip.dev/ |
| Microsoft REST API Guidelines | https://github.com/microsoft/api-guidelines |
| OAuth 2.0 (RFC 6749) | https://datatracker.ietf.org/doc/html/rfc6749 |
| JSON Web Token (RFC 7519) | https://datatracker.ietf.org/doc/html/rfc7519 |
| JSON Merge Patch (RFC 7396) | https://datatracker.ietf.org/doc/html/rfc7396 |
| NO_COLOR Standard | https://no-color.org/ |
| sysexits(3) — Exit Codes | https://man.freebsd.org/cgi/man.cgi?query=sysexits |

---

*Document compiled from industry standards: Microsoft Azure Architecture Best Practices, OpenAPI/Swagger Specification, Google Open Source Documentation, clig.dev CLI Design Guide, GNU/Linux man-pages conventions, Python argparse library, Stripe API documentation patterns, GitHub API documentation, and RFC specifications for HTTP, OAuth 2.0, and JWT.*
