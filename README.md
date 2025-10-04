````markdown
# 📘 API GraphQL – Gestion des Comptes Utilisateurs

Ce document décrit toutes les **requêtes** et **mutations** disponibles dans l’API GraphQL.  
Chaque exemple est donné au **format JSON** compatible avec **Postman**, **Insomnia** ou **GraphiQL**.

---

## 🔐 Authentification JWT

### 1. Obtenir un token
```json
{
  "query": "mutation { tokenAuth(username: \"USER_IDENTIFIANT\", password: \"PASSWORD\") { token } }"
}
````

### 2. Rafraîchir un token

```json
{
  "query": "mutation { refreshToken(token: \"TOKEN_ACTUEL\") { token } }"
}
```

### 3. Vérifier un token

```json
{
  "query": "mutation { verifyToken(token: \"TOKEN\") { payload } }"
}
```

---

## 🧾 QUERIES

### 1. Récupérer son propre compte

```json
{
  "query": "query { account { userIdentifier firstName email role city country phone isVerified } }"
}
```

**Résultat attendu :**

```json
{
  "data": {
    "account": {
      "userIdentifier": "USR12345",
      "firstName": "David",
      "email": "david@example.com",
      "role": "STUDENT",
      "city": "Goma",
      "country": "RDC",
      "phone": "+243970000000",
      "isVerified": false
    }
  }
}
```

**Erreurs possibles :**

* `INVALID_USER_IDENTIFIANT`
* `Authentication credentials were not provided.`

---

### 2. Récupérer tous les comptes (admin uniquement)

```json
{
  "query": "query { allAccounts { userIdentifier firstName email role } }"
}
```

**Résultat attendu :**

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

### 3. Récupérer un compte par identifiant

```json
{
  "query": "query { accountByIdentifiant(userIdentifiant: \"USR12345\") { firstName email role } }"
}
```

**Résultat attendu :**

```json
{
  "data": {
    "accountByIdentifiant": {
      "firstName": "David",
      "email": "david@example.com",
      "role": "STUDENT"
    }
  }
}
```

**Erreur possible :**

* `ACCOUNT_DOESNT_EXIST`

---

## ⚙️ MUTATIONS

### 1. Créer un compte

```json
{
  "query": "mutation { createAccount(firstName: \"David\", sex: \"M\", dateOfBirth: \"1998-04-21\", password: \"StrongP@ss123\", role: \"STUDENT\", email: \"david@example.com\", city: \"Goma\", country: \"RDC\", phone: \"+243970000000\") { account { userIdentifier firstName role email isVerified } } }"
}
```

**Résultat attendu :**

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

**Erreurs possibles :**

* `EMAIL_REQUIRED`
* `PHONE_REQUIRED`
* `CITY_REQUIRED`
* `COUNTRY_REQUIRED`
* `EMAIL_ALREAD_TEKEN`
* `INVALID_EMAIL`
* `WEAK_PASSWORD`

---

### 2. Mettre à jour son profil

```json
{
  "query": "mutation { updateAccount(firstName: \"David\", email: \"newmail@example.com\", city: \"Kinshasa\") { account { firstName email city } } }"
}
```

**Résultat attendu :**

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

**Erreurs possibles :**

* `USER_ACCOUNT_NOT_EXIST`
* `INVALID_EMAIL`

---

### 3. Vérifier un compte

```json
{
  "query": "mutation { verifyAccount(codeVerif: \"ABCD1234\") { isVerified } }"
}
```

**Résultat attendu :**

```json
{ "data": { "verifyAccount": { "isVerified": true } } }
```

**Erreurs possibles :**

* `CODE_INVALID`
* `CODE_EXPIRED`

---

### 4. Demander un code de vérification

```json
{
  "query": "mutation { requestCode(emailTitle: \"Vérification de compte\") { isCodeSent } }"
}
```

**Résultat attendu :**

```json
{ "data": { "requestCode": { "isCodeSent": true } } }
```

---

### 5. Changer son mot de passe

```json
{
  "query": "mutation { changePassword(oldPassword: \"OldPass123!\", newPassword: \"NewP@ss456\") { isPwdChanged } }"
}
```

**Résultat attendu :**

```json
{ "data": { "changePassword": { "isPwdChanged": true } } }
```

**Erreur possible :**

* `WRONG_CURRENT_PASSWORD`

---

### 6. Réinitialiser son mot de passe

```json
{
  "query": "mutation { resetPassword(username: \"USR12345\", code: \"VERIF1234\", newPassword: \"NewP@ss789\") { isPwdReset } }"
}
```

**Résultat attendu :**

```json
{ "data": { "resetPassword": { "isPwdReset": true } } }
```

**Erreurs possibles :**

* `USERNAME_DOESNT_EXIST`
* `CODE_INVALID`
* `CODE_EXPIRED`

---

### 7. Supprimer son propre compte

```json
{
  "query": "mutation { deleteAccount(userPassword: \"MyPassword123\") { isDeleted } }"
}
```

**Résultat attendu :**

```json
{ "data": { "deleteAccount": { "isDeleted": true } } }
```

**Erreurs possibles :**

* `WRONG_PASSWORD`
* `DELETE_ACCOUNT_ERROR`

---

### 8. Supprimer un compte en tant qu’admin

```json
{
  "query": "mutation { adminDeleteAccount(accIdentifiant: \"USR12345\", adminPassword: \"AdminPass123\") { isDeleted } }"
}
```

**Résultat attendu :**

```json
{ "data": { "adminDeleteAccount": { "isDeleted": true } } }
```

**Erreurs possibles :**

* `WRONG_PASSWORD`
* `OPERATION_DENIED`
* `ACCOUNT_DOESNT_EXIST`

---

## 🧠 Notes techniques

* Toutes les requêtes protégées nécessitent un **header JWT** :

  ```
  Authorization: JWT <votre_token>
  ```
* Les identifiants (`userIdentifier`) sont générés automatiquement.
* Les validations des champs se font via les fonctions du module `tools.py`.

---

## 🧾 Codes d’erreur communs

| Code                       | Description                           |
| -------------------------- | ------------------------------------- |
| `INVALID_USER_IDENTIFIANT` | Profil introuvable                    |
| `ACCOUNT_DOESNT_EXIST`     | Compte inexistant                     |
| `EMAIL_REQUIRED`           | Email obligatoire pour enseignant     |
| `PHONE_REQUIRED`           | Téléphone obligatoire pour enseignant |
| `CITY_REQUIRED`            | Ville obligatoire pour enseignant     |
| `COUNTRY_REQUIRED`         | Pays obligatoire pour enseignant      |
| `EMAIL_ALREAD_TEKEN`       | Email déjà utilisé                    |
| `USER_ACCOUNT_NOT_EXIST`   | Profil non trouvé                     |
| `WRONG_CURRENT_PASSWORD`   | Ancien mot de passe incorrect         |
| `WRONG_PASSWORD`           | Mot de passe erroné                   |
| `DELETE_ACCOUNT_ERROR`     | Erreur lors de la suppression         |
| `CODE_INVALID`             | Code de vérification invalide         |
| `CODE_EXPIRED`             | Code expiré                           |
| `OPERATION_DENIED`         | Action refusée (non admin)            |

---

## 🧰 Technologies

* **Graphene-Django**
* **Django ORM**
* **JWT Authentication**
* **Custom validators (tools.py)**

---

© 2025 – API Utilisateurs | Développé avec ❤️ et GraphQL.

```
```
