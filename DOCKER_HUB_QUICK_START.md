# GitHub Actions Docker Hub Setup - Quick Checklist

## What's Automated

✅ Automatic Docker image builds on:
- Every push to `main` or `develop` branch
- Every git tag you create (e.g., `v1.0.0`)
- Pull request builds (no push)

✅ Automatic image push to Docker Hub with:
- Branch name tags (`main`, `develop`)
- Semantic version tags (`v1.0.0`, `1.0`)
- Latest tag on main branch
- Commit SHA tags

## Quick Setup (3 Steps)

### Step 1: Create Docker Hub Access Token
- Log in to https://hub.docker.com
- Click profile icon → **Account Settings**
- Click **Security** → **New Access Token**
- Description: `GitHub Actions`
- Permissions: `Read & Write`
- Click **Generate** and **copy the token**

### Step 2: Add GitHub Secrets
Go to your repository on GitHub:
1. **Settings** tab → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secret #1:
   - Name: `DOCKER_USERNAME`
   - Value: `quincycheng` (your Docker Hub username)
4. Add secret #2:
   - Name: `DOCKER_PASSWORD`
   - Value: (paste the token from Step 1)

### Step 3: Test It Out
1. Commit and push the workflow files to your repo
2. Push code to `main` or `develop` branch
3. Go to **Actions** tab to see the build running
4. After it succeeds, run:
   ```bash
   docker pull quincycheng/entrasonar-mcp:latest
   ```

## Creating a Release

```bash
# Create a version tag
git tag v1.0.0

# Push the tag
git push origin v1.0.0
```

This will automatically build and push images with tags:
- `quincycheng/entrasonar-mcp:v1.0.0`
- `quincycheng/entrasonar-mcp:1.0`
- `quincycheng/entrasonar-mcp:latest`

## Monitoring Builds

1. Go to your GitHub repository
2. Click **Actions** tab
3. Click on any workflow run to see logs

## Troubleshooting

**Workflow doesn't run?**
- Check that workflow file is in `.github/workflows/docker-publish.yml`
- Make sure you pushed to `main` or `develop` (not a different branch)

**Push to Docker Hub fails?**
- Verify `DOCKER_USERNAME` is set correctly in GitHub secrets
- Verify `DOCKER_PASSWORD` is the **access token** (not your password)
- Check token has `Read & Write` permissions
- Make sure token hasn't expired

**Build fails?**
- Check Actions logs for error details
- Verify `Dockerfile` is valid in repository root
- Ensure all dependencies in `requirements.txt` are available

## See Also

- **Full Setup Guide**: [DOCKER_HUB_SETUP.md](DOCKER_HUB_SETUP.md)
- **Workflow Configuration**: [.github/workflows/docker-publish.yml](.github/workflows/docker-publish.yml)
