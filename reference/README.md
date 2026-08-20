# reference/

Questa cartella contiene il **materiale di analisi** su cui si basa il confronto tra il mio notebook e i notebook ufficiali di fast.ai.

I notebook di riferimento veri e propri **non stanno più qui**: sono nelle copie complete dei repo forkati, presenti nella radice del repository.

| Cosa | Dove sta ora |
|---|---|
| Notebook del corso fast.ai 2022 | `course22/` — copia completa del [fork di `course22`](https://github.com/BTConomista/course22) |
| Capitoli del libro *Deep Learning for Coders* | `fastbook/` — copia completa del [fork di `fastbook`](https://github.com/BTConomista/fastbook) |
| Confronto dettagliato cella per cella | `reference/CONFRONTO.md` |
| Esecuzioni con output salvati | `runs/` — vedi `runs/README.md` |
| Varianti storiche dei miei notebook | `variants/` — vedi `variants/README.md` |

---

## Perché i notebook sono stati spostati

All'inizio questa cartella conteneva due notebook caricati a mano, che servivano da termine di paragone per `basics-model.ipynb`:

- `00_is_it_a_bird_creating_a_model_from_your_own_data.ipynb`
- `01_intro.ipynb`

Quando i repo `course22` e `fastbook` sono stati copiati per intero nel repository, quei due file sono diventati doppioni dei loro originali. Tenere due copie dello stesso notebook è una fonte di confusione: non è più ovvio quale sia la versione "buona", e le due copie possono divergere nel tempo senza che nessuno se ne accorga. Entrambi sono stati quindi rimossi, e restano qui solo i documenti di analisi.

### `01_intro.ipynb` — rimosso

La copia che stava qui **non era l'originale del repo**: era la versione esportata da **Google Colab**, riconoscibile da due dettagli:

- i link alle immagini erano URL assolute verso GitHub
  (`https://github.com/fastai/fastbook/blob/master/images/...?raw=1`)
  invece dei path locali `images/...` usati nell'originale;
- i metadati del notebook contenevano `"colab": {"provenance": []}`.

Il contenuto era però lo stesso: **tutte e 22 le celle di codice erano identiche byte per byte**, e delle 171 celle di testo ne differivano 28 — 21 per i path delle immagini e 7 per soli spazi a fine riga.

La copia in `fastbook/01_intro.ipynb` è quindi **preferibile**: è l'originale canonico, e adesso i suoi path locali `images/...` funzionano davvero, perché la cartella `fastbook/images/` è presente nel repository. La copia Colab è stata rimossa e `CONFRONTO.md` ora punta a `fastbook/01_intro.ipynb`.

### `00_is_it_a_bird_creating_a_model_from_your_own_data.ipynb` — rimosso

Questo file era **identico byte per byte** a `course22/00-is-it-a-bird-creating-a-model-from-your-own-data.ipynb`
(MD5 `6cd8a93a1977ceaad3b3e698d4c7d362`, 732.679 byte): un duplicato esatto, senza alcuna differenza nemmeno negli output salvati.

È stato rimosso e `CONFRONTO.md` punta alla copia dentro `course22/`.

---

## La cartella `is-it-a-bird/` recuperata

Prima ancora di `reference/`, il repository aveva una cartella `is-it-a-bird/` con tre notebook, creata nel commit `e043be7` e cancellata per intero nel commit `4d6b757`. Non erano doppioni: ripescandoli dalla storia di git è emerso che due dei tre contenevano materiale che non esisteva da nessun'altra parte.

| File cancellato | Verdetto | Destinazione |
|---|---|---|
| `basicsmodel.ipynb` | stesse celle di `basics-model.ipynb`, ma **con gli output** dell'esecuzione (991 KB) | `runs/basics-model-eseguito.ipynb` |
| `forkofbasicsmodel.ipynb` | 16 celle su 19 identiche, **3 migliorie** assenti dal notebook principale | assorbito in `basics-model.ipynb` |
| `basics1.ipynb` | snapshot parziale precedente, 10 celle su 19 | `variants/basics1.ipynb` |

Le tre migliorie assorbite sono `safesearch="moderate"` nella ricerca immagini, la guardia `if urls:` contro l'`IndexError`, e `timeout=25` nel download — tutte documentate nelle rispettive celle di `CONFRONTO.md`.

---

## Nota sui nomi usati nel confronto

In `CONFRONTO.md` i tre notebook sono chiamati:

| Nome nel documento | File |
|---|---|
| **Mio** | `basics-model.ipynb` (radice del repository) |
| **Originale** | `course22/00-is-it-a-bird-creating-a-model-from-your-own-data.ipynb` |
| **Libro** | `fastbook/01_intro.ipynb` |

**Mio** e **Originale** sono imparentati — il primo nasce dal secondo tramite "Copy & Edit" di Kaggle — e per questo vengono confrontati con dei veri *diff* riga per riga. Il **Libro** è un file indipendente (dataset, API e nomi di variabili diversi), quindi viene confrontato per fase equivalente.
