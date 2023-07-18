# MODELS

1. [ ] Rivedere attributi relativi a private network in project
   - Serve Marica
2. [ ] Rivedere attributi nelle quote e quali tipologie di quote esistono. Capire se metterli tutti in Quota o specificarli nelle singole classi derivate
   - Serve Marica
3. [ ] Create separate entity GPU when dealing with images that can use one or multiple GPUs?
   - Serve Marica

# SCHEMAS

1. [ ]  Creare/modificare le funzioni di update di tutti gli elementi. Derivarli da Query o lasciare Query a parte perche' potrebbe usare i parametri come regexp? Impedire di modificare il nome dei service type? Rivedere soprattutto le Update e le Query degli specifici service se servono o meno.
2. [ ] Sistemare Quota attributes in base al modello neo4j. Eventualmente aggiornare le classi extended (richiede M.2)

# API

1. [ ] Check uniqueness when creating any type that may require uniqueness
2. [ ] Nei get di Service specificare la sottoclasse corretta? Verificare che se uso Service normale non perdo informazioni
3. [ ] Nei get di Quota specificare la sottoclasse corretta? Richiede (S.2)
4. [ ] Aggiornare procedure di delete di tutti gli elementi. Se un elemento non ha più connessione e deve averne rimuoverlo. In alcuni casi bisogna fare il cascade degli elementi.
5. [ ] Creare post per Quota (UUID di project e service)
6. [ ] Aggiungere dove serve gli endpoints per la connessione con altri elementi.

# AUTENTICAZIONE

- [ ] Integrare autenticazione
