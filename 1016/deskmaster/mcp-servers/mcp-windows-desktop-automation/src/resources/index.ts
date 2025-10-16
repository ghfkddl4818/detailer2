/**
 * Resources module for MCP Windows Desktop Automation
 */

import { McpServer, ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as autoIt from 'node-autoit-koffi';
import { log } from '../utils/logger/logger';

/**
 * Register all resources with the MCP server
 */
export function registerAllResources(server: McpServer): void {
  // Register file resources
  registerFileResources(server);
  
  // Register screenshot resources
  registerScreenshotResources(server);
}

/**
 * Register file resources
 */
function registerFileResources(server: McpServer): void {
  server.resource(
    'file',
    new ResourceTemplate('file://{path*}', { 
      list: async () => {
        return { resources: [] }; // Empty list by default
      }
    }),
    async (uri, params) => {
      try {
        // Ensure filePath is a string
        const filePath = Array.isArray(params.path) ? params.path.join('/') : params.path;
        log.verbose('Reading file resource', JSON.stringify({ uri: uri.href, filePath }));
        
        // Check if file exists
        const stats = await fs.stat(filePath);
        
        if (stats.isDirectory()) {
          // List directory contents
          const files = await fs.readdir(filePath);
          const resources = await Promise.all(
            files.map(async (file) => {
              const fullPath = path.join(filePath, file);
              const fileStats = await fs.stat(fullPath);
              return {
                uri: `file://${fullPath.replace(/\\/g, '/')}`,
                name: file,
                description: fileStats.isDirectory() ? 'Directory' : 'File'
              };
            })
          );
          
          return {
            contents: [{
              uri: uri.href,
              text: `Directory: ${filePath}\n${files.join('\n')}`,
              mimeType: 'text/plain'
            }]
          };
        } else {
          // Read file content
          const content = await fs.readFile(filePath);
          const extension = path.extname(filePath).toLowerCase();
          
          // Determine if it's a text or binary file
          const isTextFile = [
            '.txt', '.md', '.js', '.ts', '.html', '.css', '.json', '.xml', 
            '.csv', '.log', '.ini', '.cfg', '.conf', '.py', '.c', '.cpp', 
            '.h', '.java', '.sh', '.bat', '.ps1'
          ].includes(extension);
          
          if (isTextFile) {
            return {
              contents: [{
                uri: uri.href,
                text: content.toString('utf-8'),
                mimeType: getMimeType(extension)
              }]
            };
          } else {
            return {
              contents: [{
                uri: uri.href,
                blob: content.toString('base64'),
                mimeType: getMimeType(extension)
              }]
            };
          }
        }
      } catch (error) {
        log.error('Error reading file resource', error);
        throw new Error(`Failed to read file: ${error instanceof Error ? error.message : String(error)}`);
      }
    }
  );
}

/**
 * Register screenshot resources
 */
function registerScreenshotResources(server: McpServer): void {
  server.resource(
    'screenshot',
    new ResourceTemplate('screenshot://{window?}', { 
      list: async () => {
        return { resources: [] }; // Empty list by default
      }
    }),
    async (uri, params) => {
      try {
        await autoIt.init();
        // Ensure window is a string if provided
        const windowName = params.window ? String(params.window) : undefined;
        log.verbose('Taking screenshot', JSON.stringify({ uri: uri.href, window: windowName }));
        
        // If window parameter is provided, activate that window first
        if (windowName) {
          const windowExists = await autoIt.winExists(windowName);
          if (windowExists) {
            await autoIt.winActivate(windowName);
            // Wait a moment for the window to activate
            await new Promise(resolve => setTimeout(resolve, 500));
          } else {
            throw new Error(`Window "${windowName}" not found`);
          }
        }
        
        // TODO: Implement actual screenshot capture
        // This is a placeholder - in a real implementation, you would use
        // a library like 'screenshot-desktop' or other Windows API bindings
        // to capture the screen or specific window
        
        // For now, we'll return a placeholder message
        return {
          contents: [{
            uri: uri.href,
            text: `Screenshot of ${windowName || 'full screen'} would be captured here`,
            mimeType: 'text/plain'
          }]
        };
        
        // In a real implementation, you would return something like:
        /*
        return {
          contents: [{
            uri: uri.href,
            blob: screenshotBase64Data,
            mimeType: 'image/png'
          }]
        };
        */
      } catch (error) {
        log.error('Error taking screenshot', error);
        throw new Error(`Failed to take screenshot: ${error instanceof Error ? error.message : String(error)}`);
      }
    }
  );
}

/**
 * Get MIME type based on file extension
 */
function getMimeType(extension: string): string {
  const mimeTypes: Record<string, string> = {
    '.txt': 'text/plain',
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.ts': 'application/typescript',
    '.json': 'application/json',
    '.xml': 'application/xml',
    '.md': 'text/markdown',
    '.csv': 'text/csv',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.pdf': 'application/pdf',
    '.doc': 'application/msword',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.xls': 'application/vnd.ms-excel',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.ppt': 'application/vnd.ms-powerpoint',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.zip': 'application/zip',
    '.rar': 'application/x-rar-compressed',
    '.7z': 'application/x-7z-compressed',
    '.tar': 'application/x-tar',
    '.gz': 'application/gzip'
  };
  
  return mimeTypes[extension] || 'application/octet-stream';
}
