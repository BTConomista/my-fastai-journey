# Confronto dei tre notebook "Is it a bird?"

Questo documento confronta, cella per cella e riga per riga, i tre notebook presenti nel repository:

| Nome usato qui | File | Provenienza |
|---|---|---|
| **Mio** | `basics-model.ipynb` | fork personale del notebook Kaggle |
| **Originale** | `reference/00_is_it_a_bird_creating_a_model_from_your_own_data.ipynb` | notebook Kaggle di Jeremy Howard |
| **Libro** | `reference/01_intro.ipynb` | capitolo 1 di *Deep Learning for Coders with fastai and PyTorch* (fastbook) |

**Mio** e **Originale** sono imparentati (il primo deriva dal secondo tramite "Copy & Edit" di Kaggle), quindi vengono confrontati con dei veri *diff* riga per riga.
Il **Libro** non deriva dallo stesso file — usa dataset, API e nomi di variabili diversi — quindi viene confrontato per **fase equivalente**, mostrando il codice completo di entrambe le parti.

Ogni cella è documentata con:

- il **codice completo** (anche quando è identico nei due file);
- una **spiegazione tecnica** riga per riga;
- una **spiegazione in parole semplici** per chi è ai primi passi;
- quando la cella è identica, il **perché probabilmente non è stata modificata**;
- eventuali **note extra** utili per imparare qualcosa in più.

---

# PARTE A · Mio vs Originale

---

## Cella 1 — Check connessione internet

**Originale**
```python
#NB: Kaggle requires phone verification to use the internet or a GPU...
import socket,warnings
try:
    socket.setdefaulttimeout(1)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('1.1.1.1', 53))
except socket.error as ex: raise Exception("STOP: No internet. Click '>|' in top right and set 'Internet' switch to on")
```

**Mio**
```python
#NB: Kaggle requires phone verification to use the internet or a GPU...
import socket,warnings
import time
try:
    socket.setdefaulttimeout(1)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('1.1.1.1', 53))
except socket.error as ex: raise Exception("STOP: No internet. Click '>|' in top right and set 'Internet' switch to on")
```

```diff
 import socket,warnings
+import time
 try:
```

### Spiegazione tecnica, riga per riga

- `import socket,warnings` — `socket` è il modulo di rete di basso livello della libreria standard. `warnings` viene importato ma **non è mai usato in nessuna cella del notebook**: è un residuo ereditato dal template Kaggle, presente identico in entrambi i file. Non fa danni, occupa solo un pizzico di memoria.
- `import time` (solo Mio) — non serve a niente *in questa cella*: serve alla cella 8, dove userai `time.sleep(5)`. L'Originale invece importa lo sleep localmente (`from time import sleep`) dentro la cella che lo usa. Spostandolo qui hai centralizzato gli import in cima, ma hai creato una dipendenza d'ordine: se qualcuno esegue la cella 8 senza aver mai eseguito la cella 1, otterrà `NameError: name 'time' is not defined`.
- `socket.setdefaulttimeout(1)` — imposta un timeout **globale** di 1 secondo per tutti i socket creati da qui in poi nel processo. È un'impostazione a livello di modulo, non della singola connessione: resta attiva per tutto il resto del notebook.
- `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` — crea un socket IPv4 (`AF_INET`) di tipo stream (`SOCK_STREAM` = TCP).
- `.connect(('1.1.1.1', 53))` — apre una connessione TCP verso il resolver DNS pubblico di Cloudflare sulla porta 53. Curiosità: la porta 53 è normalmente associata a UDP per le query DNS, ma i resolver pubblici accettano anche TCP (usato per risposte lunghe) — quindi la connessione riesce e serve da "ping applicativo".
- `except socket.error as ex:` — da Python 3.3 in poi `socket.error` è semplicemente un **alias di `OSError`**, mantenuto per retrocompatibilità.
- `raise Exception(...)` — solleva un'eccezione con un messaggio umano. È un **fail-fast deliberato**: meglio fermarsi subito con "non hai internet" che fallire venti celle dopo con uno stack trace incomprensibile dentro `download_url`.

### In parole semplici

Questa cella è un controllo preliminare. Prova a "telefonare" a un server molto affidabile di internet (uno dei DNS di Cloudflare) e aspetta massimo 1 secondo. Se non risponde, il notebook si ferma subito dicendoti chiaramente che manca la connessione — invece di andare avanti e schiantarsi più tardi con un errore che non capiresti. Serve soprattutto su Kaggle, dove l'accesso a internet va acceso a mano con un interruttore, e capita spessissimo di dimenticarsene.

### Extra

Un socket aperto e mai chiuso come qui resta a carico del garbage collector Python. In uno script "serio" si userebbe `with socket.socket(...) as s:` — ma trattandosi di un unico socket in un notebook usa-e-getta, nessuno dei due autori se n'è preoccupato.

---

## Cella 2 — Setup / installazione pacchetti

**Originale**
```python
import os
iskaggle = os.environ.get('KAGGLE_KERNEL_RUN_TYPE', '')

if iskaggle:
    !pip install -Uqq fastai
```

**Mio**
```python
# --- Setup opzionale (consigliato su Kaggle) ---
import os, importlib
iskaggle = bool(os.environ.get("KAGGLE_KERNEL_RUN_TYPE", ""))

if iskaggle:
    %pip -q install -U fastai ddgs numpy==1.24.3
    importlib.invalidate_caches()
```

```diff
-import os
-iskaggle = os.environ.get('KAGGLE_KERNEL_RUN_TYPE', '')
+import os, importlib
+iskaggle = bool(os.environ.get("KAGGLE_KERNEL_RUN_TYPE", ""))
 
 if iskaggle:
-    !pip install -Uqq fastai
+    %pip -q install -U fastai ddgs numpy==1.24.3
+    importlib.invalidate_caches()
```

### Spiegazione tecnica, riga per riga

- `os.environ.get('KAGGLE_KERNEL_RUN_TYPE', '')` — legge una variabile d'ambiente che **esiste solo sui kernel Kaggle**. Il secondo argomento `''` è il valore di default se la variabile non esiste, così non serve un `try/except KeyError`. È il modo idiomatico per scrivere un notebook che funziona sia su Kaggle sia sul proprio portatile senza modifiche.
- `bool(...)` (solo Mio) — l'Originale usa la stringa direttamente, sfruttando il fatto che in Python una stringa vuota è *falsy* e una piena è *truthy*. Il `bool()` rende la conversione esplicita: comportamento identico, intenzione più chiara.
- `!pip` vs `%pip` — questa è la differenza più importante della cella. `!comando` esegue il comando in una **shell di sistema separata**; `%pip` è un *magic command* di IPython che installa nell'**ambiente Python del kernel attualmente in esecuzione**. Su macchine con più installazioni Python (Colab e Kaggle ne hanno spesso più di una) `!pip` può installare in un interprete diverso da quello che sta girando: il pacchetto risulta "installato" ma `import` fallisce lo stesso. `%pip` elimina questo intero problema. È una correzione reale, non estetica.
- Flag: `-U` = upgrade all'ultima versione; `-q` / `-qq` = quiet, riduce l'output (`-qq` più aggressivo di `-q`).
- `ddgs` in più — il pacchetto di ricerca immagini, che l'Originale installa in una cella separata (vedi Cella 3).
- `numpy==1.24.3` — un **pin di versione esatta**. Serve perché numpy 2.x ha rotto la compatibilità binaria (ABI) con i pacchetti compilati contro numpy 1.x: torch, pandas, scikit-learn precompilati si aspettano l'API C vecchia e crashano con errori del tipo *"numpy.dtype size changed"*. Fissare 1.24.3 evita che pip risolva silenziosamente a numpy 2.
- `importlib.invalidate_caches()` — Python memorizza in cache la mappa dei moduli disponibili sui percorsi di import. Se installi un pacchetto **dopo** che il kernel è partito, quella cache è obsoleta e `import ddgs` può fallire pur essendo il pacchetto sul disco. Questa riga forza la ri-scansione, evitando il classico "devi riavviare il kernel".

### In parole semplici

Qui si installano le librerie necessarie: `fastai` (il framework di intelligenza artificiale), `ddgs` (per cercare immagini su DuckDuckGo) e una versione ben precisa di `numpy` (la libreria matematica su cui si appoggia tutto). L'`if iskaggle:` fa in modo che l'installazione parta **solo** se stai lavorando su Kaggle: se sei sul tuo computer, probabilmente hai già installato tutto e reinstallare ogni volta sarebbe una perdita di tempo. La riga finale è un trucchetto per dire a Python "guarda che ho appena installato roba nuova, riguarda cosa c'è disponibile" — senza di essa, a volte devi riavviare tutto.

### Extra

Il pin di numpy è una scelta *difensiva* che si porta dietro un costo: negli output di esecuzione reale compare una lunga lista di conflitti (`tensorflow requires numpy>=1.26`, `jax requires numpy>=1.25`…). Il pin risolve il problema di questo notebook ma ne crea altri per i pacchetti non usati — un compromesso accettabile in un notebook monouso, inaccettabile in un ambiente di produzione condiviso.

---

## Cella 3 — Installazione separata di `duckduckgo_search` *(solo Originale)*

**Originale**
```python
# Skip this cell if you already have duckduckgo_search installed
!pip install -Uqq duckduckgo_search
```

**Mio**
```
(cella assente — l'installazione è confluita nella cella 2)
```

### Spiegazione tecnica

Nell'Originale l'installazione della libreria di ricerca è isolata in una cella propria. La scelta è didattica prima che tecnica: separando "libreria per cercare immagini" da "framework di deep learning", il lettore vede a colpo d'occhio quale pacchetto serve a quale scopo. C'è anche un vantaggio pratico esplicitato dal commento: rieseguendo il notebook con il pacchetto già presente, si può **saltare selettivamente questa singola cella** senza rilanciare anche l'installazione di fastai (che è pesante). Nel Mio le due installazioni sono fuse: un solo passaggio del resolver di pip invece di due — più veloce, ma si perde la granularità.

### In parole semplici

È solo una seconda cella che installa un'altra libreria. Nel file Mio è stato messo tutto insieme nella cella precedente per fare prima.

### Extra

`duckduckgo_search` e `ddgs` sono lo **stesso progetto**: gli autori l'hanno rinominato. Chi oggi esegue l'Originale così com'è rischia di installare un pacchetto deprecato o non più aggiornato — il passaggio a `ddgs` è, di fatto, una manutenzione necessaria.

---

## Cella 4 — Funzione di ricerca immagini

**Originale**
```python
from duckduckgo_search import DDGS 
from fastcore.all import *

def search_images(keywords, max_images=200): return L(DDGS().images(keywords, max_results=max_images)).itemgot('image')
```

**Mio**
```python
from fastcore.all import L
from ddgs import DDGS

def search_images_ddg(keywords, max_images=200):
    with DDGS() as ddg:
        return L(ddg.images(keywords, max_results=max_images)).itemgot('image')

# alias breve, come spesso nei notebook fastai
search_images = search_images_ddg
```

```diff
-from duckduckgo_search import DDGS 
-from fastcore.all import *
+from fastcore.all import L
+from ddgs import DDGS
 
-def search_images(keywords, max_images=200): return L(DDGS().images(keywords, max_results=max_images)).itemgot('image')
+def search_images_ddg(keywords, max_images=200):
+    with DDGS() as ddg:
+        return L(ddg.images(keywords, max_results=max_images)).itemgot('image')
+
+search_images = search_images_ddg
```

### Spiegazione tecnica, riga per riga

- `from fastcore.all import *` (Originale) vs `from fastcore.all import L` (Mio) — il primo è un **wildcard import**: porta nel namespace centinaia di nomi, con rischio concreto di collisioni silenziose (fastcore ridefinisce ad esempio `Path`). L'import mirato prende solo `L`: più pulito e più prevedibile. Attenzione però: nel notebook Mio più avanti c'è comunque `from fastai.vision.all import *`, che reintroduce il wildcard — quindi il beneficio è parziale.
- `DDGS()` — istanzia il client che interroga (per scraping non ufficiale) il motore immagini di DuckDuckGo. Non esiste una API pubblica documentata: la libreria imita le chiamate del browser, ed è per questo che occasionalmente si rompe.
- `.images(keywords, max_results=max_images)` — restituisce una **lista di dizionari**, uno per immagine, con chiavi come `image` (URL diretto del file), `thumbnail`, `title`, `url` (pagina sorgente), `height`, `width`, `source`.
- `L(...)` — è la lista potenziata di **fastcore**. Si comporta come una `list` normale ma aggiunge metodi in stile funzionale e un `repr` più compatto (mostra il conteggio e i primi elementi invece di stampare migliaia di righe: in un notebook è una comodità enorme).
- `.itemgot('image')` — metodo di `L`: applica `d['image']` a ogni elemento. È l'equivalente conciso di `[d['image'] for d in risultati]`. Quindi il valore di ritorno finale è una lista di **soli URL**, tutto il resto dei metadati viene scartato.
- `with DDGS() as ddg:` (solo Mio) — **context manager**: garantisce che la sessione HTTP sottostante (connection pool, cookie, token di sessione) venga chiusa in modo pulito anche se il codice interno solleva un'eccezione. Il pacchetto vecchio tollerava l'uso "al volo" affidandosi al garbage collector; il nuovo `ddgs` è più rigoroso, e usare `with` è la pratica raccomandata.
- `search_images = search_images_ddg` — non è una copia della funzione, è un **secondo nome che punta allo stesso oggetto funzione** (in Python le funzioni sono oggetti di prima classe). Serve a non dover riscrivere tutte le chiamate successive nel notebook, che usano il nome breve ereditato dall'Originale.

### In parole semplici

Questa è la funzione "motore di ricerca" del progetto: le passi delle parole (es. `'bird photos'`) e ti restituisce una lista di indirizzi web di immagini. `with DDGS() as ddg:` significa "apri il collegamento, usalo, e chiudilo sempre correttamente quando hai finito, anche se qualcosa va storto nel mezzo" — come aprire un rubinetto sapendo che verrà richiuso da solo. L'ultima riga crea un "soprannome": così nel resto del notebook puoi scrivere `search_images(...)` invece del nome lungo.

### Extra

`max_images=200` è un **valore di default del parametro**: se chiami la funzione senza specificarlo, cerca 200 immagini. Questo diventa cruciale nella cella 8, dove la funzione viene chiamata senza il parametro — quindi lì scarica 200 immagini per query, non 1 come nei test.

---

## Cella 5 — Primo test di ricerca

**Originale**
```python
urls = search_images('bird photos', max_images=1)
urls[0]
```

**Mio**
```python
#NB: `search_images` depends on duckduckgo.com, which doesn't always return correct responses.
#    If you get a JSON error, just try running it again (it may take a couple of tries).
urls = search_images('bird photos', max_images=1)
urls[0]
```

```diff
+#NB: `search_images` depends on duckduckgo.com, which doesn't always return correct responses.
+#    If you get a JSON error, just try running it again (it may take a couple of tries).
 urls = search_images('bird photos', max_images=1)
 urls[0]
```

### Spiegazione tecnica, riga per riga

- `search_images('bird photos', max_images=1)` — qui `max_images=1` è passato **esplicitamente**, sovrascrivendo il default di 200. È un test di fumo: verificare che la catena "libreria installata → connessione → parsing risposta" funzioni, prima di lanciare il download pesante. Chiedere 1 sola immagine rende il test istantaneo e non consuma quota di rate-limit.
- `urls[0]` — ultima espressione della cella. Jupyter cattura automaticamente il valore dell'ultima espressione e lo stampa come output (`Out[n]:`), senza bisogno di `print()`. È un comportamento del kernel IPython, non di Python: in uno script normale questa riga non stamperebbe nulla.
- Il commento aggiunto — segnala che lo scraping non ufficiale può restituire errori JSON intermittenti (il sito cambia struttura, o applica rate-limit). È presente nel notebook pubblico originale di Jeremy Howard: la sua assenza nella copia "Originale" di questo repo suggerisce che quella copia sia stata leggermente potata.

### In parole semplici

È un test rapido: "cerca **una sola** foto di uccello e mostrami il link". Se vedi comparire un indirizzo web sotto la cella, tutto funziona e puoi proseguire. Il commento ti avvisa che ogni tanto questa riga può dare errore per colpa del sito, non per colpa tua: basta rieseguirla.

### Extra

`urls[0]` fallirebbe con `IndexError` se la ricerca non restituisse nulla. In una delle varianti del notebook (`forkofbasicsmodel.ipynb`) esisteva proprio la correzione a questo problema (`if urls: … else: print("Nessun risultato")`) — una migliora che non è mai arrivata in `basics-model.ipynb`.

---

## Cella 6 — Download `bird.jpg` + miniatura · **identica in entrambi**

**Originale e Mio (byte per byte uguali)**
```python
from fastdownload import download_url
dest = 'bird.jpg'
download_url(urls[0], dest, show_progress=False)

from fastai.vision.all import *
im = Image.open(dest)
im.to_thumb(256,256)
```

### Spiegazione tecnica, riga per riga

- `from fastdownload import download_url` — `fastdownload` è una piccola libreria dell'ecosistema fastai che avvolge il download HTTP aggiungendo retry automatici, gestione dei redirect e barra di avanzamento opzionale.
- `dest = 'bird.jpg'` — percorso relativo: il file finisce nella working directory del kernel.
- `download_url(urls[0], dest, show_progress=False)` — scarica il primo (e unico) URL trovato. `show_progress=False` disattiva la barra: in esecuzione automatica sarebbe solo rumore nell'output.
- `from fastai.vision.all import *` — **questo è l'import più importante di tutto il notebook.** Con una riga porta nel namespace praticamente tutto: `Image` (il modulo PIL ripubblicato), `Path`, `DataBlock`, `ImageBlock`, `CategoryBlock`, `RandomSplitter`, `parent_label`, `Resize`, `download_images`, `resize_images`, `verify_images`, `get_image_files`, `vision_learner`, `resnet18`, `error_rate`, `PILImage`… Tutto il codice dalle celle successive dipende da questa riga: se salti questa cella, **niente funziona più**.
- `Image.open(dest)` — apre il file con Pillow.
- `im.to_thumb(256,256)` — `to_thumb` **non è un metodo di Pillow**: è un metodo che fastai aggiunge dinamicamente (monkey-patching) alla classe `PIL.Image.Image`. Genera una miniatura che **preserva le proporzioni originali** entro un riquadro 256×256. Essendo l'ultima espressione, Jupyter la renderizza come immagine inline.

### Perché è identica nei due file

Perché è codice puramente meccanico e già corretto: scarica un file, aprilo, mostralo. Non c'è nessuna scelta di modellazione, nessuna API deprecata, nessun parametro da tarare. Chi ha creato il fork ha modificato solo ciò che era rotto (il pacchetto DDG), obsoleto (`!pip`) o soggetto a preferenza (quante immagini scaricare) — e questa cella non rientra in nessuna delle tre categorie. È un buon indicatore di quanto il fork sia stato "chirurgico".

### In parole semplici

Due cose: scarica davvero l'immagine trovata prima e la salva sul disco col nome `bird.jpg`, poi la apre e ne mostra una versione rimpicciolita nel notebook — così controlli con i tuoi occhi di aver scaricato un uccello e non, che so, una pagina di errore. Questo file `bird.jpg` non è usa-e-getta: resterà lì fino alla fine ed è **la stessa identica foto** su cui il modello farà la sua predizione finale.

### Extra

Il fatto che l'immagine di test finale sia stata scaricata *prima* dell'allenamento è metodologicamente interessante: quella foto non è mai entrata nel dataset di training (che sta in `bird_or_not/`), quindi la predizione finale è un test onesto su dati mai visti.

---

## Cella 7 — Download `forest.jpg` + miniatura

**Originale**
```python
download_url(search_images('forest photos', max_images=1)[0], 'forest.jpg', show_progress=False)
Image.open('forest.jpg').to_thumb(256,256)
```

**Mio**
```python
download_url(search_images('forest photos', max_images=1)[0], 'forest.jpg', show_progress=False)

Image.open('forest.jpg').to_thumb(256, 256)
```

```diff
 download_url(search_images('forest photos', max_images=1)[0], 'forest.jpg', show_progress=False)
-Image.open('forest.jpg').to_thumb(256,256)
+
+Image.open('forest.jpg').to_thumb(256, 256)
```

### Spiegazione tecnica

Stessa logica della cella 6, ma compressa: la chiamata a `search_images(...)` è **annidata** dentro `download_url` e indicizzata con `[0]` sul posto, senza salvare la lista in una variabile intermedia. Nessuna variabile `urls` per la foresta viene mai creata — coerente col fatto che, a differenza di `bird.jpg`, `forest.jpg` non verrà più riusato in seguito. Le uniche differenze tra i due file sono una riga vuota e uno spazio dopo la virgola: **zero impatto funzionale**, probabilmente auto-formattazione dell'editor.

### In parole semplici

Identico a prima, ma per la foresta: cerca, scarica, mostra la miniatura. A questo punto hai verificato che la ricerca funziona per entrambe le categorie e puoi passare al download in grande.

### Extra

Nota l'asimmetria: `bird.jpg` viene salvata in una variabile (`dest`) e riusata alla fine, `forest.jpg` no. Il notebook, di fatto, non testa mai il modello su un'immagine di foresta — un piccolo buco nella verifica finale che nessuna delle due versioni colma.

---

## Cella 8 — Download in batch + ridimensionamento

**Originale**
```python
searches = 'forest','bird'
path = Path('bird_or_not')
from time import sleep

for o in searches:
    dest = (path/o)
    dest.mkdir(exist_ok=True, parents=True)
    download_images(dest, urls=search_images(f'{o} photo'))
    sleep(10)  # Pause between searches to avoid over-loading server
    download_images(dest, urls=search_images(f'{o} sun photo'))
    sleep(10)
    download_images(dest, urls=search_images(f'{o} shade photo'))
    sleep(10)
    resize_images(path/o, max_size=400, dest=path/o)
```

**Mio**
```python
searches = 'forest', 'bird'
path = Path('bird_or_not')

for o in searches:
    dest = (path/o)
    dest.mkdir(exist_ok=True, parents=True)
    download_images(dest, urls=search_images(f'{o} photo'))
    time.sleep(5)
    resize_images(path/o, max_size=400, dest=path/o)
```

```diff
-searches = 'forest','bird'
+searches = 'forest', 'bird'
 path = Path('bird_or_not')
-from time import sleep
 
 for o in searches:
     dest = (path/o)
     dest.mkdir(exist_ok=True, parents=True)
     download_images(dest, urls=search_images(f'{o} photo'))
-    sleep(10)  # Pause between searches to avoid over-loading server
-    download_images(dest, urls=search_images(f'{o} sun photo'))
-    sleep(10)
-    download_images(dest, urls=search_images(f'{o} shade photo'))
-    sleep(10)
+    time.sleep(5)
     resize_images(path/o, max_size=400, dest=path/o)
```

### Spiegazione tecnica, riga per riga

- `searches = 'forest','bird'` — è una **tupla** (le parentesi sono opzionali in Python). L'ordine qui è `forest` prima, `bird` dopo — ma è irrilevante per le etichette finali, perché fastai ordinerà le classi alfabeticamente nel vocabolario. Tienilo a mente per la cella 12.
- `path = Path('bird_or_not')` — `Path` arriva da `fastai.vision.all` (che ripubblica la `Path` di `pathlib`, ulteriormente estesa da fastcore con metodi come `.ls()`).
- `dest = (path/o)` — l'operatore `/` su un `Path` **non è una divisione**: è overloading dell'operatore per concatenare percorsi. `Path('bird_or_not')/'bird'` produce `bird_or_not/bird`. È il modo moderno e cross-piattaforma di costruire percorsi (funziona sia con `/` su Linux/Mac sia con `\` su Windows, senza cambiare il codice).
- `dest.mkdir(exist_ok=True, parents=True)` — `parents=True` crea anche le cartelle intermedie mancanti (`bird_or_not/` se non esiste); `exist_ok=True` evita l'errore se la cartella c'è già, rendendo la cella **idempotente**: puoi rieseguirla senza rompere nulla.
- `search_images(f'{o} photo')` — la f-string costruisce la query (`'bird photo'`, `'forest photo'`). **Nota critica: qui `max_images` non è passato**, quindi vale il default `200`. Questa cella cerca fino a 200 immagini per query, non 1.
- `download_images(dest, urls=...)` — funzione di `fastai.vision.utils`. Scarica in **parallelo su più thread** e, cosa fondamentale, **ignora silenziosamente i download falliti** (URL morti, timeout, 403). Non solleva eccezioni: preferisce restituire 180 immagini su 200 piuttosto che fermarsi al primo errore. Questa tolleranza è esattamente il motivo per cui serve la cella 9 di pulizia.
- `sleep(...)` — pausa tra le ricerche per non farsi bloccare dal rate-limiter di DuckDuckGo. L'Originale usa 10 secondi, il Mio 5.
- `resize_images(path/o, max_size=400, dest=path/o)` — ridimensiona ogni immagine perché il lato più lungo sia al massimo 400px. Poiché `dest` è la stessa cartella di origine, **sovrascrive gli originali**. Riduce lo spazio su disco e, soprattutto, accelera il caricamento durante il training (leggere e decodificare un JPEG da 4000px per poi ridurlo a 192px a ogni epoca sarebbe uno spreco enorme di CPU).

### In parole semplici

Questa è la cella che costruisce davvero il dataset. Per ognuna delle due categorie crea una cartella (`bird_or_not/bird/` e `bird_or_not/forest/`) e ci scarica dentro fino a 200 foto, poi le rimpicciolisce tutte per non occupare spazio inutile. Le pause servono a non "bussare" troppo in fretta al motore di ricerca, che altrimenti potrebbe bloccarti temporaneamente.

**La differenza che conta davvero:** l'Originale fa **tre ricerche diverse** per categoria — "bird photo", "bird sun photo", "bird shade photo" — cioè cerca uccelli al sole e in ombra, non solo generici. Questo serve a dare al modello foto **variate**: se tutte le foto di uccelli fossero soleggiate e tutte quelle di foreste ombrose, il modello potrebbe imparare la scorciatoia sbagliata "luminoso = uccello" invece di guardare davvero la forma dell'animale. Il Mio fa una sola ricerca: dataset fino a tre volte più piccolo e meno vario, ma costruito in molto meno tempo.

### Extra

Le pause totali: Originale 30 secondi per categoria × 2 = 60 secondi di sola attesa; Mio 5 × 2 = 10 secondi. Sommato ai download, la differenza di tempo di esecuzione della cella è notevole — probabilmente la motivazione principale della semplificazione.

---

## Cella 9 — Pulizia del dataset · **identica in entrambi**

**Originale e Mio (byte per byte uguali)**
```python
failed = verify_images(get_image_files(path))
failed.map(Path.unlink)
len(failed)
```

### Spiegazione tecnica, riga per riga

- `get_image_files(path)` — cammina **ricorsivamente** nell'albero di cartelle sotto `bird_or_not/` e restituisce una `L` di tutti i file con estensione riconosciuta come immagine. Ricorsivo è essenziale: le immagini sono nelle sottocartelle `bird/` e `forest/`, non nella radice.
- `verify_images(...)` — prova ad **aprire davvero** ogni file con Pillow e verificarne l'integrità. Restituisce una `L` contenente solo i percorsi dei file **problematici**. Intercetta i casi tipici dello scraping: JPEG troncati per connessione caduta a metà, pagine HTML di errore salvate con estensione `.jpg`, formati non supportati dall'installazione di Pillow corrente (nell'esecuzione reale comparivano proprio i warning *"AVIF support not installed"*).
- `failed.map(Path.unlink)` — `.map` è un metodo di `L` che applica una funzione a ogni elemento. Il dettaglio elegante: `Path.unlink` è passato come **metodo non legato** (unbound), quindi `Path.unlink(p)` equivale a `p.unlink()` — cioè "cancella il file". È un idioma fastcore molto conciso rispetto a `for p in failed: p.unlink()`.
- `len(failed)` — ultima espressione, stampata da Jupyter: quante immagini sono state scartate. Nell'esecuzione reale documentata negli output: **5**.

### Perché è identica nei due file

Perché non c'è niente da personalizzare: è un passaggio di igiene obbligatorio quando i dati arrivano da internet, e la formulazione fastai è già la più compatta possibile. Nessuna delle motivazioni che hanno guidato le altre modifiche del fork (pacchetto rinominato, `!pip`→`%pip`, meno immagini per velocità) tocca questa cella. È lo stesso motivo per cui è identica anche la cella 6: il fork ha cambiato solo ciò che era rotto o soggetto a preferenza.

### In parole semplici

Quando scarichi centinaia di immagini da internet, alcune arrivano inevitabilmente rovinate: download interrotto a metà, oppure il sito ti ha restituito una pagina di errore invece della foto. Se queste finissero nell'allenamento, il modello si bloccherebbe con un errore. Questa cella le controlla tutte una per una, individua quelle rotte, le cancella, e ti dice quante ne ha buttate.

### Extra

Questa cella è importante concettualmente perché è la **conseguenza diretta** della scelta di costruirsi il dataset da soli. Il notebook del Libro non ha nulla di simile, e non per pigrizia: partendo da un dataset accademico già curato, non ci sono file rotti da rimuovere. È il prezzo (giusto) da pagare per lavorare con dati del mondo reale.

---

## Cella 10 — DataBlock e DataLoaders

**Originale**
```python
dls = DataBlock(
    blocks=(ImageBlock, CategoryBlock), 
    get_items=get_image_files, 
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=[Resize(192, method='squish')]
).dataloaders(path)

dls.show_batch(max_n=6)
```

**Mio**
```python
dls = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=[Resize(192, method='squish')]
).dataloaders(path, bs=32)

dls.show_batch(max_n=6)
```

```diff
     item_tfms=[Resize(192, method='squish')]
-).dataloaders(path)
+).dataloaders(path, bs=32)
```

*(le altre righe differiscono solo per spazi finali rimossi)*

### Spiegazione tecnica, parametro per parametro

- `DataBlock(...)` — non è il dataset: è un **progetto/ricetta** che descrive *come* costruirlo. Solo la successiva chiamata `.dataloaders(path)` lo applica a dati concreti. Questa separazione permette di riusare la stessa ricetta su cartelle diverse.
- `blocks=(ImageBlock, CategoryBlock)` — dichiara i tipi di input e output: immagine in ingresso, **una singola categoria** in uscita. Se il problema fosse multi-etichetta si userebbe `MultiCategoryBlock`; se fosse regressione, `RegressionBlock`. Questa tupla è ciò che determina automaticamente anche la funzione di loss usata più avanti (`CrossEntropyLoss` per la classificazione a singola etichetta).
- `get_items=get_image_files` — la funzione (passata come oggetto, senza parentesi!) che elenca gli elementi grezzi.
- `splitter=RandomSplitter(valid_pct=0.2, seed=42)` — divide i dati in **80% training** (le immagini su cui il modello impara) e **20% validation** (immagini tenute da parte per misurare quanto ha imparato davvero, mai usate per aggiornare i pesi). Il `seed=42` fissa il generatore pseudo-casuale, così la divisione è **identica a ogni riesecuzione** — indispensabile per confrontare esperimenti in modo onesto. (Curiosità: 42 come seed è una convenzione scherzosa diffusissima nel software, riferimento a *Guida galattica per autostoppisti*.)
- `get_y=parent_label` — ricava l'etichetta dal **nome della cartella genitore** del file: `bird_or_not/bird/xyz.jpg` → etichetta `"bird"`. È il motivo per cui la cella 8 doveva creare quelle sottocartelle con quei nomi precisi.
- `item_tfms=[Resize(192, method='squish')]` — trasformazione applicata a **ogni singola immagine** prima di raggrupparla in un batch (necessario perché la GPU richiede tensori di dimensione uniforme). `method='squish'` **deforma** l'immagine per farla entrare nel quadrato 192×192, invece di ritagliarla: conserva tutto il contenuto ma altera le proporzioni. L'alternativa `'crop'` (default di `Resize`) fa l'opposto: proporzioni intatte, bordi tagliati via.
- `.dataloaders(path, bs=32)` — **la differenza funzionale reale.** Il batch size di default di fastai è **64**: l'Originale, non specificandolo, allena a 64; il Mio lo dimezza a 32. Conseguenze concrete: con batch più piccoli si fanno **il doppio degli aggiornamenti dei pesi per epoca**, si usa meno memoria GPU, ma le stime del gradiente sono più rumorose (calcolate su meno esempi). Non è meglio né peggio in assoluto — su GPU con poca VRAM, o dataset piccoli, 32 è una scelta ragionevole.
- `dls.show_batch(max_n=6)` — puramente diagnostico: mostra 6 immagini con la relativa etichetta. Serve a intercettare *prima* dell'allenamento errori grossolani (etichette invertite, immagini nere, ritagli sbagliati).

### In parole semplici

Qui si prepara il "materiale di studio" per il modello. Si dice: dove sono le immagini, come dividerle tra esercizi da studiare (80%) e verifica finale (20%), come capire l'etichetta corretta di ognuna (guardando la cartella in cui si trova), e a che dimensione ridurle tutte. Il *batch size* è quante immagini il modello guarda insieme prima di aggiornare quello che ha imparato: come studiare 32 flashcard alla volta invece di 64 — gruppi più piccoli significano ripassare più spesso e occupare meno memoria, ma con "voti" un po' più ballerini. `show_batch` alla fine è solo un controllo a occhio: ti fa vedere 6 immagini con la loro etichetta, per accorgerti subito se qualcosa è impostato male.

### Extra

Un limite condiviso da tutti e tre i notebook: `item_tfms` c'è, ma manca del tutto `batch_tfms=aug_transforms()`, cioè la **data augmentation** (rotazioni, ribaltamenti, variazioni di luminosità applicate al volo durante il training). Su dataset piccoli come questo l'augmentation è di solito la singola aggiunta con il miglior rapporto sforzo/beneficio contro l'overfitting — è la prima cosa da provare per migliorare il notebook.

---

## Cella 11 — Creazione del learner e training

**Originale**
```python
learn = vision_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(3)
```

**Mio**
```python
learn =  vision_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(3)
```

```diff
-learn = vision_learner(dls, resnet18, metrics=error_rate)
+learn =  vision_learner(dls, resnet18, metrics=error_rate)
 learn.fine_tune(3)
```

*(unica differenza: un doppio spazio dopo `=`. Funzionalmente identiche.)*

### Spiegazione tecnica, riga per riga

- `vision_learner(dls, resnet18, metrics=error_rate)` — costruisce un oggetto `Learner`, che tiene insieme **tre cose**: i dati (`dls`), il modello, e la strategia di ottimizzazione. Il modello è assemblato automaticamente: prende il **corpo convoluzionale di resnet18 pre-addestrato su ImageNet** (~11,7 milioni di parametri, allenato su 1,2 milioni di foto di 1000 categorie diverse), **butta via la sua testa originale** a 1000 uscite, e ci attacca una **testa nuova** (pooling adattivo medio+massimo, batch-norm, dropout, strati lineari) dimensionata sulle **2 classi** del problema, con pesi inizializzati casualmente. Nota storica: fino a fastai 2.5 questa funzione si chiamava `cnn_learner` — se trovi tutorial vecchi con quel nome, è la stessa cosa.
- `metrics=error_rate` — **non influenza l'allenamento**. La funzione che guida l'ottimizzazione è la *loss* (scelta automaticamente in base ai `blocks`: cross-entropy). La metrica serve solo all'essere umano: viene calcolata sul validation set a fine di ogni epoca e stampata in tabella. `error_rate` è semplicemente `1 - accuracy`.
- `learn.fine_tune(3)` — è la ricetta di **transfer learning** best-practice di fastai, e dietro questa singola riga succedono due fasi distinte:
  - **Fase 1 (1 epoca, default `freeze_epochs=1`)**: il corpo pre-addestrato viene **congelato** (i suoi pesi non si aggiornano) e si allena solo la testa nuova. Questo è cruciale: la testa parte da pesi casuali, quindi all'inizio produce errori enormi e gradienti enormi; se il corpo non fosse congelato, quei gradienti distruggerebbero le feature visive già ottime imparate su ImageNet.
  - **Fase 2 (3 epoche, il numero passato)**: si **scongela** tutta la rete e si allena end-to-end usando **learning rate discriminativi** — un tasso di apprendimento molto basso per gli strati iniziali (che riconoscono bordi, texture, pattern universali validi per qualsiasi immagine) e progressivamente più alto per gli strati finali (che riconoscono concetti specifici del dominio). Il tutto con una schedulazione *one-cycle*: il learning rate sale e poi scende lungo l'epoca.
- Perché funziona così bene su così poche immagini: il modello non sta imparando "cos'è un'immagine" da zero — quello lo sa già grazie a ImageNet. Sta solo imparando a **ricombinare feature che possiede già** per distinguere due categorie nuove. È esattamente per questo che 200 foto bastano per arrivare al 100% di accuratezza, dove partendo da zero ne servirebbero centinaia di migliaia.

### In parole semplici

Questa è la cella che **allena il modello**. `resnet18` è una rete neurale già esperta di immagini in generale: qualcun altro l'ha allenata per settimane su oltre un milione di foto di ogni genere. Invece di ripartire da zero, la si "specializza" sul tuo problema — questo si chiama *fine-tuning*, cioè "messa a punto". Funziona in due tempi: prima si insegna solo all'ultimo pezzo della rete a distinguere uccelli da foreste (un giro veloce, tenendo fermo tutto il resto per non rovinare quello che già sa), poi si affina l'intera rete per altri 3 giri, migliorandola gradualmente. È come prendere un fotografo esperto e insegnargli a riconoscere due specie particolari: molto più veloce che insegnare a qualcuno cos'è una fotografia partendo da zero.

### Extra

Qui Mio e Originale coincidono perfettamente — nessuna delle due versioni ha toccato la scelta del modello o il numero di epoche. È significativo: chi ha fatto il fork ha modificato l'infrastruttura (pacchetti, installazione, quantità di dati) ma **non ha toccato una virgola delle scelte di machine learning**. Il cuore modellistico del notebook è rimasto quello di Jeremy Howard.

---

## Cella 12 — Predizione finale · **identica in entrambi**

**Originale e Mio (byte per byte uguali)**
```python
is_bird,_,probs = learn.predict(PILImage.create('bird.jpg'))
print(f"This is a: {is_bird}.")
print(f"Probability it's a bird: {probs[0]:.4f}")
```

### Spiegazione tecnica, riga per riga

- `PILImage.create('bird.jpg')` — `PILImage` è il tipo immagine di fastai (sottoclasse di `PIL.Image.Image` arricchita). `.create()` è un costruttore flessibile che accetta un percorso, un oggetto `Path`, dei byte grezzi, un array numpy o un tensore — qui riceve la stringa del file scaricato nella cella 6.
- `learn.predict(...)` — esegue l'inferenza. Sotto il cofano applica all'immagine **le stesse trasformazioni usate per il validation set** (quindi solo il `Resize(192, squish)`, senza augmentation casuali), mette il modello in modalità valutazione, calcola l'output e gli applica softmax.
- `is_bird,_,probs = ...` — **spacchettamento di tupla**: `predict` restituisce sempre 3 valori. Il primo è l'etichetta decodificata come stringa leggibile (`'bird'` o `'forest'`); il secondo è l'indice numerico della classe predetta, scartato con `_` (convenzione Python per "valore che non mi interessa"); il terzo è il **tensore completo delle probabilità**, una per classe, che somma a 1.
- `f"…{is_bird}…"` — f-string, interpolazione diretta della variabile nella stringa.
- `probs[0]:.4f` — `probs[0]` è la probabilità della **prima classe del vocabolario**, e `:.4f` la formatta con 4 decimali. Punto delicato: perché l'indice 0 corrisponde proprio a "bird"? Perché `CategoryBlock` costruisce il vocabolario delle classi **ordinandole alfabeticamente** — e `'bird' < 'forest'`. Funziona, ma è una **dipendenza implicita e silenziosa**: se un giorno si rinominassero le cartelle (poniamo `uccello` e `foresta`), l'indice 0 punterebbe a `foresta` e il codice continuerebbe a girare stampando allegramente il numero sbagliato, senza alcun errore. Un modo robusto sarebbe `probs[dls.vocab.o2i['bird']]`.

### Perché è identica nei due file

Perché è la "riga d'arrivo" del notebook e funziona già: non dipende da nessun pacchetto esterno rinominato, non ha parametri di performance da tarare, non contiene nulla di deprecato. È il terzo caso — insieme alle celle 6 e 9 — in cui il fork non ha avuto nulla da correggere. Emerge un pattern chiaro: **le modifiche del fork si concentrano tutte nella prima metà del notebook** (setup, pacchetti, raccolta dati), mentre la seconda metà (preparazione, training, inferenza) è rimasta sostanzialmente intatta.

### In parole semplici

È il momento della verità: prendi la foto di uccello scaricata all'inizio — che il modello non ha **mai visto** durante l'allenamento — e gli chiedi "cos'è questa?". Lui risponde con un'etichetta (`bird` o `forest`) e un numero tra 0 e 1 che dice quanto è sicuro: `1.0000` significa sicurezza totale. Nell'esecuzione reale documentata negli output, il risultato era esattamente `This is a: bird.` con probabilità `1.0000`.

### Extra

Una probabilità di 1.0000 non va letta come "il modello è infallibile": significa che, dopo il softmax, l'altra classe ha ricevuto una probabilità così bassa da arrotondarsi a zero con 4 decimali. Su un problema binario tra due categorie visivamente lontanissime (un uccello e una foresta), con un modello pre-addestrato su ImageNet, è un risultato del tutto atteso — non una prova che il modello sia bravo su casi difficili.

---

## Cella 13 — Chiusura del notebook

**Originale** *(due celle **markdown**)*
```markdown
Good job, resnet18. :)

So, as you see, in the space of a few years, creating computer vision classification
models has gone from "so hard it's a joke" to "trivially easy and free"! …
```
```markdown
Now it's your turn. Click "Copy & Edit" and try creating your own image classifier
using your own image searches!

If you enjoyed this, please consider clicking the "upvote" button in the top-right…
```

**Mio** *(due celle **di codice**, vuote)*
```python

```
```python

```

### Spiegazione tecnica

Differenza non solo di contenuto ma di **tipo di cella**: markdown contro codice. L'Originale chiude con testo — una riflessione sul salto compiuto dalla computer vision (richiamando la battuta XKCD del 2015 citata all'inizio del notebook, che considerava "riconoscere un uccello" un problema da team di ricerca e cinque anni di lavoro) e un invito esplicito a cliccare "Copy & Edit" e lasciare un upvote. Quest'ultimo dettaglio rivela la natura del file: è un **notebook pubblico di Kaggle**, dove la visibilità nella community dipende dagli upvote ricevuti, e "Copy & Edit" è il meccanismo con cui un lettore si crea la propria copia modificabile — letteralmente l'azione che ha generato la catena di file da cui deriva `basics-model.ipynb`.

### In parole semplici

L'autore originale chiude con un messaggio di incoraggiamento e l'invito a farne una versione tua. Nel file Mio, avendo già fatto esattamente questo, quel testo è stato cancellato e sostituito da due celle vuote — spazio bianco pronto per i prossimi esperimenti.

### Extra

Queste due celle vuote sono, in un certo senso, la firma più chiara del passaggio da "notebook da leggere" a "notebook da usare". L'Originale è un prodotto finito da pubblicare; il Mio è un quaderno di lavoro aperto.

---

# PARTE B · Struttura equivalente con il Libro

Il codice del Libro non deriva dallo stesso file, quindi un diff riga-per-riga produrrebbe solo rumore. Qui il confronto è per **fase equivalente**, con il codice completo di entrambe le parti.

---

## Fase 1 — Setup ambiente

**Mio**
```python
import socket,warnings
import time
try:
    socket.setdefaulttimeout(1)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('1.1.1.1', 53))
except socket.error as ex: raise Exception("STOP: No internet...")

import os, importlib
iskaggle = bool(os.environ.get("KAGGLE_KERNEL_RUN_TYPE", ""))
if iskaggle:
    %pip -q install -U fastai ddgs numpy==1.24.3
    importlib.invalidate_caches()
```

**Libro**
```python
#hide
! [ -e /content ] && pip install -Uqq fastbook
import fastbook
fastbook.setup_book()
```
```python
#hide
from fastbook import *
```

### Spiegazione tecnica

- `! [ -e /content ] && pip install -Uqq fastbook` — non è Python, è **shell**. `[ -e /content ]` è il test bash "esiste il percorso `/content`?"; `&&` esegue il comando successivo solo se il test riesce. `/content` è la directory di lavoro caratteristica di **Google Colab**: questa riga significa quindi "se siamo su Colab, installa fastbook". È lo stesso identico pattern dell'`if iskaggle:`, ma scritto in shell invece che in Python e con un altro ambiente come bersaglio.
- `fastbook.setup_book()` — funzione della libreria `fastbook`, scritta apposta per accompagnare il libro. Fa in una riga ciò che il notebook Mio fa in due celle: verifica/installa `fastai` e `fastcore`, imposta opzioni di visualizzazione (larghezza colonne pandas, backend grafico inline), rileva l'ambiente (Colab / Kaggle / locale) e adatta la configurazione, e su Colab gestisce eventualmente il mount di Google Drive per salvare i dati tra sessioni.
- `from fastbook import *` — wildcard che porta dentro fastai completo più le utility del libro: `gv` (per i diagrammi Graphviz), `image_cat()`, `widgets`, `SimpleNamespace`.
- `#hide` — non è un commento qualsiasi: è una **direttiva di nbdev/Jupyter Book** che significa "non mostrare questa cella nella versione HTML o cartacea del libro". È la prova diretta che questo `.ipynb` non è solo eseguibile, ma è anche il **sorgente da cui viene generato il libro pubblicato**. Le varianti presenti più avanti nel file sono `#hide_input` (mostra solo l'output, nascondi il codice — usato per i diagrammi, dove al lettore interessa la figura, non il codice che la disegna) e `#hide_output` (l'opposto).

### In parole semplici

Nel notebook Mio si fanno il controllo di internet e l'installazione dei pacchetti passo per passo, a mano. Il Libro nasconde tutto dietro un'unica funzione (`setup_book()`) scritta apposta dagli autori, così il lettore non deve capire nulla di installazioni per iniziare. Le etichette `#hide` servono al sistema che trasforma il notebook nelle pagine del libro: dicono "questa cella è roba tecnica, non stamparla nel libro" — un dettaglio che negli altri notebook non ha senso, perché non devono diventare un libro.

### Extra

Il fatto che il libro sia scritto *dentro* i notebook non è un dettaglio marginale: è una scelta metodologica dichiarata dagli autori (c'è una intera sezione del capitolo intitolata *"Sidebar: This Book Was Written in Jupyter Notebooks"*). Ogni figura, ogni output e ogni tabella del libro stampato sono stati generati eseguendo davvero il codice — niente screenshot, niente risultati riportati a mano.

---

## Fase 2 — Procurarsi le immagini

**Mio** *(la parte più corposa del notebook: 6 celle di codice)*
```python
from fastcore.all import L
from ddgs import DDGS
def search_images_ddg(keywords, max_images=200):
    with DDGS() as ddg:
        return L(ddg.images(keywords, max_results=max_images)).itemgot('image')
search_images = search_images_ddg

urls = search_images('bird photos', max_images=1)
urls[0]

from fastdownload import download_url
dest = 'bird.jpg'
download_url(urls[0], dest, show_progress=False)
from fastai.vision.all import *
im = Image.open(dest)
im.to_thumb(256,256)

download_url(search_images('forest photos', max_images=1)[0], 'forest.jpg', show_progress=False)
Image.open('forest.jpg').to_thumb(256, 256)

searches = 'forest', 'bird'
path = Path('bird_or_not')
for o in searches:
    dest = (path/o)
    dest.mkdir(exist_ok=True, parents=True)
    download_images(dest, urls=search_images(f'{o} photo'))
    time.sleep(5)
    resize_images(path/o, max_size=400, dest=path/o)

failed = verify_images(get_image_files(path))
failed.map(Path.unlink)
len(failed)
```

**Libro** *(una riga)*
```python
from fastai.vision.all import *
path = untar_data(URLs.PETS)/'images'
```

### Spiegazione tecnica

- `untar_data(URLs.PETS)` — scarica un archivio `.tgz` da un URL registrato nella classe `URLs` (ospitato su S3 dalla stessa fastai), lo estrae in una **cache locale** (`~/.fastai/data/`) e restituisce il `Path` della cartella estratta. Se il dataset è già in cache da un'esecuzione precedente, salta il download e ritorna subito: rieseguire la cella costa zero.
- `URLs.PETS` — punta all'**Oxford-IIIT Pet Dataset**, un dataset accademico: 37 razze di cani e gatti, circa 200 immagini per razza, ~7.400 immagini totali, tutte verificate e con annotazioni. Zero file rotti, classi bilanciate.
- `/'images'` — il solito operatore di concatenazione percorsi: entra nella sottocartella con le foto.
- Il dataset usa una convenzione di naming precisa: i file delle **razze di gatto iniziano con la lettera maiuscola** (`Bengal_101.jpg`), quelli dei cani con la minuscola (`beagle_32.jpg`). È esattamente questa convenzione che la Fase 3 sfrutterà con `is_cat`.

### In parole semplici

Nel notebook Mio bisogna andare "a caccia" delle immagini su internet: definire una funzione di ricerca, testarla, scaricarne centinaia, ripulire quelle rotte — sei celle di lavoro vero. Il Libro invece scarica un pacchetto di foto **già pronto, già etichettato e già pulito**, preparato anni fa da ricercatori dell'Università di Oxford. Una riga di codice, zero pulizia necessaria, perché il lavoro sporco l'ha già fatto qualcun altro.

### Extra

Questa è la differenza filosofica più profonda tra i due notebook. Quello Mio insegna qualcosa che il Libro (in questo capitolo) non insegna affatto: **come ci si procura i dati quando nessuno te li ha preparati**. Nel mondo reale è la parte che occupa la maggioranza del tempo di un progetto di machine learning — e non è un caso che il notebook di Jeremy Howard da cui deriva sia stato scritto proprio per mostrare quello, come complemento pratico al capitolo teorico del libro.

---

## Fase 3 — Preparazione dei dati (DataLoaders)

**Mio**
```python
dls = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=[Resize(192, method='squish')]
).dataloaders(path, bs=32)

dls.show_batch(max_n=6)
```

**Libro**
```python
def is_cat(x): return x[0].isupper()
dls = ImageDataLoaders.from_name_func(
    path, get_image_files(path), valid_pct=0.2, seed=42,
    label_func=is_cat, item_tfms=Resize(224))
```

### Spiegazione tecnica

- `ImageDataLoaders.from_name_func(...)` — è una **factory di alto livello**: internamente costruisce comunque un `DataBlock` equivalente, ma espone meno parametri, pre-cablando le scelte del caso comune ("immagini in cartella, etichetta ricavabile dal nome del file"). Stessa libreria, stesso risultato, meno righe e meno visibilità sui passaggi.
- `def is_cat(x): return x[0].isupper()` — `x` è il **nome del file** (non il percorso completo: `from_name_func` applica la funzione a `Path.name`). `x[0]` è il primo carattere, `.isupper()` verifica se è maiuscolo. Restituisce `True`/`False`, quindi il vocabolario delle classi risultante è **booleano**, non testuale come `['bird','forest']`.
- `label_func=is_cat` — è l'equivalente di `get_y=parent_label`, ma legge da un posto diverso: **il nome del file** invece della **cartella genitore**. Due strategie per due strutture dati diverse: nel caso Mio le immagini sono state organizzate in cartelle apposta, qui i metadati erano già codificati nei nomi.
- `Resize(224)` **senza `method=`** — usa il default di fastai, che è **`'crop'`** (ritaglio centrato), non `'squish'`. Il crop conserva le proporzioni naturali ma **taglia via i bordi**; lo squish conserva tutto ma **deforma**. Su foto di animali il crop centrato ha senso (il soggetto è quasi sempre al centro); su foto generiche da ricerca web lo squish è più prudente perché non rischia di tagliare via proprio l'uccello.
- `224` invece di `192` — 224×224 è la risoluzione **storica standard** con cui sono state addestrate le architetture ImageNet (resnet incluse). Usarla significa dare al modello input della stessa scala su cui è stato pre-addestrato. I 192px del notebook Mio sono un po' più piccoli: training più veloce, un filo meno dettaglio.
- Assente nel Libro: `bs=` (quindi 64 di default) e `show_batch` (il libro mostra le immagini più avanti, in una cella dedicata).

### In parole semplici

Entrambi dicono al modello la stessa cosa: dove sono le immagini, come capire l'etichetta di ognuna, come dividerle tra studio e verifica, a che dimensione ridurle. Cambia **da dove si legge l'etichetta**: nel Mio si guarda in che cartella si trova la foto (`bird/` o `forest/`), nel Libro si guarda se il nome del file inizia con la maiuscola (maiuscola = gatto). E cambia **come si ridimensiona**: il Mio "schiaccia" l'immagine nel quadrato senza perdere niente ma deformandola, il Libro la ritaglia al centro perdendo i bordi ma mantenendo le proporzioni naturali.

### Extra

Il `DataBlock` è considerato l'API "vera" di fastai: più verbosa, ma capace di gestire qualsiasi combinazione di input e output (immagini→maschere, testo→categoria, tabelle→numeri). Le `ImageDataLoaders.from_*` sono scorciatoie costruite sopra di esso per i casi frequenti. Il Libro parte dalla scorciatoia per far vedere subito un risultato, e introduce il `DataBlock` completo solo nel capitolo 2 — è una scelta didattica precisa: prima il "wow", poi i dettagli.

---

## Fase 4 — Training

**Mio**
```python
learn = vision_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(3)
```

**Libro**
```python
learn = vision_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(1)
```

### Spiegazione tecnica

Stessa identica funzione, stessa metrica, stesso meccanismo di fine-tuning in due fasi descritto nella cella 11 della Parte A. Cambiano due soli parametri:

- `resnet34` vs `resnet18` — 34 strati contro 18, circa **21,8 milioni di parametri contro 11,7**. Più capacità di rappresentazione: su ImageNet resnet34 raggiunge un'accuratezza top-1 nota di circa il 73% contro il ~70% di resnet18. Il costo è tempo di training e di inferenza maggiore, e più memoria GPU.
- `fine_tune(1)` vs `fine_tune(3)` — il Libro fa **una sola epoca** nella seconda fase. Sommando la fase congelata iniziale, sono in tutto 2 passaggi sui dati, contro i 4 del notebook Mio.

Il Libro può permettersi meno epoche perché gioca con carte migliori: un dataset **già pulito e bilanciato** (Fase 2) e un modello **più capace**. E soprattutto perché l'obiettivo è diverso: dimostrare in trenta secondi di esecuzione che "si può fare", non spremere l'ultimo punto percentuale di accuratezza. Il commento `# CLICK ME` sopra quella cella nel Libro lo dice apertamente — è pensata per essere il primo pulsante che un lettore preme in tutto il libro.

### In parole semplici

È come scegliere tra due studenti: uno più semplice e veloce da istruire, a cui fai fare 3 ripassi (resnet18), e uno più portato che impara bene anche con un ripasso solo (resnet34) — anche perché il suo materiale di studio è già ordinato e pulito, mentre l'altro è stato raccolto al volo da internet.

### Extra

Nessuno dei tre notebook usa `learn.lr_find()`, lo strumento fastai che cerca automaticamente il learning rate ottimale prima di allenare. Non serve, perché `fine_tune()` applica già valori di default molto solidi — ma è il passo successivo naturale quando si vuole spingere davvero l'accuratezza.

---

## Fase 5 — Predizione

**Mio**
```python
is_bird,_,probs = learn.predict(PILImage.create('bird.jpg'))
print(f"This is a: {is_bird}.")
print(f"Probability it's a bird: {probs[0]:.4f}")
```

**Libro**
```python
#hide_output
uploader = widgets.FileUpload()
uploader
```
```python
#hide
# For the book, we can't actually click an upload button, so we fake it
uploader = SimpleNamespace(data = ['images/chapter1_cat_example.jpg'])
```
```python
img = PILImage.create(uploader.data[0])
is_cat,_,probs = learn.predict(img)
print(f"Is this a cat?: {is_cat}.")
print(f"Probability it's a cat: {probs[1].item():.6f}")
```

### Spiegazione tecnica

- `widgets.FileUpload()` — controllo interattivo di **ipywidgets**: renderizza un vero pulsante HTML di upload nel browser e, tramite il protocollo *comm* di Jupyter (un canale bidirezionale tra la pagina web e il kernel Python), trasferisce i byte del file scelto dall'utente dentro l'oggetto `uploader`. Permette a un lettore che sta eseguendo il notebook dal vivo di provare il modello su una **propria** foto.
- `#hide_output` sopra — significa "nel libro stampato mostra il codice ma non l'output": un pulsante di upload in un PDF sarebbe inutile.
- `SimpleNamespace(data = [...])` — `SimpleNamespace` (dal modulo `types`) crea al volo un oggetto con attributi arbitrari. Qui **rimpiazza** l'uploader vero con un finto oggetto che espone lo stesso attributo `.data`, puntando a una foto di esempio inclusa nel repo del libro. È un trucco di sostituzione per far funzionare l'esempio anche quando non c'è nessun essere umano a cliccare (generazione della versione statica del libro). Le due celle sono di fatto **mutuamente esclusive nell'uso reale**: o si clicca davvero, o si esegue la finta — un dettaglio che a una lettura veloce del notebook può sfuggire completamente.
- `probs[1].item()` — due differenze. L'indice `1` invece di `0` perché qui il vocabolario è booleano (`False`/`True` derivati da `is_cat`) e la posizione 1 corrisponde a "è un gatto". `.item()` converte il tensore PyTorch a elemento singolo in un normale `float` Python — non strettamente necessario per la formattazione, ma esplicito. E `.6f` invece di `.4f`: sei decimali invece di quattro.
- La stessa fragilità già segnalata nella Parte A si ripresenta identica: l'indice della classe è cablato a mano e dipende dall'ordinamento interno del vocabolario.

### In parole semplici

Nel notebook Mio si testa sempre sulla stessa foto scaricata all'inizio: comodo e ripetibile, ma statico. Il Libro fa comparire un vero pulsante "carica file", così chi legge può provare il modello con **una foto sua** — molto più coinvolgente. Siccome però un libro stampato non si può cliccare, la cella subito dopo finge il caricamento usando una foto di esempio già pronta, in modo che l'esempio funzioni comunque anche sulla pagina di carta.

### Extra

Il numero di decimali non è casuale: con `.6f` il Libro può mostrare qualcosa come `0.999998` invece di un arrotondato `1.0000`, comunicando meglio l'idea che il modello produce **probabilità continue**, non certezze binarie — un punto concettuale che il capitolo insiste molto a far passare.

---

# Sintesi finale

| | Mio | Originale | Libro |
|---|---|---|---|
| **File** | `basics-model.ipynb` | `reference/00_is_it_a_bird_creating_a_model_from_your_own_data.ipynb` | `reference/01_intro.ipynb` |
| **Provenienza** | fork personale | notebook Kaggle di Jeremy Howard | cap. 1 di *Deep Learning for Coders* (fastbook) |
| Origine dei dati | ricerca web (DuckDuckGo) | ricerca web (DuckDuckGo) | dataset accademico pronto |
| Query per categoria | 1 | 3 (photo/sun/shade) | — |
| Pulizia necessaria | sì (`verify_images`) | sì (`verify_images`) | no |
| API dati | `DataBlock` (esplicita) | `DataBlock` (esplicita) | `ImageDataLoaders` (scorciatoia) |
| Etichette da | cartella (`parent_label`) | cartella (`parent_label`) | nome file (`is_cat`) |
| Resize | 192px, squish (deforma) | 192px, squish (deforma) | 224px, crop (ritaglia) |
| Batch size | 32 (esplicito) | 64 (default) | 64 (default) |
| Modello | resnet18 (~11,7M param) | resnet18 (~11,7M param) | resnet34 (~21,8M param) |
| Epoche fine-tune | 3 | 3 | 1 |
| Input predizione | file fisso | file fisso | upload interattivo |
| Celle di markdown | 6 | 19 | 171 |

**Pattern emerso dal confronto Mio ↔ Originale:** tutte le modifiche del fork si concentrano nella **prima metà** del notebook — pacchetti rinominati, `!pip`→`%pip`, pin di numpy, meno immagini scaricate. La **seconda metà** (pulizia, DataBlock, training, predizione) è rimasta praticamente intatta, con l'unica eccezione del `bs=32`. In altre parole: è stata aggiornata l'infrastruttura, non è stata toccata la sostanza di machine learning.
