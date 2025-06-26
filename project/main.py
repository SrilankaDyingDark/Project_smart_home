from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from typing import List
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from collections import defaultdict
import numpy as np
from scipy.stats import pearsonr
from typing import Dict, Any, List
from datetime import datetime

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ 用户 CRUD ------------------ #
@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users", response_model=List[schemas.User])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, updated: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated.dict().items():
        setattr(user, key, value)
    db.commit()
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}

# ------------------ 设备 CRUD ------------------ #
@app.post("/devices", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@app.get("/devices", response_model=List[schemas.Device])
def list_devices(db: Session = Depends(get_db)):
    return db.query(models.Device).all()

@app.put("/devices/{device_id}", response_model=schemas.Device)
def update_device(device_id: int, updated: schemas.DeviceCreate, db: Session = Depends(get_db)):
    device = db.query(models.Device).get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    for key, value in updated.dict().items():
        setattr(device, key, value)
    db.commit()
    return device

@app.delete("/devices/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(models.Device).get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
    return {"detail": "Device deleted"}

# ------------------ 使用记录 CRUD ------------------ #
@app.post("/usagelogs", response_model=schemas.UsageLog)
def create_usage_log(log: schemas.UsageLogCreate, db: Session = Depends(get_db)):
    db_log = models.UsageLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@app.get("/usagelogs", response_model=List[schemas.UsageLog])
def list_usage_logs(db: Session = Depends(get_db)):
    return db.query(models.UsageLog).all()

@app.put("/usagelogs/{log_id}", response_model=schemas.UsageLog)
def update_usage_log(log_id: int, updated_log: schemas.UsageLogCreate, db: Session = Depends(get_db)):
    log = db.query(models.UsageLog).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Usage log not found")
    for key, value in updated_log.dict().items():
        setattr(log, key, value)
    db.commit()
    db.refresh(log)
    return log

@app.delete("/usagelogs/{log_id}")
def delete_usage_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(models.UsageLog).get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Usage log not found")
    db.delete(log)
    db.commit()
    return {"detail": "Usage log deleted"}

# ------------------ 安防事件 CRUD ------------------ #
@app.post("/securityevents", response_model=schemas.SecurityEvent)
def create_event(event: schemas.SecurityEventCreate, db: Session = Depends(get_db)):
    db_event = models.SecurityEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/securityevents", response_model=List[schemas.SecurityEvent])
def list_events(db: Session = Depends(get_db)):
    return db.query(models.SecurityEvent).all()

@app.put("/securityevents/{event_id}", response_model=schemas.SecurityEvent)
def update_event(event_id: int, updated: schemas.SecurityEventCreate, db: Session = Depends(get_db)):
    event = db.query(models.SecurityEvent).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Security event not found")
    for key, value in updated.dict().items():
        setattr(event, key, value)
    db.commit()
    return event

@app.delete("/securityevents/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.SecurityEvent).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Security event not found")
    db.delete(event)
    db.commit()
    return {"detail": "Security event deleted"}

# ------------------ 用户反馈 CRUD ------------------ #
@app.post("/feedbacks", response_model=schemas.Feedback)
def create_feedback(fb: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    db_fb = models.Feedback(**fb.dict())
    db.add(db_fb)
    db.commit()
    db.refresh(db_fb)
    return db_fb

@app.get("/feedbacks", response_model=List[schemas.Feedback])
def list_feedbacks(db: Session = Depends(get_db)):
    return db.query(models.Feedback).all()

@app.put("/feedbacks/{feedback_id}", response_model=schemas.Feedback)
def update_feedback(feedback_id: int, updated: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).get(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    for key, value in updated.dict().items():
        setattr(feedback, key, value)
    db.commit()
    return feedback

@app.delete("/feedbacks/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).get(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    db.delete(feedback)
    db.commit()
    return {"detail": "Feedback deleted"}

# ------------------ 分析 API ------------------ #
# ------------------ 设备使用频率及时间段分析接口 ------------------ #
@app.get("/analysis/device-usage")
def analyze_device_usage(db: Session = Depends(get_db)):
    usage_logs = db.query(models.UsageLog).all()
    devices = db.query(models.Device).all()
    device_map = {device.id: device.name for device in devices}

    daily_usage_freq = defaultdict(lambda: defaultdict(int))
    hourly_distribution = defaultdict(lambda: defaultdict(int))

    for log in usage_logs:
        device_name = device_map.get(log.device_id, "Unknown")

        if log.start_time:
            day = log.start_time.date()
            daily_usage_freq[device_name][str(day)] += 1

        # 小时分布
        if log.start_time and log.finish_time:
            start_hour = log.start_time.hour
            end_hour = log.finish_time.hour
            for hour in range(start_hour, end_hour + 1):
                hourly_distribution[device_name][hour] += 1

    # 计算每天平均使用频率
    average_daily_freq = {}
    for device, day_counts in daily_usage_freq.items():
        total_usage = sum(day_counts.values())
        num_days = len(day_counts)
        average = total_usage / num_days if num_days else 0
        average_daily_freq[device] = round(average, 2)

    result = {
        "daily_usage_frequency": {
            device: dict(date_counts) for device, date_counts in daily_usage_freq.items()
        },
        "average_daily_frequency": average_daily_freq,
        "hourly_distribution": {
            device: dict(hour_dist) for device, hour_dist in hourly_distribution.items()
        }
    }
    return result

# ------------------ 设备同时使用情况分析接口 ------------------ #
from sqlalchemy import and_

@app.get("/analysis/device-cousage")
def analyze_device_cousage(db: Session = Depends(get_db)):
    logs = db.query(models.UsageLog).all()
    device_map = {device.id: device.name for device in db.query(models.Device).all()}

    co_usage = defaultdict(lambda: defaultdict(int))

    user_logs = defaultdict(list)
    for log in logs:
        user_logs[log.user_id].append(log)

    for logs_per_user in user_logs.values():
        # 按开始时间排序
        logs_per_user.sort(key=lambda x: x.start_time)
        n = len(logs_per_user)

        for i in range(n):
            for j in range(i + 1, n):
                log1 = logs_per_user[i]
                log2 = logs_per_user[j]

                # 判断是否时间重叠（存在交集）
                if log1.finish_time >= log2.start_time and log2.finish_time >= log1.start_time:
                    name1 = device_map.get(log1.device_id, f"Device {log1.device_id}")
                    name2 = device_map.get(log2.device_id, f"Device {log2.device_id}")
                    if name1 != name2:
                        co_usage[name1][name2] += 1
                        co_usage[name2][name1] += 1 

    # 将 defaultdict 转为普通 dict 输出
    result = {k: dict(v) for k, v in co_usage.items()}
    return {"co_usage": result}

# ------------------ 3 ------------------ #
def classify_correlation(corr: float) -> str:
    """将皮尔逊系数转化为语言描述"""
    if abs(corr) > 0.7:
        return "强相关"
    elif abs(corr) > 0.4:
        return "中相关"
    elif abs(corr) > 0.2:
        return "弱相关"
    else:
        return "无明显相关"

@app.get("/analysis/area-vs-usage", response_model=Dict[str, Any])
def analyze_area_vs_usage(db: Session = Depends(get_db)):
    user_usage = defaultdict(int)
    user_area = {}

    users = db.query(models.User).all()
    for user in users:
        if user.house_area:
            user_area[user.id] = user.house_area

    logs = db.query(models.UsageLog).all()
    for log in logs:
        user_usage[log.user_id] += 1

    data = []
    for uid in user_usage:
        if uid in user_area:
            data.append({
                "user_id": uid,
                "house_area": user_area[uid],
                "usage_count": user_usage[uid]
            })

    if not data:
        return {"message": "无足够数据进行分析"}

    areas = [d["house_area"] for d in data]
    usages = [d["usage_count"] for d in data]

    # 相关性分析
    corr, _ = pearsonr(areas, usages)
    correlation_strength = classify_correlation(corr)

    # 分区域分组分析（划分小/中/大房型）
    area_groups = {
        "小户型 (<=80㎡)": [],
        "中户型 (81-120㎡)": [],
        "大户型 (>120㎡)": []
    }
    for d in data:
        if d["house_area"] <= 80:
            area_groups["小户型 (<=80㎡)"].append(d["usage_count"])
        elif d["house_area"] <= 120:
            area_groups["中户型 (81-120㎡)"].append(d["usage_count"])
        else:
            area_groups["大户型 (>120㎡)"].append(d["usage_count"])

    area_stats = {
        label: {
            "user_count": len(usages),
            "avg_usage": float(np.mean(usages)) if usages else 0
        }
        for label, usages in area_groups.items()
    }

    # 异常用户识别
    usage_mean = np.mean(usages)
    usage_std = np.std(usages)
    threshold_low = usage_mean - 1.2 * usage_std
    threshold_high = usage_mean + 1.2 * usage_std

    outliers = []
    for d in data:
        if d["house_area"] > 120 and d["usage_count"] < threshold_low:
            d["outlier_reason"] = "大房低使用"
            outliers.append(d)
        elif d["house_area"] <= 80 and d["usage_count"] > threshold_high:
            d["outlier_reason"] = "小房高使用"
            outliers.append(d)

    return {
        "summary": {
            "total_users": len(data),
            "correlation_coefficient": round(corr, 4),
            "correlation_strength": correlation_strength,
            "avg_area": float(np.mean(areas)),
            "avg_usage": float(np.mean(usages)),
            "max_area": float(np.max(areas)),
            "max_usage": float(np.max(usages)),
            "min_area": float(np.min(areas)),
            "min_usage": float(np.min(usages)),
        },
        "group_analysis": area_stats,
        "outliers": outliers,
        "raw_data": data
    }

# ------------------ 4.自行设计子问题 ------------------ #
@app.get("/auto-alarm-check", response_model=list[schemas.SecurityEventWithDetails])
def auto_alarm_check(db: Session = Depends(get_db)):
    logs = db.query(models.UsageLog).all()
    alerts = []

    abnormal_hours = list(range(0, 5))
    suspicious_device_types = ["door_lock", "security_camera"]
    
    for log in logs:
        user = db.query(models.User).get(log.user_id)
        device = db.query(models.Device).get(log.device_id)

        reasons = []
        if log.start_time.hour in abnormal_hours:
            reasons.append("异常时段使用")
        if device.type in suspicious_device_types:
            reasons.append("可疑设备类型")
        if (log.finish_time - log.start_time).total_seconds() > 3600:  # 使用超过1小时
            reasons.append("长时间使用")
        
        if reasons:
            message = f"⚠️ 检测到异常: {' & '.join(reasons)} - 设备: {device.name} (用户: {user.name})"
            
            event = models.SecurityEvent(
                user_id=log.user_id,
                event=message,
                severity="warning" if len(reasons) < 2 else "critical",
                timestamp=datetime.utcnow()
            )
            db.add(event)
            db.flush() 
            
            alerts.append(schemas.SecurityEventWithDetails(
                id=event.id,
                user_id=log.user_id,
                event=message,
                severity=event.severity,
                timestamp=event.timestamp,
                user_name=user.name,
                device_name=device.name,
                device_type=device.type,
                start_time=log.start_time,
                duration_minutes=round((log.finish_time - log.start_time).total_seconds() / 60, 1),
                reasons=reasons
            ))

    db.commit()

    severity_order = {"critical": 0, "warning": 1}
    alerts.sort(key=lambda x: severity_order.get(x.severity, 2))
    return alerts

# uvicorn main:app --reload --port 8080
