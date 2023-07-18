## Create

- [x] Verificare che alla creazione di SLA, UserGroup non abbia già una SLA che lo colleghi ad un altro progetto sullo stesso provider.
- [x] Verificare che alla creazione di un provider non ci siano UUID ripetuti su instanze diverse dello stesso tipo.
  - Verificare anche su instanze di tipi diversi?




## Endpoint per avere da uno specifico service la lista degli IDP supportati dal corrispondente provider

- [x] Creazione endpoint
- Qual è l'utilizzo o il comportamento atteso di questa parte? Chi è che utilizza questo endpoint? In che momento? Possibilità di volerne uno specifico?

## Definire come univoci gli attributi di alcune relazioni in base all'entità connessa.

- Probabilmente serve l'uso di constraints
- Le constraints non possono essere applicate in contemporanea sui nodi e sulle relazioni (o una o l'altra).
- [x] Aggiungere òogica di controllo a livello backend. Ci sono dei check prima di creare i nodi e le relazioni.
- Integrare a livello NEO4j? (NO?)
  - Per verificare che una relazione con degli attributi che non possono essere duplicati sullo stesso provider, non sia già stata usata da quel provider, prima faccio un merge sul provider e la relazione, se il merge non trova un match allora posso creare/connettere il nodo di destinazione con i parametri specificati. La formuala è la seguente (da testare nel caso in cui più nodi 'destinazione' matchino i valori passati):
  ```
  MERGE (p:Provider{name: 'provider0'})-[r:AVAILABLE_VM_IMAGE{name:"img2", uuid:"00bdfd1e-43b7-4263-be72-e79582c1cb0b"}]->(q:Image)
  ON CREATE SET q.os= "Windows",
      q.cuda_support= false,
      q.gpu_driver= false,
      q.description= "",
      q.distribution= "Ubuntu",
      q.version= "20.04",
      q.architecture= "x86_64"
  RETURN p,r,q
  ```

## Task asincrone

- [ ] Testare l'esecuzione di più operazioni in contemporanea e comparare i tempi impiegati

## Tests

- [ ] Vedere se esiste un modo automatico o un template per scrivere i test relativi a REST api
- [ ] Implementare tests
- [ ] Aggiornare script di popolamento automatico con la nuova **logica**
- [x] Sistemare la parte di tear-up e tear-down del database -> usare un mock db
- [ ] Nelle crud aggiungere i collegamenti con altri nodi
  - [ ] Testare relationships
- [ ] Test relativi alle varie eccezioni sui pydantic model
  - [ ] In flavor testare il fatto che con NUm GPUS = 0 se ho GPU vendor o GPU model diversi da nOne ho un errore

## Punti aperti

- Nei project all'interno di una SLA aggiungere anche uuid e name dato dal rispettivo provider?
- Service ha un uuid e un name specifico del provider o solo l'endpoint?
- Nei service ritornati da una SLA serve anche l'uuid del provider? Puo' tornare utile al service provider ranker o bastano i dati del servizio e poi una volta scelto il servizio posso ricavare il provider con un'altra get?
- Aggiornare endpoint di creazione della SLA a partire da endpoint di user_group/project? (NO?)
- Modificare schema usergroup e SLA in modo che da user group si veda la SLA e non viceversa? (NO?)
  - Questo non porta ad una rimozione diretta dell'endpoint services di usergroup perchè perdiamo l'informazione relativa ai details dei servizi associati.
- Integrare l'entità metrica nel DB? Relativo a service o provider?
- Integrare Logging?
- Se ho uniqueIDProperty e name unique, posso mettere nomi duplicati perche' genera in automatico un uuid univoco. Ok cosi o rimuovere uniqueIdProperty e tenere solamente name? Nel secondo caso alcune cose automatiche/standard potrebbero non esserlo piu'.

## [ ] Implementare logica di rimozione di collegamenti (ad esempio la rimozione di quote dai servizi o di un'immagine da un provider che non la supporta più)

- Provider:
  - Rimozione manuale di un qualsiasi collegamento sempre disponibile
  - Rimozione automatica di un qualsiasi collegamento quando c'è un l'aggiornamento del provider? Quando un oggetto non è più nella lista lo rimuovo? (SI?)
    - Questo comando puo' essere all'endpoint PUT che viene usato solo dallo script mentre manualmente si usa PATCH?
- UserGroup:
  - Avendo solo relazioni con le SLA e visto che la SLA non ha senso di esistere senza uno UserGroup associato, la relazione si rimuove solo all'eliminazione della SLA.
- SLA:

  - Deve avere sempre uno UserGroup e un Project quindi tali relazioni rimangono finchè tali entità esistono. Se la SLA viene cancellata bisogna rimuovere il collegamento con lo UserGroup.
    - In teoria bisognerebbe rimuovere anche il Project visto che non ha più senso di esistere ma questo potrebbe creare inconsistenze con la realtà (in quanto il project potrebbe ancora esiste sul provider).
  - La rimozione di una quota da un servizio viene fatta specificando l'uid della quota?


