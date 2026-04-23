# VPS Deployment Guide - MichelinBot

## Prerequisites

- VPS with **Ubuntu 22.04/24.04** or **Debian 12**
- Minimum **2GB RAM**, **1 vCPU**, **20GB disk**
- Root or sudo access

---

## Step 1: Server Preparation

### 1.1 Update System

```bash
# Connect to your VPS
ssh root@your-vps-ip

# Update packages
apt update && apt upgrade -y

# Set timezone (optional)
timedatectl set-timezone Europe/Paris
```

### 1.2 Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Enable and start Docker
systemctl enable docker
systemctl start docker

# Verify installation
docker --version
docker-compose --version
```

---

## Step 2: Deploy Application

### 2.1 Clone Repository

```bash
# Install git if not present
apt install git -y

# Clone your repository
cd /opt
git clone <your-repo-url> michelin-bot
cd michelin-bot
```

### 2.2 Configure Environment

```bash
# Create production environment file
cat > .env.prod << 'EOF'
# Database
POSTGRES_DB=michelin_db
POSTGRES_USER=michelin_user
POSTGRES_PASSWORD=CHANGE_ME_TO_STRONG_PASSWORD
DATABASE_URL=postgresql+psycopg://michelin_user:CHANGE_ME_TO_STRONG_PASSWORD@postgres:5432/michelin_db

# API
ZHIPUAI_API_KEY=your_zhipuai_api_key_here
ALLOWED_ORIGINS=http://your-server-ip,http://your-domain.com
EOF

# Edit with your values
nano .env.prod
```

**⚠️ IMPORTANT:** Replace these values:
- `CHANGE_ME_TO_STRONG_PASSWORD` - Use a strong password (generate with: `openssl rand -base64 32`)
- `your_zhipuai_api_key_here` - Your Zhipu AI API key
- `your-server-ip` or `your-domain.com` - Your server address

---

## Step 3: Configure Firewall

```bash
# Install UFW if not present
apt install ufw -y

# Configure firewall
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (important first!)
ufw allow 22/tcp

# Allow HTTP
ufw allow 80/tcp

# Optional: Allow HTTPS (if you add SSL later)
# ufw allow 443/tcp

# Enable firewall
ufw enable
ufw status
```

---

## Step 4: Start Services

```bash
# Build and start production containers
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Check container status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## Step 5: Verify Deployment

```bash
# Test API health
curl http://localhost/api/health

# Expected response:
# {"status":"healthy","version":"1.0.0","llm_configured":true,...}

# Test from outside (run on your local machine)
curl http://your-vps-ip/api/health
```

---

## Step 6: Access the Application

**From your browser:**
- `http://your-vps-ip/` - Home page
- `http://your-vps-ip/chat` - Chat interface
- `http://your-vps-ip/api/docs` - API documentation

---

## Management Commands

```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f

# View specific service logs
docker-compose -f docker-compose.prod.yml logs -f api
docker-compose -f docker-compose.prod.yml logs -f nginx

# Restart services
docker-compose -f docker-compose.prod.yml restart

# Restart specific service
docker-compose -f docker-compose.prod.yml restart api

# Stop all services
docker-compose -f docker-compose.prod.yml down

# Start after stop
docker-compose -f docker-compose.prod.yml up -d

# Update and rebuild
git pull
docker-compose -f docker-compose.prod.yml up -d --build

# Check resource usage
docker stats
```

---

## Optional: Add Domain Name

### 1. Point Domain to VPS

Add A record in your DNS:
```
A    @    your-vps-ip
A    www    your-vps-ip
```

### 2. Update ALLOWED_ORIGINS

```bash
nano .env.prod

# Update this line:
ALLOWED_ORIGINS=http://yourdomain.com,https://yourdomain.com

# Restart
docker-compose -f docker-compose.prod.yml restart api
```

---

## Optional: Add SSL (HTTPS)

```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Stop nginx container temporarily
docker-compose -f docker-compose.prod.yml stop nginx

# Get certificate (replace with your domain)
certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Certificates will be at:
# /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem

# Update nginx to use SSL (you'll need to modify nginx/nginx.conf)
```

---

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs <service-name>

# Check disk space
df -h

# Check memory
free -h
```

### Can't access from browser

```bash
# Check if port 80 is listening
netstat -tlnp | grep :80

# Check firewall
ufw status

# Check if nginx is running
docker-compose -f docker-compose.prod.yml ps nginx
```

### API errors

```bash
# Check API logs
docker-compose -f docker-compose.prod.yml logs api

# Check environment variables
docker-compose -f docker-compose.prod.yml exec api env | grep ZHIPUAI
```

---

## Security Checklist

- [ ] Changed default database password
- [ ] Set strong API key
- [ ] Firewall enabled (only ports 22, 80 open)
- [ ] SSH key authentication enabled (disable password login)
- [ ] Regular security updates: `apt update && apt upgrade -y`
- [ ] Monitor logs for suspicious activity
- [ ] Consider fail2ban for SSH protection

---

## File Structure After Deployment

```
/opt/michelin-bot/
├── docker-compose.prod.yml
├── docker-compose.yml           # Local dev (not used in prod)
├── .env.prod                     # Production secrets
├── michelin-bot/
│   ├── Dockerfile
│   ├── app.py
│   └── ...
├── michelin-front/
│   ├── Dockerfile
│   └── ...
└── nginx/
    ├── nginx.conf
    └── logs/
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Start | `docker-compose -f docker-compose.prod.yml up -d` |
| Stop | `docker-compose -f docker-compose.prod.yml down` |
| Restart | `docker-compose -f docker-compose.prod.yml restart` |
| Logs | `docker-compose -f docker-compose.prod.yml logs -f` |
| Status | `docker-compose -f docker-compose.prod.yml ps` |
| Update | `git pull && docker-compose -f docker-compose.prod.yml up -d --build` |
