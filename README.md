# 🥷 Syafiq Kay - Digital Ninja Portfolio

A Django-powered digital portfolio website with a ninja/samurai aesthetic, featuring bilingual support (English/Japanese) and three interconnected applications for knowledge management.

## 🌸 Project Overview

This project showcases a modern Django web application with a beautiful sakura-themed design, combining traditional Japanese aesthetics with contemporary web development practices. The site serves as both a personal portfolio and a comprehensive knowledge management system.

## 🎯 Key Features

- **Ninja/Samurai Theme**: Beautiful sakura pink aesthetic with Japanese typography
- **Bilingual Support**: English and Japanese content throughout
- **Responsive Design**: Optimized for all devices with A4-width content layout
- **Three Core Apps**: Reference management, journals, and Zettelkasten note-taking
- **Security Focused**: Comprehensive security assessment and implementations
- **AI Partnership**: Built in collaboration with GitHub Copilot

## 📁 Project Structure

```
syafiq-kay/
├── homepage/          # Main homepage and static pages
├── reference/         # Reference management system
├── journals/          # Journal and blog system
├── noto_garden/       # Zettelkasten note-taking app
├── syafiqkay/         # Django project settings
├── templates/         # Shared templates
├── static/           # Static assets (CSS, JS, images)
├── scripts/          # Utility scripts
└── staticfiles/      # Collected static files
```

## 🚀 Applications

### 1. Homepage App
- **Purpose**: Main portfolio page with personal statement and navigation
- **Features**: Banner, LinkedIn integration, security assessment, session summary
- **Theme**: Pink sakura gradient with zen landscape imagery

### 2. Reference App
- **Purpose**: Academic and professional reference management
- **Features**: Category-based organization, external links, search functionality
- **Theme**: Pink sakura badges and horizontal card layout

### 3. Journals App
- **Purpose**: Blog and journal entries with markdown support
- **Features**: Tag system, author filtering, markdown rendering
- **Theme**: Green accents with horizontal card layout

### 4. Noto Garden App
- **Purpose**: Zettelkasten-style note-taking system
- **Features**: Bi-directional linking, graph visualization, tag management
- **Theme**: Purple gradients with admin-only editing

## 🛠️ Technology Stack

- **Backend**: Django 4.x with Python 3.12
- **Frontend**: Bootstrap 5, Custom CSS with Japanese fonts
- **Database**: SQLite (development), PostgreSQL ready
- **Security**: CSRF protection, XSS prevention, input validation
- **Styling**: Sakura/Mount Fuji pastel palette

## 📋 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/syafiqkay/syafiq-kay.git
   cd syafiq-kay
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**:
   ```bash
   python manage.py runserver
   ```

## 🎨 Design Philosophy

The project follows a "Digital Ninja" aesthetic that combines:
- **Traditional Japanese Elements**: Sakura pink, Mount Fuji blue, zen imagery
- **Modern Web Design**: Clean layouts, responsive grids, subtle animations
- **Typography**: Japanese font stacks for authentic feel
- **Color Harmony**: Pastel palette for visual comfort

## 🔒 Security

The application includes comprehensive security measures:
- Input validation and sanitization
- CSRF protection on all forms
- XSS prevention with content filtering
- Rate limiting on sensitive endpoints
- Secure password handling
- Admin-only access controls where appropriate

## 📖 Documentation

- **Security Assessment**: Available at `/security-assessment/`
- **Session Summary**: Available at `/session-summary/`
- **Noto Garden Guide**: Available at `/noto-garden/guide/`
- **Development Journal**: Available in the journals section

## 🤝 Contributing

This project was built in partnership with GitHub Copilot. Contributions are welcome following these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GitHub Copilot**: AI pair programming partner
- **Django Community**: For the excellent framework
- **Bootstrap Team**: For the responsive framework
- **Unsplash**: For beautiful stock photography
- **Japanese Typography**: For inspiration on font choices

## 📞 Contact

- **LinkedIn**: [Syafiq Kay](https://www.linkedin.com/in/syafiqkay/)
- **GitHub**: [syafiqkay](https://github.com/syafiqkay)
- **Website**: [Live Demo](https://www.syafiqkay.com)

---

*Built with ❤️ and 🥷 by Syafiq Kay in partnership with GitHub Copilot*
