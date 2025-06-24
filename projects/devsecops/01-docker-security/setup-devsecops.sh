#!/bin/bash

# DevSecOps Environment Setup Script
# This script sets up your development environment for DevSecOps projects

echo "🚀 Setting up DevSecOps Development Environment"
echo "=============================================="

# Check if Docker is installed and running
echo "📋 Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed"
    if docker info &> /dev/null; then
        echo "✅ Docker is running"
    else
        echo "❌ Docker is not running. Please start Docker Desktop."
        echo "   Then run this script again."
        exit 1
    fi
else
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    echo "   Download from: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Check if kubectl is installed
echo "📋 Checking kubectl installation..."
if command -v kubectl &> /dev/null; then
    echo "✅ kubectl is installed"
    echo "   Version: $(kubectl version --client --short)"
else
    echo "❌ kubectl is not installed"
    exit 1
fi

# Check if minikube is installed
echo "📋 Checking minikube installation..."
if command -v minikube &> /dev/null; then
    echo "✅ minikube is installed"
else
    echo "❌ minikube is not installed"
    exit 1
fi

# Check if terraform is installed
echo "📋 Checking terraform installation..."
if command -v terraform &> /dev/null; then
    echo "✅ terraform is installed"
    echo "   Version: $(terraform version | head -n 1)"
else
    echo "❌ terraform is not installed"
    exit 1
fi

echo ""
echo "🎯 All tools are installed! Let's test the Docker implementation..."

# Navigate to the Docker project directory
cd "$(dirname "$0")/dockerfiles/network-monitor"

# Check if required files exist
echo "📋 Checking required files..."
if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile found"
else
    echo "❌ Dockerfile not found"
    exit 1
fi

if [ -f "network_monitor.py" ]; then
    echo "✅ network_monitor.py found"
else
    echo "❌ network_monitor.py not found"
    exit 1
fi

if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Build the Docker image
echo ""
echo "🔨 Building Docker image..."
docker build -t network-monitor:devsecops .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo "   Image: network-monitor:devsecops"
else
    echo "❌ Docker build failed"
    exit 1
fi

# Test the container
echo ""
echo "🧪 Testing container..."
docker run --rm -d --name test-monitor network-monitor:devsecops

if [ $? -eq 0 ]; then
    echo "✅ Container started successfully!"
    
    # Check container status
    sleep 2
    if docker ps | grep -q test-monitor; then
        echo "✅ Container is running"
    else
        echo "⚠️  Container may have stopped (check logs)"
    fi
    
    # Stop the test container
    docker stop test-monitor
    echo "✅ Test container stopped"
else
    echo "❌ Container failed to start"
    exit 1
fi

echo ""
echo "🎉 DevSecOps environment setup complete!"
echo ""
echo "📚 Next Steps:"
echo "1. Start minikube: minikube start"
echo "2. Create Kubernetes manifests for your security tools"
echo "3. Deploy your containerized security stack"
echo "4. Test the CI/CD pipeline"
echo ""
echo "📖 Resources:"
echo "- Docker Security: https://docs.docker.com/develop/security-best-practices/"
echo "- Kubernetes Security: https://kubernetes.io/docs/concepts/security/"
echo "- Terraform Security: https://www.terraform.io/docs/cloud/guides/recommended-practices/security.html"
echo ""
echo "🚀 Ready to continue with Phase 2 of your DevSecOps roadmap!" 