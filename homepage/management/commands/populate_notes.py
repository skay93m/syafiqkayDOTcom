from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from noto_garden.models import Note, Tag
import datetime
import time
import random


class Command(BaseCommand):
    help = 'Populate Noto Garden with starter Zettelkasten notes'

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
                         '#DDA0DD', '#98D8C8', '#FFB6C1', '#F39C12', '#E74C3C']
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

        # Define notes to create
        notes_data = [
            {
                'title': 'Authentication Methods Overview',
                'content': '''Authentication verifies the identity of users, devices, or systems - the foundation of cybersecurity.

## Authentication Factors:
- **Knowledge** (passwords, PINs, security questions)
- **Possession** (tokens, smart cards, mobile devices)  
- **Inherence** (biometrics: fingerprints, facial recognition)
- **Behavior** (typing patterns, mouse movements)

## Multi-Factor Authentication (MFA):
Combines multiple factors for stronger security:
- Something you know + Something you have
- Significantly reduces successful attacks
- Standard requirement for sensitive systems

## Modern Authentication Trends:
- **Passwordless Authentication** - Eliminates passwords entirely
- **Single Sign-On (SSO)** - One login for multiple systems
- **Risk-based Authentication** - Adaptive based on context
- **Continuous Authentication** - Ongoing verification

## Implementation Considerations:
- User experience vs security balance
- Backup authentication methods
- Legacy system integration challenges
- Compliance requirements (NIST, ISO 27001)

Authentication systems integrate with Identity and Access Management platforms like Microsoft Entra ID to provide comprehensive security frameworks.

**Connected Concepts**: Zero Trust Security, Conditional Access, OAuth 2.0, Biometric Security''',
                'tags': ['security', 'authentication', 'identity', 'mfa', 'cybersecurity']
            },
            {
                'title': 'Zero Trust Security Architecture',
                'content': '''Zero Trust is a security model that assumes no implicit trust and continuously validates every transaction.

## Core Philosophy:
"Never trust, always verify" - Traditional perimeter-based security is insufficient in modern, distributed environments.

## Key Principles:
1. **Verify Explicitly** - Always authenticate and authorize
2. **Least Privilege Access** - Limit user access with Just-In-Time (JIT)
3. **Assume Breach** - Design systems expecting compromise

## Implementation Pillars:
### Identity & Access Management
- Strong authentication mechanisms
- Conditional access policies
- Privileged access management (PAM)

### Device Security
- Device compliance validation
- Mobile device management (MDM)
- Endpoint detection and response (EDR)

### Network Security
- Micro-segmentation
- Software-defined perimeters
- Encrypted communications

### Data Protection
- Data classification and labeling
- Rights management
- Data loss prevention (DLP)

## Benefits:
- **Reduced Attack Surface** - Minimize potential entry points
- **Enhanced Visibility** - Comprehensive monitoring and analytics
- **Improved Compliance** - Better audit trails and controls
- **Flexible Architecture** - Supports cloud and hybrid environments

## Implementation Challenges:
- Complex integration requirements
- User experience considerations
- Legacy system compatibility
- Resource and skill requirements

Zero Trust requires robust Authentication Methods and integrates with modern identity platforms for effective implementation.

**Connected Concepts**: Authentication Methods, Conditional Access, Network Segmentation, Identity Governance''',
                'tags': ['security', 'zero-trust', 'architecture', 'framework', 'cybersecurity']
            },
            {
                'title': 'OAuth 2.0 Authorization Framework',
                'content': '''OAuth 2.0 enables secure authorization without sharing credentials - fundamental to modern API security.

## The Problem OAuth Solves:
Traditional username/password sharing for third-party access creates security risks. OAuth provides delegated authorization without credential exposure.

## Core Components:
- **Resource Owner** - User who owns the protected data
- **Client** - Application requesting access to resources
- **Authorization Server** - Issues access tokens (e.g., Microsoft Entra ID)
- **Resource Server** - Hosts protected resources/APIs

## Grant Types:
### Authorization Code (Recommended)
Most secure flow for server-side applications:
1. Client redirects user to authorization server
2. User authenticates and grants consent
3. Authorization server redirects with authorization code
4. Client exchanges code for access token
5. Client uses token to access protected resources

### Client Credentials
For service-to-service authentication:
- No user interaction required
- Client authenticates directly with authorization server
- Suitable for backend processes and microservices

### Implicit (Deprecated)
Previously used for single-page applications, now replaced by Authorization Code with PKCE.

## Security Enhancements:
### PKCE (Proof Key for Code Exchange)
- Essential for public clients (mobile apps, SPAs)
- Prevents authorization code interception attacks
- Uses cryptographically random code verifier

### Additional Security Measures:
- **State Parameter** - CSRF protection
- **Scope Limitation** - Principle of least privilege
- **Token Validation** - Verify issuer, audience, expiration
- **Secure Storage** - Protect tokens from unauthorized access

## Common Use Cases:
- Social login (Google, Facebook, GitHub)
- API access delegation
- Microservices authentication
- Third-party integrations
- Mobile app authorization

## Best Practices:
- Always use HTTPS for token endpoints
- Implement proper token storage
- Regular token rotation
- Monitor for suspicious activities
- Validate all tokens server-side

OAuth 2.0 is foundational to modern Authentication Methods and critical for API Security implementations.

**Connected Concepts**: OpenID Connect, JWT Tokens, API Security, Authentication Methods, PKCE''',
                'tags': ['oauth', 'authorization', 'api', 'security', 'protocol', 'tokens']
            },
            {
                'title': 'Conditional Access Policies',
                'content': '''Conditional Access brings signals together to make authorization decisions and enforce organizational policies.

## How It Works:
Conditional Access evaluates signals during authentication to determine if access should be granted, blocked, or require additional verification.

## Signal Types:
### User and Group Information
- User identity and group memberships
- User risk level (based on behavior analysis)
- Admin role assignments
- Guest vs member users

### Location-Based Signals
- Geographic location (country, region)
- IP address ranges and named locations
- Trusted vs untrusted networks
- Travel patterns and anomalies

### Device Signals
- Device compliance status
- Device platform (iOS, Android, Windows)
- Managed vs unmanaged devices
- Device risk assessment

### Application Signals
- Specific applications being accessed
- Application sensitivity levels
- Data classification requirements
- Legacy vs modern authentication

### Session Signals
- Sign-in frequency patterns
- Session duration requirements
- Application usage patterns
- Real-time risk assessment

## Common Policy Examples:
### Multi-Factor Authentication Requirements
- Require MFA for all admin users
- Require MFA when accessing from untrusted locations
- Require MFA for high-risk applications

### Device-Based Controls
- Block access from non-compliant devices
- Require managed devices for sensitive apps
- Allow personal devices with restrictions

### Location-Based Controls
- Block access from specific countries
- Require additional verification for unusual locations
- Allow access only from corporate networks

### Application-Specific Controls
- Require app protection policies for mobile access
- Block legacy authentication protocols
- Implement session controls for web applications

## Implementation Strategy:
### Phase 1: Discovery and Planning
- Identify user groups and access patterns
- Map applications and their sensitivity levels
- Define security requirements and compliance needs

### Phase 2: Policy Development
- Start with report-only mode
- Create policies for specific groups/scenarios
- Test policies thoroughly before enforcement

### Phase 3: Gradual Rollout
- Begin with pilot groups
- Monitor user impact and feedback
- Gradually expand to broader populations

### Phase 4: Optimization
- Analyze policy effectiveness
- Adjust based on user behavior and security incidents
- Continuous monitoring and improvement

## Best Practices:
- Always test in report-only mode first
- Provide clear communication to users
- Have break-glass procedures for emergencies
- Regular policy reviews and updates
- Monitor for unintended access blocks

## Integration with Zero Trust:
Conditional Access is a key component of Zero Trust Architecture, providing dynamic access controls based on real-time risk assessment.

Conditional Access policies work alongside Authentication Methods and integrate with comprehensive identity platforms like Microsoft Entra ID.

**Connected Concepts**: Zero Trust Security, Risk-Based Authentication, Identity Protection, Device Management''',
                'tags': ['conditional-access', 'security', 'policy', 'azure', 'identity', 'risk-assessment']
            }
        ]

        self.stdout.write('Creating Zettelkasten network of notes...')
        
        created_count = 0
        for note_data in notes_data:
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

        # Now create connections between notes
        self.stdout.write('\\nCreating note connections...')
        notes = Note.objects.all()
        
        # Find notes by title and create connections
        try:
            # Get the original Microsoft Entra ID note
            entra_note = Note.objects.filter(title__icontains='Microsoft Entra ID').first()
            auth_note = Note.objects.filter(title__icontains='Authentication Methods').first()
            zero_trust_note = Note.objects.filter(title__icontains='Zero Trust').first()
            oauth_note = Note.objects.filter(title__icontains='OAuth').first()
            conditional_note = Note.objects.filter(title__icontains='Conditional Access').first()

            # Create logical connections
            if entra_note and auth_note:
                entra_note.connections.add(auth_note)
                entra_note.connections.add(zero_trust_note)
                entra_note.connections.add(conditional_note)
                
            if auth_note and zero_trust_note:
                auth_note.connections.add(zero_trust_note)
                auth_note.connections.add(oauth_note)
                
            if zero_trust_note and conditional_note:
                zero_trust_note.connections.add(conditional_note)
                
            if oauth_note and auth_note:
                oauth_note.connections.add(auth_note)

            self.stdout.write(self.style.SUCCESS('✓ Created note connections'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not create all connections: {e}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\\n🎉 Successfully created {created_count} notes!'
            )
        )
        self.stdout.write(f'Total notes in system: {Note.objects.count()}')
        self.stdout.write(f'Total tags in system: {Tag.objects.count()}')
        self.stdout.write('\\n🌸 Your Zettelkasten garden is ready to explore!')
