# Heroku App Manager Dashboard

A comprehensive Flask-based dashboard to monitor and control all your Heroku applications from a single interface.

## Features

### 📊 **Dashboard Overview**
- **Real-time Status Monitoring** - View the current status of all your Heroku apps
- **Beautiful Card Layout** - Each app displayed in an organized card format
- **Category Organization** - Apps grouped by categories (Security, Migration Tools, etc.)
- **Live Statistics** - Total apps, running/stopped counts, last update time

### 🎛️ **App Control**
- **Start/Stop/Restart** - Control app dynos with one-click actions
- **Status Indicators** - Visual status badges (Running, Stopped, Error, Unknown)
- **Quick Access** - Direct links to live applications
- **Logs Viewer** - View recent application logs in a modal

### 🔄 **Auto-Refresh**
- **Real-time Updates** - Dashboard refreshes every 30 seconds
- **Manual Refresh** - Floating refresh button for instant updates
- **Loading States** - Visual feedback during operations

### 🎨 **Modern UI**
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Bootstrap 5** - Modern, clean interface
- **Gradient Background** - Beautiful visual design
- **Toast Notifications** - User feedback for all actions

## App Categories

The dashboard automatically categorizes your Heroku apps:

- **Security & Compliance** - Security operations and compliance platforms
- **Migration Tools** - Splunk migration platforms (Google SecOps, Microsoft Security, CrowdStrike)
- **Risk Management** - Integrated risk management platforms
- **Incident Response** - Security incident response tools
- **Security Tools** - Cyber agent configurators and security utilities

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd heroku-app-manager
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure Heroku CLI is installed and authenticated:**
   ```bash
   heroku login
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the dashboard:**
   Open your browser to `http://localhost:5000`

## Deployment to Heroku

1. **Create a new Heroku app:**
   ```bash
   heroku create heroku-app-manager
   ```

2. **Deploy:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

3. **Open the deployed app:**
   ```bash
   heroku open
   ```

## Configuration

The app configurations are defined in `app.py` in the `APP_CONFIGS` dictionary. To add new apps or modify descriptions:

```python
APP_CONFIGS = {
    'your-app-name': {
        'description': 'Your app description',
        'category': 'Your Category'
    }
}
```

## API Endpoints

### GET `/api/apps`
Returns JSON array of all Heroku apps with their status and information.

### POST `/api/apps/<app_name>/action`
Performs actions on a specific app. Accepts JSON body with `action` field:
- `start` - Scale web dynos to 1
- `stop` - Scale web dynos to 0  
- `restart` - Restart all dynos

### GET `/api/apps/<app_name>/logs`
Returns recent logs for the specified app.

## Requirements

- Python 3.7+
- Flask 3.1.1
- Heroku CLI
- Valid Heroku authentication

## Security Notes

- This application requires Heroku CLI access
- Ensure proper authentication before deployment
- Consider adding authentication for production use
- Logs may contain sensitive information

## Troubleshooting

### Common Issues:

1. **"Command not found: heroku"**
   - Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

2. **Authentication errors**
   - Run `heroku login` to authenticate

3. **App not found errors**
   - Verify app names in `APP_CONFIGS` match your actual Heroku apps

4. **Timeout errors**
   - Commands have a 30-second timeout; check your network connection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details
