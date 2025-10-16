/**
 * Keyboard-related tools for MCP Windows Desktop Automation
 */

import * as autoIt from 'node-autoit-koffi';
import { z } from 'zod';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { createToolResponse, createErrorResponse } from '../utils/types';
import { log } from '../utils/logger/logger';

/**
 * Register keyboard-related tools with the MCP server
 */
export function registerKeyboardTools(server: McpServer): void {
  // send - Send keystrokes to the active window
  server.tool(
    'send',
    {
      text: z.string().describe('Text or keys to send'),
      mode: z.number().optional().default(0).describe('Send mode flag')
    },
    async ({ text, mode }) => {
      try {
        log.verbose('send called', { text, mode });
        await autoIt.init();
        await autoIt.send(text, mode);
        return createToolResponse(`Sent keystrokes: "${text}" with mode ${mode}`);
      } catch (error) {
        log.error('send failed', error);
        return createErrorResponse(error instanceof Error ? error : String(error));
      }
    }
  );

  // clipGet - Get the text from the clipboard
  server.tool(
    'clipGet',
    {
      bufSize: z.number().optional().describe('Buffer size for clipboard content')
    },
    async ({ bufSize }) => {
      try {
        log.verbose('clipGet called', { bufSize });
        await autoIt.init();
        const clipboardContent = await autoIt.clipGet(bufSize);
        log.verbose('clipGet result', JSON.stringify({ clipboardContent }));
        return createToolResponse(`Clipboard content: "${clipboardContent}"`);
      } catch (error) {
        log.error('clipGet failed', error);
        return createErrorResponse(error instanceof Error ? error : String(error));
      }
    }
  );

  // clipPut - Put text into the clipboard
  server.tool(
    'clipPut',
    {
      text: z.string().describe('Text to put in the clipboard')
    },
    async ({ text }) => {
      try {
        log.verbose('clipPut called', { text });
        await autoIt.init();
        await autoIt.clipPut(text);
        return createToolResponse(`Text set to clipboard: "${text}"`);
      } catch (error) {
        log.error('clipPut failed', error);
        return createErrorResponse(error instanceof Error ? error : String(error));
      }
    }
  );

  // autoItSetOption - Set AutoIt options
  server.tool(
    'autoItSetOption',
    {
      option: z.string().describe('Option name'),
      value: z.number().describe('Option value')
    },
    async ({ option, value }) => {
      try {
        log.verbose('autoItSetOption called', { option, value });
        await autoIt.init();
        const result = await autoIt.autoItSetOption(option, value);
        return createToolResponse(`AutoIt option "${option}" set to ${value} with result: ${result}`);
      } catch (error) {
        log.error('autoItSetOption failed', error);
        return createErrorResponse(error instanceof Error ? error : String(error));
      }
    }
  );

  // opt - Alias for autoItSetOption
  server.tool(
    'opt',
    {
      option: z.string().describe('Option name'),
      value: z.number().describe('Option value')
    },
    async ({ option, value }) => {
      try {
        log.verbose('opt called', { option, value });
        await autoIt.init();
        const result = await autoIt.opt(option, value);
        return createToolResponse(`AutoIt option "${option}" set to ${value} with result: ${result}`);
      } catch (error) {
        log.error('opt failed', error);
        return createErrorResponse(error instanceof Error ? error : String(error));
      }
    }
  );

  // toolTip - Display a tooltip
  server.tool(
    'toolTip',
    {
      text: z.string().describe('Tooltip text'),
      x: z.number().optional().describe('X coordinate'),
      y: z.number().optional().describe('Y coordinate')
    },
    async ({ text, x, y }) => {
      try {
        log.verbose('toolTip called', { text, x, y });
        await autoIt.init();
        await autoIt.toolTip(text, x, y);
        const position = x !== undefined && y !== undefined ? ` at position (${x}, ${y})` : '';
        return createToolResponse(`Tooltip displayed: "${text}"${position}`);
      } catch (error) {
        log.error('toolTip failed', error);
        return createErrorResponse(error instanceof Error ? error : String(error));
      }
    }
  );
}
