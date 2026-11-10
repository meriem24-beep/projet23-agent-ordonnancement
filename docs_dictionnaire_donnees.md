# Dictionnaire de données — Projet 23

| Fichier | Champ | Type | Description |
|---|---|---|---|
| orders.csv | order_id | texte | Identifiant unique de l'ordre de fabrication |
| orders.csv | product_family | catégorie | Famille de produit fabriqué |
| orders.csv | quantity | entier | Quantité demandée |
| orders.csv | release_date | date ISO | Date à partir de laquelle l'ordre peut commencer |
| orders.csv | due_date | date ISO | Date limite de livraison |
| orders.csv | priority | catégorie | Priorité haute, normale ou basse |
| orders.csv | material | catégorie | Matière principale |
| orders.csv | variant | catégorie | Variante standard ou renforcée |
| machines.csv | machine_id | texte | Identifiant unique de machine |
| machines.csv | machine_type | catégorie | Étape de production réalisable |
| machines.csv | available_minutes_per_day | entier | Capacité disponible par jour |
| machines.csv | availability_start/end | date ISO | Période de disponibilité dans le scénario |
| machines.csv | tool_id | texte | Outillage installé sur la machine |
| operators.csv | operator_id | texte | Identifiant unique d'opérateur |
| operators.csv | skills | liste séparée par `;` | Types de machines sur lesquels l'opérateur est qualifié |
| operators.csv | shift_start/end | heure | Horaires journaliers |
| operations.csv | operation_id | texte | Identifiant unique d'opération |
| operations.csv | order_id | texte | Ordre auquel appartient l'opération |
| operations.csv | sequence | entier | Rang de l'opération dans la gamme |
| operations.csv | required_machine_type | catégorie | Type de machine nécessaire |
| operations.csv | processing_time_minutes | entier | Durée estimée de traitement |
| operations.csv | required_tool_id | texte | Outillage nécessaire |
| setup_times.csv | machine_type | catégorie | Type de machine concerné |
| setup_times.csv | from_product_family/to_product_family | catégorie | Famille avant/après changement |
| setup_times.csv | setup_time_minutes | entier | Durée de réglage/nettoyage |
| tools.csv | tool_id | texte | Identifiant d'outillage |
| tools.csv | compatible_machine_type | catégorie | Type de machine compatible |
| disruptions.csv | event_id | texte | Identifiant de l'événement |
| disruptions.csv | event_type | catégorie | Panne, commande urgente ou absence |
| disruptions.csv | event_date/start_time/end_time | date/heure | Moment et durée de l'événement |
| disruptions.csv | target_id | texte | Machine, opérateur ou nouvel ordre visé |
| disruptions.csv | description | texte | Description lisible du scénario |

## Relations principales
- `operations.order_id` référence `orders.order_id`.
- `operations.required_tool_id` référence `tools.tool_id`.
- `machines.tool_id` référence `tools.tool_id`.
- `setup_times` associe une transition de familles à un type de machine.
- `operators.skills` doit contenir le type de machine de l'opération pour qu'un opérateur puisse l'exécuter.


## Scénario de commande urgente
L’événement `EVT002` référence désormais `OF_URGENT_01`, présent dans `orders.csv` avec ses opérations dans `operations.csv`. Les ordres lancés avant le 10 novembre sont considérés comme du backlog déjà en attente au début de l’horizon.
