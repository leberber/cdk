#!/bin/bash

# Configuration variables
EC2_IP="35.181.57.216"
SSH_KEY="/Users/yazidmekhtoub/.ssh/amanu-ssh-key.pem"
EC2_USER="ec2-user"

# Directories
FRONTEND_DIR="frontend"
BACKEND_DIR="backend"

# Image names
BACKEND_IMAGE="backend"
FRONTEND_IMAGE="frontend"

# File names
BACKEND_TAR="backend.tar.gz"
FRONTEND_TAR="frontend.tar.gz"
DOCKER_COMPOSE_FILE="docker-compose.yml"
EC2_DEPLOY_SCRIPT="ec2-deploy.sh"


echo "Building and deploying to EC2: $EC2_IP"

# Build Angular app first
echo "Building Angular app..."
cd $FRONTEND_DIR
npm run build
cd ..

# Build images for AMD64 platform (EC2 compatible)
echo "Building backend image for AMD64..."
docker build --platform linux/amd64 -t $BACKEND_IMAGE $BACKEND_DIR/

echo "Building frontend image for AMD64..."
docker build --platform linux/amd64 -t $FRONTEND_IMAGE $FRONTEND_DIR/

# Save and transfer images
echo "Saving and transferring images..."
docker save $BACKEND_IMAGE | gzip > $BACKEND_TAR
docker save $FRONTEND_IMAGE | gzip > $FRONTEND_TAR

echo "Copying files to EC2..."
scp -i "$SSH_KEY" $BACKEND_TAR $EC2_USER@$EC2_IP:~/
scp -i "$SSH_KEY" $FRONTEND_TAR $EC2_USER@$EC2_IP:~/
scp -i "$SSH_KEY" $DOCKER_COMPOSE_FILE $EC2_USER@$EC2_IP:~/
scp -i "$SSH_KEY" $EC2_DEPLOY_SCRIPT $EC2_USER@$EC2_IP:~/

# Execute deployment on EC2
echo "Running deployment on EC2..."
ssh -i "$SSH_KEY" $EC2_USER@$EC2_IP "chmod +x $EC2_DEPLOY_SCRIPT && ./$EC2_DEPLOY_SCRIPT"

# Clean up local tar files
rm -f $BACKEND_TAR $FRONTEND_TAR

echo "✅ Deployment finished!"
echo "🌐 Frontend: http://$EC2_IP"
echo "🌐 Frontend: http://elsuq.org"
echo "📚 Backend API: http://$EC2_IP:8000/docs"