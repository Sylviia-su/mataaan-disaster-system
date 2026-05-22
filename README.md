# 🚦 馬太鞍溪防災積木元件系統

**防災積木元件創新賽 — 2025 花蓮馬太鞍溪堰塞湖情境**

> 以模組化「積木」概念設計的防災數位工具，整合路燈警示、逃生路徑、安全回報與 AI 影像辨識，每個元件均可獨立使用，也可彼此拼接串聯。

---

## 📋 專案說明

本系統以 2025 年 9 月花蓮馬太鞍溪堰塞湖事件為設計情境，開發一套可模組化部署的防災數位工具。

### 核心設計理念

```
民眾回報（Call）  →  AI 解析  →  標準化 JSON
                                      ↓
應變中心分析（Analysis）  →  路燈控制 / 逃生路徑更新 / 資源調度
```

---

## 🗂️ 專案結構

```
streetlight-alert/
├── frontend/
│   └── index.html          # 主介面（單頁應用，含所有功能，RWD）
├── backend/
│   ├── app.py              # Flask API（模擬路燈控制器）
│   └── requirements.txt
└── README.md
```

---

## ✨ 功能模組

| 模組 | 說明 | 類型 |
|------|------|------|
| 👥 使用者流程 | 4 個 Persona 的完整操作流程與差異對照 | 展示 |
| 🚦 路燈警示控制 | 四級警戒燈色、人工確認、人工直接控制 | Call + Analysis |
| 🗺️ 逃生路徑 | 預設路線、即時定位、AI 路況修正、收容所地圖 | Analysis |
| 🆘 安全回報 | SALT 急救分級、GPS+地址並行、匿名回報 | Call |
| 🤖 AI 影像辨識 | Claude Vision 判斷積水坍方、輸出 JSON | Call + Analysis |
| 📊 監測資料 | 水位雨量圖表、NCDR 監測頁嵌入 | 展示 |
| 🔗 資料來源 | 9 個公開資料 API 連結 | 參考 |

---

## 🚀 啟動方式

### 前端（直接開啟，無需伺服器）

```bash
# 直接用瀏覽器開啟即可，支援手機與桌機
open frontend/index.html
```

> ⚠️ AI 影像辨識需要 Anthropic API 金鑰。其餘功能均可離線使用（含 OpenStreetMap 地圖）。

### 後端（選用）

```bash
cd backend
pip install -r requirements.txt --break-system-packages
python app.py
# API 運行於 http://localhost:5000
```

---

## 📡 後端 API

```
GET  /api/status           系統狀態摘要
GET  /api/lights           所有路燈狀態
POST /api/alert            觸發警戒等級
POST /api/alert/clear      解除警報
GET  /api/logs             警報紀錄
POST /api/demo/replay      播放時間軸 Demo
```

**觸發警報範例**

```json
POST /api/alert
{
  "level": "red",
  "area_ids": ["SL-001", "SL-002"],
  "event_id": "E2025-091801",
  "message": "馬太鞍溪水位超過警戒線"
}
```

**AI 影像辨識輸出範例**

```json
{
  "hazard_type": "積水",
  "severity": "medium",
  "water_depth_estimate": "約 30-50 公分",
  "description": "道路積水，部分路面不可見",
  "immediate_action": "繞行台 9 線，避免此路段",
  "safe_for_evacuation": false
}
```

---

## 🗺️ 積木拼接架構

```
[感測器 / 民眾回報 / 影像上傳]
         ↓
   [通報 JSON 標準格式]
         ↓
   [AI 分析 / 路況判斷]
         ↓
[路燈 API] [地圖標記] [LINE Bot] [應變中心儀表板]
```

---

## 👥 Persona 設計

| Persona | 角色 | 接收警報方式 | 行動觸發 |
|---------|------|------------|---------|
| 林小姐 | 一般居民（主流程） | LINE Bot | 自主查看路徑疏散 |
| 陳阿公 | 獨居老人 | 路燈閃爍 + 語音電話 | 按鍵求助，等志工 |
| 王大偉 | 志工協調員 | LINE Bot 任務指派 | 接任務後主動出發 |
| 林佳慧 | 應變中心人員 | 系統儀表板 | 審核核准後發布 |

---

## 📅 2025 馬太鞍溪事件時間軸

| 日期 | 事件 | 警戒等級 |
|------|------|---------|
| 2025-07-26 | 堰塞湖形成 | 🔵 監控中 |
| 2025-08-12 | 楊柳颱風，首次疏散令 | 🟡 黃色警戒 |
| 2025-09-22 | 林保署發布紅色警戒，撤離 8000 人 | 🔴 紅色警戒 |
| 2025-09-23 14:40 | 堰塞湖溢流，19 死 | 🚨 潰壩溢流 |

---

## 🔗 資料來源

- [NCDR 堰塞湖監測](https://watch.ncdr.nat.gov.tw/watch_barrier_map_v2)
- [水利署即時水位](https://fhy.wra.gov.tw/fhyv2/monitor/water)
- [水利署即時雨量](https://fhy.wra.gov.tw/fhyv2/monitor/rain)
- [花蓮縣政府堰塞湖專區](https://www.hl.gov.tw/ysh/)
- [林保署監測系統](https://www.iiicloud.com.tw/FarmlandQlakenew/BarrierLake)
- [水位 Open Data API](https://data.gov.tw/dataset/25768)
- [中央氣象署開放資料](https://opendata.cwa.gov.tw/about/application)

---

## 📝 授權

MIT License — 本專案為參賽作品，資料來源版權歸各原始資料提供單位所有。
