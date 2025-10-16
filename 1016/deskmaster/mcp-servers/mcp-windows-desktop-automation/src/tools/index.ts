/**
 * Tools module for MCP Windows Desktop Automation
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { registerMouseTools } from './mouse';
import { registerKeyboardTools } from './keyboard';
import { registerWindowTools } from './window';
import { registerProcessTools } from './process';
import { registerControlTools } from './control';

/**
 * Register all AutoIt tools with the MCP server
 */
export function registerAllTools(server: McpServer): void {
  registerMouseTools(server);
  registerKeyboardTools(server);
  registerWindowTools(server);
  registerProcessTools(server);
  registerControlTools(server);
}
