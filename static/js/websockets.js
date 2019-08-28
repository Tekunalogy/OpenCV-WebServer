class Socket {
    constructor(path) {
        this._url = `ws://${location.host}${path}`;
        this._socket = new WebSocket(this._url);
        this._messageQueue = [];

        this._socket.onopen = () => this._messageQueue.forEach(this.send);
    }

    isOpen() { return this._socket.readyState === WebSocket.OPEN; }

    isClosed() { return this._socket.readyState === WebSocket.CLOSED; }

    isConnecting() { return this._socket.readyState === WebSocket.CONNECTING; }

    close() {
        if (this.isOpen()) {
            this._socket.close();
        }
    }

    onRecv(callback) {
        this._socket.onmessage = callback;
    }

    send(obj) {
        const message = JSON.stringify(obj);
        if (this.isOpen()) {
            this._socket.send(message);
        } else if (this.isConnecting()) {
            this._messageQueue.push(message);
        } else {
            // ?
        }
    }
}
