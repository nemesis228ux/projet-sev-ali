# Système de Gestion Bancaire – FastAPI 🏦

Ce projet est une petite API RESTful de gestion bancaire développée avec FastAPI, SQLAlchemy et Pydantic. Il permet la gestion des utilisateurs, banques, comptes, cartes et transactions, avec une authentification sécurisée par JWT.
Il s'agit d'un projet collaboratif entre:
<div align="center">
  <a href="https://github.com/nemesis228ux" target="_blank">
    <img src="https://img.shields.io/badge/Nemesis228Ux-Dev_1-cyan?style=for-the-badge&logo=github" alt="Badge de profil de Nemesis228Ux" />
  </a>
  <a href="https://github.com/SevTify404" target="_blank">
    <img src="https://img.shields.io/badge/Sevtify404-Dev_2-red?style=for-the-badge&logo=github" alt="Badge de profil de Sevtify404" />
  </a>
</div>

---

## Fonctionnalités principales 👨🏾‍💻
- Authentification (inscription, login, JWT)
- Gestion des utilisateurs (CRUD)
- Gestion des banques
- Gestion des comptes bancaires
- Gestion des cartes bancaires
- Gestion des transactions (dépôt, retrait, transfert)
- Sécurisation des endpoints (dépendances, vérification admin, etc.)
- Réponses API uniformisées
---

## Stack technique 💼
- Python 3.12+
- FastAPI
- SQLAlchemy
- Pydantic
- MySQL ou PostgreSQL (configurable)
- JWT (python-jose)
- Hashage des mots de passe (passlib, bcrypt)
---

## ⚙️ Installation

1. **Cloner le dépôt 🔗**
```bash
git clone <url-du-repo>
cd projet-sev-ali
```
2. **Créer un environnement virtuel 📦**
```bash
python -m venv venv
source venv/bin/activate
```
3. **Installer les dépendances 🔂**
```bash
pip install -r requirements.txt
```
4. **Configurer les variables d'environnement 📄**

Créer un fichier `.env` à la racine avec :
```
DATABASE_USER=...
DATABASE_PASSWORD=...
DATABASE_HOST=...
DATABASE_NAME=...
DATABASE_TYPE=mysql
DATABASE_PILOT=pymysql
SECRET_KEY=...
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_MINUTES=30
ENVIRONMENT=DEV
```

5. **Créer les tables 📜**
```bash
python -m app.create_table
```

6. **Lancer le serveur 🚀**
```bash
uvicorn app.main:app --port 8000
```
---


## 🗂️ Structure du projet
```
app/
  ├── auth/         # Authentification & sécurité
  ├── core/         # Config & base de données
  ├── crud/         # Accès aux données (CRUD)
  ├── models/       # Modèles SQLAlchemy
  ├── routes/       # Endpoints FastAPI
  ├── schemas/      # Schémas Pydantic
  └── utils/        # Utilitaires divers
```
---

## 🧩 Exemples d'API
- `POST /auth/register` : Inscription utilisateur
- `POST /auth/login` : Connexion utilisateur (JWT)
- `GET /users/` : Liste des utilisateurs (auth requis)
- `GET /banques/` : Liste des banques
- `POST /comptes/create` : Créer un compte bancaire
- `POST /cartes/create` : Créer une carte bancaire
- `POST /transactions/` : Effectuer une transaction
---

## 📉 Documentation Complète
La documentation complète interactive sera disponible à l'adresse : `http://localhost:8000/docs` après le lancement du serveur

---

## 🛡 Sécurité & bonnes pratiques
- Protéger les routes sensibles (admin, utilisateur connecté)
- Ne jamais exposer le fichier `.env` ou les secrets
- Tester les cas d’erreur et les accès non autorisés

---
## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

```
1. Forker le projet
2. Créer une branche (`git checkout -b feature/ma-feature`)
3. Commiter vos modifications
4. Ouvrir une Pull Request
```
---
## ⚖️ Licence

Ce projet est open-source et distribué sous la licence `MIT`.

