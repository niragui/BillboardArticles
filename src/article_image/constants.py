CSS_TEXT = """
  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #f4f4f4;
      color: #333;
    }

    .container {
      display: flex;
      flex-direction: row;
      max-width: 1400px;
      margin: 40px auto;
      background-color: #fff;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .left-panel {
      width: 30%;
      background-color: #00ff9a;
      padding: 20px;
      border-right: 1px solid #ddd;
    }

    .left-panel h1 {
      font-size: 24px;
      margin-bottom: 10px;
    }

    .left-panel h2 {
      font-size: 18px;
      margin-bottom: 20px;
      color: #666;
    }

    .left-panel img {
      width: 100%;
      height: auto;
      margin-bottom: 20px;
      border-radius: 6px;
    }

    .meta {
      font-size: 14px;
      margin-top: 10px;
      color: #555;
    }

    .right-panel {
      width: 70%;
      padding: 20px;
    }

    .right-panel p {
      line-height: 1.6;
      margin-bottom: 16px;
    }

    @media (max-width: 768px) {
      .container {
        flex-direction: column;
      }

      .left-panel,
      .right-panel {
        width: 100%;
      }

      .left-panel {
        border-right: none;
        border-bottom: 1px solid #ddd;
      }
    }
  </style>
"""