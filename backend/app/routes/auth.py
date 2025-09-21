from flask import Blueprint, request, jsonify, redirect, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import requests
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/status')
def auth_status():
    """Check authentication system status."""
    return {
        'status': 'active',
        'message': 'Authentication system is running'
    }

@auth_bp.route('/callback')
def auth_callback():
    """Handle Microsoft OAuth callback."""
    try:
        # Get authorization code from query parameters
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            return jsonify({
                'error': 'Authentication failed',
                'error_description': request.args.get('error_description', 'Unknown error')
            }), 400
        
        if not code:
            return jsonify({
                'error': 'Authorization code not provided'
            }), 400
        
        # Exchange code for access token
        token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
        token_data = {
            'client_id': os.environ.get('MICROSOFT_CLIENT_ID'),
            'client_secret': os.environ.get('MICROSOFT_CLIENT_SECRET'),
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': os.environ.get('MICROSOFT_REDIRECT_URI'),
            'scope': 'https://graph.microsoft.com/User.Read https://graph.microsoft.com/Mail.Read'
        }
        
        response = requests.post(token_url, data=token_data)
        
        if response.status_code != 200:
            return jsonify({
                'error': 'Token exchange failed',
                'details': response.text
            }), 400
        
        token_info = response.json()
        access_token = token_info.get('access_token')
        
        # Get user info from Microsoft Graph
        user_url = 'https://graph.microsoft.com/v1.0/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(user_url, headers=headers)
        
        if user_response.status_code != 200:
            return jsonify({
                'error': 'Failed to get user info',
                'details': user_response.text
            }), 400
        
        user_info = user_response.json()
        
        # Create JWT token for our app
        jwt_token = create_access_token(identity=user_info.get('id'))
        
        # Redirect to frontend with token
        frontend_url = os.environ.get('FRONTEND_URL', 'https://email-manager-ia.vercel.app')
        return redirect(f"{frontend_url}?token={jwt_token}")
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

# Additional auth routes will be implemented in the next phase