# transcripts/

Le **trascrizioni delle lezioni video** del corso, per poter cercare nel parlato di Jeremy Howard
come si cerca in un file: trovare dove spiega `DataBlock`, rileggere il passaggio sul transfer
learning, ritrovare il minuto esatto da riguardare.

Per la mappa completa di un capitolo vedi il [README principale](../README.md).

| Lezione | Video | Durata | Trascrizione |
|---|---|---|---|
| 1 — *Getting started* | [`8SF_h3xF3cE`](https://youtu.be/8SF_h3xF3cE) | 1h 22m 55s | [`lesson01transcript_.md`](lesson01transcript_.md) (con timestamp) e [`lesson01transcript.txt`](lesson01transcript.txt) (solo testo), piu' [`lesson-01-index.md`](lesson-01-index.md) per navigarle |

---

## Cosa c'è qui

| File | Cos'è |
|---|---|
| `lesson01transcript_.md` | La trascrizione con i timestamp: 71 paragrafi da circa un minuto, ognuno aperto da `[hh:mm:ss]`, cioè il punto del video in cui comincia |
| `lesson01transcript.txt` | Lo stesso testo di seguito, senza timestamp. Comodo per cercarci dentro o per passarlo a un altro strumento |
| `lesson-01-index.md` | L'indice analitico: mappa della lezione e tabella concetto → minuti |
| `fetch.py` | Lo strumento che ricostruisce una trascrizione dai sottotitoli, per le prossime lezioni |

## Come si rigenera

```bash
pip install yt-dlp
python3 transcripts/fetch.py 8SF_h3xF3cE transcripts/lesson-01.md
```

Lo stesso comando, cambiando l'ID del video, vale per qualunque altra lezione. Il file che ne esce
ha 769 blocchi di sottotitolo raggruppati in 71 paragrafi, nello stesso formato di
`lesson01transcript_.md`. I file intermedi dello scaricamento (`.json3`, `.vtt`) restano fuori dal
repository: li tiene fuori il `.gitignore` di questa cartella.

**Da dove viene il testo.** Dai sottotitoli inglesi pubblicati insieme al video, che per questa
lezione sono *curati* e non generati automaticamente: hanno punteggiatura, maiuscole e nomi propri
scritti bene. È il motivo per cui vale la pena partire da lì invece di trascrivere l'audio con un
modello di speech-to-text — non ci sono errori di riconoscimento da correggere.

**Una nota su YouTube.** Oggi quasi tutti i player client di `yt-dlp` vengono respinti con
*"Sign in to confirm you're not a bot"*. L'unico che passa è `web_embedded`, ed è quello che
`fetch.py` forza. Se un domani lo script smettesse di funzionare, quasi certamente è quella la riga
da cambiare.

---

## Indice della lezione 1

Ricostruito da me scorrendo la trascrizione: serve a saltare al punto giusto del video, o del file
generato, senza doverlo leggere tutto. Qui sotto la versione per grandi blocchi; in
[`lesson-01-index.md`](lesson-01-index.md) c'e' quella a grana fine, con in piu' una tabella che dice
in quali minuti compare ciascun concetto — `DataBlock`, `fine_tune`, transfer learning e gli altri.

| Minuto | Argomento |
|---|---|
| 00:00 | La vignetta xkcd di fine 2015 — riconoscere un uccello in una foto come esempio di cosa è "quasi impossibile" — e la promessa di costruire proprio quel sistema in due minuti |
| 01:06 | Il classificatore uccello / foresta scritto in diretta: ricerca e download delle immagini, addestramento, predizione |
| 05:49 | Quanto è costato: meno di due minuti in tutto |
| 06:55 | Cos'altro è cambiato nel frattempo: gli esempi di generazione di immagini da testo |
| 10:03 | Cosa hanno costruito gli studenti delle edizioni precedenti |
| 12:15 | Come è insegnato il corso: Dylan Wiliam, l'approccio dall'alto verso il basso, prima il risultato e poi il perché |
| 17:42 | Perché ascoltare Jeremy: il suo percorso, il libro, le presentazioni |
| 20:07 | Com'era prima delle reti neurali: le *feature* costruite a mano, una per una |
| 23:59 | Zeiler e Fergus: cosa impara davvero ogni strato di una rete, guardato strato per strato |
| 26:51 | I tre miti da smontare: serve tanta matematica, servono tanti dati, servono computer costosi |
| 29:42 | Transfer learning, PyTorch contro TensorFlow, e cos'è la libreria fastai |
| 34:20 | Jupyter notebook e i server cloud: dove si esegue davvero il codice del corso |
| 38:12 | Il notebook riga per riga: ricerca delle immagini, download, pulizia di quelle rotte |
| 41:37 | `DataBlock`: l'oggetto centrale, e i pochi elementi che bisogna dargli |
| 46:57 | Dal `DataBlock` ai `DataLoaders`, poi il `learner` e `resnet18` |
| 48:59 | `fine_tune`: cosa succede davvero nelle epoche, e come si legge `error_rate` |
| 53:27 | `predict` sulla singola immagine |
| 54:19 | Gli altri domini con la stessa struttura: segmentazione, dati tabellari, filtraggio collaborativo |
| 65:39 | I notebook del corso, e cos'altro si fa con un notebook (queste slide sono un notebook) |
| 67:41 | NLP, e cosa il deep learning oggi sa e non sa fare |
| 70:57 | Un passo indietro: il machine learning come lo descrisse Arthur Samuel alla fine degli anni '50 |
| 73:30 | Pesi, misura del risultato, aggiornamento: il ciclo che sta sotto a tutto |
| 75:29 | Perché serve una funzione abbastanza flessibile — ed è lì che entra la rete neurale |
| 77:38 | Mandare un modello in produzione: `learn.predict` e i dettagli fastidiosi intorno |
| 78:54 | I compiti: sperimentare, portare il proprio lavoro sul forum, rispondere ai quiz del libro |

---

## Provenienza e licenza

Il parlato delle lezioni è di **Jeremy Howard / fast.ai**, come i notebook in `course22/` e la
prosa in `fastbook/`: le trascrizioni stanno qui come materiale di studio, non sono opera mia, e il
[video originale](https://youtu.be/8SF_h3xF3cE) resta il riferimento. Di questa cartella sono mie
soltanto due cose: `fetch.py` e `lesson-01-index.md`.
