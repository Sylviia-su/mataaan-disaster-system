"""
路燈警示系統 - 後端 API
以 2025 花蓮馬太鞍溪堰塞湖事件為基礎設計警戒分級
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

# ── 警戒等級定義（根據真實事件設計）──────────────────────────
#
# LEVEL 1「監控」   → 堰塞湖形成、相對穩定（7月底~8月初）
# LEVEL 2「黃色警戒」→ 颱風接近、水位持續上升（8月12日楊柳颱風）
# LEVEL 3「紅色警戒」→ 水位超過警戒線、強制疏散（9月22日）
# LEVEL 4「潰壩溢流」→ 洪水已衝出、緊急逃生（9月23日14:40）

ALERT_LEVELS = {
    "monitor": {
        "label":       "監控中",
        "description": "堰塞湖形成，水位持續觀測中",
        "color":       "blue",
        "flash":       False,
        "flash_speed": None,
        "action":      "持續監測水位，民眾正常生活",
        "real_date":   "2025-07-26",
    },
    "yellow": {
        "label":       "黃色警戒",
        "description": "颱風接近，水位快速上升，預防性疏散",
        "color":       "amber",
        "flash":       True,
        "flash_speed": "slow",
        "action":      "低窪地區民眾準備疏散，隨時注意通知",
        "real_date":   "2025-08-12",
    },
    "red": {
        "label":       "紅色警戒",
        "description": "水位超過警戒線，強制疏散令發布",
        "color":       "red",
        "flash":       True,
        "flash_speed": "fast",
        "action":      "立即疏散，前往光榮國小等指定收容所",
        "real_date":   "2025-09-22",
    },
    "breach": {
        "label":       "潰壩溢流",
        "description": "堰塞湖已溢流，洪水正在下衝，立即逃生",
        "color":       "red",
        "flash":       True,
        "flash_speed": "urgent",
        "action":      "立即往高處逃生，不要等待，不要返家取物",
        "real_date":   "2025-09-23",
    },
    "clear": {
        "label":       "警報解除",
        "description": "警報解除，路燈恢復正常",
        "color":       "white",
        "flash":       False,
        "flash_speed": None,
        "action":      "請等待官方通知後再返家",
        "real_date":   None,
    },
}

# ── 模擬路燈資料庫（依光復鄉實際地點）──────────────────────
STREETLIGHTS = {
    "SL-001": {
        "name": "太巴塱村入口",
        "lat": 23.6432, "lng": 121.4231,
        "zone": "upstream",
        "status": "normal", "color": "white", "flash": False,
    },
    "SL-002": {
        "name": "省道193線42K",
        "lat": 23.6389, "lng": 121.4187,
        "zone": "upstream",
        "status": "normal", "color": "white", "flash": False,
    },
    "SL-003": {
        "name": "光復鄉公所前",
        "lat": 23.6501, "lng": 121.4312,
        "zone": "downtown",
        "status": "normal", "color": "white", "flash": False,
    },
    "SL-004": {
        "name": "馬太鞍溪橋頭",
        "lat": 23.6355, "lng": 121.4098,
        "zone": "upstream",
        "status": "normal", "color": "white", "flash": False,
    },
    "SL-005": {
        "name": "光榮村（收容所）",
        "lat": 23.6478, "lng": 121.4267,
        "zone": "shelter",
        "status": "normal", "color": "white", "flash": False,
    },
    "SL-006": {
        "name": "大馬村",
        "lat": 23.6320, "lng": 121.4050,
        "zone": "upstream",
        "status": "normal", "color": "white", "flash": False,
    },
    "SL-007": {
        "name": "大平村",
        "lat": 23.6290, "lng": 121.4020,
        "zone": "upstream",
        "status": "normal", "color": "white", "flash": False,
    },
}

ALERT_LOG = []
CURRENT_LEVEL = "clear"


# ── 核心邏輯：依等級與區域決定燈號行為 ──────────────────────
def get_zone_command(level: str, zone: str) -> dict:
    """
    收容所（shelter）在紅色/潰壩時變綠色常亮，引導民眾前往
    其他區域依警戒等級變色閃爍
    """
    lvl = ALERT_LEVELS[level]

    if zone == "shelter":
        if level in ["red", "breach"]:
            return {"color": "green", "flash": False, "status": "shelter"}
        return {"color": "white", "flash": False, "status": "normal"}

    return {
        "color":       lvl["color"],
        "flash":       lvl["flash"],
        "flash_speed": lvl["flash_speed"],
        "status":      "alert" if level != "clear" else "normal",
    }


def apply_alert_level(level: str, area_ids: list = None) -> dict:
    """
    套用警戒等級到指定路燈
    積木輸出介面：接收等級代碼 → 控制所有路燈
    """
    global CURRENT_LEVEL
    CURRENT_LEVEL = level

    target_ids = area_ids or list(STREETLIGHTS.keys())
    results = []

    for light_id in target_ids:
        if light_id not in STREETLIGHTS:
            continue
        zone = STREETLIGHTS[light_id]["zone"]
        cmd  = get_zone_command(level, zone)
        time.sleep(0.05)
        STREETLIGHTS[light_id].update(cmd)
        STREETLIGHTS[light_id]["updated_at"] = datetime.now().isoformat()
        results.append({"light_id": light_id, "applied": cmd})

    log_entry = {
        "timestamp":   datetime.now().isoformat(),
        "level":       level,
        "label":       ALERT_LEVELS[level]["label"],
        "description": ALERT_LEVELS[level]["description"],
        "action":      ALERT_LEVELS[level]["action"],
        "area_ids":    target_ids,
        "affected":    len(results),
    }
    ALERT_LOG.append(log_entry)

    return {
        "success":     True,
        "level":       level,
        "label":       ALERT_LEVELS[level]["label"],
        "description": ALERT_LEVELS[level]["description"],
        "action":      ALERT_LEVELS[level]["action"],
        "affected":    len(results),
        "timestamp":   log_entry["timestamp"],
    }


# ── API 路由 ────────────────────────────────────────────────

@app.route("/api/levels", methods=["GET"])
def get_levels():
    return jsonify(ALERT_LEVELS)


@app.route("/api/lights", methods=["GET"])
def get_all_lights():
    return jsonify({
        "lights":        STREETLIGHTS,
        "total":         len(STREETLIGHTS),
        "current_level": CURRENT_LEVEL,
    })


@app.route("/api/alert", methods=["POST"])
def trigger_alert():
    """
    觸發警戒等級

    {
        "level": "monitor" | "yellow" | "red" | "breach" | "clear",
        "area_ids": ["SL-001"],     // 留空 = 全部
        "triggered_by": "林保署",
        "water_level_m": 1139.5
    }
    """
    data = request.get_json()
    if not data or "level" not in data:
        return jsonify({"error": "缺少 level 欄位"}), 400

    level = data["level"]
    if level not in ALERT_LEVELS:
        return jsonify({"error": f"無效等級，有效值為 {list(ALERT_LEVELS.keys())}"}), 400

    result = apply_alert_level(level, data.get("area_ids") or [])
    result["triggered_by"]  = data.get("triggered_by", "應變中心")
    result["water_level_m"] = data.get("water_level_m")
    return jsonify(result)


@app.route("/api/alert/clear", methods=["POST"])
def clear_alert():
    return jsonify(apply_alert_level("clear"))


@app.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify({
        "logs":  list(reversed(ALERT_LOG)),
        "total": len(ALERT_LOG),
    })


@app.route("/api/status", methods=["GET"])
def get_status():
    alert_count  = sum(1 for l in STREETLIGHTS.values() if l.get("status") == "alert")
    return jsonify({
        "total_lights":  len(STREETLIGHTS),
        "alert_lights":  alert_count,
        "normal_lights": len(STREETLIGHTS) - alert_count,
        "current_level": CURRENT_LEVEL,
        "current_label": ALERT_LEVELS[CURRENT_LEVEL]["label"],
        "last_alert":    ALERT_LOG[-1]["timestamp"] if ALERT_LOG else None,
        "mode":          "simulation",
    })


@app.route("/api/demo/replay", methods=["POST"])
def demo_replay():
    """Demo 用：依序播放馬太鞍溪事件時間軸"""
    sequence = [
        {"level": "monitor", "note": "2025-07-26 堰塞湖成形"},
        {"level": "yellow",  "note": "2025-08-12 楊柳颱風，首次疏散令"},
        {"level": "red",     "note": "2025-09-22 林保署發布紅色警戒"},
        {"level": "breach",  "note": "2025-09-23 14:40 溢流，緊急逃生"},
    ]
    results = []
    for step in sequence:
        time.sleep(0.3)
        r = apply_alert_level(step["level"])
        r["note"] = step["note"]
        results.append(r)

    return jsonify({
        "success":  True,
        "message":  "完成馬太鞍溪事件時間軸模擬",
        "sequence": results,
    })


if __name__ == "__main__":
    print("路燈警示系統後端啟動（2025花蓮版）")
    print("警戒等級：monitor → yellow → red → breach → clear")
    print("http://localhost:5000/api/status")
    app.run(debug=True, port=5000)
