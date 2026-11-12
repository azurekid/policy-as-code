const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const client = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].at(-1)[1];

function startClient({ startupError } = {}) {
  const status = { textContent: 'Connecting...', className: '' };
  const timers = new Map();
  const errors = [];
  let socket;
  let terminal;
  class Terminal {
    constructor() {
      if (startupError) throw startupError;
      terminal = this;
      this.cols = 80;
      this.rows = 24;
    }
    loadAddon() {}
    open() {}
    focus() {}
    write(data) { this.output = data; }
    onData(callback) { this.input = callback; }
    onResize(callback) { this.resize = callback; }
  }
  class WebSocket {
    static OPEN = 1;
    constructor(url) {
      socket = this;
      this.url = url;
      this.readyState = 0;
      this.sent = [];
    }
    send(data) { this.sent.push(data); }
    close() { this.closed = true; this.onclose(); }
  }
  vm.runInNewContext(client, {
    document: { getElementById: () => status },
    window: { location: { protocol: 'https:', host: 'runner.example' } },
    Terminal,
    FitAddon: { FitAddon: class { fit() {} } },
    ResizeObserver: class { observe() {} },
    WebSocket,
    console: { error: (...args) => errors.push(args) },
    setTimeout: (callback, delay) => { timers.set(1, { callback, delay }); return 1; },
    clearTimeout: (id) => timers.delete(id)
  });
  return { status, timers, errors, socket, terminal };
}

test('reports terminal startup errors instead of leaving Connecting displayed', () => {
  const error = new Error('Terminal is not defined');
  const result = startClient({ startupError: error });
  assert.equal(result.status.textContent, `Terminal initialization failed: ${error.message}`);
  assert.equal(result.status.className, 'disconnected');
  assert.equal(result.errors[0][1], error);
  assert.equal(result.socket, undefined);
});

test('bounds a stalled connection and preserves its error after closing', () => {
  const { status, socket, timers, errors } = startClient();
  const timeout = timers.get(1);
  assert.equal(timeout.delay, 15000);
  timeout.callback();
  assert.equal(status.textContent, 'Connection timed out. Reload to reconnect.');
  assert.equal(status.className, 'disconnected');
  assert.equal(socket.closed, true);
  assert.equal(timers.size, 0);
  assert.equal(errors.length, 1);
});

test('reports WebSocket errors without replacing them with Disconnected', () => {
  const { status, socket, timers, errors } = startClient();
  const error = new Error('Handshake failed');
  socket.onerror(error);
  socket.onclose();
  assert.equal(status.textContent, 'Connection failed. Reload to reconnect.');
  assert.equal(status.className, 'disconnected');
  assert.equal(timers.size, 0);
  assert.equal(errors[0][1], error);
});

test('connected terminal still exchanges input, output and resize messages', () => {
  const { status, socket, terminal, timers } = startClient();
  assert.equal(socket.url, 'wss://runner.example');
  socket.readyState = 1;
  socket.onopen();
  assert.equal(status.textContent, 'Connected');
  assert.equal(timers.size, 0);
  assert.deepEqual(JSON.parse(socket.sent[0]), { type: 'resize', cols: 80, rows: 24 });
  terminal.input('echo hello\r');
  assert.equal(socket.sent[1], 'echo hello\r');
  terminal.resize({ cols: 100, rows: 40 });
  assert.deepEqual(JSON.parse(socket.sent[2]), { type: 'resize', cols: 100, rows: 40 });
  socket.onmessage({ data: 'hello\r\n' });
  assert.equal(terminal.output, 'hello\r\n');
  socket.onclose();
  assert.equal(status.textContent, 'Disconnected');
});
