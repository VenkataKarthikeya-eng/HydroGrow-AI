import logging
import sys

def setup_logger(name: str = "hydrogrow") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

app_logger = setup_logger("hydrogrow.app")
ml_logger = setup_logger("hydrogrow.ml")
iot_logger = setup_logger("hydrogrow.iot")
automation_logger = setup_logger("hydrogrow.automation")

def log_api_request(method: str, path: str, status_code: int, duration_ms: float):
    app_logger.info(f"API: {method} {path} | Status: {status_code} | Duration: {duration_ms}ms")

def log_ml_inference(model_name: str, version: str, duration_ms: float, confidence: float):
    ml_logger.info(f"ML: {model_name} ({version}) | Duration: {duration_ms}ms | Confidence: {confidence}%")

def log_iot_event(device_name: str, event_type: str, details: str):
    iot_logger.info(f"IoT: Device '{device_name}' | Event: {event_type} | Details: {details}")

def log_automation_execution(rule_name: str, action: str, result: str):
    automation_logger.info(f"Automation: Rule '{rule_name}' | Action: {action} | Result: {result}")
