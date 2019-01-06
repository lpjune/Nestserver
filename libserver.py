
import sys
import selectors
import json
import io
import struct

doorStatus = 0
roofStatus = 0
bPadStatus = 0
tPadStatus = 0

status = str(doorStatus) + str(roofStatus) + str(bPadStatus) + str(tPadStatus)

request_search = {
    "backButton": "Previous camera...",
    "nextButton": "Next camera...",
    "menuDiagnosticBtn": "Running diagnostics...",
    "systemHaltButton": "HALTING.",
    "doorsSwitchOn": "Opening doors...",
    "doorsSwitchOff": "Closing doors...",
    "roofSwitchOn": "Opening roof...",
    "roofSwitchOff": "Closing roof...",
    "extendPadSwitchOn": "Extending pad...",
    "extendPadSwitchOff": "Retracting pad...",
    "raisePadSwitchOn": "Raising pad...",
    "raisePadSwitchOff": "Lowering pad...",
    "status": status
}



class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.response_created = False

    def refresh(self):
        global request_search
        global status
        request_search = {
            "backButton": "Previous camera...",
            "nextButton": "Next camera...",
            "menuDiagnosticBtn": "Running diagnostics...",
            "systemHaltButton": "HALTING.",
            "doorsSwitchOn": "Opening doors...",
            "doorsSwitchOff": "Closing doors...",
            "roofSwitchOn": "Opening roof...",
            "roofSwitchOff": "Closing roof...",
            "extendPadSwitchOn": "Extending pad...",
            "extendPadSwitchOff": "Retracting pad...",
            "raisePadSwitchOn": "Raising pad...",
            "raisePadSwitchOff": "Lowering pad...",
            "status": status}

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._send_buffer:
            #print("sending", repr(self._send_buffer), "to", self.addr)
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                if sent and not self._send_buffer:
                    self.close()

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(
        self, *, content_bytes, content_type, content_encoding
    ):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def _create_response_json_content(self):

        global doorStatus
        global roofStatus
        global bPadStatus
        global tPadStatus
        global status

        action = self.request.get("action")
        if action == "search":
            query = self.request.get("value")
            ###
            if query == "doorsSwitchOff" and bPadStatus == 1:
                answer = "Error: Cannot close doors with bottom pad extended"
            elif query == "extendPadSwitchOn" and doorStatus == 0:
                answer = "Error: Cannot extend pad with doors closed"
            elif query == "raisePadSwitchOn" and roofStatus == 0:
                answer = "Error: Cannot raise pad with roof closed"
            elif query == "roofSwitchOff" and tPadStatus == 1:
                answer = "Error: Cannot close roof with pad raised"
            elif query == "doorsSwitchOn" and doorStatus == 1:
                answer = "Error: Doors already open"
            elif query == "doorsSwitchOff" and doorStatus == 0:
                answer = "Error: Doors already closed"
            elif query == "roofSwitchOn" and roofStatus == 1:
                answer = "Error: Roof already open"
            elif query == "roofSwitchOff" and roofStatus == 0:
                answer = "Error: Roof already closed"
            elif query == "extendPadSwitchOn" and bPadStatus == 1:
                answer = "Error: Bottom Pad already extended"
            elif query == "extendPadSwitchOff" and bPadStatus == 0:
                answer = "Error: Bottom Pad already retracted"
            elif query == "raisePadSwitchOn" and tPadStatus == 1:
                answer = "Error: Top Pad already raised"
            elif query == "raisePadSwitchOff" and tPadStatus == 0:
                answer = "Error: Top Pad already lowered"
            else:
                answer = request_search.get(query) or f'No match for "{query}".'

            ###
            if answer == "Opening doors...":
                doorStatus = 1
            elif answer == "Closing doors...":
                doorStatus = 0
            elif answer == "Opening roof...":
                roofStatus = 1
            elif answer == "Closing roof...":
                roofStatus = 0
            elif answer == "Extending pad...":
                bPadStatus = 1
            elif answer == "Retracting pad...":
                bPadStatus = 0
            elif answer == "Raising pad...":
                tPadStatus = 1
            elif answer == "Lowering pad...":
                tPadStatus = 0
                
            
            status = str(doorStatus) + str(roofStatus) + str(bPadStatus) + str(tPadStatus)
            self.refresh()
            answer = answer + status
            content = {"result": answer}
            
        else:
            content = {"result": f'Error: invalid action "{action}".'}
        content_encoding = "utf-8"
        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        
        return response

    def _create_response_binary_content(self):
        response = {
            "content_bytes": b"First 10 bytes of request: "
            + self.request[:10],
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.request is None:
                self.process_request()

    def write(self):
        if self.request:
            if not self.response_created:
                self.create_response()

        self._write()

    def close(self):
        #print("closing connection to", self.addr)
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                f"error: selector.unregister() exception for",
                f"{self.addr}: {repr(e)}",
            )

        try:
            self.sock.close()
        except OSError as e:
            print(
                f"error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def process_protoheader(self):
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(
                ">H", self._recv_buffer[:hdrlen]
            )[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f'Missing required header "{reqhdr}".')

    def process_request(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)
            #print("received request", repr(self.request), "from", self.addr)
        else:
            # Binary or unknown content-type
            self.request = data
            #print(
                #f'received {self.jsonheader["content-type"]} request from',
                #self.addr,
            #)
        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")

    def create_response(self):
        if self.jsonheader["content-type"] == "text/json":
            response = self._create_response_json_content()
        else:
            # Binary or unknown content-type
            response = self._create_response_binary_content()
        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message
