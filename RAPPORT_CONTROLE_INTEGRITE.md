# Rapport — contrôle d’intégrité TransConnect

## Outil livré

Le tableau de bord est accessible depuis l’accueil de l’administration ou directement à
`/admin/health-check/`. Il présente cinq contrôles, le nombre d’anomalies trouvées et des liens
vers les objets concernés afin de faciliter leur vérification. Le bouton **Télécharger le résultat
en CSV** exporte les anomalies et leurs liens pour servir de preuve au rendu.

## Contrôles et règles métier

| Contrôle | Règle métier protégée | Scénario pouvant produire l’incohérence | Résultat observé |
|---|---|---|---:|
| Offres orphelines | Une offre `proposee` ou `acceptee` doit concerner une expédition `publiee` ou `attribuee`. | Une mise à jour directe du statut de l’expédition en SQL ou via `QuerySet.update()` ne déclenche pas les validations Python et peut rendre l’offre incohérente. | 1 |
| Expéditions publiées depuis plus de 7 jours | Une expédition encore `publiee` doit être examinée si elle n’a pas évolué depuis plus de sept jours. | Une offre peut ne jamais être acceptée ou le traitement peut être abandonné sans que le statut de l’expédition soit actualisé. | 0 |
| Transporteurs sans flotte | Une entreprise de type `transporteur` devrait posséder au moins un véhicule pour proposer un service de transport. | Un véhicule peut être supprimé ou l’entreprise peut être créée sans que sa flotte soit enregistrée. | 1 |
| Véhicules disponibles déjà attribués | Un véhicule utilisé par une offre `acceptee` ne devrait pas rester marqué `disponible=True`. | L’acceptation d’une offre peut être effectuée sans mettre à jour la disponibilité du véhicule, notamment lors d’une opération en masse. | 1 |
| Propositions en doublon | Un transporteur ne devrait pas avoir plusieurs offres `proposee` pour la même expédition. | Une répétition de soumission ou une création en masse sans vérification préalable peut produire plusieurs offres proposées. | 0 |

## Résultats sur la base locale

État observé le 20 octobre 2026 : **3 anomalies au total** — une offre orpheline, un transporteur
sans flotte et un véhicule disponible associé à une offre acceptée. Aucune expédition publiée
depuis plus de sept jours ni aucun groupe de propositions en doublon n’a été détecté.

Ces nombres décrivent la base locale au moment de l’exécution et peuvent changer avec les données.
Pour le rendu, télécharger le CSV depuis `/admin/health-check/?format=csv` ou joindre une capture
de la page montrant les résultats à jour.

## Usage de l’assistant IA et limite des opérations en masse

L’assistant a aidé à construire les contrôles ORM et les personnalisations de l’administration.
Pour l’action groupée de clôture des expéditions, le code parcourt les objets sélectionnés et appelle
`save()` sur chacun, au lieu d’utiliser `QuerySet.update()`. Cette approche déclenche `full_clean()`
via la méthode `save()` du modèle. Un `update()` SQL contournerait `save()` et `clean()` et pourrait
laisser les données métier incohérentes.

Les contrôles du tableau de bord servent à détecter les incohérences restantes ; ils ne remplacent
pas les validations au moment de l’écriture.
