const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const crypto = require('crypto');
const fs = require('fs');

// --- VAULT (AES-256 Encryption) ---
const ALGORITHM = 'aes-256-cbc';
const SECRET_KEY = crypto.scryptSync('universal-manager-secret-stajyer', 'salt', 32);

function encrypt(text) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(ALGORITHM, SECRET_KEY, iv);
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return `${iv.toString('hex')}:${encrypted}`;
}

function decrypt(hash) {
    const parts = hash.split(':');
    const iv = Buffer.from(parts.shift(), 'hex');
    const encryptedText = parts.join(':');
    const decipher = crypto.createDecipheriv(ALGORITHM, SECRET_KEY, iv);
    let decrypted = decipher.update(encryptedText, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}

// --- LOCAL STORAGE (JSON DB) ---
const dbPath = path.join(app.getPath('userData'), 'projects.json');

function readDB() {
    if (!fs.existsSync(dbPath)) return { projects: [] };
    return JSON.parse(fs.readFileSync(dbPath, 'utf8'));
}

function writeDB(data) {
    fs.writeFileSync(dbPath, JSON.stringify(data, null, 2));
}

// --- ELECTRON WINDOW ---
function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false,
            contextIsolation: true,
        },
        titleBarStyle: 'hidden',
        titleBarOverlay: {
            color: '#0a0a0f',
            symbolColor: '#ffffff',
            height: 30
        }
    });

    win.loadFile('src/index.html');
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// --- IPC HANDLERS ---
ipcMain.handle('get-projects', () => {
    const db = readDB();
    // Return safe projection
    return db.projects.map(p => ({
        id: p.id,
        name: p.name,
        description: p.description,
        nodesCount: (p.nodes || []).length
    }));
});

ipcMain.handle('add-project', (event, { name, description }) => {
    const db = readDB();
    const newProject = {
        id: Date.now().toString(),
        name,
        description,
        nodes: []
    };
    db.projects.push(newProject);
    writeDB(db);
    return { success: true, id: newProject.id };
});
