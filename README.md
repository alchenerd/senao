# Container User Guide

## Pull Docker Image

```
docker pull alchenerd/senao-app
```

## Build Docker Image

```
docker build -t alchenerd/senao-app .
```

## Run Docker Image

```
# With .env file that has `DATABASE_URL`
docker run -p 8000:8000 --env-file .env -v ./data:/app/data alchenerd/senao-app

# Without .env file; default DB URL is 'sqlite:///./data/senao.db'
docker run -p 8000:8000 -v ./data:/app/data alchenerd/senao-app
```

After starting the container, visit http://localhost:8000/docs to verify.

---

# API Tutorial

## Account Creation

Creates an account.

- endpoint: /accounts
- method: POST
- json payload schema: {"username": str, "password": str}

### Sample Request

```
curl -X 'POST' \
'http://localhost:8000/accounts' \
-H 'accept: application/json' \
-H 'Content-type: application/json' \
-d '{
"username": "root",
"password": "Password123"
}'
```

### Sample Reply

#### 201 Created
```
{
  "success": true,
  "reason": "Account `root` created"
}
```

#### 409 Conflict
```
{
  "success": false,
  "reason": "Username `root` already exists"
}
```

#### 422 Unprocessable Entity
```
{
  "success": false,
  "reason": "Username too short, minimum 3 characters"
}
```


## Account Validation

Validates an account (username, password).

- endpoint: /accounts/validate/
- method: POST
- json payload schema: {"username": str, "password": str}

### Sample Request

```
curl -X 'POST' \
'http://localhost:8000/accounts/validate/' \
-H 'accept: application/json' \
-H 'Content-type: application/json' \
-d '{
"username": "root",
"password": "Password123"
}'
```

### Sample Replies

#### 200 OK
```
{
  "success": true,
  "reason": "Validation success"
}
```

#### 401 Unauthorized
```
{
  "success": false,
  "reason": "Incorrect username or password"
}
```

#### 429 Too Many Requests
```
{
  "success": false,
  "reason": "Too many login attempts since 2024-08-27 06:28:47.488741"
}
```
