# Permissions & Groups Setup

## Custom Permissions
Added inside Book model:
- can_view
- can_create
- can_edit
- can_delete

## Groups
Created in Django Admin:
- Viewers → can_view
- Editors → can_view, can_create, can_edit
- Admins → all permissions

## Protected Views
book_list      → requires can_view  
create_book    → requires can_create  
edit_book      → requires can_edit

HTTPS & Security Configuration Documentation

This application has been configured to enforce secure HTTPS communication and protect user data using industry-recommended security settings.

1. HTTPS Enforcement

SECURE_SSL_REDIRECT = True forces all HTTP requests to be redirected to HTTPS.

HTTP Strict Transport Security (HSTS) is enabled for one year:

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

2. Secure Cookies

SESSION_COOKIE_SECURE = True ensures session cookies are only sent over HTTPS.

CSRF_COOKIE_SECURE = True ensures the CSRF cookie is also HTTPS-only.

3. Browser Security Headers

X_FRAME_OPTIONS = "DENY" protects against clickjacking.

SECURE_CONTENT_TYPE_NOSNIFF = True prevents MIME-sniffing.

SECURE_BROWSER_XSS_FILTER = True adds an extra layer of XSS protection.

4. Deployment Security

HTTPS is enabled on the deployment server using an SSL/TLS certificate and additional security headers (Nginx/Apache configuration included above).

5. Conclusion

These settings ensure:

Encrypted data transmission

Protection from common web attacks (XSS, clickjacking, MIME-sniffing)

Strong browser enforcement of HTTPS

Secure storage of session and CSRF cookies
