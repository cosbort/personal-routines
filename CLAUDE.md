# Personal Routines

Routine automatizzate che girano ogni mattina tramite Claude Code on the web.

## Hacker News Daily Digest

Invia ogni mattina un'email con i 5 articoli più "hype" del giorno su Hacker News,
con riassunto generato da Claude. Il testo completo della routine è nel thread di
configurazione — questo file documenta le dipendenze operative.

### Come funziona

1. Fetch top 30 storie da HN API (`hacker-news.firebaseio.com`)
2. Calcola hype score = `score + (descendants × 2)`
3. Prende le top 5 e genera riassunti in italiano via web fetch
4. Invia l'email via Gmail SMTP usando `gmail_send.py`

### Setup iniziale (una tantum)

#### 1. Genera un Gmail App Password

1. Vai su [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   (richiede 2FA attiva sull'account Google)
2. Nome app: `HN Digest Routine` (o qualsiasi)
3. Copia la password a 16 caratteri generata

#### 2. Aggiungi le variabili d'ambiente nella routine

Nel pannello di configurazione della routine su code.claude.com, aggiungi:

| Variabile | Valore |
|---|---|
| `GMAIL_USER` | il tuo indirizzo Gmail |
| `GMAIL_APP_PASSWORD` | la password a 16 caratteri |

#### 3. Verifica manuale

```bash
GMAIL_USER=you@gmail.com \
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx \
python3 gmail_send.py --subject "Test" --html "<h1>funziona</h1>"
```

### Invio email nella routine

Alla fine della routine, dopo aver composto l'HTML dell'email, esegui:

```bash
python3 gmail_send.py \
  --subject "🔥 HN Daily Digest — lunedì 18 maggio 2026" \
  --html-file /tmp/hn_digest.html
```

Oppure direttamente passando l'HTML come stringa:

```bash
python3 gmail_send.py --subject "..." --html "$HTML_BODY"
```

### Gestione errori

- Se `GMAIL_APP_PASSWORD` non è settato → lo script esce con errore e la routine
  lo intercetta, creando una bozza via Gmail MCP come fallback.
- Se SMTP fallisce (rete, credenziali) → logga l'errore nella session log.

### File

| File | Scopo |
|---|---|
| `gmail_send.py` | Helper Python per invio via Gmail SMTP |
| `CLAUDE.md` | Questo file — documentazione operativa |
