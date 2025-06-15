# Residenz

**Residenz** è una piattaforma per la predizione di prezzi immobiliari a parte da variabili strutturali dell'immobile; è composta da un'interfaccia frontend sviluppata in **Angular**, una dashboard analitica basata su **Streamlit**, e un backend integrato tramite **Docker**.

## Versioni online

- 🔗 **Frontend (Angular)**: [https://residenzangular.onrender.com/](https://residenzangular.onrender.com/)
- 🔗 **Frontend (Streamlit, versione didattica)**: [https://residenz.onrender.com/](https://residenz.onrender.com/)

## Esecuzione locale

Per eseguire l’intero progetto in locale (frontend, backend e dashboard), è necessario utilizzare **Docker** tramite il comando:

```bash
docker-compose up --build
```

Assicurati di eseguire questo comando dalla **cartella principale del progetto** (`dashboard_locale_demo`).

Questo comando provvederà a:
- Costruire e avviare i container per il backend, il frontend e la dashboard Streamlit.
- Esporre le porte necessarie per accedere all’applicazione localmente tramite browser.

## Requisiti

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Struttura del progetto

```
dashboard_locale_demo/
├── backend/           # API e logica di business
├── frontend/          # Interfaccia Angular
├── dashboard/         # Applicazione Streamlit
├── docker-compose.yml # Configurazione dei container
```

---
