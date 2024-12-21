# ChirpStack Device Activator

**ChirpStack Device Activator** is a Python application designed to manage the creation and activation of devices in ChirpStack. It supports automated device configuration, activation, and customization based on LoRaWAN protocols.

## Features

- **Device Creation**: Automates the creation of devices using a CSV configuration.
- **Device Activation**: Activates devices for ABP and OTAA protocols.
- **Device Settings Update**: Enables devices and configures frame-counter validation during activation.
- **Validation**: Ensures required parameters are provided for different protocols.

## Prerequisites

- **Python 3.8+**: Install Python and `pip`.
- **ChirpStack API Token**: Obtain an API token from your ChirpStack instance.
- **gRPC Library**: Install dependencies for gRPC communication.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ChirpStack_Device_Activator.git
   cd ChirpStack_Device_Activator
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the application in `config.py`:
   ```python
   server = "your-chirpstack-server:port"
   api_token = "your-api-token"
   ```

## CSV File Structure

The `devices.csv` file defines the devices for creation and activation. Include the following headers:

| **Field**        | **Description**                                      |
|-------------------|------------------------------------------------------|
| `Name`           | Device name                                          |
| `Desc`           | Device description                                   |
| `DevEUI`         | Device unique identifier                             |
| `JoinEUI`        | Join EUI (required for OTAA)                         |
| `DevProID`       | Device profile ID                                    |
| `DevAddr`        | Device address (required for ABP)                    |
| `NwkSKey`        | Network session key                                  |
| `AppSKey`        | Application session key                              |
| `SNwkSKey`       | Serving network session key (ABP 1.1)                |
| `FNwkSKey`       | Forwarding network session key (ABP 1.1)             |
| `AppKey`         | Application key (required for OTAA)                  |
| `NwkKey`         | Network key (required for OTAA 1.1)                  |
| `Protocol`       | Protocol type (`ABP104`, `ABP110`, `OTAA104`, etc.)  |
| `SkipFcntChk`    | Frame-counter validation (`TRUE`/`FALSE`)            |
| `IsDisable`      | Disable device (`TRUE`/`FALSE`)                      |

## Usage

1. **Test Connection**:
   ```bash
   python src/test_connection.py
   ```

2. **Create and Activate Devices**:
   ```bash
   python src/main.py
   ```

3. **Activate Existing Devices**:
   ```bash
   python src/activeDevice.py
   ```

## Example Device Data

Example `devices.csv` content:
```csv
Name,Desc,DevEUI,JoinEUI,DevProID,DevAddr,NwkSKey,AppSKey,SNwkSKey,FNwkSKey,AppKey,NwkKey,Protocol,SkipFcntChk,IsDisable
LightSensor,Light Monitoring,0004A30B001C5432,,28c27b72-1860-42af-97f8-aabc69a01281,01ed8596,2ffb137b9176c75ff9d0a5faf8738552,dd89e2f64a6af3a90d50f9610a29fd06,,,,ABP104,TRUE,FALSE
```

## Contribution

Feel free to fork the project and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```
```markdown
# ChirpStack 設備啟用器

**ChirpStack 設備啟用器** 是一個 Python 應用程式，用於管理 ChirpStack 中設備的創建與啟用。該工具支持基於 LoRaWAN 協議的自動化設備配置、啟用及客製化。

## 功能

- **設備創建**：透過 CSV 配置自動創建設備。
- **設備啟用**：支持 ABP 和 OTAA 協議的設備啟用。
- **設備設定更新**：啟用設備並配置 Frame-Counter 驗證。
- **資料驗證**：確保不同協議類型需要的參數完整性。

## 需求

- **Python 3.8+**：安裝 Python 和 `pip`。
- **ChirpStack API Token**：從您的 ChirpStack 實例中取得 API Token。
- **gRPC 庫**：安裝 gRPC 通訊的相關依賴。

## 安裝

1. 克隆專案：
   ```bash
   git clone https://github.com/your-username/ChirpStack_Device_Activator.git
   cd ChirpStack_Device_Activator
   ```

2. 建立虛擬環境並啟用：
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```

4. 配置應用程式至 `config.py`：
   ```python
   server = "your-chirpstack-server:port"
   api_token = "your-api-token"
   ```

## CSV 檔案結構

`devices.csv` 文件定義了需創建與啟用的設備。包括以下欄位：

| **欄位**          | **描述**                                             |
|-------------------|-----------------------------------------------------|
| `Name`           | 設備名稱                                             |
| `Desc`           | 設備描述                                             |
| `DevEUI`         | 設備唯一標識符                                       |
| `JoinEUI`        | Join EUI（OTAA 必填）                                 |
| `DevProID`       | 設備配置檔案 ID                                      |
| `DevAddr`        | 設備地址（ABP 必填）                                  |
| `NwkSKey`        | 網路會話密鑰                                         |
| `AppSKey`        | 應用會話密鑰                                         |
| `SNwkSKey`       | 服務網路會話密鑰（ABP 1.1）                           |
| `FNwkSKey`       | 轉發網路會話密鑰（ABP 1.1）                           |
| `AppKey`         | 應用密鑰（OTAA 必填）                                 |
| `NwkKey`         | 網路密鑰（OTAA 1.1 必填）                             |
| `Protocol`       | 協議類型（如 `ABP104`, `ABP110`, `OTAA104` 等）       |
| `SkipFcntChk`    | Frame-Counter 驗證（`TRUE`/`FALSE`）                  |
| `IsDisable`      | 禁用設備（`TRUE`/`FALSE`）                            |

## 使用方法

1. **測試連線**：
   ```bash
   python src/test_connection.py
   ```

2. **創建與啟用設備**：
   ```bash
   python src/main.py
   ```

3. **啟用已創建設備**：
   ```bash
   python src/activeDevice.py
   ```

## 範例設備資料

範例 `devices.csv` 內容：
```csv
Name,Desc,DevEUI,JoinEUI,DevProID,DevAddr,NwkSKey,AppSKey,SNwkSKey,FNwkSKey,AppKey,NwkKey,Protocol,SkipFcntChk,IsDisable
LightSensor,Light Monitoring,0004A30B001C5432,,28c27b72-1860-42af-97f8-aabc69a01281,01ed8596,2ffb137b9176c75ff9d0a5faf8738552,dd89e2f64a6af3a90d50f9610a29fd06,,,,ABP104,TRUE,FALSE
```

## 貢獻

歡迎 Fork 本專案並提交 Pull Request，貢獻您的代碼！

## 授權

本專案採用 MIT 授權條款，詳見 `LICENSE` 文件。
```