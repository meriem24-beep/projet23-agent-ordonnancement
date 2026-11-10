# Projet 23 — Agent intelligent d’ordonnancement de production

**État :** cadrage initial + dataset synthétique V2.  
**Sujet :** agent d’ordonnancement de production pour un atelier industriel fictif.

## Problème
Un atelier de tôlerie fabrique des armoires électriques, coffrets industriels et caissons de machines. Il doit affecter les opérations aux machines et opérateurs, respecter les précédences, disponibilités, outillages, changements de série et échéances, puis recalculer le planning lors d’une perturbation.

## Principe de conception
- **Le solveur décide** : il produit un planning soumis à des contraintes explicites.
- **Le LLM explique** : il répond aux questions en s’appuyant sur le planning et les raisons structurées fournies par le solveur.
- Le LLM ne doit jamais inventer ni modifier directement les décisions du solveur.

## Contenu du dépôt
- `data/synthetic_v2/` : 7 CSV de données fictives (31 ordres, 8 machines, 10 opérateurs, 145 opérations, 3 perturbations).
- `src_generer_donnees.py` : génération déterministe (graine 23).
- `src_valider_donnees.py` : contrôles de cohérence structurelle.
- `docs_dictionnaire_donnees.md` : dictionnaire des données.
- `docs/` : cadrage, architecture initiale et plan de travail.
- `prompts/` : prompt d’audit indépendant du dataset.

## Reproduire les données
Depuis la racine du dépôt :
```bash
python src_generer_donnees.py --out data/synthetic_v2 --seed 23
python src_valider_donnees.py data/synthetic_v2
```
Le validateur vérifie la cohérence structurelle. **Il ne prouve pas** qu’un planning faisable existe, que toutes les échéances sont atteignables, ni que les paramètres sont industriellement calibrés.

## Limites connues à traiter
1. Les durées sont simulées et doivent être auditées.
2. La faisabilité doit être mesurée par un vrai modèle de planning, en tenant compte des précédences, des ressources, des shifts et des setups.
3. Les disponibilités d’opérateurs et de machines doivent être interprétées sans double comptage.
4. Les événements de perturbation doivent être appliqués à leur date/heure et testés par comparaison avant/après replanning.
5. La commande urgente est désormais une vraie commande dans `orders.csv` et possède ses opérations.

## Prochain jalon
Implémenter un premier solveur sur un petit sous-ensemble, produire un planning vérifiable, puis ajouter les perturbations. Voir `docs/PLAN.md`.

## Données
Toutes les données sont fictives, générées à des fins pédagogiques. Elles ne décrivent aucune entreprise réelle.
