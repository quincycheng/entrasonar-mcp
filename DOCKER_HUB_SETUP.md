# Docker Hub Setup Guide

This guide explains how to configure GitHub Actions to automatically build and push your Docker image to Docker Hub.

## Prerequisites

- Docker Hub account (create one at https://hub.docker.com if you don't have it)
- Access to the GitHub repository settings

## Step-by-Step Configuration

### 1. Create Docker Hub Access Token

1. Go to [Docker Hub](https://hub.docker.com) and log in with your account
2. Click your profile icon in the top right corner → **Account Settings**
3. In the left sidebar, click **Security**
4. Click **New Access Token**
5. Fill in the details:
   - **Access Token Description**: `GitHub Actions` (or any descriptive name)
   - **Permissions**: Select `Read & Write` to allow pushing images
6. Click **Generate**
7. **Copy the token** and save it somewhere safe (you won't see it again)

### 2. Add GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** tab (top of the page)
3. In the left sidebar, go to **Secrets and variables** → **Actions**
4. Click **New repository secret** button

**Add the following secrets:**

#### Secret 1: DOCKER_USERNAME
- **Name**: `DOCKER_USERNAME`
- **Value**: Your Docker Hub username (e.g., `quincycheng`)
- Click **Add secret**

#### Secret 2: DOCKER_PASSWORD
- **Name**: `DOCKER_PASSWORD`
- **Value**: The access token you generated in Step 1
- Click **Add secret**

### 3. Verify the Setup

After adding both secrets:
1. Go back to your repository
2. Click on **Actions** tab
3. You should see the workflow files listed on the left (including "Docker Build and Publish")
4. When you push code to `main` or `develop` branch (or create a tag), the workflow will automatically trigger

## How It Works

The Docker Build and Publish workflow automatically:

### On Push to main/develop:
- Builds the Docker image
- Pushes to Docker Hub as:
  - `quincycheng/entrasonar-mcp:main` or `quincycheng/entrasonar-mcp:develop` (branch name)
  - `quincycheng/entrasonar-mcp:latest` (for main branch only)
  - `quincycheng/entrasonar-mcp:<short-sha>` (git commit hash)

### On Pull Requests:
- Builds the Docker image for testing
- Does NOT push to Docker Hub
- Verifies the build doesn't break

### On Git Tags (Release):
- Builds the Docker image
- Pushes with semantic version tags:
  - `quincycheng/entrasonar-mcp:v1.0.0` (full version)
  - `quincycheng/entrasonar-mcp:1.0` (major.minor)
  - `quincycheng/entrasonar-mcp:latest` (for production releases)

## Tagging for Releases

To create a release and automatically push with version tags:

```bash
# Create and push a version tag
git tag v0.1.0
git push origin v0.1.0
```

This will trigger the workflow and push images with tags:
- `quincycheng/entrasonar-mcp:v0.1.0`
- `quincycheng/entrasonar-mcp:0.1`
- `quincycheng/entrasonar-mcp:latest`

## Monitoring Builds

1. Go to your repository
2. Click **Actions** tab
3. Click on any workflow run to see:
   - Build logs
   - Step-by-step progress
   - Any errors or warnings

## Testing Locally

You can also build and test the image locally before pushing:

```bash
# Build the image locally
docker build -t quincycheng/entrasonar-mcp:test .

# Run the container
docker run -p 8000:8000 quincycheng/entrasonar-mcp:test

# Push to Docker Hub (requires manual setup)
docker push quincycheng/entrasonar-mcp:test
```

## Troubleshooting

### Workflow doesn't trigger
- Make sure you pushed to `main` or `develop` branch
- Check that the workflow file is in `.github/workflows/` directory
- Go to **Actions** tab to see if there are any errors

### Push to Docker Hub fails
- Verify `DOCKER_USERNAME` secret is set correctly
- Verify `DOCKER_PASSWORD` secret is the access token (not your Docker Hub password)
- Check that the access token has `Read & Write` permissions
- Regenerate the token if needed

### Image won't build
- Check the build logs in the **Actions** tab
- Ensure your `Dockerfile` is valid and in the repository root
- Check that all dependencies in `requirements.txt` are available

## Security Notes

- The `DOCKER_PASSWORD` secret is your Docker Hub access token - keep it safe
- GitHub Actions automatically masks secrets in logs for security
- Consider using a dedicated Docker Hub account or limiting token permissions if needed
- Rotate your access token periodically

## Next Steps

1. Commit and push the workflow file to your repository
2. Follow the configuration steps above
3. Push code to `main` or `develop` to test the workflow
4. Check the **Actions** tab to see your first build

Your Docker images will be available at:
- https://hub.docker.com/r/quincycheng/entrasonar-mcp
- Pull with: `docker pull quincycheng/entrasonar-mcp`
