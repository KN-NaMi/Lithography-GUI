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
            margin: 0;
            padding: 20px;
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
        }
         .port-select {
            background-color: #2a2a2a;
            color: #e8eaed;
            border: 1px solid #444;
            padding: 5px;
            border-radius: 4px;
        }
        .dashboard-title {
            margin: 20px 0;
            font-size: 24px;
        }

        .main-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-top: 20px;
        }

        .panel {
            background-color: #111;
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
            font-size: 20px;
            margin: 0;
        }

        .controls {
            display: flex;
            gap: 8px;
        }

        .camera-view {
            width: 100%;
            height: 300px;
            background-color: #333;
            border-radius: 4px;
        }

        .mask-view {
            width: 100%;
            height: 300px;
            background-color: #fff;
            border-radius: 4px;
        }

        .motion-controls {
            display: flex;
            gap: 20px;
        }
         .motion-layout {
            display: flex;
            gap: 20px;
            align-items: flex-start;
        }

         .position-display {
            background-color: #2a2a2a;
            padding: 15px;
            border-radius: 4px;
            margin-top: 40px; /* Align with the circle */
            width: 200px;
        }

        .mode-section {
            margin-top: 20px;
            padding: 15px;
            background-color: #222;
            border-radius: 4px;
        }

        .input-group {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
        }

        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }

        .container {
            width: 384px;
            height: 384px;
            flex-shrink: 0;
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
           .icon-button {
            background: none;
            border: none;
            padding: 8px;
            cursor: pointer;
            color: #e8eaed;
        }
        
    </style>
</head>
<body>
    <div class="header">
        <h1>NaMi Lithography GUI</h1>
        <button class="icon-button">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 15a3 3 0 1 1 0-6 3 3 0 0 1 0 6Z"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1Z"/>
            </svg>
        </button>
    </div>

    <h1 class="dashboard-title">Dashboard</h1>

    <div class="main-grid">
        <!-- Camera Panel -->
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
            <div class="camera-view"></div>
        </div>

        <!-- Motion Panel -->
    <div class="panel">
        <div class="panel-header">
            <h2 class="panel-title">Motion</h2>
            <div class="controls">
                <select class="port-select">
                        <option>COM1</option>
                        <option>COM2</option>
                        <option>COM3</option>
                        <option>COM4</option>
                        <option>COM5</option>
                        <option>COM6</option>
                        <option>COM7</option>
                        <option>COM8</option>
                </select>
                <button class="icon-button">⚙️</button>
            </div>
        </div>
              <div class="motion-layout">
        <!== kolko -->
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

        <div class="position-display">
            <div class="position-title">Current Position</div>
                <div class="position-inputs">
                    <div class="input-group">
                        <label>X:</label>
                        <input type="number" value="50" readonly>
                    </div>
                    <div class="input-group">
                        <label>Y:</label>
                        <input type="number" value="50" readonly>
                    </div>
                </div>
            <div class="position-title" style="margin-top: 15px;">Set Position</div>
                <div class="position-inputs">
                    <div class="input-group">
                        <label>X:</label>
                        <input type="number" value="50">
                    </div>
                    <div class="input-group">
                        <label>Y:</label>
                        <input type="number" value="50">
                    </div>
                    <button class="btn-start">Set</button>
                </div>
            </div>
        </div>
    </div>

        <!-- Mask Panel -->
        <div class="panel">
            <div class="panel-header">
                <h2 class="panel-title">Mask</h2>
                <div class="controls">
                    <button class="icon-button">↑</button>
                    <button class="icon-button">⚙️</button>
                </div>
            </div>
            <div class="mask-view"></div>
        </div>

        <!-- Projector Panel -->
        <div class="panel">
            <div class="panel-header">
                <h2 class="panel-title">Projector</h2>
                <div class="controls">
                    <select class="port-select">
                        <option>COM1</option>
                        <option>COM2</option>
                        <option>COM3</option>
                        <option>COM4</option>
                        <option>COM5</option>
                        <option>COM6</option>
                        <option>COM7</option>
                        <option>COM8</option>
                    </select>
                    <button class="icon-button">⚙️</button>
                </div>
            </div>
            <div class="mode-section">
                <h3>UV Mode</h3>
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
                    <button style="background-color: #ff4444;">Abort</button>
                    <button style="background-color: #333;">Start</button>
                </div>
            </div>
            <div class="mode-section">
                <h3>RED Mode</h3>
                <div class="input-group">
                    <label>Intensity:</label>
                    <input type="number" value="80" min="0" max="100">
                    <span>%</span>
                </div>
                <div class="button-group">
                    <button style="background-color: #4CAF50;">ON</button>
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