from __future__ import annotations
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from .schemas import CalcRequest, CalcResponse
from . import operations as ops
from .logger_setup import configure_logging

configure_logging()
log = logging.getLogger("calculator.app")

app = FastAPI(title="FastAPI Calculator", version="1.0.0")

# Basic CORS in case you open the page from another host
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    log.info("REQ %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
        log.info("RES %s %s -> %s", request.method, request.url.path, response.status_code)
        return response
    except Exception as e:
        log.exception("Unhandled error: %s", e)
        raise

@app.get("/", response_class=HTMLResponse, summary="Simple UI")
def root_ui():
    # Minimal UI so Playwright can simulate user input
    # This calls the /api/calc endpoint via fetch
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Calculator</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 560px; margin: 2rem auto; }
    label { display:block; margin: 0.5rem 0 0.25rem; }
    input, select, button { padding: 0.5rem; font-size: 1rem; }
    .row { display:flex; gap: 0.5rem; align-items: center; }
    #result { margin-top: 1rem; font-weight: 600; }
  </style>
</head>
<body>
  <h1>FastAPI Calculator</h1>
  <div class="row">
    <label for="a">A</label>
    <input id="a" type="number" step="any" value="2" />
    <label for="op">Op</label>
    <select id="op">
      <option value="add">+</option>
      <option value="subtract">−</option>
      <option value="multiply">×</option>
      <option value="divide">÷</option>
      <option value="power">^</option>
    </select>
    <label for="b">B</label>
    <input id="b" type="number" step="any" value="3" />
    <button id="calc">Calculate</button>
  </div>
  <div id="result">Result: <span id="value">—</span></div>

  <script>
    document.getElementById("calc").addEventListener("click", async () => {
      const a = parseFloat(document.getElementById("a").value);
      const b = parseFloat(document.getElementById("b").value);
      const op = document.getElementById("op").value;

      const res = await fetch("/api/calc", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ a, b, op })
      });
      if (!res.ok) {
        const err = await res.json();
        document.getElementById("value").textContent = "Error: " + (err.detail || res.status);
        return;
      }
      const data = await res.json();
      document.getElementById("value").textContent = data.result;
    });
  </script>
</body>
</html>
    """

@app.post("/api/calc", response_model=CalcResponse, summary="Calculate")
def calculate(payload: CalcRequest):
    log.info("Calculate: %s %s %s", payload.a, payload.op, payload.b)
    try:
        result: float
        if payload.op == "add":
            result = ops.add(payload.a, payload.b)
        elif payload.op == "subtract":
            result = ops.subtract(payload.a, payload.b)
        elif payload.op == "multiply":
            result = ops.multiply(payload.a, payload.b)
        elif payload.op == "divide":
            result = ops.divide(payload.a, payload.b)
        elif payload.op == "power":
            result = ops.power(payload.a, payload.b)
        else:
            raise ValueError(f"Unsupported operation {payload.op}")
        log.info("Result: %s", result)
        return CalcResponse(result=result)
    except ZeroDivisionError as zde:
        log.warning("Divide by zero: a=%s b=%s", payload.a, payload.b)
        raise HTTPException(status_code=400, detail=str(zde))
    except Exception as e:
        log.exception("Calculation error")
        raise HTTPException(status_code=400, detail=str(e))
