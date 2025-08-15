# Operations Guide

## 🚀 Operational Overview

This document provides comprehensive operational procedures for the Diet Planner application, covering deployment, monitoring, maintenance, and incident response.

## 📋 Table of Contents

- [Quick Operations](#quick-operations)
- [Environment Management](#environment-management)
- [Deployment Procedures](#deployment-procedures)
- [Monitoring & Alerting](#monitoring--alerting)
- [Maintenance & Updates](#maintenance--updates)
- [Backup & Recovery](#backup--recovery)
- [Incident Response](#incident-response)
- [Performance Tuning](#performance-tuning)
- [Security Operations](#security-operations)
- [Troubleshooting](#troubleshooting)

## ⚡ Quick Operations

### Daily Operations Checklist

```bash
# Morning health check
curl -f https://your-api-domain.com/api/health
curl -f https://your-app.netlify.app

# Check application metrics
curl -s https://your-api-domain.com/api/metrics | grep -E "(error_count|request_count|uptime)"

# Review overnight logs
docker-compose -f infra/docker-compose.dev.yml logs --since 24h | grep -i error

# Verify database connectivity
psql -U diet_user -d diet_planner -c "SELECT COUNT(*) FROM users;"
```

### Emergency Commands

```bash
# Emergency application restart
docker-compose -f infra/docker-compose.dev.yml restart api

# Check system resources
docker stats
df -h
free -h

# View recent errors
tail -f apps/api/logs/diet_planner.log | grep ERROR

# Database emergency access
psql -U diet_user -d diet_planner -h localhost -p 5432
```

## 🌍 Environment Management

### Environment Configuration

| Environment | API URL | Frontend URL | Database | Purpose |
|-------------|---------|--------------|----------|----------|
| **Development** | http://localhost:5001 | http://localhost:3000 | Local PostgreSQL | Local development |
| **Staging** | https://staging-api.render.com | https://staging.netlify.app | Render PostgreSQL | Pre-production testing |
| **Production** | https://api.your-domain.com | https://your-domain.com | Render PostgreSQL | Live production |

### Environment Variables by Stage

#### Development
```bash
APP_ENV=development
DEBUG=True
POSTGRES_HOST=localhost
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:3002
JWT_ACCESS_TOKEN_EXPIRES=24h
```

#### Staging
```bash
APP_ENV=staging
DEBUG=False
POSTGRES_HOST=<render-staging-host>
CORS_ORIGINS=https://staging.netlify.app
JWT_ACCESS_TOKEN_EXPIRES=2h
```

#### Production
```bash
APP_ENV=production
DEBUG=False
POSTGRES_HOST=<render-production-host>
CORS_ORIGINS=https://your-production-domain.com
JWT_ACCESS_TOKEN_EXPIRES=30m
```

### Environment Promotion

```bash
# Promote staging to production
git checkout main
git merge develop
git push origin main

# Verify deployment
make verify-production
```

## 🚀 Deployment Procedures

### Local Development Deployment

```bash
# Start local development environment
cd infra
docker-compose -f docker-compose.dev.yml up -d

# Verify services
docker-compose -f docker-compose.dev.yml ps
curl http://localhost:5001/api/health

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

### Production Deployment

#### Automated Deployment (Recommended)

```bash
# Production deployment via CI/CD
git checkout main
git pull origin main
git push origin main  # Triggers GitHub Actions

# Monitor deployment
gh run list --workflow=api.yml
gh run list --workflow=web.yml
```

#### Manual Deployment (Emergency)

```bash
# API deployment to Render
curl -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"clearCache": false}'

# Frontend deployment to Netlify
cd apps/web
npm run build
netlify deploy --prod --dir=build
```

### Deployment Verification

```bash
# Automated verification script
#!/bin/bash
API_URL="https://your-api-domain.com"
WEB_URL="https://your-web-domain.com"

echo "🔍 Verifying API deployment..."
if curl -f "$API_URL/api/health"; then
    echo "✅ API is healthy"
else
    echo "❌ API health check failed"
    exit 1
fi

echo "🔍 Verifying web deployment..."
if curl -f "$WEB_URL"; then
    echo "✅ Web is accessible"
else
    echo "❌ Web accessibility check failed"
    exit 1
fi

echo "🎉 Deployment verification complete!"
```

## 📊 Monitoring & Alerting

### Health Check Endpoints

```bash
# Basic health check
GET /api/health
# Response: {"status": "healthy", "timestamp": "...", "uptime": 3600}

# Detailed health check
GET /api/health/detailed
# Response: Comprehensive system health with database, external services

# Performance metrics
GET /api/metrics
# Response: Prometheus-compatible metrics

# Performance analysis
GET /api/performance
# Response: Slow queries and requests analysis
```

### Monitoring Dashboards

#### Application Metrics
- **Uptime**: Service availability percentage
- **Response Time**: P95, P99 response times
- **Error Rate**: 4xx and 5xx error percentages
- **Request Volume**: Requests per minute/hour
- **Database Performance**: Query response times

#### System Metrics
- **CPU Usage**: Current and average CPU utilization
- **Memory Usage**: Memory consumption and available memory
- **Disk Usage**: Storage utilization and free space
- **Database Connections**: Active connections and pool status

### Alerting Rules

#### Critical Alerts (Immediate Response)
```yaml
# API down
- alert: APIDown
  condition: http_check{endpoint="/api/health"} == 0
  duration: 30s
  severity: critical

# High error rate
- alert: HighErrorRate
  condition: rate(http_errors_total[5m]) > 0.1
  duration: 2m
  severity: critical

# Database connection failure
- alert: DatabaseDown
  condition: database_connections_active == 0
  duration: 1m
  severity: critical
```

#### Warning Alerts (Monitor Closely)
```yaml
# High response time
- alert: HighResponseTime
  condition: http_request_duration_p95 > 2s
  duration: 5m
  severity: warning

# High CPU usage
- alert: HighCPU
  condition: cpu_usage > 80%
  duration: 10m
  severity: warning
```

### Log Management

#### Log Locations
```bash
# Application logs
apps/api/logs/diet_planner.log

# Docker container logs
docker-compose logs api
docker-compose logs postgres

# System logs (production)
/var/log/nginx/access.log
/var/log/nginx/error.log
```

#### Log Analysis Commands
```bash
# Error analysis
grep "ERROR" apps/api/logs/diet_planner.log | tail -50

# Performance analysis
grep "Slow request" apps/api/logs/diet_planner.log

# Security analysis
grep "Failed login" apps/api/logs/diet_planner.log
grep "Rate limit" apps/api/logs/diet_planner.log

# User activity
grep "Successful login" apps/api/logs/diet_planner.log | wc -l
```

## 🔧 Maintenance & Updates

### Regular Maintenance Schedule

#### Daily
- [ ] Check application health status
- [ ] Review error logs for anomalies
- [ ] Monitor resource usage trends
- [ ] Verify backup completion

#### Weekly
- [ ] Review security logs
- [ ] Update documentation if needed
- [ ] Performance trend analysis
- [ ] Dependency vulnerability scan

#### Monthly
- [ ] Update dependencies
- [ ] Review and rotate secrets
- [ ] Database maintenance and optimization
- [ ] Disaster recovery test

#### Quarterly
- [ ] Security audit and penetration testing
- [ ] Performance baseline review
- [ ] Infrastructure cost optimization
- [ ] Documentation review and update

### Dependency Updates

```bash
# Check for API dependency updates
cd apps/api
pip list --outdated
safety check
pip-audit

# Check for web dependency updates
cd apps/web
npm outdated
npm audit

# Update dependencies (staging first)
cd apps/api
pip install -r requirements.txt --upgrade
pip freeze > requirements.txt

cd apps/web
npm update
npm audit fix
```

### Database Maintenance

```bash
# Database performance tuning
psql -U diet_user -d diet_planner -c "
    VACUUM ANALYZE users;
    VACUUM ANALYZE diet_plans;
    VACUUM ANALYZE meal_logs;
"

# Index optimization
psql -U diet_user -d diet_planner -c "
    REINDEX TABLE users;
    REINDEX TABLE diet_plans;
"

# Database statistics
psql -U diet_user -d diet_planner -c "
    SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del 
    FROM pg_stat_user_tables;
"
```

## 💾 Backup & Recovery

### Backup Strategy

#### Automated Backups
- **Database**: Daily automated backups via Render
- **Application Data**: Weekly full backup
- **Configuration**: Daily configuration backup to Git
- **Logs**: 30-day log retention

#### Manual Backup Commands
```bash
# Database backup
pg_dump -U diet_user -h localhost diet_planner > backup_$(date +%Y%m%d_%H%M%S).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz apps/

# Configuration backup
git add -A && git commit -m "Configuration backup $(date)"
```

### Recovery Procedures

#### Database Recovery
```bash
# Restore from backup
psql -U diet_user -d diet_planner < backup_20241215_120000.sql

# Verify restoration
psql -U diet_user -d diet_planner -c "SELECT COUNT(*) FROM users;"
```

#### Application Recovery
```bash
# Restore application
tar -xzf app_backup_20241215.tar.gz

# Restart services
docker-compose -f infra/docker-compose.dev.yml down
docker-compose -f infra/docker-compose.dev.yml up -d
```

#### Disaster Recovery Plan
1. **Assessment**: Evaluate scope of failure
2. **Communication**: Notify stakeholders
3. **Recovery**: Execute appropriate recovery procedure
4. **Verification**: Confirm system functionality
5. **Post-mortem**: Document lessons learned

## 🚨 Incident Response

### Incident Classification

#### Severity Levels
- **P0 (Critical)**: Complete service outage
- **P1 (High)**: Major functionality impaired
- **P2 (Medium)**: Minor functionality affected
- **P3 (Low)**: Cosmetic issues

#### Response Times
- **P0**: 15 minutes
- **P1**: 1 hour
- **P2**: 4 hours
- **P3**: Next business day

### Incident Response Procedures

#### P0/P1 Incident Response
```bash
# 1. Immediate assessment
curl -f https://your-api-domain.com/api/health
curl -f https://your-web-domain.com

# 2. Check recent deployments
gh run list --limit 5

# 3. Review logs
docker-compose logs --tail=100 | grep ERROR

# 4. Rollback if needed
git revert HEAD
git push origin main

# 5. Emergency restart
docker-compose restart api
```

#### Communication Template
```
🚨 INCIDENT ALERT - P0/P1

Incident ID: INC-2024-001
Start Time: 2024-12-15 14:30 UTC
Status: Investigating

Issue: API returning 500 errors
Impact: Users cannot generate diet plans
Actions: Investigating application logs, checking database connectivity

Updates will be provided every 30 minutes.
```

### Post-Incident Review

1. **Timeline**: Document incident timeline
2. **Root Cause**: Identify underlying cause
3. **Response**: Evaluate response effectiveness
4. **Prevention**: Define preventive measures
5. **Action Items**: Create follow-up tasks

## ⚡ Performance Tuning

### Performance Monitoring

```bash
# API performance check
curl -w "@curl-format.txt" -s https://your-api-domain.com/api/health

# Database performance
psql -U diet_user -d diet_planner -c "
    SELECT query, mean_time, calls 
    FROM pg_stat_statements 
    ORDER BY mean_time DESC 
    LIMIT 10;
"

# System performance
top -p $(pgrep -f python)
iostat -x 1 5
```

### Optimization Strategies

#### Database Optimization
- **Indexing**: Create indexes on frequently queried columns
- **Query Optimization**: Analyze and optimize slow queries
- **Connection Pooling**: Configure optimal pool sizes
- **Partitioning**: Consider table partitioning for large datasets

#### Application Optimization
- **Caching**: Implement Redis caching for frequent queries
- **Code Profiling**: Identify and optimize slow functions
- **Memory Management**: Monitor and optimize memory usage
- **Async Processing**: Use background tasks for heavy operations

## 🔐 Security Operations

### Security Monitoring

```bash
# Failed login attempts
grep "Failed login" apps/api/logs/diet_planner.log | tail -20

# Rate limiting violations
grep "Rate limit exceeded" apps/api/logs/diet_planner.log

# Unusual activity patterns
grep "$(date --date='1 hour ago' '+%Y-%m-%d %H')" apps/api/logs/diet_planner.log | \
  grep -E "(ERROR|WARNING)" | wc -l
```

### Security Maintenance

```bash
# Regular security scans
cd apps/api
safety check
bandit -r app.py
pip-audit

cd apps/web
npm audit

# SSL certificate check
curl -vI https://your-domain.com 2>&1 | grep -A 10 "Server certificate"
```

## 🔧 Troubleshooting

### Common Issues

#### API Issues
```bash
# API not responding
docker-compose ps api
docker-compose logs api

# Database connection issues
psql -U diet_user -d diet_planner -c "SELECT 1;"

# High memory usage
docker stats api
```

#### Frontend Issues
```bash
# Build failures
cd apps/web
npm run build

# Runtime errors
npm test
```

#### Database Issues
```bash
# Connection pool exhaustion
psql -U diet_user -d diet_planner -c "
    SELECT count(*) FROM pg_stat_activity 
    WHERE state = 'active';
"

# Slow queries
psql -U diet_user -d diet_planner -c "
    SELECT query, mean_time 
    FROM pg_stat_statements 
    WHERE mean_time > 1000;
"
```

### Diagnostic Commands

```bash
# System health check
#!/bin/bash
echo "=== System Health Check ==="
echo "Date: $(date)"
echo "Uptime: $(uptime)"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')"
echo "Memory: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "Disk: $(df -h / | awk 'NR==2 {print $3 "/" $2 " (" $5 " used)"}')"
echo "API Status: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/api/health)"
echo "Database: $(psql -U diet_user -d diet_planner -c "SELECT 1;" 2>/dev/null && echo "OK" || echo "ERROR")"
```

### Emergency Contacts

- **Primary On-Call**: +1-555-0123
- **Secondary On-Call**: +1-555-0124
- **Management**: manager@dietplanner.com
- **Infrastructure**: devops@dietplanner.com

---

**Last Updated**: December 2024
**Next Review**: March 2025
