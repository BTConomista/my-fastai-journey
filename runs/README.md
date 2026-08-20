# runs/

Questa cartella conserva le **esecuzioni** dei notebook: copie salvate *con i risultati dentro*.

Per la mappa completa di un capitolo vedi il [README principale](../README.md).

I notebook nella radice del repository sono tenuti puliti (output azzerati), perché è così che il codice si legge e si confronta bene. Ma azzerare gli output significa anche buttare via la prova che il modello ha davvero funzionato: i numeri del training, le immagini scaricate, le predizioni finali. Qui quei risultati vengono conservati.

| File | Origine |
|---|---|
| `basics-model-eseguito.ipynb` | esecuzione di `basics-model.ipynb` su Kaggle con GPU |

---

## `basics-model-eseguito.ipynb`

**Cos'è.** La versione eseguita di `basics-model.ipynb`: 19 celle, di cui 9 con output salvati, per un totale di 991 KB (contro i 5 KB della versione pulita — la differenza sono le immagini e le tabelle incorporate).

**Da dove viene.** Era stato caricato come `is-it-a-bird/basicsmodel.ipynb` nel commit `e043be7`, e rimosso nel commit `4d6b757` insieme al resto della cartella. È stato recuperato dalla storia di git ed è **identico byte per byte** al blob originale `1b2cadc`.

**Rapporto con `basics-model.ipynb`.** Al momento dell'esecuzione le due versioni avevano le **19 celle di codice identiche**. Poi `basics-model.ipynb` ha ricevuto tre migliorie (`safesearch`, guardia su `urls`, `timeout`) che questo file non ha, perché è la fotografia di un'esecuzione avvenuta *prima*. Non va quindi allineato al notebook principale: il suo valore sta proprio nell'essere una fotografia, e riallinearlo la falsificherebbe.

**Cosa contiene di interessante.**

Il training completo, `resnet18` con `fine_tune(3)`:

| fase | epoch | train_loss | valid_loss | error_rate | time |
|---|---|---|---|---|---|
| fit iniziale (testa) | 0 | 0.801308 | 0.634666 | 0.243243 | 00:01 |
| fine-tuning | 0 | 0.074213 | 0.020849 | 0.000000 | 00:00 |
| fine-tuning | 1 | 0.037667 | 0.000777 | 0.000000 | 00:00 |
| fine-tuning | 2 | 0.024937 | 0.000142 | 0.000000 | 00:00 |

e la predizione finale:

```
This is a: bird.
Probability it's a bird: 1.0000
```

Vale la pena leggere quella tabella, perché racconta esattamente cosa fa `fine_tune`. Nella prima riga solo la testa del modello viene addestrata, col resto della rete congelato: l'errore è ancora al 24%. Nelle tre righe successive viene scongelato tutto e la rete intera si adatta al problema: l'errore crolla a zero già alla prima epoca, e la `valid_loss` continua a scendere di un ordine di grandezza per epoca. Un `error_rate` di 0.000000 non è un bug — distinguere uccelli da foreste è un compito facile per una rete pre-addestrata su ImageNet, e il set di validazione è piccolo (~37 immagini, quindi un solo errore varrebbe 0.027).

Negli output restano visibili anche due cose che nella versione pulita si perdono:

- il download dei pesi pre-addestrati (`resnet18-f37072fd.pth`, 44.7 MB) — la prova che il modello **non** parte da zero;
- gli avvisi `AVIF support not installed` di Pillow e il conteggio `5` di `verify_images`: cinque immagini scaricate da DuckDuckGo erano illeggibili e sono state scartate prima del training. È il motivo per cui quella cella di pulizia esiste.
