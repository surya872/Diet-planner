"""
Application Monitoring and Health Checks
Implements comprehensive monitoring for production readiness
"""

import time
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy import text


class ApplicationMonitor:
    """Centralized application monitoring"""
    
    def __init__(self, app: Optional[Flask] = None):
        self.app = app
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
        
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Initialize monitoring for Flask app"""
        self.app = app
        
        # Setup request monitoring
        @app.before_request
        def before_request():
            request.start_time = time.time()
            self.request_count += 1
        
        @app.after_request
        def after_request(response):
            request_time = time.time() - getattr(request, 'start_time', time.time())
            
            # Log slow requests
            if request_time > 1.0:  # Log requests taking more than 1 second
                app.logger.warning(
                    f"Slow request: {request.method} {request.path} took {request_time:.2f}s"
                )
            
            # Count errors
            if response.status_code >= 400:
                self.error_count += 1
            
            return response
        
        # Setup error handlers
        @app.errorhandler(404)
        def not_found(error):
            return jsonify({
                'error': 'Resource not found',
                'status': 404,
                'timestamp': datetime.utcnow().isoformat()
            }), 404
        
        @app.errorhandler(500)
        def internal_error(error):
            app.logger.error(f"Internal server error: {str(error)}")
            return jsonify({
                'error': 'Internal server error',
                'status': 500,
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status"""
        from app import db
        
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'uptime': time.time() - self.start_time,
            'version': '1.0.0',
            'environment': self.app.config.get('FLASK_ENV', 'unknown'),
            'checks': {}
        }
        
        # Database health check
        try:
            db.session.execute(text('SELECT 1'))
            health_data['checks']['database'] = {
                'status': 'healthy',
                'response_time': self._measure_db_response_time()
            }
        except Exception as e:
            health_data['status'] = 'unhealthy'
            health_data['checks']['database'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
        
        # System resource checks
        health_data['checks']['system'] = self._get_system_health()
        
        # Application metrics
        health_data['metrics'] = self._get_application_metrics()
        
        # External service checks
        health_data['checks']['external_services'] = self._check_external_services()
        
        return health_data
    
    def _measure_db_response_time(self) -> float:
        """Measure database response time"""
        from app import db
        
        start_time = time.time()
        try:
            db.session.execute(text('SELECT 1'))
            return round((time.time() - start_time) * 1000, 2)  # Return in milliseconds
        except Exception:
            return -1
    
    def _get_system_health(self) -> Dict[str, Any]:
        """Get system resource health metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            system_health = {
                'status': 'healthy',
                'cpu_usage_percent': cpu_percent,
                'memory_usage_percent': memory.percent,
                'memory_available_mb': round(memory.available / 1024 / 1024, 2),
                'disk_usage_percent': disk.percent,
                'disk_free_gb': round(disk.free / 1024 / 1024 / 1024, 2)
            }
            
            # Mark as unhealthy if resources are critically low
            if (cpu_percent > 90 or 
                memory.percent > 90 or 
                disk.percent > 95):
                system_health['status'] = 'unhealthy'
            elif (cpu_percent > 75 or 
                  memory.percent > 75 or 
                  disk.percent > 85):
                system_health['status'] = 'warning'
            
            return system_health
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _get_application_metrics(self) -> Dict[str, Any]:
        """Get application-specific metrics"""
        uptime_hours = (time.time() - self.start_time) / 3600
        
        return {
            'uptime_hours': round(uptime_hours, 2),
            'total_requests': self.request_count,
            'total_errors': self.error_count,
            'error_rate': round((self.error_count / max(self.request_count, 1)) * 100, 2),
            'requests_per_hour': round(self.request_count / max(uptime_hours, 0.01), 2)
        }
    
    def _check_external_services(self) -> Dict[str, Any]:
        """Check external service availability"""
        services = {}
        
        # Check Gemini AI service
        try:
            import google.generativeai as genai
            # Simple check - if we can configure without error, service is likely available
            genai.configure(api_key=self.app.config.get('GEMINI_API_KEY', 'test'))
            services['gemini_ai'] = {
                'status': 'healthy',
                'last_checked': datetime.utcnow().isoformat()
            }
        except Exception as e:
            services['gemini_ai'] = {
                'status': 'unhealthy',
                'error': str(e),
                'last_checked': datetime.utcnow().isoformat()
            }
        
        return services
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get metrics summary for monitoring dashboards"""
        return {
            'uptime_seconds': time.time() - self.start_time,
            'request_count': self.request_count,
            'error_count': self.error_count,
            'error_rate': self.error_count / max(self.request_count, 1),
            'memory_usage_mb': psutil.Process().memory_info().rss / 1024 / 1024,
            'cpu_usage_percent': psutil.cpu_percent()
        }


class PerformanceProfiler:
    """Performance profiling for optimization"""
    
    def __init__(self):
        self.slow_queries = []
        self.slow_requests = []
    
    def profile_query(self, query: str, execution_time: float):
        """Profile database query performance"""
        if execution_time > 0.5:  # Log queries taking more than 500ms
            self.slow_queries.append({
                'query': query[:200],  # Truncate long queries
                'execution_time': execution_time,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Keep only last 100 slow queries
            self.slow_queries = self.slow_queries[-100:]
    
    def profile_request(self, endpoint: str, method: str, execution_time: float):
        """Profile request performance"""
        if execution_time > 1.0:  # Log requests taking more than 1 second
            self.slow_requests.append({
                'endpoint': endpoint,
                'method': method,
                'execution_time': execution_time,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Keep only last 100 slow requests
            self.slow_requests = self.slow_requests[-100:]
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance analysis report"""
        return {
            'slow_queries': self.slow_queries[-10:],  # Last 10 slow queries
            'slow_requests': self.slow_requests[-10:],  # Last 10 slow requests
            'query_count': len(self.slow_queries),
            'request_count': len(self.slow_requests)
        }


# Initialize global instances
monitor = ApplicationMonitor()
profiler = PerformanceProfiler()


def setup_monitoring(app: Flask):
    """Setup comprehensive monitoring for the application"""
    monitor.init_app(app)
    
    # Setup health check endpoints
    @app.route('/health')
    @app.route('/api/health')
    def health_check():
        """Simple health check endpoint"""
        health_data = monitor.get_health_status()
        status_code = 200 if health_data['status'] == 'healthy' else 503
        return jsonify(health_data), status_code
    
    @app.route('/health/detailed')
    @app.route('/api/health/detailed')
    def detailed_health_check():
        """Detailed health check with all metrics"""
        return jsonify(monitor.get_health_status())
    
    @app.route('/metrics')
    @app.route('/api/metrics')
    def metrics():
        """Prometheus-style metrics endpoint"""
        metrics_data = monitor.get_metrics_summary()
        
        # Format as Prometheus metrics
        prometheus_format = []
        for key, value in metrics_data.items():
            prometheus_format.append(f"diet_planner_{key} {value}")
        
        return '\n'.join(prometheus_format), 200, {'Content-Type': 'text/plain'}
    
    @app.route('/performance')
    @app.route('/api/performance')
    def performance_report():
        """Performance analysis endpoint"""
        return jsonify(profiler.get_performance_report())
    
    # Setup logging configuration
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.config.get('TESTING'):
            # Create logs directory if it doesn't exist
            import os
            os.makedirs('logs', exist_ok=True)
            
            file_handler = RotatingFileHandler(
                'logs/diet_planner.log', 
                maxBytes=10240000, 
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Diet Planner monitoring initialized')
    
    return monitor, profiler
