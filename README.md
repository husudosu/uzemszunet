# Üzemszünet
Ez a alkalmazás segít abban, hogy értesülj bizonyos szolgáltatók tervezett üzemszünetiről.

## Támogatott szolgáltatók
Jelen pillanatban csak az Eon tervezett áramszüneteit tudja lekérdezni a szkript, de valószínűleg ez a jövőben változni fog.

Ha esetleg lenne igény további szolgáltatókra, akkor várom a javaslatokat issue-ként.

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
Amikor telepíted ezt a programot akkor rendelkezel az 'uzemszunet.cfg' nevezetű fájllal, ahol tudod módosítani a szkript paramétereit.

Konfiguráció útvonala:

- **UNIX (Linux, MAC):** ~/.config/uzemszunet/uzemszunet.cfg
- **Windows:** %appdata%\uzemszunet\uzemszunet.cfg


### Minta konfiguráció:
```ini
[Uzemszunet]

; Ezeket a településeket fogja keresni a rendszer.
; Ügyelj arra, hogy megfelelő formában add meg a település nevét!
; Célszerű ellenőrizni a szolgáltató által biztosított fájlt!
telepulesek = ["Budapest", "Debrecen"]

; Ennyi nappal az áramszünet előtt menjen az értesítő
; 0 = Az áramszünet napján is szól
; Több nap is megadható vesszővel elválasztva
notifcation_days = [0, 1, 3, 7]

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

[EON]
; Ez a XLS fájlnak a letöltési útvonala.
; Ezt neked csak akkor kell módosítani, ha megváltozik az EON-nál az elérési útvonal.
xls_url = https://fbapps.cloudwave.hu/eon/eonuzemzavar/page/xls
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

## TODO:
- Több szolgáltató hozzáadása,
- Bővebb dokumentáció,
- Struktúra változtatások (Külön modulban minden szolgáltató),
- Tesztelés régebbi Python verziókkal is

## Tervezett szolgátatók:
- Émász (Felfüggesztették a tervezett karbantartásokat, COVID miatt),
- MindigTV
