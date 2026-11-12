
sample_records = [

    {
        "cheat_sheet": "Authentication",
        "vulnerability": "Weak authentication can allow attackers to access user accounts.",
        "recommended_control": "Use secure authentication, account lockout protections and appropriate authentication policies.",
        "exact_parameter": "Authentication configuration and login attempt limits",
        "owasp_top10_category": "A07:2025 Authentication Failures",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Password Storage",
        "vulnerability": "Storing passwords in plain text or using weak hashing can expose user credentials.",
        "recommended_control": "Store passwords using a strong password hashing algorithm such as Argon2id.",
        "exact_parameter": "Password hashing algorithm and work factor",
        "owasp_top10_category": "A04:2025 Cryptographic Failures",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Session Management",
        "vulnerability": "Poor session management can allow attackers to hijack user sessions.",
        "recommended_control": "Use secure session IDs and regenerate them after authentication.",
        "exact_parameter": "Session ID, cookie Secure, HttpOnly and SameSite attributes",
        "owasp_top10_category": "A07:2025 Authentication Failures",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Forgot Password",
        "vulnerability": "Weak password reset processes can allow unauthorized account access.",
        "recommended_control": "Use random, single-use, time-limited password reset tokens.",
        "exact_parameter": "Reset token expiry and single-use validation",
        "owasp_top10_category": "A07:2025 Authentication Failures",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Multifactor Authentication",
        "vulnerability": "Single-factor authentication increases the risk of account compromise.",
        "recommended_control": "Enable multifactor authentication and protect recovery methods.",
        "exact_parameter": "MFA enrollment, verification and recovery settings",
        "owasp_top10_category": "A07:2025 Authentication Failures",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Cross-Site Request Forgery Prevention",
        "vulnerability": "Attackers may trick authenticated users into submitting unwanted requests.",
        "recommended_control": "Use CSRF tokens and validate request origins where appropriate.",
        "exact_parameter": "CSRF token validation and Origin header",
        "owasp_top10_category": "A01:2025 Broken Access Control",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Cross Site Scripting Prevention",
        "vulnerability": "Untrusted input may execute malicious scripts in a user's browser.",
        "recommended_control": "Use context-aware output encoding and safe DOM methods.",
        "exact_parameter": "Output encoding and HTML sanitization",
        "owasp_top10_category": "A05:2025 Injection",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "SQL Injection Prevention",
        "vulnerability": "Untrusted input may change the meaning of database queries.",
        "recommended_control": "Use parameterized queries or prepared statements.",
        "exact_parameter": "SQL query parameters and prepared statements",
        "owasp_top10_category": "A05:2025 Injection",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Input Validation",
        "vulnerability": "Invalid or malicious input may cause unexpected application behavior.",
        "recommended_control": "Validate input using allowlists, data types and length limits.",
        "exact_parameter": "Input type, allowed characters and maximum length",
        "owasp_top10_category": "A05:2025 Injection",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "File Upload",
        "vulnerability": "Unsafe file uploads may introduce malicious files or allow unauthorized access.",
        "recommended_control": "Validate file types, file size, file signatures and storage location.",
        "exact_parameter": "Allowed extensions, MIME type, file signature and maximum file size",
        "owasp_top10_category": "A04:2025 Cryptographic Failures",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Logging",
        "vulnerability": "Missing security logs can make suspicious activities difficult to detect.",
        "recommended_control": "Record security events and protect logs against unauthorized access or modification.",
        "exact_parameter": "Authentication events, access failures and log retention settings",
        "owasp_top10_category": "A09:2025 Security Logging and Alerting Failures",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Error Handling",
        "vulnerability": "Detailed error messages may expose sensitive application information.",
        "recommended_control": "Show generic errors to users and keep technical details in secure logs.",
        "exact_parameter": "Error response details and exception logging",
        "owasp_top10_category": "A10:2025 Mishandling of Exceptional Conditions",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html",
    },

    {
        "cheat_sheet": "HTTP Headers",
        "vulnerability": "Missing security headers can expose applications to browser-based attacks.",
        "recommended_control": "Configure appropriate HTTP security response headers.",
        "exact_parameter": "X-Content-Type-Options and Referrer-Policy",
        "owasp_top10_category": "A02:2025 Security Misconfiguration",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Content Security Policy",
        "vulnerability": "Malicious scripts may execute in the browser if content sources are unrestricted.",
        "recommended_control": "Configure a restrictive Content Security Policy.",
        "exact_parameter": "Content-Security-Policy: default-src 'self'",
        "owasp_top10_category": "A05:2025 Injection",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Secrets Management",
        "vulnerability": "Exposed API keys and passwords can allow unauthorized access.",
        "recommended_control": "Store secrets in secure secret management systems and rotate them regularly.",
        "exact_parameter": "Secret storage, access permissions and rotation interval",
        "owasp_top10_category": "A02:2025 Security Misconfiguration",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html",
    },

    {
        "cheat_sheet": "REST Security",
        "vulnerability": "Insecure REST APIs may expose sensitive data or allow unauthorized requests.",
        "recommended_control": "Use authentication, authorization, HTTPS and input validation.",
        "exact_parameter": "Authorization header and API access controls",
        "owasp_top10_category": "A01:2025 Broken Access Control",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Authorization",
        "vulnerability": "Incorrect access permissions may allow users to access other users' data.",
        "recommended_control": "Enforce server-side authorization checks for every protected resource.",
        "exact_parameter": "Role permissions and resource-level access checks",
        "owasp_top10_category": "A01:2025 Broken Access Control",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html",
    },

    {
        "cheat_sheet": "Transport Layer Security",
        "vulnerability": "Unencrypted communication may expose sensitive information.",
        "recommended_control": "Use modern TLS configurations and disable insecure protocols.",
        "exact_parameter": "Minimum TLS version: TLS 1.2",
        "owasp_top10_category": "A04:2025 Cryptographic Failures",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html"
    },

    {
        "cheat_sheet": "Unvalidated Redirects and Forwards",
        "vulnerability": "Attackers may redirect users to malicious websites.",
        "recommended_control": "Validate redirect destinations using an allowlist.",
        "exact_parameter": "Allowed redirect destination URLs",
        "owasp_top10_category": "A01:2025 Broken Access Control",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html",
    },

    {
        "cheat_sheet": "Server Side Request Forgery Prevention",
        "vulnerability": "Attackers may trick servers into sending requests to internal or restricted resources.",
        "recommended_control": "Validate destination addresses and restrict outbound network requests.",
        "exact_parameter": "Allowed destination hosts, IP addresses and URL schemes",
        "owasp_top10_category": "A01:2025 Broken Access Control",
        "source_url": "https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html"
    }

]
