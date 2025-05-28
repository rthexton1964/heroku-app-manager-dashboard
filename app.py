#!/usr/bin/env python3
"""
Heroku App Management Dashboard
A simple Flask application to manage and monitor Heroku apps
"""

import os
import subprocess
import json
import logging
from datetime import datetime
from flask import Flask, render_template, jsonify, request
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# App configurations with descriptions
APP_CONFIGS = {
    'accenture-secops-compliance': {
        'description': 'Security Operations Compliance Platform with MITRE ATT&CK and regulatory frameworks',
        'category': 'Security & Compliance'
    },
    'cyber-agent-configurator-app': {
        'description': 'Cyber Agent Configuration and Management Platform',
        'category': 'Security Tools'
    },
    'irm-platform-app': {
        'description': 'Integrated Risk Management Platform for enterprise risk assessment',
        'category': 'Risk Management'
    },
    'security-incident-demo-app': {
        'description': 'Security Incident Response Demo Platform with AI-powered analysis',
        'category': 'Incident Response'
    },
    'splunk-crowdstrike-migration': {
        'description': 'Splunk to CrowdStrike Migration Platform with automated conversion tools',
        'category': 'Migration Tools'
    },
    'splunk-to-google-secops': {
        'description': 'Splunk to Google Security Operations Migration Platform with Chronicle integration',
        'category': 'Migration Tools'
    },
    'splunk-to-microsoft-security': {
        'description': 'Splunk to Microsoft Security Migration Platform with Sentinel and Copilot integration',
        'category': 'Migration Tools'
    }
}

def run_heroku_command(command):
    """Execute a Heroku CLI command and return the result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'success': result.returncode == 0,
            'output': result.stdout.strip(),
            'error': result.stderr.strip()
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'output': '',
            'error': 'Command timed out'
        }
    except Exception as e:
        return {
            'success': False,
            'output': '',
            'error': str(e)
        }

def get_app_status(app_name):
    """Get the status of a Heroku app"""
    command = f"heroku ps -a {app_name} --json"
    result = run_heroku_command(command)
    
    if result['success']:
        try:
            processes = json.loads(result['output'])
            if not processes:
                return 'stopped'
            
            # Check if any web dynos are running
            web_processes = [p for p in processes if p['type'] == 'web']
            if web_processes:
                return 'running' if web_processes[0]['state'] == 'up' else 'stopped'
            return 'stopped'
        except json.JSONDecodeError:
            return 'unknown'
    return 'error'

def get_app_info(app_name):
    """Get detailed information about a Heroku app"""
    command = f"heroku apps:info -a {app_name} --json"
    result = run_heroku_command(command)
    
    if result['success']:
        try:
            return json.loads(result['output'])
        except json.JSONDecodeError:
            return None
    return None

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/apps')
def get_apps():
    """API endpoint to get all Heroku apps with their status"""
    apps = []
    
    for app_name, config in APP_CONFIGS.items():
        status = get_app_status(app_name)
        app_info = get_app_info(app_name)
        
        app_data = {
            'name': app_name,
            'description': config['description'],
            'category': config['category'],
            'status': status,
            'url': f"https://{app_name}.herokuapp.com" if app_info else None,
            'last_updated': datetime.now().isoformat()
        }
        
        if app_info:
            app_data.update({
                'created_at': app_info.get('created_at'),
                'updated_at': app_info.get('updated_at'),
                'region': app_info.get('region', {}).get('name'),
                'stack': app_info.get('stack', {}).get('name')
            })
        
        apps.append(app_data)
    
    return jsonify(apps)

@app.route('/api/apps/<app_name>/action', methods=['POST'])
def app_action(app_name):
    """Perform actions on Heroku apps (start, stop, restart)"""
    action = request.json.get('action')
    
    if app_name not in APP_CONFIGS:
        return jsonify({'success': False, 'error': 'App not found'}), 404
    
    if action == 'start':
        command = f"heroku ps:scale web=1 -a {app_name}"
    elif action == 'stop':
        command = f"heroku ps:scale web=0 -a {app_name}"
    elif action == 'restart':
        command = f"heroku ps:restart -a {app_name}"
    else:
        return jsonify({'success': False, 'error': 'Invalid action'}), 400
    
    result = run_heroku_command(command)
    
    if result['success']:
        # Get updated status
        new_status = get_app_status(app_name)
        return jsonify({
            'success': True,
            'message': f'Successfully {action}ed {app_name}',
            'status': new_status
        })
    else:
        return jsonify({
            'success': False,
            'error': result['error'] or 'Command failed'
        }), 500

@app.route('/api/apps/<app_name>/logs')
def get_app_logs(app_name):
    """Get recent logs for a Heroku app"""
    if app_name not in APP_CONFIGS:
        return jsonify({'success': False, 'error': 'App not found'}), 404
    
    command = f"heroku logs --tail -n 50 -a {app_name}"
    result = run_heroku_command(command)
    
    if result['success']:
        return jsonify({
            'success': True,
            'logs': result['output'].split('\n')
        })
    else:
        return jsonify({
            'success': False,
            'error': result['error'] or 'Failed to fetch logs'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Heroku App Manager on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
