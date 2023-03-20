# Basic Fields

"type" : "string",

    - The type of response the server/client was sent.

---

## Client Type Fields
Information from the below fields is concatenated to the string sent by the client depending on the "type" category of the message.

### **"type" : "signin"**

- **POST:**

    - "name":      "username (pennwest email)",
    
    - "pass":      "password (set via signup)".

- **RECIEVE:**
    - headers: 200, OK


### **"type" : "signup_start"**

- **GET:**

    - "isreset": "boolean, from app, whether or not this request is for a password reset",

    - "name":      "string, from user, username (pennwest email)",

- **RECIEVE:**
    - headers: 200, OK


### **"type" : "signup_continue"**

- **POST:**

    - "isreset": "boolean, whether or not this request is for a password reset",

    - "name":      "string, from app, username (pennwest email)",

    - "checksum":  "string, from user, information sent to the user's pennwest email via a verification email".

- **RECIEVE:**
    - headers: 200, OK


### **"type" : "signup_end"**

- **POST:**

    - "isreset": "boolean, from app, whether or not this request is for a password reset",

    - "name":      "string, from app, username (pennwest email)",

    - "password":  "string, the user's chosen password".

- **RECIEVE:**
    - headers: 200, OK
