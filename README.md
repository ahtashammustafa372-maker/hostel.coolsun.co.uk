# Coolsun Hostel ERP

This is the repository for the Coolsun Hostel ERP.

## Server Deployment Instructions

To deploy the latest changes to the live UK server, follow these simple steps:

1. **SSH into your server:**
   ```bash
   ssh your_user@hostel.coolsun.co.uk
   ```

2. **Navigate to the project directory:**
   ```bash
   cd /path/to/your/project
   ```

3. **Run the deployment script:**
   ```bash
   bash deploy.sh
   ```

The `deploy.sh` script will automatically:
- Pull the latest code from GitHub
- Install any new Node.js dependencies
- Rebuild the React frontend for production
- Restart the backend service (you may need to configure the exact service name in `deploy.sh`)

## Notes on Database
The `.gitignore` is configured to ignore `hostel.db`. The production database will remain completely separate from the local testing database. Never commit or push the production database to GitHub.
