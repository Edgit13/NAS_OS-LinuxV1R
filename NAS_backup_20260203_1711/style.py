STYLE_CSS = '''
<style>
    :root {
        --bg: #0d1117;
        --card-bg: #161b22;
        --border: #30363d;
        --text: #c9d1d9;
        --gray: #8b949e;
        --green: #3fb950;
        --red: #f85149;
        --blue: #58a6ff;
        --yellow: #d29922;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
        background: var(--bg);
        color: var(--text);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    
    .dashboard {
        width: 100%;
        max-width: 500px;
    }
    
    .login-container {
        width: 100%;
        max-width: 400px;
    }
    
    header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    header h1 {
        font-size: 28px;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    
    .card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    .card h3 {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }
    
    .status-dot.online {
        background: var(--green);
        box-shadow: 0 0 8px var(--green);
    }
    
    .status-dot.offline {
        background: var(--red);
    }
    
    .disk-meta {
        color: var(--gray);
        font-size: 13px;
        margin-bottom: 10px;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: var(--border);
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--blue), var(--green));
        transition: width 0.3s ease;
    }
    
    .btn-group {
        display: flex;
        gap: 10px;
    }
    
    .btn {
        flex: 1;
        padding: 10px 16px;
        border-radius: 6px;
        text-align: center;
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
        transition: all 0.2s;
        border: 1px solid var(--border);
    }
    
    .btn-on {
        background: var(--green);
        color: #000;
    }
    
    .btn-on:hover {
        background: #2ea043;
        transform: translateY(-1px);
    }
    
    .btn-off {
        background: var(--card-bg);
        color: var(--red);
        border-color: var(--red);
    }
    
    .btn-off:hover {
        background: var(--red);
        color: #fff;
        transform: translateY(-1px);
    }
    
    /* Login Form Styles */
    .login-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 30px;
    }
    
    .form-group {
        margin-bottom: 20px;
    }
    
    .form-group label {
        display: block;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 8px;
        color: var(--text);
    }
    
    .form-group input {
        width: 100%;
        padding: 12px;
        background: var(--bg);
        border: 1px solid var(--border);
        border-radius: 6px;
        color: var(--text);
        font-size: 14px;
        transition: border-color 0.2s;
    }
    
    .form-group input:focus {
        outline: none;
        border-color: var(--blue);
    }
    
    .btn-login {
        width: 100%;
        padding: 12px;
        background: var(--green);
        color: #000;
        border: none;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .btn-login:hover {
        background: #2ea043;
        transform: translateY(-1px);
    }
    
    .error-msg {
        background: rgba(248, 81, 73, 0.1);
        border: 1px solid var(--red);
        border-radius: 6px;
        padding: 12px;
        margin-bottom: 20px;
        color: var(--red);
        font-size: 14px;
    }
    
    .logout-btn {
        color: var(--red);
        text-decoration: none;
        font-size: 12px;
        font-weight: bold;
    }
    
    .logout-btn:hover {
        text-decoration: underline;
    }
</style>
'''
