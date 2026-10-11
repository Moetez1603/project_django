# Journal de Traçabilité de l'Usage de l'IA (AI_LOG.md)
Projet : **TransConnect (Partie Models — Jalon 1)**  
Étudiant : **Moetez Bouaicha**  
Branche : `jalon-1`  

---

## Entrée [2026-09-29]
- **Outil IA utilisé :** ChatGPT / Claude
- **Prompt :**  
  > "Génère les modèles Django pour TransConnect : Utilisateur avec AbstractUser, Entreprise, Vehicule et Expedition en respectant le diagramme de classe de l'atelier."
- **Sortie obtenue (résumé) :**  
  Génération initiale des modèles `Utilisateur`, `Entreprise`, `Vehicule` et `Expedition` dans leurs applications respectives.
- **Écarts identifiés vs cahier des charges :**  
  - Le modèle `Entreprise` utilisait `matricule_fiscale` au lieu de `matricule_fiscal`, et la relation OneToOne vers `Utilisateur` était nommée `gerant` au lieu de `utilisateur`.
  - Un champ `adresse` a été indûment placé sur le modèle `Utilisateur`, alors que selon le diagramme UML de classe, l'adresse est un attribut propre à l'entité `Entreprise`.
  - Dans `Vehicule`, la clé étrangère vers l'entreprise était nommée `proprietaire` au lieu de `entreprise`, et le champ booléen était nommé `disponibilite` au lieu de `disponible`.
  - La capacité du véhicule `capacite_kg` était un `IntegerField` standard et non un `PositiveIntegerField`.
  - Le modèle `Offre` n'a pas été généré lors de ce premier jet.
- **Correction apportée et justification :**  
  Les modèles ont été commités pour initialiser le jalon (`commit b87bf2d`), avec nécessité d'un refactoring et d'un exercice de Bug Hunt pour réaligner le code sur les spécifications exactes de l'énoncé.

---

## Entrée [2026-10-06]
- **Outil IA utilisé :** Claude / Copilot
- **Prompt :**  
  > "Ajoute le modèle Offre dans OffreApp et finalise les modèles manquants pour TransConnect."
- **Sortie obtenue (résumé) :**  
  Création d'une ébauche pour le modèle `Offre` et tentatives de corrections sur `Expedition` et `Vehicule`.
- **Écarts identifiés vs cahier des charges :**  
  - Dans `ExpeditionApp`, la fonction de génération automatique de la référence n'était pas intégrée au cycle de vie du modèle (`save()`).
  - Dans `OffreApp`, l'entité `Offre` était incomplète : le champ `date_proposition` était absent, la relation avec `Vehicule` manquait, et le champ statut utilisait la valeur `'en_attente'` au lieu de la liste de choix imposée (`proposee`, `acceptee`, `refusee`, `retiree`).
  - Non-respect de la convention de nommage des commits (`models manquants` au lieu de `AI:` / `Review:`).
- **Correction apportée et justification :**  
  Arrêt du développement avant application finale des migrations pour mener une revue systématique de code et l'exercice Bug Hunt formalisé.

---

## Entrée [2026-10-11]
- **Outil IA utilisé :** Antigravity (Google DeepMind)
- **Prompt :**  
  > "Réalise l'exercice IV — Bug Hunt tracé sur l'entité Offre à partir du snippet fourni, identifie les 4 anomalies, corrige-les et harmonise l'ensemble des 5 modèles du projet TransConnect selon le diagramme de classe et le tableau de contraintes."
- **Sortie obtenue (résumé) :**  
  Identification précise et correction des 4 anomalies du modèle `Offre`. Harmonisation complète des modèles `Utilisateur`, `Entreprise`, `Vehicule`, `Expedition` et `Offre`, avec leurs validateurs métier et leurs configurations dans l'administration Django.
- **Écarts identifiés vs cahier des charges :**  
  1. **Bug Hunt Anomalie 1 (Offre.prix) :** Défini comme `CharField(max_length=10)`. Type inapproprié pour manipuler un montant monétaire.
  2. **Bug Hunt Anomalie 2 (Offre.delai_jours) :** Défini comme `IntegerField()`. Autorise les valeurs négatives ou nulles, en contradiction avec la contrainte `PositiveIntegerField`.
  3. **Bug Hunt Anomalie 3 (Offre.date_proposition) :** Défini avec `auto_now=True`. Écrase la date de proposition lors de chaque modification de l'offre (par exemple au changement de statut).
  4. **Bug Hunt Anomalie 4 (Offre.vehicule & audit) :** Clé étrangère déclarée avec `null=True`. Or le cahier des charges impose qu'une offre soit obligatoirement associée à un véhicule disponible du transporteur. De plus, les champs obligatoires `created_at` et `updated_at` étaient omis.
  5. **Écarts sur les autres modèles :** Retrait de `adresse` sur `Utilisateur`, renommage de `matricule_fiscale` en `matricule_fiscal`, `gerant` en `utilisateur`, `disponibilite` en `disponible`, `proprietaire` en `entreprise`, `chargeur` en `entreprise`, et mise en place de l'auto-génération de `reference` dans `Expedition`.
- **Correction apportée et justification :**  
  - `Offre.prix` : Modifié en `DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])` pour garantir la précision arithmétique et la conformité financière.
  - `Offre.delai_jours` : Modifié en `PositiveIntegerField(validators=[MinValueValidator(1)])` pour contraindre le délai à un nombre de jours strictement positif.
  - `Offre.date_proposition` : Modifié en `DateField(auto_now_add=True)` pour enregistrer définitivement la date de création de l'offre sans altération lors des mises à jour.
  - `Offre.vehicule` : Clé étrangère rendue obligatoire (`null=False`), avec validation dans `clean()` vérifiant que le véhicule appartient bien au transporteur soumettant l'offre et qu'il est disponible (`disponible=True`).
  - Ajout systématique de `created_at` (`DateTimeField(auto_now_add=True)`) et `updated_at` (`DateTimeField(auto_now=True)`) sur l'entité `Offre`.
  - Harmonisation stricte de l'ensemble des relations et noms d'attributs de tous les modèles avec le diagramme UML (Figure 1).
