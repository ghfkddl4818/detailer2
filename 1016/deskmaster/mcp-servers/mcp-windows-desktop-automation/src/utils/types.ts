/**
 * Shared type definitions for MCP Windows Desktop Automation
 */

import { z } from 'zod';
import { CallToolResult, TextContent } from '@modelcontextprotocol/sdk/types.js';

/**
 * Point coordinates
 */
export interface Point {
  x: number;
  y: number;
}

/**
 * Rectangle coordinates
 */
export interface Rect {
  left: number;
  top: number;
  right: number;
  bottom: number;
}

/**
 * Standard tool response creator
 */
export function createToolResponse(message: string): CallToolResult {
  return {
    content: [
      {
        type: 'text',
        text: message
      } as TextContent
    ]
  };
}

/**
 * Standard error response creator
 */
export function createErrorResponse(error: Error | string): CallToolResult {
  const errorMessage = typeof error === 'string' ? error : error.message;
  return {
    content: [
      {
        type: 'text',
        text: `Error: ${errorMessage}`
      } as TextContent
    ],
    isError: true
  };
}

/**
 * Common Zod schemas for tool parameters
 */
export const schemas = {
  // Window identification
  windowTitle: z.string().describe('Window title'),
  windowText: z.string().optional().describe('Window text'),
  
  // Mouse parameters
  mouseButton: z.enum(['left', 'right', 'middle']).optional().default('left').describe('Mouse button'),
  mouseSpeed: z.number().min(1).max(100).optional().default(10).describe('Mouse movement speed (1-100)'),
  mouseX: z.number().describe('X coordinate'),
  mouseY: z.number().describe('Y coordinate'),
  mouseClicks: z.number().min(1).optional().default(1).describe('Number of clicks'),
  
  // Control parameters
  controlName: z.string().describe('Control identifier'),
  controlText: z.string().describe('Text to set/send to control'),
  
  // Process parameters
  processName: z.string().describe('Process name or executable path'),
  processTimeout: z.number().optional().describe('Timeout in milliseconds'),
  
  // Common parameters
  handle: z.number().describe('Window or control handle'),
  bufferSize: z.number().optional().describe('Buffer size for string operations')
};
