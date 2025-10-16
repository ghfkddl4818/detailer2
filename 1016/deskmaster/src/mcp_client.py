"""MCP Client - Interface to MCP servers."""
import subprocess
import json
import os
from typing import Optional, Dict, Any, List
from pathlib import Path

class MCPClient:
    """Client for communicating with MCP servers."""

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.mcp_config_path = Path(__file__).parent.parent / ".mcp.json"

        # Load MCP configuration
        with open(self.mcp_config_path, 'r') as f:
            self.mcp_config = json.load(f)

        # MCP server processes
        self.servers = {}

    def start_server(self, server_name: str) -> bool:
        """Start an MCP server process."""
        if server_name in self.servers:
            self.logger.info(f"MCP server '{server_name}' already running")
            return True

        server_config = self.mcp_config['mcpServers'].get(server_name)
        if not server_config:
            self.logger.error("mcp-server-not-found", f"Server '{server_name}' not in config")
            return False

        try:
            command = server_config['command']
            args = server_config.get('args', [])
            env = os.environ.copy()

            # Add environment variables from config
            if 'env' in server_config:
                for key, value in server_config['env'].items():
                    # Replace ${VAR} with environment variable
                    if value.startswith('${') and value.endswith('}'):
                        env_var = value[2:-1]
                        env[key] = os.getenv(env_var, '')
                    else:
                        env[key] = value

            # Start the server process
            process = subprocess.Popen(
                [command] + args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )

            self.servers[server_name] = process
            self.logger.info(f"Started MCP server: {server_name}")
            return True

        except Exception as e:
            self.logger.error("mcp-server-start-failed", f"{server_name}: {e}")
            return False

    def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Optional[Dict]:
        """
        Call a tool on an MCP server.

        Args:
            server_name: Name of the MCP server
            tool_name: Name of the tool to call
            arguments: Tool arguments

        Returns:
            Tool response or None on error
        """
        if server_name not in self.servers:
            if not self.start_server(server_name):
                return None

        process = self.servers[server_name]

        # MCP JSON-RPC request
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": 1
        }

        try:
            # Send request
            process.stdin.write((json.dumps(request) + '\n').encode())
            process.stdin.flush()

            # Read response
            response_line = process.stdout.readline().decode()
            response = json.loads(response_line)

            if 'error' in response:
                self.logger.error("mcp-tool-call-error", f"{tool_name}: {response['error']}")
                return None

            return response.get('result')

        except Exception as e:
            self.logger.error("mcp-tool-call-failed", f"{tool_name}: {e}")
            return None

    def stop_all_servers(self):
        """Stop all MCP server processes."""
        for name, process in self.servers.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                self.logger.info(f"Stopped MCP server: {name}")
            except:
                process.kill()
                self.logger.info(f"Killed MCP server: {name}")

    # Windows UIA helpers
    def uia_find_element(self, criteria: Dict[str, str]) -> Optional[Dict]:
        """Find UI element using Windows UIA."""
        return self.call_tool('windows-automation', 'WinGetHandle', criteria)

    def uia_click(self, handle: str) -> bool:
        """Click UI element."""
        result = self.call_tool('windows-automation', 'ControlClick', {'handle': handle})
        return result is not None

    def uia_get_text(self, handle: str) -> Optional[str]:
        """Get text from UI element."""
        result = self.call_tool('windows-automation', 'ControlGetText', {'handle': handle})
        return result.get('text') if result else None

    def uia_scroll(self, direction: str = 'down', amount: int = 1) -> bool:
        """Scroll in Chrome window."""
        result = self.call_tool('windows-automation', 'MouseWheel', {
            'direction': direction,
            'clicks': amount
        })
        return result is not None

    # Gemini Vision helpers
    def gemini_analyze_image(self, image_path: str, prompt: str) -> Optional[str]:
        """Analyze image using Gemini Vision."""
        result = self.call_tool('gemini', 'generate_content', {
            'prompt': prompt,
            'image': image_path
        })
        return result.get('text') if result else None

    def gemini_solve_captcha(self, image_path: str) -> Optional[Dict]:
        """Solve CAPTCHA using Gemini Vision."""
        prompt = "This is a CAPTCHA image. Please extract the text or answer shown in the image. Return only the answer text, nothing else."
        result = self.gemini_analyze_image(image_path, prompt)

        if result:
            return {
                'answer': result.strip(),
                'confidence': 0.8  # Placeholder confidence
            }
        return None

    # OCR helpers
    def ocr_extract_text(self, image_source: str, source_type: str = 'file', language: str = 'kor+eng') -> Optional[str]:
        """
        Extract text from image using OCR.

        Args:
            image_source: File path, URL, or bytes
            source_type: 'file', 'url', or 'bytes' (not used, kept for compatibility)
            language: Tesseract language code (default: 'kor+eng')

        Returns:
            Extracted text or None
        """
        # mcp-ocr perform_ocr expects a single 'input_data' parameter
        arguments = {
            'input_data': image_source,
            'language': language,
            'config': '--oem 3 --psm 6'
        }

        result = self.call_tool('ocr', 'perform_ocr', arguments)

        # mcp-ocr returns the text directly, not in a dict
        if result and isinstance(result, str):
            return result
        elif result and isinstance(result, dict):
            return result.get('text')
        return None

    def ocr_get_languages(self) -> List[str]:
        """Get list of supported OCR languages."""
        result = self.call_tool('ocr', 'get_supported_languages', {})
        return result.get('languages', []) if result else []
