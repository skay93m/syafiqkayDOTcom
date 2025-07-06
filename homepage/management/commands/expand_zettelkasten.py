from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from noto_garden.models import Note, Tag
import datetime
import time
import random


class Command(BaseCommand):
    help = 'Expand the Zettelkasten with additional interconnected notes'

    def handle(self, *args, **options):
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('No user found'))
            return

        # Get existing tags
        existing_tags = {tag.name: tag for tag in Tag.objects.all()}

        def create_tag_if_needed(tag_name):
            if tag_name not in existing_tags:
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
                         '#DDA0DD', '#98D8C8', '#FFB6C1', '#F39C12', '#E74C3C', 
                         '#3498DB', '#2ECC71', '#F1C40F', '#E67E22', '#9B59B6']
                tag = Tag.objects.create(name=tag_name, color=random.choice(colors))
                existing_tags[tag_name] = tag
                return tag
            return existing_tags[tag_name]

        def create_note(title, content, tag_names=None):
            # Generate unique ID
            now = datetime.datetime.now()
            timestamp = now.strftime('%Y%m%d%H%M%S')
            microseconds = str(now.microsecond).zfill(6)
            random_suffix = str(random.randint(100, 999))
            unique_id = timestamp + microseconds[:3] + random_suffix
            
            # Ensure uniqueness
            while Note.objects.filter(unique_id=unique_id).exists():
                time.sleep(0.01)
                now = datetime.datetime.now()
                timestamp = now.strftime('%Y%m%d%H%M%S')
                microseconds = str(now.microsecond).zfill(6)
                random_suffix = str(random.randint(100, 999))
                unique_id = timestamp + microseconds[:3] + random_suffix

            note = Note.objects.create(
                title=title,
                content=content,
                unique_id=unique_id,
                author=user
            )

            if tag_names:
                note_tags = [create_tag_if_needed(tag_name) for tag_name in tag_names]
                note.tags.set(note_tags)

            return note

        # Additional expansion notes
        expansion_notes = [
            {
                'title': 'Identity and Access Management (IAM)',
                'content': '''IAM is the foundational discipline for managing digital identities and controlling access to resources.

## Core Components:
### Identity Management
- **User Identity Lifecycle** - Creation, modification, deletion
- **Identity Repositories** - Active Directory, LDAP, cloud directories
- **Identity Federation** - Connecting multiple identity systems
- **Identity Governance** - Policies, compliance, audit trails

### Access Management
- **Authentication** - Verifying user identity
- **Authorization** - Granting appropriate permissions
- **Session Management** - Controlling user sessions
- **Single Sign-On (SSO)** - Unified access experience

## Modern IAM Challenges:
- **Hybrid Environments** - On-premises + cloud resources
- **Mobile and Remote Access** - BYOD and remote workforce
- **API Economy** - Service-to-service authentication
- **Regulatory Compliance** - GDPR, HIPAA, SOX requirements

## Cloud IAM Evolution:
Traditional IAM focused on perimeter security, but modern cloud IAM emphasizes:
- **Identity as the New Perimeter** - User and device identity matters more than network location
- **Contextual Access** - Dynamic decisions based on risk factors
- **Least Privilege** - Minimal access rights for required functionality
- **Continuous Monitoring** - Real-time threat detection and response

## Best Practices:
- Regular access reviews and certifications
- Automated provisioning and deprovisioning
- Strong password policies and MFA enforcement
- Privileged access management (PAM)
- Comprehensive audit logging and monitoring

IAM platforms like Microsoft Entra ID provide comprehensive solutions that integrate with Authentication Methods, Zero Trust Architecture, and Conditional Access policies.

**Connected Concepts**: [[20250706180204]], [[Authentication Methods]], [[Zero Trust Security]], [[Conditional Access]], [[Privileged Access Management]]''',
                'tags': ['iam', 'identity', 'access-management', 'security', 'governance', 'authentication']
            },
            {
                'title': 'Security Information and Event Management (SIEM)',
                'content': '''SIEM provides centralized security monitoring and incident response capabilities across the entire IT infrastructure.

## Core Functions:
### Data Collection and Aggregation
- **Log Collection** - Network devices, servers, applications, security tools
- **Event Normalization** - Standardizing different log formats
- **Data Correlation** - Linking related events across systems
- **Real-time Processing** - Immediate threat detection

### Analytics and Detection
- **Rule-based Detection** - Predefined security patterns
- **Behavior Analytics** - Anomaly detection using machine learning
- **Threat Intelligence** - Integration with external threat feeds
- **Risk Scoring** - Prioritizing security events

### Response and Reporting
- **Incident Management** - Workflow automation and case tracking
- **Forensics Support** - Detailed investigation capabilities
- **Compliance Reporting** - Regulatory and audit requirements
- **Dashboards and Alerting** - Visual monitoring and notifications

## Modern SIEM Evolution:
### Traditional SIEM Limitations:
- High maintenance overhead
- False positive fatigue
- Limited cloud visibility
- Scaling challenges

### Next-Generation SIEM:
- **Cloud-native Architecture** - Scalable, elastic infrastructure
- **AI/ML Integration** - Advanced threat detection
- **Extended Detection and Response (XDR)** - Broader visibility
- **Security Orchestration** - Automated response workflows

## Integration with Identity Security:
SIEM platforms monitor identity-related events:
- Failed authentication attempts
- Privilege escalation activities
- Unusual access patterns
- Account compromises

## Cloud SIEM Benefits:
- **Reduced Infrastructure Costs** - No on-premises hardware
- **Faster Deployment** - Quick setup and configuration
- **Automatic Updates** - Latest threat detection capabilities
- **Global Threat Intelligence** - Cloud-based threat feeds

## Implementation Considerations:
- **Data Sources** - Comprehensive log collection strategy
- **Use Cases** - Specific security scenarios to monitor
- **Retention Policies** - Balancing storage costs with investigation needs
- **Skills and Training** - SOC analyst capabilities

SIEM solutions complement IAM systems by providing visibility into authentication and access events, supporting Zero Trust Architecture monitoring.

**Connected Concepts**: [[Identity and Access Management]], [[Zero Trust Security]], [[Incident Response]], [[Threat Intelligence]], [[Security Operations]]''',
                'tags': ['siem', 'security', 'monitoring', 'incident-response', 'analytics', 'threat-detection']
            },
            {
                'title': 'Privileged Access Management (PAM)',
                'content': '''PAM protects organizations from the risks associated with privileged accounts through specialized security controls and monitoring.

## Why PAM Matters:
Privileged accounts are prime targets for attackers because they provide:
- **Administrative Access** - Full control over systems
- **Lateral Movement** - Ability to access multiple systems
- **Data Exfiltration** - Access to sensitive information
- **Persistent Access** - Long-term system control

## Core PAM Components:
### Privileged Account Discovery
- **Asset Inventory** - Identifying all privileged accounts
- **Account Classification** - Categorizing by risk level
- **Orphaned Account Detection** - Finding forgotten accounts
- **Shadow IT Discovery** - Uncovering hidden privileged access

### Access Control and Vaulting
- **Password Vaulting** - Secure storage of privileged credentials
- **Check-in/Check-out** - Temporary credential access
- **Automatic Rotation** - Regular password changes
- **Just-in-Time Access** - Temporary privilege elevation

### Session Management
- **Session Recording** - Complete audit trail of privileged sessions
- **Session Monitoring** - Real-time oversight of privileged activities
- **Session Termination** - Automatic session cutoff
- **Keystroke Logging** - Detailed activity tracking

### Privileged Analytics
- **Behavior Analysis** - Detecting unusual privileged activities
- **Risk Scoring** - Assessing privileged session risk
- **Compliance Reporting** - Regulatory audit support
- **Threat Detection** - Identifying potential compromises

## Implementation Models:
### Traditional PAM
- **On-premises deployment** - Full organizational control
- **Hardware-based vaults** - Dedicated security appliances
- **Manual workflows** - Administrator-managed processes

### Cloud PAM
- **SaaS solutions** - Reduced management overhead
- **API integrations** - Automated workflows
- **Elastic scaling** - Growing with organizational needs
- **Global accessibility** - Remote workforce support

## PAM Best Practices:
- **Principle of Least Privilege** - Minimal necessary access
- **Regular Access Reviews** - Periodic privilege validation
- **Multi-factor Authentication** - Strong privileged account protection
- **Segregation of Duties** - Preventing single points of failure
- **Emergency Access Procedures** - Break-glass scenarios

## Integration with Identity Ecosystem:
PAM works alongside IAM systems to provide comprehensive identity security:
- **Identity Lifecycle Management** - Automated provisioning/deprovisioning
- **Role-based Access Control** - Privilege assignment based on roles
- **Conditional Access** - Risk-based privileged access decisions
- **Zero Trust Architecture** - Continuous privileged access validation

PAM solutions integrate with Microsoft Entra ID and other identity platforms to provide unified privileged access governance.

**Connected Concepts**: [[Identity and Access Management]], [[Zero Trust Security]], [[Conditional Access]], [[Authentication Methods]], [[Security Operations]]''',
                'tags': ['pam', 'privileged-access', 'security', 'governance', 'credentials', 'monitoring']
            },
            {
                'title': 'OpenID Connect (OIDC)',
                'content': '''OpenID Connect extends OAuth 2.0 to provide authentication capabilities, enabling secure identity verification for modern applications.

## The Identity Layer:
While OAuth 2.0 handles authorization, OIDC adds authentication by:
- **Identity Verification** - Confirming user identity
- **Standardized Claims** - Consistent user information format
- **Secure Token Exchange** - Cryptographically signed identity tokens
- **Interoperability** - Standard protocol across platforms

## Core Components:
### ID Tokens
- **JWT Format** - JSON Web Token structure
- **Signed Claims** - Cryptographically verified user information
- **Standard Claims** - sub, iss, aud, exp, iat, auth_time
- **Custom Claims** - Application-specific user attributes

### OIDC Flows:
#### Authorization Code Flow
Most secure for server-side applications:
1. User authentication at identity provider
2. Authorization code returned to application
3. Application exchanges code for tokens
4. ID token provides user identity information

#### Implicit Flow (Legacy)
Previously used for browser-based applications:
- ID token returned directly to browser
- No server-side component required
- Now deprecated in favor of Authorization Code + PKCE

#### Hybrid Flow
Combines authorization code and implicit flows:
- Some tokens returned immediately
- Others exchanged via back-channel
- Useful for complex application architectures

## Key Endpoints:
### Discovery Endpoint
Provides OIDC provider configuration:
- Authorization endpoint URL
- Token endpoint URL
- Supported scopes and claims
- Signing algorithms and keys

### UserInfo Endpoint
Returns authenticated user information:
- Protected by access token
- Additional claims beyond ID token
- RESTful API for user attributes

### JWKS Endpoint
Provides public keys for token verification:
- JSON Web Key Set format
- Regular key rotation support
- Cryptographic signature validation

## Security Features:
### Token Validation
- **Signature Verification** - Cryptographic integrity
- **Audience Validation** - Token intended recipient
- **Issuer Validation** - Token source verification
- **Expiration Checking** - Time-based validity

### Additional Security Measures:
- **Nonce Parameter** - Replay attack prevention
- **State Parameter** - CSRF protection
- **PKCE Extension** - Authorization code interception prevention
- **Token Binding** - Token-to-session cryptographic binding

## Common Use Cases:
- **Single Sign-On (SSO)** - Unified authentication experience
- **Social Login** - Third-party identity provider integration
- **API Authentication** - Service-to-service identity verification
- **Mobile Applications** - Secure native app authentication
- **Web Applications** - Browser-based identity verification

## Implementation Considerations:
- **Token Storage** - Secure client-side token management
- **Session Management** - Coordinating OIDC with application sessions
- **Error Handling** - Graceful authentication failure responses
- **Performance** - Token validation and caching strategies

OIDC builds upon OAuth 2.0 Authorization Framework and integrates with modern Authentication Methods in identity platforms like Microsoft Entra ID.

**Connected Concepts**: [[OAuth 2.0 Authorization Framework]], [[Authentication Methods]], [[JWT Tokens]], [[Single Sign-On]], [[Identity Federation]]''',
                'tags': ['oidc', 'openid-connect', 'authentication', 'oauth', 'identity', 'jwt', 'sso']
            },
            {
                'title': 'JSON Web Tokens (JWT)',
                'content': '''JWT provides a compact, URL-safe means of representing claims to be transferred between parties, fundamental to modern authentication.

## JWT Structure:
### Three Parts (Base64URL encoded):
1. **Header** - Token type and signing algorithm
2. **Payload** - Claims and user information
3. **Signature** - Cryptographic verification

Format: `header.payload.signature`

## Header Component:
```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "key-identifier"
}
```

Common algorithms:
- **RS256** - RSA with SHA-256 (asymmetric)
- **HS256** - HMAC with SHA-256 (symmetric)
- **ES256** - ECDSA with SHA-256 (elliptic curve)

## Payload Claims:
### Standard Claims (RFC 7519):
- **iss** (issuer) - Token issuer
- **sub** (subject) - Token subject (user ID)
- **aud** (audience) - Token recipient
- **exp** (expiration) - Expiration time
- **iat** (issued at) - Issue time
- **nbf** (not before) - Token valid from
- **jti** (JWT ID) - Unique token identifier

### Custom Claims:
Application-specific information:
- User roles and permissions
- Profile information
- Application context
- Session details

## Token Types:
### Access Tokens
- **Short-lived** (15-60 minutes)
- **Resource access** - API authorization
- **Stateless** - Self-contained authorization
- **Revocation challenges** - Difficult to invalidate

### ID Tokens (OIDC)
- **Identity verification** - User authentication proof
- **Signed claims** - Cryptographically verified user info
- **Client consumption** - Application identity information
- **Non-repudiation** - Proof of identity provider attestation

### Refresh Tokens
- **Long-lived** (days to months)
- **Token renewal** - Obtaining new access tokens
- **Secure storage** - More sensitive than access tokens
- **Revocation support** - Can be invalidated

## Security Considerations:
### Token Validation:
1. **Signature verification** - Cryptographic integrity
2. **Claims validation** - iss, aud, exp, nbf
3. **Algorithm verification** - Prevent algorithm confusion
4. **Key validation** - Trusted signing keys

### Common Vulnerabilities:
- **Algorithm confusion** - None algorithm attacks
- **Weak secrets** - Brute force attacks on HMAC
- **Token storage** - XSS and local storage risks
- **Replay attacks** - Token interception and reuse

## Best Practices:
### Token Design:
- **Minimal payload** - Reduce token size
- **Appropriate expiration** - Balance security and usability
- **Audience specificity** - Limit token scope
- **Sensitive data exclusion** - Avoid PII in tokens

### Implementation:
- **HTTPS only** - Encrypted token transmission
- **Secure storage** - HttpOnly cookies or secure storage
- **Token rotation** - Regular refresh token updates
- **Comprehensive logging** - Token usage monitoring

## Storage Options:
### Browser Applications:
- **HttpOnly Cookies** - XSS protection (recommended)
- **Local Storage** - Vulnerable to XSS
- **Session Storage** - Temporary storage
- **Memory only** - Most secure, short-lived

### Mobile Applications:
- **Secure enclave** - Hardware-backed storage
- **Keychain services** - iOS/Android secure storage
- **Encrypted storage** - Application-level encryption

JWT is fundamental to OAuth 2.0 and OpenID Connect implementations, providing the token format for secure authentication and authorization.

**Connected Concepts**: [[OAuth 2.0 Authorization Framework]], [[OpenID Connect]], [[Authentication Methods]], [[API Security]], [[Token-based Authentication]]''',
                'tags': ['jwt', 'tokens', 'authentication', 'authorization', 'security', 'oauth', 'oidc']
            }
        ]

        self.stdout.write('Expanding Zettelkasten with additional security concepts...')
        
        created_count = 0
        for note_data in expansion_notes:
            try:
                note = create_note(
                    title=note_data['title'],
                    content=note_data['content'],
                    tag_names=note_data['tags']
                )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {note.title} (ID: {note.unique_id})')
                )
                time.sleep(0.1)  # Small delay between creations
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Failed to create note: {note_data["title"]} - {e}')
                )

        # Create connections between new and existing notes
        self.stdout.write('\\nCreating expanded note connections...')
        
        try:
            # Get existing notes
            entra_note = Note.objects.filter(title__icontains='Microsoft Entra ID').first()
            auth_note = Note.objects.filter(title__icontains='Authentication Methods').first()
            zero_trust_note = Note.objects.filter(title__icontains='Zero Trust').first()
            oauth_note = Note.objects.filter(title__icontains='OAuth').first()
            conditional_note = Note.objects.filter(title__icontains='Conditional Access').first()
            
            # Get new notes
            iam_note = Note.objects.filter(title__icontains='Identity and Access Management').first()
            siem_note = Note.objects.filter(title__icontains='Security Information and Event Management').first()
            pam_note = Note.objects.filter(title__icontains='Privileged Access Management').first()
            oidc_note = Note.objects.filter(title__icontains='OpenID Connect').first()
            jwt_note = Note.objects.filter(title__icontains='JSON Web Tokens').first()

            # Create logical connections
            if iam_note:
                if entra_note:
                    iam_note.connections.add(entra_note)
                if auth_note:
                    iam_note.connections.add(auth_note)
                if zero_trust_note:
                    iam_note.connections.add(zero_trust_note)
                if conditional_note:
                    iam_note.connections.add(conditional_note)
                if pam_note:
                    iam_note.connections.add(pam_note)
                    
            if siem_note:
                if iam_note:
                    siem_note.connections.add(iam_note)
                if zero_trust_note:
                    siem_note.connections.add(zero_trust_note)
                if pam_note:
                    siem_note.connections.add(pam_note)
                    
            if pam_note:
                if auth_note:
                    pam_note.connections.add(auth_note)
                if conditional_note:
                    pam_note.connections.add(conditional_note)
                if zero_trust_note:
                    pam_note.connections.add(zero_trust_note)
                    
            if oidc_note:
                if oauth_note:
                    oidc_note.connections.add(oauth_note)
                if auth_note:
                    oidc_note.connections.add(auth_note)
                if jwt_note:
                    oidc_note.connections.add(jwt_note)
                    
            if jwt_note:
                if oauth_note:
                    jwt_note.connections.add(oauth_note)
                if auth_note:
                    jwt_note.connections.add(auth_note)

            self.stdout.write(self.style.SUCCESS('✓ Created expanded note connections'))
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not create all connections: {e}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\\n🎉 Successfully expanded Zettelkasten with {created_count} new notes!'
            )
        )
        self.stdout.write(f'Total notes in system: {Note.objects.count()}')
        self.stdout.write(f'Total tags in system: {Tag.objects.count()}')
        self.stdout.write('\\n🌸 Your expanded Zettelkasten garden is thriving!')
