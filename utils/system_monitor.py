import psutil
import threading
import time

class SystemMonitor:
    """Monitors system resources like CPU and RAM."""
    
    def __init__(self, update_interval=2):
        self.update_interval = update_interval
        self.is_running = False
        self.cpu_percent = 0
        self.memory_percent = 0
        self.memory_info = {}
        self.update_callback = None
    
    def start(self, callback=None):
        """Start monitoring system resources."""
        if self.is_running:
            return
        
        self.is_running = True
        self.update_callback = callback
        
        thread = threading.Thread(target=self._monitor_loop)
        thread.daemon = True
        thread.start()
    
    def stop(self):
        """Stop monitoring."""
        self.is_running = False
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.is_running:
            try:
                self.cpu_percent = psutil.cpu_percent(interval=0.1)
                
                memory = psutil.virtual_memory()
                self.memory_percent = memory.percent
                self.memory_info = {
                    "total": self._format_bytes(memory.total),
                    "used": self._format_bytes(memory.used),
                    "available": self._format_bytes(memory.available),
                    "percent": memory.percent
                }
                
                if self.update_callback:
                    self.update_callback({
                        "cpu": self.cpu_percent,
                        "memory": self.memory_percent,
                        "memory_info": self.memory_info
                    })
                
                time.sleep(self.update_interval / 1000)
            except Exception as e:
                print(f"Monitor error: {e}")
    
    def get_cpu_percent(self):
        """Get current CPU usage percentage."""
        return self.cpu_percent
    
    def get_memory_percent(self):
        """Get current memory usage percentage."""
        return self.memory_percent
    
    def get_memory_info(self):
        """Get detailed memory information."""
        return self.memory_info
    
    @staticmethod
    def _format_bytes(bytes_val):
        """Format bytes to human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024:
                return f"{bytes_val:.1f}{unit}"
            bytes_val /= 1024
        return f"{bytes_val:.1f}TB"
    
    def get_status_string(self):
        """Get formatted status string."""
        return f"CPU: {self.cpu_percent:.1f}% | RAM: {self.memory_percent:.1f}%"
