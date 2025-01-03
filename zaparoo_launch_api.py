import json
import uuid
import websocket
import threading
from typing import Optional


class ZaparooRestResult:
    def __init__(self):
        self.error_code = 0
        self.result = None

    def set_error_code(self, error_code: int):
        self.error_code = error_code

    def get_error_code(self) -> int:
        return self.error_code

    def set_result(self, result: dict):
        self.result = result

    def get_result(self) -> Optional[dict]:
        return self.result

    def has_result(self) -> bool:
        return self.result is not None


def _create_base_doc(method: str, content: str = '', uid: str = '') -> dict:
    doc = {
        "jsonrpc": "2.0",
        "method": method,
        "id": str(uuid.uuid4()),
        "params": {
            "text": content,
            "uid": uid
        }
    }
    return doc


def parse_no_result(result_container: ZaparooRestResult) -> int:
    if result_container.get_error_code() == 0 and not result_container.has_result():
        if 'result' not in result_container.get_result():
            return 3  # Failed to launch path
    return result_container.get_error_code()


class ZaparooLaunchApi:
    def __init__(self, url: str):
        self._url = url

    def launch(self, content: str, uid: str = '') -> int:
        doc = _create_base_doc('launch', content, uid)
        result = self.launch_payload(doc)
        return parse_no_result(result)

    def stop(self) -> int:
        doc = _create_base_doc('stop')
        result = self.launch_payload(doc)
        return parse_no_result(result)

    def launch_payload(self, doc: dict) -> ZaparooRestResult:
        result = ZaparooRestResult()
        complete = threading.Event()

        def on_message(ws, message):
            try:
                result_data = json.loads(message)
                if result_data.get("id") != doc["id"]:
                    return
                result.set_result(result_data)
            except json.JSONDecodeError:
                result.set_error_code(4)  # Failed to parse JSON
            finally:
                complete.set()

        try:
            ws = websocket.WebSocketApp(self._url, on_message=on_message)
            ws.on_open = lambda ws_param: ws_param.send(json.dumps(doc))

            # Start WebSocket client
            ws_thread = threading.Thread(target=ws.run_forever)
            ws_thread.start()

            # Wait for completion or failure
            if not complete.wait(timeout=10):  # Timeout after 10 seconds
                result.set_error_code(2)  # Failed to connect or receive response

            ws.close()
        except Exception as e:
            result.set_error_code(1)  # General failure to open socket

        return result
