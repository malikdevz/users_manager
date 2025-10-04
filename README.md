````markdown
# 📘 GraphQL API – User Account Management

This document describes all available **queries** and **mutations** in the GraphQL API.  
Each example is provided in **JSON format**, compatible with **Postman**, **Insomnia**, or **GraphiQL**.

---

## 🔐 JWT Authentication

### 1. Get a Token

```json
{
  "query": "mutation { tokenAuth(username: \"USER_IDENTIFIER\", password: \"PASSWORD\") { token } }"
}
````

### 2. Refresh a Token

```json
{
  "query": "mutation { refreshToken(token: \"CURRENT_TOKEN\") { token } }"
}
```

### 3. Verify a Token

```json
{
  "query": "mutation { verifyToken(token: \"TOKEN\") { payload } }"
}
```

---

## 🧾 QUERIES

### 1. Get Your Own Account

```json
{
  "query": "query { account { userIdentifier firstName email role city country phone isVerified } }"
}
```

**Expected Result:**

```json
{
  "data": {
    "account": {
      "userIdentifier": "USR12345",
      "firstName": "David",
      "email": "david@example.com",
      "role": "STUDENT",
      "city": "Goma",
      "country": "DRC",
      "phone": "+243970000000",
      "isVerified": false
    }
  }
}
```

**Possible Errors:**

* `INVALID_USER_IDENTIFIER`
* `Authentication credentials were not provided.`

---

### 2. Get All Accounts (Admin Only)

```json
{
  "query": "query { allAccounts { userIdentifier firstName email role } }"
}
```

**Expected Result:**

```json
{
  "data": {
    "allAccounts": [
      {
        "userIdentifier": "USR11111",
        "firstName": "Alice",
        "email": "alice@example.com",
        "role": "STUDENT"
      },
      {
        "userIdentifier": "USR22222",
        "firstName": "Bob",
        "email": "bob@example.com",
        "role": "TEACHER"
      }
    ]
  }
}
```

---

### 3. Get an Account by Identifier

```json
{
  "query": "query { accountByIdentifier(userIdentifier: \"USR12345\") { firstName email role } }"
}
```

**Expected Result:**

```json
{
  "data": {
    "accountByIdentifier": {
      "firstName": "David",
      "email": "david@example.com",
      "role": "STUDENT"
    }
  }
}
```

**Possible Error:**

* `ACCOUNT_DOESNT_EXIST`

---

## ⚙️ MUTATIONS

### 1. Create an Account

```json
{
  "query": "mutation { createAccount(firstName: \"David\", sex: \"M\", dateOfBirth: \"1998-04-21\", password: \"StrongP@ss123\", role: \"STUDENT\", email: \"david@example.com\", city: \"Goma\", country: \"DRC\", phone: \"+243970000000\") { account { userIdentifier firstName role email isVerified } } }"
}
```

**Expected Result:**

```json
{
  "data": {
    "createAccount": {
      "account": {
        "userIdentifier": "USR87956",
        "firstName": "David",
        "role": "STUDENT",
        "email": "david@example.com",
        "isVerified": false
      }
    }
  }
}
```

**Possible Errors:**

* `EMAIL_REQUIRED`
* `PHONE_REQUIRED`
* `CITY_REQUIRED`
* `COUNTRY_REQUIRED`
* `EMAIL_ALREADY_TAKEN`
* `INVALID_EMAIL`
* `WEAK_PASSWORD`

---

### 2. Update Your Profile

```json
{
  "query": "mutation { updateAccount(firstName: \"David\", email: \"newmail@example.com\", city: \"Kinshasa\") { account { firstName email city } } }"
}
```

**Expected Result:**

```json
{
  "data": {
    "updateAccount": {
      "account": {
        "firstName": "David",
        "email": "newmail@example.com",
        "city": "Kinshasa"
      }
    }
  }
}
```

**Possible Errors:**

* `USER_ACCOUNT_NOT_EXIST`
* `INVALID_EMAIL`

---

### 3. Verify an Account

```json
{
  "query": "mutation { verifyAccount(codeVerif: \"ABCD1234\") { isVerified } }"
}
```

**Expected Result:**

```json
{ "data": { "verifyAccount": { "isVerified": true } } }
```

**Possible Errors:**

* `CODE_INVALID`
* `CODE_EXPIRED`

---

### 4. Request a Verification Code

```json
{
  "query": "mutation { requestCode(emailTitle: \"Account Verification\") { isCodeSent } }"
}
```

**Expected Result:**

```json
{ "data": { "requestCode": { "isCodeSent": true } } }
```

---

### 5. Change Your Password

```json
{
  "query": "mutation { changePassword(oldPassword: \"OldPass123!\", newPassword: \"NewP@ss456\") { isPwdChanged } }"
}
```

**Expected Result:**

```json
{ "data": { "changePassword": { "isPwdChanged": true } } }
```

**Possible Error:**

* `WRONG_CURRENT_PASSWORD`

---

### 6. Reset Your Password

```json
{
  "query": "mutation { resetPassword(username: \"USR12345\", code: \"VERIF1234\", newPassword: \"NewP@ss789\") { isPwdReset } }"
}
```

**Expected Result:**

```json
{ "data": { "resetPassword": { "isPwdReset": true } } }
```

**Possible Errors:**

* `USERNAME_DOESNT_EXIST`
* `CODE_INVALID`
* `CODE_EXPIRED`

---

### 7. Delete Your Own Account

```json
{
  "query": "mutation { deleteAccount(userPassword: \"MyPassword123\") { isDeleted } }"
}
```

**Expected Result:**

```json
{ "data": { "deleteAccount": { "isDeleted": true } } }
```

**Possible Errors:**

* `WRONG_PASSWORD`
* `DELETE_ACCOUNT_ERROR`

---

### 8. Delete an Account as Admin

```json
{
  "query": "mutation { adminDeleteAccount(accIdentifier: \"USR12345\", adminPassword: \"AdminPass123\") { isDeleted } }"
}
```

**Expected Result:**

```json
{ "data": { "adminDeleteAccount": { "isDeleted": true } } }
```

**Possible Errors:**

* `WRONG_PASSWORD`
* `OPERATION_DENIED`
* `ACCOUNT_DOESNT_EXIST`

---

## 🧠 Technical Notes

* All protected queries require a **JWT header**:

  ```
  Authorization: JWT <your_token>
  ```
* Identifiers (`userIdentifier`) are generated automatically.
* Field validation is handled via functions in the `tools.py` module.

---

## 🧾 Common Error Codes

| Code                      | Description                  |
| ------------------------- | ---------------------------- |
| `INVALID_USER_IDENTIFIER` | Profile not found            |
| `ACCOUNT_DOESNT_EXIST`    | Account does not exist       |
| `EMAIL_REQUIRED`          | Email required for teacher   |
| `PHONE_REQUIRED`          | Phone required for teacher   |
| `CITY_REQUIRED`           | City required for teacher    |
| `COUNTRY_REQUIRED`        | Country required for teacher |
| `EMAIL_ALREADY_TAKEN`     | Email already used           |
| `USER_ACCOUNT_NOT_EXIST`  | Profile not found            |
| `WRONG_CURRENT_PASSWORD`  | Wrong current password       |
| `WRONG_PASSWORD`          | Incorrect password           |
| `DELETE_ACCOUNT_ERROR`    | Error deleting account       |
| `CODE_INVALID`            | Invalid verification code    |
| `CODE_EXPIRED`            | Verification code expired    |
| `OPERATION_DENIED`        | Action denied (not admin)    |

---

## 🧰 Technologies

* **Graphene-Django**
* **Django ORM**
* **JWT Authentication**
* **Custom validators (tools.py)**

---

© 2025 – User API | Built with ❤️ and GraphQL.

```
```
