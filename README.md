# my-fastai-journey

Il mio percorso con *Practical Deep Learning for Coders* di fast.ai: i notebook che scrivo io, affiancati alle fonti ufficiali da cui partono, con il confronto riga per riga tra le due cose.

Il repository è organizzato **per capitolo**. Ogni capitolo ha tre versioni dello stesso argomento — la mia, quella del corso, quella del libro — e un documento che le mette a confronto.

---

## Capitolo 1 — Classificatore di immagini

Il primo modello: riconoscere una categoria di immagini da un dataset costruito da zero.
Corso: lezione 1, *Getting started* · Libro: capitolo 1, *Your Deep Learning Journey*.

### Scritti da me

| File | Cos'è |
|---|---|
| [`basics-model.ipynb`](basics-model.ipynb) | **La versione corrente.** 19 celle, di cui 13 di codice (2 delle quali vuote, in coda). Output puliti. Uccello vs foresta. |
| [`runs/basics-model-eseguito.ipynb`](runs/basics-model-eseguito.ipynb) | La stessa cosa **eseguita**, con i risultati dentro: tabella del training, immagini, predizione finale. |
| [`variants/basics1.ipynb`](variants/basics1.ipynb) | Primo tentativo parziale, 10 celle: si ferma al download della prima immagine. |

Dettagli su come sono nati questi due ultimi file: [`runs/README.md`](runs/README.md) e [`variants/README.md`](variants/README.md).

### Dal corso — `course22/`

Copia completa del [mio fork di `course22`](https://github.com/BTConomista/course22), il repository ufficiale dell'edizione 2022 del corso. Della **lezione 1** fanno parte:

| File | Cos'è |
|---|---|
| [`course22/00-is-it-a-bird-creating-a-model-from-your-own-data.ipynb`](course22/00-is-it-a-bird-creating-a-model-from-your-own-data.ipynb) | **Il notebook da cui nasce il mio.** 31 celle, 715 KB perché conserva gli output di Jeremy Howard. |
| [`course22/clean/00-is-it-a-bird-creating-a-model-from-your-own-data.ipynb`](course22/clean/00-is-it-a-bird-creating-a-model-from-your-own-data.ipynb) | Lo stesso senza prosa né output: 16 celle, 5 KB. Le 12 celle di codice sono le stesse, **tranne una** — questa versione ha già una nota sul cambio di API di DuckDuckGo che nella versione principale manca. |
| [`course22/01-jupyter-notebook-101.ipynb`](course22/01-jupyter-notebook-101.ipynb) | L'altro notebook della lezione 1: come si usa Jupyter. Anche in [versione clean](course22/clean/01-jupyter-notebook-101.ipynb). |
| [`course22/slides/lesson1.pdf`](course22/slides/lesson1.pdf) | Le slide della lezione. |
| [`course22/slides/birds.ipynb`](course22/slides/birds.ipynb) | Il notebook che Jeremy proietta a schermo durante la lezione (66 celle). Non è il notebook da studiare: è il supporto della spiegazione. |

### Il video della lezione — `transcripts/`

La lezione 1 registrata: [*Getting started*](https://youtu.be/8SF_h3xF3cE), 1h 22m 55s. È il filo che tiene insieme le tre colonne qui sopra — Jeremy costruisce il notebook del corso a schermo e intanto spiega il perché di ogni riga.

| File | Cos'è |
|---|---|
| [`transcripts/lesson-01-index.md`](transcripts/lesson-01-index.md) | **L'indice della lezione**, a grana di due o tre minuti, piu' una tabella che dice in quali minuti compare ciascun concetto — `DataBlock`, `fine_tune`, transfer learning, `timm`. Serve a trovare il punto giusto senza riguardarsi un'ora e mezza. |
| [`transcripts/README.md`](transcripts/README.md) | Come si rigenera la trascrizione, da dove viene il testo, e la nota sulla provenienza. |
| [`transcripts/fetch.py`](transcripts/fetch.py) | Genera la trascrizione integrale in locale (`transcripts/lesson-01.md`, ~12.200 parole con timestamp) partendo dai sottotitoli ufficiali del video. Il testo non è versionato: è di fast.ai, non mio. |

### Dal libro — `fastbook/`

Copia completa del [mio fork di `fastbook`](https://github.com/BTConomista/fastbook), il repository ufficiale del libro *Deep Learning for Coders with fastai and PyTorch*. Del **capitolo 1** fanno parte:

| File | Cos'è |
|---|---|
| [`fastbook/01_intro.ipynb`](fastbook/01_intro.ipynb) | **Il capitolo completo.** 194 celle, di cui 171 di prosa e 22 di codice: è un capitolo di libro scritto dentro un notebook. |
| [`fastbook/clean/01_intro.ipynb`](fastbook/clean/01_intro.ipynb) | Lo stesso senza prosa: 57 celle, 16 KB. Le 22 celle di codice sono le stesse; 7 differiscono solo per le direttive di impaginazione (`#hide_input`, `#caption`, `#id`) che servono a produrre il libro cartaceo e qui sono state tolte. È la versione da usare per seguire il capitolo scrivendo. |
| [`fastbook/app_jupyter.ipynb`](fastbook/app_jupyter.ipynb) | Appendice *Introduction to Jupyter*, che il libro affianca al capitolo 1. |
| [`fastbook/images/`](fastbook/images) | Le immagini del capitolo. Servono davvero: senza questa cartella i diagrammi di `01_intro.ipynb` non si vedono. |

### Il confronto

**→ [`reference/CONFRONTO.md`](reference/CONFRONTO.md)** — confronto cella per cella e riga per riga fra i tre notebook, con spiegazione tecnica, spiegazione in parole semplici e note di approfondimento per ogni cella.

È diviso in due parti, perché i tre file non sono parenti allo stesso modo:

- **Parte A — il mio vs quello del corso.** Sono lo stesso file: il mio nasce da un "Copy & Edit" su Kaggle. Vengono quindi confrontati con dei veri *diff*. Oggi restano **2 celle su 11 identiche all'originale** — la pulizia del dataset e la predizione finale; tutto il resto è stato modificato per aggiornare librerie ormai rinominate e per rendere più robusta la parte che dipende dalla rete.
- **Parte B — il mio vs il libro.** Non c'è parentela: il libro usa un altro dataset (*Oxford-IIIT Pet* invece di immagini cercate sul web), un'altra API (`ImageDataLoaders` invece di `DataBlock`) e un altro modello (`resnet34` invece di `resnet18`). Il confronto è quindi per **fase equivalente**: stessa tappa del ragionamento, due modi di scriverla.

Note su cosa c'era prima nella cartella `reference/` e dove è finito: [`reference/README.md`](reference/README.md).

---

## Come è organizzato il repository

| Cartella | Cosa contiene |
|---|---|
| radice | i miei notebook, versione corrente |
| `runs/` | le mie esecuzioni, con gli output salvati |
| `variants/` | varianti storiche dei miei notebook |
| `reference/` | i documenti di confronto e analisi |
| `transcripts/` | indice e strumento di trascrizione delle lezioni video |
| `course22/` | copia del repository del corso fast.ai 2022 |
| `fastbook/` | copia del repository del libro |

La regola che tiene in piedi l'ordine: **il materiale ufficiale non si modifica mai**. `course22/` e `fastbook/` sono copie fedeli, e restano tali — se una cosa va cambiata, si cambia nel mio notebook e si annota la differenza nel confronto. Così `git status` su quelle due cartelle è sempre vuoto, e qualunque differenza fra il mio lavoro e l'originale è intenzionale e documentata.

Per aggiungere un capitolo: una sezione in questo README con le tre colonne (mio / corso / libro), l'indice della lezione video in `transcripts/` e un documento di confronto in `reference/`.

---

## Provenienza e licenze

Il codice che scrivo io è sotto [Apache 2.0](LICENSE), la licenza di questo repository.

Le cartelle `course22/` e `fastbook/` **non sono opera mia**: sono copie dei repository di fast.ai, di Jeremy Howard e Sylvain Gugger. Vanno lette con le loro condizioni, non con quelle di questo repository:

- `fastbook/` porta la propria licenza in [`fastbook/LICENSE`](fastbook/LICENSE): il **codice** dei notebook è GPL v3, mentre la **prosa** (le celle di testo, che nel capitolo 1 sono 171 su 194) non è concessa in ridistribuzione — il repository di fastai ne consente copie o fork per uso personale. Chi legge questa copia dovrebbe fare riferimento all'[originale](https://github.com/fastai/fastbook).
- `course22/` non contiene un file di licenza. In assenza di condizioni esplicite vale il copyright degli autori: la copia sta qui come materiale di studio, e l'[originale](https://github.com/fastai/course22) resta il riferimento.

Anche il parlato delle lezioni video è di fast.ai. Per questo `transcripts/` contiene l'indice che ho scritto io e lo script che ricostruisce la trascrizione, ma non il testo integrale: quello si genera in locale e resta fuori dal repository.

Il confronto in `reference/` è scritto da me e cita estratti delle fonti per commentarli.
