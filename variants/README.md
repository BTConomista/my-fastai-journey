# variants/

Varianti storiche dei miei notebook: file che non sono né la versione corrente né una sua esecuzione, ma **passaggi intermedi del percorso** che vale la pena non perdere.

Per la mappa completa di un capitolo vedi il [README principale](../README.md).

| File | Cos'è |
|---|---|
| `basics1.ipynb` | primo tentativo parziale, si ferma al download della prima immagine |

---

## `basics1.ipynb`

**Cos'è.** Uno snapshot precedente di `basics-model.ipynb`, fermo a 10 celle su 19: arriva a scaricare `bird.jpg` e a mostrarne la miniatura, poi si interrompe. Manca tutta la seconda metà — download in batch, `DataBlock`, training, predizione.

**Da dove viene.** Caricato come `is-it-a-bird/basics1.ipynb` nel commit `e043be7`, rimosso nel commit `4d6b757`. Recuperato dalla storia di git, **identico byte per byte** al blob originale `cae6e35`.

**In cosa differisce.** Le sue 10 celle sono il **prefisso esatto** di `basics-model.ipynb` così com'era al commit `087f90f`. L'unica differenza di contenuto rispetto al notebook di oggi è una riga nella cella 1:

```diff
  import socket,warnings
- import time
  try:
```

`import time` non c'era ancora: è stato aggiunto dopo, nel commit `726914d`, perché serve alla `time.sleep(5)` della cella di download in batch — una cella che in `basics1.ipynb` non esiste ancora. La mancanza dell'import e la mancanza della cella che lo usa sono la stessa cosa vista da due lati, ed è questo a datare il file con precisione: è anteriore sia alla cella di download in batch sia alla sua correzione.

---

## Perché qui c'è un solo file

Dalla cartella `is-it-a-bird/` cancellata nel commit `4d6b757` sono stati recuperati **tre** notebook, ma solo questo è finito qui. Gli altri due non erano varianti da archiviare:

| File recuperato | Dove sta ora | Perché non è qui |
|---|---|---|
| `basicsmodel.ipynb` | `runs/basics-model-eseguito.ipynb` | non è una variante: stesse identiche celle di `basics-model.ipynb`, ma con gli output dell'esecuzione. Appartiene a `runs/`. |
| `forkofbasicsmodel.ipynb` | *(assorbito)* | conteneva 3 migliorie assenti dal notebook principale — `safesearch="moderate"`, la guardia `if urls:` e `timeout=25`. Sono state portate dentro `basics-model.ipynb`, che ora coincide cella per cella col fork. Tenerlo qui sarebbe un doppione esatto. |

Nessuno dei due è comunque perso: restano raggiungibili nella storia con
`git show e043be7:is-it-a-bird/<nome>.ipynb`.
