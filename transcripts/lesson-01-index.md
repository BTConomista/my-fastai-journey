# Lezione 1 — indice analitico

*Practical Deep Learning for Coders* 2022, lezione 1 — **Getting started**.
Video: <https://youtu.be/8SF_h3xF3cE> (1h 22m 55s).

Serve a **trovare il minuto giusto** senza riguardarsi la lezione e senza avere il testo sotto
mano. I timestamp sono quelli del video: aprendo il link con `?t=` seguito dai secondi si salta
direttamente al punto.

Come si rigenera la trascrizione da cui è ricavato questo indice: [`README.md`](README.md).

---

## Mappa della lezione

Grana di due o tre minuti. Le voci in grassetto sono i punti a cui si torna più spesso.

| Minuto | Cosa succede |
|---|---|
| 00:00 | La vignetta xkcd di fine 2015: capire se una foto ritrae un uccello era l'esempio di compito "quasi impossibile". Promessa di costruirlo lì per lì |
| 01:06 | **Il classificatore in diretta.** Ricerca delle immagini per "bird photo" e "forest photo" |
| 02:04 | Perché servono numeri, e come ci si arriva dalle immagini. Download del dataset |
| 03:12 | **Il `DataBlock` che regge il modello**, e la prima occhiata alle immagini scaricate |
| 04:49 | Controllo visivo di quello che è arrivato dalla rete |
| 05:49 | Il conto finale: meno di due minuti dall'inizio |
| 06:55 | Cosa si imparerà nelle settimane successive |
| 07:54 | Immagini generate da testo: dove è arrivata la generazione |
| 10:03 | Cosa hanno costruito gli studenti delle edizioni precedenti |
| 11:13 | Modelli applicati a campi lontani dalla computer vision |
| 12:15 | **Come è insegnato il corso.** Dylan Wiliam, e il principio di mostrare prima il risultato |
| 14:14 | La struttura delle lezioni, e cosa aspettarsi dai compiti |
| 15:20 | La ricerca sull'educazione dietro l'approccio dall'alto verso il basso |
| 17:42 | Perché ascoltare Jeremy: percorso, libro, riconoscimenti |
| 20:07 | **Com'era prima delle reti neurali:** le *feature* progettate a mano, una per una |
| 22:12 | Perché conviene comunque il deep learning |
| 23:59 | **Zeiler e Fergus.** Cosa impara il primo strato di una rete: bordi, gradienti, macchie di colore |
| 24:52 | Gli strati successivi: pezzi di finestra, occhi, ruote |
| 25:54 | Come le feature si combinano in rilevatori sempre più specifici |
| 26:51 | **I tre miti:** quanta matematica, quanti dati, che computer servono davvero |
| 27:50 | Studenti che hanno trasformato serie temporali e movimenti del mouse in immagini |
| 29:42 | **Transfer learning:** partire da una rete già addestrata invece che da zero |
| 30:45 | PyTorch e TensorFlow, e come si è spostato l'ago della bilancia |
| 31:37 | Lo stesso compito scritto nei due modi, a confronto |
| 33:14 | La libreria fastai e i suoi strati di astrazione |
| 34:20 | **Dove si esegue il codice:** i server cloud, e perché non serve una macchina propria |
| 35:07 | Jupyter dal vivo: celle, esecuzione, output |
| 37:13 | La prosa nelle celle di testo e il markdown |
| 38:12 | **Il notebook bird-or-not riga per riga:** ricerca, download, scarto delle immagini rotte |
| 40:00 | La documentazione di fastai e come cercarci dentro |
| 41:37 | **`DataBlock`: l'oggetto da capire** se si vuole usare fastai su dati propri |
| 42:40 | Perché non serve mettere le mani nelle architetture |
| 43:49 | I parametri del `DataBlock`, uno per uno |
| 44:44 | `item_tfms`, il ridimensionamento e la separazione del set di validazione |
| 46:57 | **Dal `DataBlock` ai `DataLoaders`**, cioè a quello che PyTorch scorre davvero |
| 48:59 | Il `learner`, e cosa fa `fine_tune` |
| 50:13 | **Le metriche**, `resnet18`, `timm`, e i pesi che arrivano da ImageNet |
| 53:27 | `predict` su una singola immagine |
| 54:19 | **Oltre la computer vision:** cos'altro ha la stessa forma |
| 55:24 | Segmentazione: assegnare una categoria a ogni pixel |
| 56:47 | Le varianti dei `DataLoaders` per i diversi tipi di dato |
| 57:58 | Il learner per la segmentazione |
| 59:00 | Dati tabellari: colonne continue e categoriche |
| 60:59 | `tabular_learner`, e la differenza rispetto alla visione |
| 62:42 | **Filtraggio collaborativo:** i voti degli utenti ai film |
| 64:29 | Predizione e voto reale, messi accanto |
| 65:39 | I notebook del corso e dove stanno |
| 66:42 | Cos'altro si fa con un notebook — anche queste slide sono un notebook |
| 67:41 | **Cosa sa fare oggi il deep learning**, e quanto poco è ancora esplorato |
| 68:58 | NLP: dove i modelli sono lo stato dell'arte |
| 69:53 | Dove invece non arrivano |
| 70:57 | **Arthur Samuel, fine anni '50:** l'idea originale di machine learning |
| 71:56 | Un programma normale contro un modello: cosa cambia nello schema |
| 72:44 | Il modello come funzione matematica |
| 73:30 | **I pesi**, la misura di quanto il risultato è buono, e come si aggiornano |
| 74:27 | Il ciclo di addestramento visto per intero |
| 75:29 | Perché serve una funzione abbastanza flessibile: da lì nasce la rete neurale |
| 76:28 | Il modello addestrato torna a essere, di fatto, un programma |
| 77:38 | **Mandarlo in produzione:** `learn.predict` e i dettagli intorno |
| 78:54 | I compiti: sperimentare invece di rileggere |
| 79:50 | Il forum, e portarci il proprio lavoro |
| 80:49 | Perché tutto questo conta in pratica |
| 82:03 | Chiusura, e i quiz in fondo al capitolo del libro |

---

## Dove compare ogni concetto

Ricavato meccanicamente dalla trascrizione: per ogni termine, i minuti dei paragrafi in cui
compare. La prima colonna è il termine, la seconda quante volte, la terza dove.

Utile al contrario: se un concetto ha un solo timestamp, quello è il punto in cui viene
introdotto e spiegato — `timm`, `ImageNet` e `transfer learning` hanno un unico posto in cui
vengono trattati davvero.

| Concetto | Paragrafi | Minuti |
|---|---|---|
| `DataBlock` | 4 | 00:03:12, 00:41:37, 00:43:49, 00:46:57 |
| `item_tfms / Resize` | 2 | 00:03:12, 00:44:44 |
| `ethics / etica` | 1 | 00:11:13 |
| `Kaggle` | 6 | 00:18:55, 00:34:20, 00:35:07, 00:38:12, 00:50:13, 01:18:54 |
| `NLP` | 2 | 00:20:07, 01:08:58 |
| `predict` | 5 | 00:22:12, 00:53:27, 00:57:58, 01:16:28, 01:17:38 |
| `weights / parametri` | 7 | 00:23:59, 00:50:13, 01:11:56, 01:12:44, 01:13:30, 01:14:27 …(+1) |
| `Zeiler & Fergus` | 1 | 00:23:59 |
| `transfer learning` | 1 | 00:29:42 |
| `PyTorch` | 6 | 00:29:42, 00:30:45, 00:31:37, 00:46:57, 00:48:59, 00:50:13 |
| `TensorFlow` | 2 | 00:29:42, 00:30:45 |
| `Jupyter` | 7 | 00:33:14, 00:34:20, 00:35:07, 00:36:09, 00:37:13, 01:04:29 …(+1) |
| `architettura` | 3 | 00:41:37, 00:42:40, 00:44:44 |
| `valid_pct / validation set` | 2 | 00:44:44, 01:02:42 |
| `DataLoaders` | 6 | 00:46:57, 00:48:59, 00:56:47, 00:59:00, 00:59:55, 01:00:59 |
| `learner` | 5 | 00:48:59, 00:50:13, 00:57:58, 00:59:55, 01:02:42 |
| `fine_tune` | 3 | 00:50:13, 00:59:55, 01:02:42 |
| `resnet18 / resnet34` | 1 | 00:50:13 |
| `timm` | 1 | 00:50:13 |
| `pretrained` | 4 | 00:50:13, 00:59:55, 01:02:42, 01:07:41 |
| `ImageNet` | 1 | 00:50:13 |
| `segmentation` | 4 | 00:54:19, 00:55:24, 00:56:47, 00:57:58 |
| `tabular` | 3 | 00:57:58, 00:59:00, 00:59:55 |
| `collaborative filtering` | 2 | 01:00:59, 01:02:42 |
| `epoch` | 1 | 01:02:42 |
| `Arthur Samuel` | 2 | 01:10:57, 01:13:30 |
| `loss` | 3 | 01:13:30, 01:14:27, 01:16:28 |

Alcuni termini che ci si aspetterebbe **non compaiono** nel parlato della lezione 1: `error_rate`
viene mostrato a schermo ma non nominato in quei termini, e `SGD`, *gradient descent* e
*overfitting* restano fuori — sono materiale delle lezioni successive. La ricerca è sul testo
della trascrizione, quindi non vede quello che sta solo nelle slide o nel codice proiettato.
