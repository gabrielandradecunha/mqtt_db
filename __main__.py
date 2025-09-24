import sys
import os
from dotenv import load_dotenv

load_dotenv()
app_port = os.getenv('APP_PORT', 8090)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    import uvicorn
    # Passar o aplicativo como uma string de importação
    uvicorn.run("main:app", host="0.0.0.0", port=int(app_port), reload=True)