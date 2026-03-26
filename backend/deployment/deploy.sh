#!/bin/bash
set -e

echo "Building AWS Lambda deployment package..."
cd "$(dirname "$0")"

# Clean previous builds
rm -rf package deployment_package.zip

# Create package layer
mkdir package
pip install -r ../requirements.txt -t package/

# Copy the application code
cp -r ../app package/
cp ../main.py package/ 2>/dev/null || true

# Strip unneeded files to reduce size
find package -type f -name '*.pyc' -delete
find package -type d -name '__pycache__' -delete

# Zip
cd package
zip -r9 ../deployment_package.zip .

echo "✅ Deployment package successfully created at backend/deployment/deployment_package.zip"
echo "You can upload this directly to AWS Lambda."
