## SQL

__users__

```
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

__roles__

```
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);
```

__user_roles__

```
CREATE TABLE IF NOT EXISTS user_roles (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);
```

## Implementation

`/login`: to be updated

`/signup`: 

__schemas__: CreateUserRequest, CreateUserResponse

__service__: create_user(CreateUserRequest): CreateUserResponse

__repository__: 

- create_user
- assign_user_role: 
    - first user: admin
    - later: user


