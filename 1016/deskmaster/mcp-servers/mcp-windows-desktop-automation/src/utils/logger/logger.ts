/**
 * Logger utility for MCP Windows Desktop Automation
 */

enum LogLevel {
  VERBOSE = 0,
  DEBUG = 1,
  INFO = 2,
  WARN = 3,
  ERROR = 4
}

class Logger {
  private level: LogLevel = LogLevel.INFO;

  /**
   * Set the minimum log level
   * @param level The minimum level to log
   */
  setLevel(level: LogLevel): void {
    this.level = level;
  }

  /**
   * Log verbose information
   * @param message The message to log
   * @param data Additional data to log (will be JSON stringified)
   */
  verbose(message: string, data?: any): void {
    if (this.level <= LogLevel.VERBOSE) {
      console.log(`[VERBOSE] ${message}`, data ? JSON.stringify(data) : '');
    }
  }

  /**
   * Log debug information
   * @param message The message to log
   * @param data Additional data to log
   */
  debug(message: string, data?: any): void {
    if (this.level <= LogLevel.DEBUG) {
      console.log(`[DEBUG] ${message}`, data || '');
    }
  }

  /**
   * Log general information
   * @param message The message to log
   * @param data Additional data to log
   */
  info(message: string, data?: any): void {
    if (this.level <= LogLevel.INFO) {
      console.log(`[INFO] ${message}`, data || '');
    }
  }

  /**
   * Log warnings
   * @param message The message to log
   * @param data Additional data to log
   */
  warn(message: string, data?: any): void {
    if (this.level <= LogLevel.WARN) {
      console.warn(`[WARN] ${message}`, data || '');
    }
  }

  /**
   * Log errors
   * @param message The message to log
   * @param data Additional data to log
   */
  error(message: string, data?: any): void {
    if (this.level <= LogLevel.ERROR) {
      console.error(`[ERROR] ${message}`, data || '');
    }
  }
}

export const log = new Logger();
