import webview
import os

class Api:
    def button_click(self, label):
        print(f"Button clicked: {label}")
        return f"You clicked {label}!"

html_content = """
<!DOCTYPE html>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NaMi Lithography GUI</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1a1a1a;
            color: #e8eaed;
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo img {
            width: 40px;
            height: 40px;
        }

        .camera-view {
            width: 100%;
            height: 300px;
            background-color: #333;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .container {
            width: 384px;
            height: 384px;
        }

        .circle-wrapper {
            width: 100%;
            height: 100%;
            position: relative;
            color: white;
        }

        .circle-container {
            transform: rotate(45deg);
            width: 100%;
            height: 100%;
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 4px;
            border-radius: 50%;
            overflow: hidden;
        }

        .mask-view {
            width: 100%;
            height: 300px;
            background-color: #fff;
            border-radius: 4px;
            overflow: hidden;
            top:25%;
            right:25%;
        }

        .inner-circle {
            position: absolute;
            z-index: 10;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(45deg);
            width: 60%;
            height: 60%;
        }

        .circle-button {
            background-color: #333;
            border: none;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }

        .outer-circle .circle-button {
            background-color: #1f1f1f;
            color: white;
        }

        .button-content {
            transform: rotate(-45deg);
        }

        .mr-20 { margin-right: 20%; }
        .mb-20 { margin-bottom: 20%; }
        .ml-20 { margin-left: 20%; }
        .mt-20 { margin-top: 20%; }

        .center-content {
            position: absolute;
            z-index: 20;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 8px;
            border-radius: 50%;
            display: grid;
            justify-content: center;
            align-items: center;
            gap: 8px;
            place-items: center;
            grid-template-areas:
                ". Y ."
                "-X home X"
                ". -Y .";
        }

        .axis-label {
            font-size: 1.25rem;
            font-weight: bold;
        }

        .home-button {
            background-color: black;
            padding: 8px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            grid-area: home;
        }

        .panel {
        z-index:1;
        display:flex;
        justify-content: space-between;
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 20px;
        }

        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .panel-title {
            font-size: 1.25rem;
            font-weight: bold;
            margin: 0;

        }
        .controls {
            display: flex;
            gap: 8px;
        }

        .icon-button {
            background: none;
            border: none;
            padding: 8px;
            cursor: pointer;
            color: #e8eaed;
        }

        .custom-select {
            position: relative;
            min-width: 120px;
            font-family: Arial, sans-serif;
            width: 200px;
        }

        .select-button {
            background-color: #2a2a2a;
            color: #e8eaed;
            padding: 8px 16px;
            border: 1px solid #444;
            border-radius: 4px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            font-size: 14px;
        }

        .select-button:hover {
            background-color: #333;
        }

        .select-button svg {
            width: 16px;
            height: 16px;
            margin-left: 8px;
            transition: transform 0.2s;
        }

        .select-button.active svg {
            transform: rotate(180deg);
        }

        .options-list {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background-color: #2a2a2a;
            border: 1px solid #444;
            border-radius: 4px;
            margin-top: 4px;
            max-height: 200px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
        }

        .options-list.show {
            display: block;
        }

        .option-item {
            padding: 8px 16px;
            cursor: pointer;
            display: flex;
            align-items: center;
            color: #e8eaed;
        }

        .option-item:hover {
            background-color: #333;
        }

        .option-item.selected {
            background-color: #404040;
        }

        .status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
        }

        .status-connected {
            background-color: #4CAF50;
        }

        .status-disconnected {
            background-color: #f44336;
        }

        .option-info {
            display: flex;
            flex-direction: column;
            font-size: 12px;
        }

        .option-name {
            font-weight: bold;
        }

        .option-description {
            color: #888;
            font-size: 11px;
        }

        .bar{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
        }
        
    </style>
</head>
<body>

    <div class="header">
        <div class="logo">
            <h1>NaMi Lithography GUI</h1> 
            
        </div>
        <button class="icon-button">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 15a3 3 0 1 1 0-6 3 3 0 0 1 0 6Z"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1Z"/>
            </svg>
        </button>
    </div>

    <div class="bar">
    <h2> Dashboard </h2>
    </div>

    <div class="custom-select">
        <button class="select-button">
            <span>Select Port</span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
        </button>
        <div class="options-list">
            <div class="option-item" data-value="COM1">
                <span class="status-indicator status-connected"></span>
                <div class="option-info">
                    <span class="option-name">COM1</span>
                    <span class="option-description">Camera Controller</span>
                </div>
            </div>
            <div class="option-item" data-value="COM2">
                <span class="status-indicator status-disconnected"></span>
                <div class="option-info">
                    <span class="option-name">COM2</span>
                    <span class="option-description">Motion Controller</span>
                </div>
            </div>
            <div class="option-item" data-value="COM3">
                <span class="status-indicator status-connected"></span>
                <div class="option-info">
                    <span class="option-name">COM3</span>
                    <span class="option-description">UV Projector</span>
                </div>
            </div>
            <div class="option-item" data-value="COM4">
                <span class="status-indicator status-connected"></span>
                <div class="option-info">
                    <span class="option-name">COM4</span>
                    <span class="option-description">RED Light</span>
                </div>
            </div>
        </div>
    </div>


    <div>
        <h1>Motion</h1>
        <div class="container">
            <div class="circle-wrapper">
                <div class="circle-container outer-circle">
                    <button class="circle-button" data-value="+10">
                        <div class="button-content mr-20 mb-20">+10</div>
                    </button>
                    <button class="circle-button" data-value="+10">
                        <div class="button-content ml-20 mb-20">+10</div>
                    </button>
                    <button class="circle-button" data-value="-10">
                        <div class="button-content mr-20 mt-20">-10</div>
                    </button>
                    <button class="circle-button" data-value="-10">
                        <div class="button-content mt-20 ml-20">-10</div>
                    </button>
                </div>

                <div class="circle-container inner-circle">
                    <button class="circle-button" data-value="+1">
                        <div class="button-content mr-20 mb-20">+1</div>
                    </button>
                    <button class="circle-button" data-value="+1">
                        <div class="button-content ml-20 mb-20">+1</div>
                    </button>
                    <button class="circle-button" data-value="-1">
                        <div class="button-content mr-20 mt-20">-1</div>
                    </button>
                    <button class="circle-button" data-value="-1">
                        <div class="button-content mt-20 ml-20">-1</div>
                    </button>
                </div>

                <div class="center-content">
                    <span class="axis-label" style="grid-area: X;">X</span>
                    <span class="axis-label" style="grid-area: Y;">Y</span>
                    <span class="axis-label" style="grid-area: -X;">-X</span>
                    <span class="axis-label" style="grid-area: -Y;">-Y</span>

                    <button class="home-button" data-value="home">
                        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed">
                            <path d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="panel">
            <div class="panel-header">
                <h2 class="panel-title">Mask</h2>
                <div class="controls">
                    <button class="icon-button">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="7 10 12 15 17 10"/>
                            <line x1="12" y1="15" x2="12" y2="3"/>
                        </svg>
                    </button>
                    <button class="icon-button">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 15a3 3 0 1 1 0-6 3 3 0 0 1 0 6Z"/>
                            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1Z"/>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="mask-view"></div>
        </div>

        <div class="panel">
            <div class="panel-header">
                <h2 class="panel-title">Projector</h2>
                <div class="controls">
                    <select class="port-select">
                        <option>COM5</option>
                    </select>
                    <button class="icon-button">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 15a3 3 0 1 1 0-6 3 3 0 0 1 0 6Z"/>
                            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1Z"/>
                        </svg>
                    </button>
                </div>
            </div>
            
            <div class="panel">
                <div class="panel-header">
                    <h2 class="panel-title">Camera</h2>
                    <div class="controls">
                        
                        <button class="icon-button">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>
                            </svg>
                        </button>
                        <button class="icon-button">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                                <circle cx="12" cy="13" r="4"/>
                            </svg>
                        </button>
                    </div>
                </div>
            <div class="camera-view">camera view</div>
        </div>


            <div class="mode-section">
                <h3 class="mode-title">UV Mode</h3>
                <div class="input-group">
                    <label>Expose Time:</label>
                    <input type="number" value="3000" min="0" step="100">
                    <span>ms</span>
                </div>
                <div class="input-group">
                    <input type="range" min="0" max="100" value="30">
                    <span>30%</span>
                </div>
                <div class="button-group">
                    <button class="btn-abort">Abort</button>
                    <button class="btn-start">Start</button>
                </div>
            </div>

            <div class="mode-section">
                <h3 class="mode-title">RED Mode</h3>
                <div class="input-group">
                    <label>Intensity:</label>
                    <input type="number" value="80" min="0" max="100">
                    <span>%</span>
                </div>
                <div class="button-group">
                    <button class="btn-on">ON</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
     document.addEventListener('DOMContentLoaded', function() {
            const selectButton = document.querySelector('.select-button');
            const optionsList = document.querySelector('.options-list');
            const options = document.querySelectorAll('.option-item');

            // Toggle dropdown
            selectButton.addEventListener('click', function() {
                selectButton.classList.toggle('active');
                optionsList.classList.toggle('show');
            });

            // Select option
            options.forEach(option => {
                option.addEventListener('click', function() {
                    // Remove selected class from all options
                    options.forEach(opt => opt.classList.remove('selected'));
                    // Add selected class to clicked option
                    this.classList.add('selected');
                    // Update button text
                    selectButton.querySelector('span').textContent = 
                        this.querySelector('.option-name').textContent;
                    // Hide dropdown
                    optionsList.classList.remove('show');
                    selectButton.classList.remove('active');

                    // You can add your custom handling here
                    console.log('Selected port:', this.dataset.value);
                });
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', function(e) {
                if (!selectButton.contains(e.target) && !optionsList.contains(e.target)) {
                    optionsList.classList.remove('show');
                    selectButton.classList.remove('active');
                }
            });
        });
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    api = Api()
    webview.create_window("Circle Menu", html=html_content, js_api=api)
    webview.start()