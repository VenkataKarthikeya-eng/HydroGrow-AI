import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from backend.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    predictions = relationship("Prediction", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_type = Column(String, default="Lettuce", nullable=False)
    input_parameters = Column(JSON, nullable=False)
    predicted_weight = Column(Float, nullable=False)
    growth_category = Column(String, nullable=False)
    recommendations = Column(JSON, nullable=True)
    explanation = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="predictions")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=False)
    conversation_summary = Column(String, nullable=True)
    last_message_time = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
    message_count = Column(Integer, nullable=True, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False) # "user" or "assistant"
    content = Column(Text, nullable=False)
    sources = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

class SensorDevice(Base):
    __tablename__ = "sensor_devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    device_name = Column(String, nullable=False)
    location = Column(String, default="Grow Room 1", nullable=False)
    device_type = Column(String, default="Hydroponic Tank Sensor", nullable=False)
    status = Column(String, default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", backref="sensor_devices")
    readings = relationship("SensorReading", back_populates="device", cascade="all, delete-orphan")

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("sensor_devices.id", ondelete="CASCADE"), nullable=False, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    water_ph = Column(Float, nullable=False)
    water_ec = Column(Float, nullable=False)
    water_temperature = Column(Float, nullable=False)
    co2 = Column(Float, nullable=False)
    nutrient_level = Column(Float, default=100.0, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    device = relationship("SensorDevice", back_populates="readings")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    alert_type = Column(String, nullable=False) # e.g. "temperature", "water_ph"
    severity = Column(String, nullable=False) # "warning" or "critical"
    parameter = Column(String, nullable=False) # e.g. "Water pH"
    message = Column(String, nullable=False)
    resolved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="alerts")

class AutomationRule(Base):
    __tablename__ = "automation_rules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_name = Column(String, nullable=False)
    parameter = Column(String, nullable=False) # e.g. "temperature", "water_ph", "water_ec", "humidity", "co2"
    condition = Column(String, nullable=False) # "above" or "below"
    threshold_value = Column(Float, nullable=False)
    action_type = Column(String, nullable=False) # e.g. "activate", "deactivate"
    action_value = Column(String, nullable=False) # e.g. "Cooling Fan", "Nutrient Pump", "pH Controller", "Grow Lights"
    enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", backref="automation_rules")

class AutomationEvent(Base):
    __tablename__ = "automation_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_id = Column(Integer, ForeignKey("automation_rules.id", ondelete="SET NULL"), nullable=True, index=True)
    sensor_reading_id = Column(Integer, ForeignKey("sensor_readings.id", ondelete="SET NULL"), nullable=True, index=True)
    event_type = Column(String, nullable=False) # e.g. "device_actuation"
    message = Column(String, nullable=False)
    status = Column(String, default="executed", nullable=False) # e.g. "executed", "failed"
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="automation_events")
    rule = relationship("AutomationRule", backref="events")
    reading = relationship("SensorReading", backref="automation_events")

class CropCycle(Base):
    __tablename__ = "crop_cycles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_name = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    current_stage = Column(String, default="Seedling", nullable=False) # "Seedling", "Vegetative", "Maturity", "Harvest"
    expected_harvest_date = Column(DateTime, nullable=False)
    growth_progress = Column(Float, default=0.0, nullable=False) # 0.0 to 100.0
    status = Column(String, default="active", nullable=False) # "active", "completed"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", backref="crop_cycles")

class PlantImage(Base):
    __tablename__ = "plant_images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    image_path = Column(String, nullable=False)
    crop_type = Column(String, default="lettuce", nullable=False)
    growth_stage = Column(String, default="Seedling", nullable=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="plant_images")
    analysis = relationship("PlantAnalysis", back_populates="image", uselist=False, cascade="all, delete-orphan")
    growth_observations = relationship("GrowthObservation", back_populates="image", cascade="all, delete-orphan")

class PlantAnalysis(Base):
    __tablename__ = "plant_analyses"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("plant_images.id", ondelete="CASCADE"), nullable=False, index=True)
    disease_name = Column(String, default="Healthy", nullable=False)
    confidence_score = Column(Float, default=1.0, nullable=False)
    severity = Column(String, default="None", nullable=False) # e.g. "Low", "Medium", "High", "None"
    health_score = Column(Float, default=100.0, nullable=False)
    nutrient_status = Column(JSON, nullable=True) # e.g. {"nitrogen": "Optimal", "calcium": "Warning"}
    recommendations = Column(JSON, nullable=True) # e.g. ["suggestion 1", "suggestion 2"]
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    image = relationship("PlantImage", back_populates="analysis")

class GrowthObservation(Base):
    __tablename__ = "growth_observations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    image_id = Column(Integer, ForeignKey("plant_images.id", ondelete="CASCADE"), nullable=False, index=True)
    height_estimate = Column(Float, default=0.0, nullable=False) # in cm
    leaf_area_estimate = Column(Float, default=0.0, nullable=False) # in cm^2
    growth_stage = Column(String, default="Seedling", nullable=False)
    growth_score = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="growth_observations")
    image = relationship("PlantImage", back_populates="growth_observations")

class DigitalTwinProfile(Base):
    __tablename__ = "digital_twin_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    farm_name = Column(String, nullable=False)
    crop_type = Column(String, default="Lettuce", nullable=False)
    system_type = Column(String, nullable=False) # e.g. "NFT Hydroponics"
    area_size = Column(Float, nullable=False)
    lighting_setup = Column(String, nullable=False)
    nutrient_system = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="digital_twin_profiles")
    simulations = relationship("SimulationRun", back_populates="profile", cascade="all, delete-orphan")

class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    profile_id = Column(Integer, ForeignKey("digital_twin_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    scenario_name = Column(String, nullable=False) # e.g. "Increase nutrients"
    duration_days = Column(Integer, default=30, nullable=False)
    initial_conditions = Column(JSON, nullable=False) # e.g. {"temperature": 25, "humidity": 60, "co2": 450, "water_ph": 6.2, "water_ec": 2.0}
    final_prediction = Column(JSON, nullable=False) # e.g. {"weight": 420.0, "height": 32.0, "health": 94.0}
    yield_change_percentage = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="simulation_runs")
    profile = relationship("DigitalTwinProfile", back_populates="simulations")
    parameters = relationship("SimulationParameters", back_populates="simulation", cascade="all, delete-orphan")
    forecasts = relationship("GrowthForecast", back_populates="simulation", cascade="all, delete-orphan")

class SimulationParameters(Base):
    __tablename__ = "simulation_parameters"

    id = Column(Integer, primary_key=True, index=True)
    simulation_id = Column(Integer, ForeignKey("simulation_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    parameter_name = Column(String, nullable=False) # e.g. "Temperature", "EC"
    original_value = Column(Float, nullable=False)
    modified_value = Column(Float, nullable=False)
    impact_score = Column(Float, default=0.0, nullable=False) # yield difference e.g. +15.0%

    # Relationships
    simulation = relationship("SimulationRun", back_populates="parameters")

class GrowthForecast(Base):
    __tablename__ = "growth_forecasts"

    id = Column(Integer, primary_key=True, index=True)
    simulation_id = Column(Integer, ForeignKey("simulation_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    day_number = Column(Integer, nullable=False)
    predicted_height = Column(Float, nullable=False)
    predicted_weight = Column(Float, nullable=False)
    health_score = Column(Float, nullable=False)
    growth_stage = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    simulation = relationship("SimulationRun", back_populates="forecasts")

class FarmDecision(Base):
    __tablename__ = "farm_decisions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    decision_type = Column(String, nullable=False) # e.g. "Climate", "Nutrition", "Disease", "Yield"
    priority = Column(String, default="MEDIUM", nullable=False) # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    title = Column(String, nullable=False)
    analysis = Column(String, nullable=False)
    recommended_action = Column(String, nullable=False)
    confidence_score = Column(Float, default=0.0, nullable=False)
    status = Column(String, default="Pending", nullable=False) # "Pending", "Executed", "Dismissed"
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="farm_decisions")
    histories = relationship("RecommendationHistory", back_populates="decision", cascade="all, delete-orphan")

class AgentExecutionLog(Base):
    __tablename__ = "agent_execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_name = Column(String, nullable=False) # "CropAgent", "ClimateAgent", "DiseaseAgent", "NutritionAgent", "OptimizationAgent"
    input_context = Column(JSON, nullable=False)
    output_result = Column(JSON, nullable=False)
    execution_time = Column(Float, default=0.0, nullable=False) # runtime in seconds
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="agent_execution_logs")

class RecommendationHistory(Base):
    __tablename__ = "recommendation_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    decision_id = Column(Integer, ForeignKey("farm_decisions.id", ondelete="CASCADE"), nullable=False, index=True)
    action_taken = Column(String, nullable=False)
    feedback = Column(String, nullable=False) # "Helpful", "Not Helpful", "Completed", "Ignored"
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="recommendation_histories")
    decision = relationship("FarmDecision", back_populates="histories")

class MLModel(Base):
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False) # e.g. "GrowthPrediction", "DiseaseDetection", "HealthClassification"
    model_type = Column(String, nullable=False) # e.g. "Regression", "Classification", "Hybrid"
    version = Column(String, nullable=False) # e.g. "1.0.0"
    algorithm = Column(String, nullable=False) # e.g. "RandomForestRegressor", "GradientBoosting", "CNN_Classifier"
    accuracy_score = Column(Float, default=0.0, nullable=False) # e.g. 0.94 / R2 0.92
    training_dataset = Column(String, nullable=False)
    model_path = Column(String, nullable=False) # file path to joblib binary
    status = Column(String, default="Active", nullable=False) # "Active", "Archived", "Training"
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class TrainingDataset(Base):
    __tablename__ = "training_datasets"

    id = Column(Integer, primary_key=True, index=True)
    dataset_name = Column(String, nullable=False)
    dataset_type = Column(String, nullable=False) # "Agronomic Predictors", "Leaf Pathology Images"
    source = Column(String, nullable=False)
    sample_count = Column(Integer, default=0, nullable=False)
    features = Column(JSON, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class ModelPredictionLog(Base):
    __tablename__ = "model_prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    model_id = Column(Integer, ForeignKey("ml_models.id", ondelete="SET NULL"), nullable=True, index=True)
    input_data = Column(JSON, nullable=False)
    prediction_output = Column(JSON, nullable=False)
    confidence_score = Column(Float, default=0.0, nullable=False)
    inference_time = Column(Float, default=0.0, nullable=False) # latency in milliseconds
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="model_prediction_logs")
    model = relationship("MLModel", backref="prediction_logs")

class IoTDeviceCredential(Base):
    __tablename__ = "iot_device_credentials"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    api_key_hash = Column(String, nullable=False)
    device_type = Column(String, nullable=False) # e.g. "ESP32", "Raspberry Pi", "Arduino"
    location = Column(String, default="Zone 1 - Hydroponics", nullable=False)
    last_seen = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    status = Column(String, default="Active", nullable=False) # "Active", "Offline", "Revoked"
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="iot_device_credentials")

class DeviceTelemetryLog(Base):
    __tablename__ = "device_telemetry_logs"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, nullable=False, index=True)
    sensor_data = Column(JSON, nullable=False)
    received_timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    processing_status = Column(String, default="Processed", nullable=False) # "Processed", "Filtered", "Error"

class CloudDeploymentLog(Base):
    __tablename__ = "cloud_deployment_logs"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, nullable=False) # e.g. "FastAPI Backend", "PostgreSQL", "React Static", "MLOps Engine"
    deployment_version = Column(String, nullable=False) # e.g. "v1.3.0"
    status = Column(String, default="Healthy", nullable=False) # "Healthy", "Warning", "Degraded"
    health_check = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class MLTrainingJob(Base):
    __tablename__ = "ml_training_jobs"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False) # e.g. "GrowthPrediction", "DiseaseDetection"
    dataset_id = Column(Integer, ForeignKey("training_datasets.id", ondelete="SET NULL"), nullable=True)
    training_status = Column(String, default="In_Progress", nullable=False) # "In_Progress", "Completed", "Failed"
    accuracy_score = Column(Float, default=0.0, nullable=False)
    started_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    dataset = relationship("TrainingDataset", backref="training_jobs")

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    farm_name = Column(String, nullable=False)
    location = Column(String, default="Main Facility", nullable=False)
    farm_size = Column(Float, default=100.0, nullable=False) # Area in sq meters
    farm_type = Column(String, default="Hydroponic NFT", nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    owner = relationship("User", backref="owned_farms")
    members = relationship("FarmMember", back_populates="farm", cascade="all, delete-orphan")
    greenhouses = relationship("Greenhouse", back_populates="farm", cascade="all, delete-orphan")
    subscriptions = relationship("FarmSubscription", back_populates="farm", cascade="all, delete-orphan")
    activity_logs = relationship("FarmActivityLog", back_populates="farm", cascade="all, delete-orphan")

class FarmMember(Base):
    __tablename__ = "farm_members"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String, default="WORKER", nullable=False) # "OWNER", "MANAGER", "WORKER", "VIEWER"
    joined_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    farm = relationship("Farm", back_populates="members")
    user = relationship("User", backref="farm_memberships")

class Greenhouse(Base):
    __tablename__ = "greenhouses"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False)
    area_size = Column(Float, default=50.0, nullable=False)
    environment_type = Column(String, default="NFT Hydroponics", nullable=False)
    automation_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    farm = relationship("Farm", back_populates="greenhouses")

class CropTemplate(Base):
    __tablename__ = "crop_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    crop_type = Column(String, default="Lettuce", nullable=False)
    growth_duration = Column(Integer, default=35, nullable=False) # Days
    optimal_temperature = Column(Float, default=22.0, nullable=False)
    optimal_ph = Column(Float, default=6.2, nullable=False)
    optimal_ec = Column(Float, default=2.0, nullable=False)
    nutrient_profile = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class FarmSubscription(Base):
    __tablename__ = "farm_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    plan = Column(String, default="FREE", nullable=False) # "FREE", "BASIC", "PRO", "ENTERPRISE"
    max_devices = Column(Integer, default=3, nullable=False)
    max_users = Column(Integer, default=2, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    farm = relationship("Farm", back_populates="subscriptions")

class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, default="General", nullable=False)
    content = Column(String, nullable=False)
    crop_type = Column(String, default="Lettuce", nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class FarmActivityLog(Base):
    __tablename__ = "farm_activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String, nullable=False)
    description = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    farm = relationship("Farm", back_populates="activity_logs")

class ExpertProfile(Base):
    __tablename__ = "expert_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    expertise_area = Column(String, nullable=False) # e.g. "Pathology", "Hydroponic Solution Chemistry", "HVAC Climate"
    experience_years = Column(Integer, default=5, nullable=False)
    certification = Column(String, default="Certified Agronomist", nullable=False)
    bio = Column(String, nullable=True)
    rating = Column(Float, default=4.9, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="expert_profile")

class FarmerCommunity(Base):
    __tablename__ = "farmer_communities"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, default="General Farming", nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    creator = relationship("User", backref="created_communities")
    posts = relationship("CommunityPost", back_populates="community", cascade="all, delete-orphan")

class CommunityPost(Base):
    __tablename__ = "community_posts"

    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("farmer_communities.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    likes = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    community = relationship("FarmerCommunity", back_populates="posts")
    user = relationship("User", backref="community_posts")

class MarketplaceProduct(Base):
    __tablename__ = "marketplace_products"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    product_name = Column(String, nullable=False)
    category = Column(String, default="Nutrients & Concentrates", nullable=False) # e.g. "Nutrients", "Sensors", "Lighting", "Seeds"
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    availability = Column(Boolean, default=True, nullable=False)
    rating = Column(Float, default=4.8, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    seller = relationship("User", backref="marketplace_products")

class CropTemplateLibrary(Base):
    __tablename__ = "crop_template_libraries"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_name = Column(String, nullable=False)
    variety = Column(String, default="Butterhead", nullable=False)
    nutrient_profile = Column(JSON, nullable=False)
    environmental_profile = Column(JSON, nullable=False)
    growth_duration = Column(Integer, default=35, nullable=False)
    success_rate = Column(Float, default=95.0, nullable=False)
    downloads = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    creator = relationship("User", backref="created_templates")

class ExpertRecommendation(Base):
    __tablename__ = "expert_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_type = Column(String, default="Lettuce", nullable=False)
    recommendation = Column(String, nullable=False)
    source = Column(String, default="AI Knowledge Engine", nullable=False)
    confidence_score = Column(Float, default=95.0, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="expert_recommendations")

class FarmIntelligenceScore(Base):
    __tablename__ = "farm_intelligence_scores"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    productivity_score = Column(Float, default=92.5, nullable=False)
    sustainability_score = Column(Float, default=88.0, nullable=False)
    automation_score = Column(Float, default=95.0, nullable=False)
    health_score = Column(Float, default=90.0, nullable=False)
    overall_score = Column(Float, default=91.4, nullable=False)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    farm = relationship("Farm", backref="intelligence_scores")

class CropProfitAnalysis(Base):
    __tablename__ = "crop_profit_analyses"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_name = Column(String, default="Butterhead Lettuce", nullable=False)
    production_cost = Column(Float, default=1.20, nullable=False) # cost per kg/head
    estimated_income = Column(Float, default=3.50, nullable=False) # price per kg/head
    profit_margin = Column(Float, default=65.7, nullable=False) # %
    market_demand_score = Column(Float, default=94.0, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    farm = relationship("Farm", backref="profit_analyses")

class MarketTrend(Base):
    __tablename__ = "market_trends"

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String, nullable=False, index=True)
    region = Column(String, default="North America", nullable=False)
    demand_score = Column(Float, default=92.0, nullable=False)
    price_prediction = Column(Float, default=3.75, nullable=False)
    trend_direction = Column(String, default="RISING", nullable=False) # RISING, STABLE, FALLING
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class FarmStrategyPlan(Base):
    __tablename__ = "farm_strategy_plans"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    strategy_type = Column(String, nullable=False) # e.g., "Yield Expansion", "Energy Cost Reduction", "Automation Upgrade"
    recommendation = Column(String, nullable=False)
    priority = Column(String, default="HIGH", nullable=False) # CRITICAL, HIGH, MEDIUM, LOW
    confidence_score = Column(Float, default=95.0, nullable=False)
    expected_impact = Column(String, nullable=False) # e.g. "+15% Yield Increase, -$450 Monthly Power Cost"
    status = Column(String, default="ACTIVE", nullable=False) # ACTIVE, COMPLETED, ARCHIVED
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    # Relationships
    farm = relationship("Farm", backref="strategy_plans")
