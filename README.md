#  Vérificateur de mots de passe

Application Python avec interface graphique qui évalue la robustesse d'un mot de passe **en temps réel**, donne des recommandations personnalisées et génère des mots de passe sécurisés.

> 100 % local : le mot de passe n'est jamais envoyé sur Internet ni enregistré.

Projet réalisé dans le cadre de mon cours de Python.

 Fonctionnalités

-  **Analyse en temps réel** de 5 critères : longueur, majuscules, minuscules, chiffres, symboles
-  **Score sur 100** avec une barre de couleur (rouge, orange, vert)
-  **Détection des pièges** : suites (`123`, `abc`, `azerty`), caractères répétés (`aaa`), mots de passe trop connus
-  **Recommandations personnalisées** selon les faiblesses détectées
-  **Générateur sécurisé** avec choix de la longueur et des types de caractères
-  **Copie protégée** : le presse-papiers se vide automatiquement après 30 secondes

 Exemples de résultats

| Mot de passe | Score | Niveau |
|---|---|---|
| `123456` | 5/100 | 🔴 Faible |
| `Soleil2024` | 68/100 | 🟠 Moyen |
| Mot de passe généré (16 caractères) | ~96/100 | 🟢 Fort |

# Lancer l'application

1. Installer [Python 3](https://www.python.org/downloads/) (Tkinter est inclus)
2. Télécharger le fichier `verificateur_mdp.py`
3. Dans un terminal, lancer :

```bash
python verificateur_mdp.py
```

Aucune bibliothèque externe n'est nécessaire.

 Technologies utilisées

- **Python 3**
- **Tkinter** : interface graphique
- **re** : expressions régulières pour analyser le mot de passe
- **secrets** : génération aléatoire cryptographiquement sûre (contrairement à `random`)

 Ce que j'ai appris

- Utiliser les expressions régulières pour détecter des motifs dans un texte
- Concevoir un système de score avec bonus et pénalités
- Créer une interface qui réagit à chaque frappe (`StringVar` + `trace_add`)
- Penser la sécurité dès la conception : aucun stockage, aucune connexion réseau

 Améliorations prévues

- Version web accessible par simple lien
- Estimation du temps nécessaire pour craquer un mot de passe
- Mode « phrase de passe » (ex. `Cheval-Lampe-Orange-42`)
- Interface plus moderne avec CustomTkinter

Licence

Ce projet est sous licence MIT.
