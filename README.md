
# Systém prezence pomocí RFID karet 

Cílem projektu je vytvoření jednoduchého a spolehlivého systému prezence, který využívá RFID technologii k zaznamenávání příchodů a odchodů uživatelů. Systém je postaven na Raspberry Pi a využívá čtečku RFID karet MF RC522. Výsledkem bude funkční zařízení s intuitivním webovým rozhraním pro běžné uživatele. 



## Potřebné komponenty

Pro realizaci tohoto projektu byly použity následující komponenty:

- **Raspberry Pi 3 Model B+** – slouží jako centrální jednotka celého systému. Zajišťuje zpracování dat, běh serveru a připojení periferií.
- **RFID čtečka MF RC522** – zařízení pro čtení RFID karet na frekvenci 13,56 MHz. Snadno se propojuje s Raspberry Pi pomocí SPI rozhraní.
- **RFID karty a přívěsky** – slouží jako unikátní identifikátory uživatelů. Bývají součástí balení s čtečkou.
- **MicroSD karta (min. 16 GB)** – pro instalaci operačního systému a uložení všech dat, databáze a aplikace.
- **Napájecí adaptér 5V 2.5A** – zajišťuje stabilní napájení Raspberry Pi, důležité pro bezproblémový provoz systému.
- **Dupont kabely** – pro snadné propojení jednotlivých komponent bez nutnosti pájení.
- **Nepájivé pole** – umožňuje rychlé a flexibilní zapojení obvodů bez pájení, ideální pro vývoj a testování prototypu.



## Instalace a postup práce

### Příprava a plánování

- Stanovení cílů projektu.
- Zakoupení potřebných součástek (viz sekce **Potřebné komponenty**).
- Instalace **Raspberry Pi OS Lite (64-bit)**.
- Povolení rozhraní: `GPIO`, `SSH`, `SPI`, nastavení připojení k Wi-Fi.
- Návrh databázové struktury (viz soubor `database.sql`).

### Nastavení vývojového prostředí

- Instalace databázového systému **SQLite**.
- Instalace Python 3 a webového frameworku **Flask**.
- Instalace potřebných Python knihoven:
  ```bash
  pip install spidev flask mfrc522

## Propojení hardware

**Zapojení RFID čtečky:**

| RFID Čtečka Pin | Raspberry Pi Pin |
|-----------------|------------------|
| SDA             | Pin 24           |
| SCK             | Pin 23           |
| MOSI            | Pin 19           |
| MISO            | Pin 21           |
| GND             | Pin 6            |
| RST             | Pin 22           |
| 3.3V            | Pin 1            |

---
## Automatické spuštění serveru po zapnutí Raspberry Pi

Aby se server automaticky spustil po zapnutí Raspberry Pi, využijeme `systemd` službu:

1. Otevři terminál na Raspberry Pi.

2. Vytvoř soubor služby:
   ```bash
   sudo nano /etc/systemd/system/rfid-server.service
Vlož tento obsah:

```bash
[Unit]
Description=RFID Attendance Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/pi-rfid/app.py
WorkingDirectory=/home/pi/pi-rfid
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target 
```
Ulož a zavři editor (CTRL+X, Y, Enter).

Aktivuj službu:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable rfid-server
sudo systemctl start rfid-server
```
Zkontroluj, že běží:

```bash
sudo systemctl status rfid-server
```

---
---
---
---
---
## Aktivace ve škole
Pro správné fungování webového rozhraní **Raspberry Pi a počítač nejsou připojeny ke stejné síti**:

Připoj Raspberry Pi a PC LAN kabelem.

Na počítači otevři `Ovládací panely > Síť a internet > Centrum síťových připojení > Změnit nastavení adaptéru`.

Pravým tlačítkem klikni na připojení ethernet (LAN) a zvol `Vlastnosti`.

Vyber Internet Protocol Version 4 `(TCP/IPv4)` a klikni na `Vlastnosti`.

Zadej statickou IP adresu:

`IP adresa: 192.168.1.1`

Maska podsítě: 

`255.255.255.0`

Na Raspberry Pi nastav také statickou IP:

```bash
sudo nano /etc/dhcpcd.conf
```
Přidej na konec:

```bash
interface eth0
static ip_address=192.168.1.2/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8
```

Restartuj Raspberry Pi:

```bash
sudo reboot
```
Na PC otevři webový prohlížeč a zadej adresu:

`http://192.168.1.2:5000`
