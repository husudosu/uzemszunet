# Üzemszünet
Az alkalmazás segít abban, hogy értesülj bizonyos szolgáltatók tervezett üzemszünetiről.

**FIGYELEM:** A program a szolgáltatók szabadon elérhető üzemszünet listáiból szedi ki az adatokat! Ha az adott szolgátatónál változik az üzemszünetek adatforrása, akkor a program működésében hibát okozhat! Amennyiben hibát tapasztalsz, kérlek ellenőrizd, hogy a program legfrissebb változata fut e, ha igen kérlek jelezd ha valami nem működik! Ügyelj a privát adataidra (konfigurációs fájlban E-mail adattok), ha hibát jelentesz be, illetve log fájlt mindig töltsd fel! A program MIT licenc alatt van.

## Támogatott szolgáltatók

- EON
- ÉMÁSZ

Ha lenne igény további szolgáltatókra, akkor várom a javaslatokat issue-ként.

## Telepítés 
Mielőtt a telepítést megkezdenéd szükséged lesz legalább Python 3.6-os verzióra, illetve a PIP-nek telepítve kell lennie!

```bash
pip3 install uzemszunet
# Vagy
pip install uzemszunet
```

vagy ha a repo-t klónozod a gyökérkönyvtárban ahol a setup.py van:
```bash 
pip3 install .
# Vagy
pip install .
```

## Konfiguráció
Amikor telepíted ezt a programot akkor rendelkezel az 'uzemszunet.cfg' nevezetű fájllal, ahol tudod módosítani a beállíátoskat

Konfiguráció útvonala:

- **UNIX (Linux, MAC):** ~/.config/uzemszunet/uzemszunet.cfg
- **Windows:** %appdata%\uzemszunet\uzemszunet.cfg


### Minta konfiguráció:
```ini
[Email]
; Erre az E-mail címre fogja küldeni a program az üzemszünetek listáját!
to_mail = example@gmail.com

smtp_host = smtp.gmail.com
smtp_port = 465

; Erről az E-mail címről fog menni az üzenet. (Lehet ugyanaz mint a to_mail!)
user = example@gmail.com

; Ha G-mail-t használsz akkor létre kell hozni egy jelszót az alkalmazáshoz!
; https://myaccount.google.com/security
password = myAppPassword

; Akkor is legyen E-mail küldve, ha nincs üzemszünet
; Így biztos lehetsz benne hogy működik a rendszer.
; Alapértelmezés szerint ki van kapcsolva!
; Értéke lehet: True vagy False
send_heartbeat = False

[EON]
; Ezeket a településeket fogja keresni a rendszer.
; Ügyelj arra, hogy megfelelő formában add meg a település nevét!
; Célszerű ellenőrizni a szolgáltató által biztosított fájlt!
telepulesek = ["Budapest", "Debrecen", "Abony"]

; Ennyi nappal az áramszünet előtt menjen az értesítő
; 0 = Az áramszünet napján is szól
; Több nap is megadható vesszővel elválasztva
notification_days = [0, 1, 3, 7]

[EMASZ]
; Ezeket a településeket fogja keresni a rendszer.
; Ügyelj arra, hogy megfelelő formában add meg a település nevét!
; Célszerű ellenőrizni a szolgáltató által biztosított fájlt!
telepulesek = ["Budapest XVI.", "Jászberény"]

; Ennyi nappal az áramszünet előtt menjen az értesítő
; 0 = Az áramszünet napján is szól
; Több nap is megadható vesszővel elválasztva
notification_days = [0, 1, 3, 7]
```
## Argumentumok
```
  -h, --help        Argumentumok megjelentíse
  --email           E-mail-ben ki lesz küldve az eredmény.
  --egyszeru_lista  Csak egyszerű zanzásított lista készül.
```

## Lehetséges hibák
Ha nem az E-mail küldéssel történt probléma, akkor a hibákról kapsz üzenetet.

## Automatikus futtatás (Linux)
Konfiguráció után egyszerűen csak bele kell tenni crontab-ba a program futtatását. 

```bash
crontab -e # Crontab szerkesztése
```

```bash
# Minden nap 0 óra 0 perckor le fog futni a program.
0 0 * * * uzemszunet --email
```
