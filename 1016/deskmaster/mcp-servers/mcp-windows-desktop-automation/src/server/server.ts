/**
 * MCP Server configuration for Windows Desktop Automation
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { WebSocket, WebSocketServer, RawData } from 'ws';
import { createServer as createHttpServer, IncomingMessage, Server as HttpServer } from 'http';
import { log } from '../utils/logger/logger';
import { Transport } from '@modelcontextprotocol/sdk/shared/transport.js';
import { JSONRPCMessage } from '@modelcontextprotocol/sdk/types.js';

/**
 * Custom WebSocket transport for MCP
 */
class WebSocketServerTransport implements Transport {
  private ws: WebSocket | null = null;
  sessionId?: string;

  constructor(ws: WebSocket) {
    this.ws = ws;
    this.sessionId = Math.random().toString(36).substring(2, 15);
    
    ws.on('message', (data: RawData) => {
      try {
        const message = JSON.parse(data.toString()) as JSONRPCMessage;
        this.onmessage?.(message);
      } catch (error) {
        this.onerror?.(new Error(`Failed to parse message: ${error}`));
      }
    });

    ws.on('close', () => {
      this.ws = null;
      this.onclose?.();
    });

    ws.on('error', (error: Error) => {
      this.onerror?.(error);
    });
  }

  onclose?: () => void;
  onerror?: (error: Error) => void;
  onmessage?: (message: JSONRPCMessage) => void;

  async start(): Promise<void> {
    log.info('WebSocket transport started');
  }

  async send(message: JSONRPCMessage): Promise<void> {
    if (!this.ws) {
      throw new Error('WebSocket not connected');
    }
    
    return new Promise((resolve, reject) => {
      this.ws!.send(JSON.stringify(message), (error?: Error) => {
        if (error) {
          reject(error);
        } else {
          resolve();
        }
      });
    });
  }

  async close(): Promise<void> {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

/**
 * Server configuration options
 */
export interface ServerConfig {
  name: string;
  version: string;
  transport: 'stdio' | 'websocket';
  port?: number;
}

/**
 * Create and configure an MCP server
 */
export async function setupServer(config: ServerConfig): Promise<{
  server: McpServer;
  httpServer?: HttpServer;
}> {
  // Create the MCP server
  const server = new McpServer({
    name: config.name,
    version: config.version
  }, {
    capabilities: {
      tools: {},
      resources: {
        subscribe: true,
        listChanged: true
      },
      prompts: {
        listChanged: true
      }
    }
  });

  // Configure the transport
  if (config.transport === 'stdio') {
    log.info('Using stdio transport');
    const transport = new StdioServerTransport();
    await server.connect(transport);
    return { server };
  } else if (config.transport === 'websocket') {
    log.info(`Using WebSocket transport on port ${config.port}`);
    
    // Create HTTP server
    const httpServer = createHttpServer();
    const wss = new WebSocketServer({ server: httpServer });
    
    // Handle WebSocket connections
    wss.on('connection', async (ws: WebSocket) => {
      log.info('New WebSocket connection');
      const transport = new WebSocketServerTransport(ws);
      await server.connect(transport);
    });
    
    // Start HTTP server
    httpServer.listen(config.port || 3000);
    
    return { server, httpServer };
  } else {
    throw new Error(`Unsupported transport: ${config.transport}`);
  }
}
