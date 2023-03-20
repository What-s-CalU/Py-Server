# Basic Fields

"type" : "string",

    - The type of response the server/client was sent.

---

## Server Type Fields

### **"type" : "signin"**

- **RECIEVE:**
    - "name", "pass" (see client structures sheet)

- **SEND:**

    - "code": "string, status code for the message (mirrors headers).",
        
        - specific to this field: "bad username, bad password, bad information". 
        
        - "bad password": password field doesn't match the database's password field for that username,

        - "bad username": username field could not be found,

        - "bad information": both fields were invalid/blank.
    
    - "message": "string, error message that conditionally is displayed to the user.",

    - headers: 200, OK


### **"type" : "signup_start"**

- **RECIEVE:**
    - "isReset", "name", (see client structures sheet)

- **SEND:**

    - "code": "string, status code for the message (mirrors headers).",
        
        - specific to this field: "bad username". 
        
        - "bad username": username field mismatches context (found for signup, not found for reset).
    
    - "message": "string, error message that conditionally is displayed to the user.",
    
    - headers: 200, OK


### **"type" : "signup_continue"**

- **POST:**

    - "isreset": "boolean, whether or not this request is for a password reset",

    - "name":      "string, from app, username (pennwest email)",

    - "checksum":  "string, from user, information sent to the user's pennwest email via a verification email".

- **RSEND:**

