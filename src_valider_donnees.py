#!/usr/bin/env python3
"""Validate relational consistency and basic feasibility of Projet 23 CSV files."""
import csv, sys
from pathlib import Path

def read(folder,name):
    with (folder/name).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def main(folder):
    folder=Path(folder); errors=[]; warnings=[]
    orders=read(folder,"orders.csv"); machines=read(folder,"machines.csv")
    operators=read(folder,"operators.csv"); ops=read(folder,"operations.csv")
    setups=read(folder,"setup_times.csv"); tools=read(folder,"tools.csv")
    disruptions=read(folder,"disruptions.csv")
    order_ids={r["order_id"] for r in orders}; machine_types={r["machine_type"] for r in machines}
    tool_map={r["tool_id"]:r["compatible_machine_type"] for r in tools}
    operator_skills={r["operator_id"]:set(r["skills"].split(";")) for r in operators}
    if len(order_ids)!=len(orders): errors.append("Identifiants de commande dupliqués.")
    if len({r["machine_id"] for r in machines})!=len(machines): errors.append("Identifiants machine dupliqués.")
    if len({r["operation_id"] for r in ops})!=len(ops): errors.append("Identifiants opération dupliqués.")
    for o in orders:
        if int(o["quantity"])<=0: errors.append(f"{o['order_id']}: quantité non positive.")
        if o["due_date"]<o["release_date"]: errors.append(f"{o['order_id']}: échéance avant date de lancement.")
        if o["priority"] not in {"haute","normale","basse"}: errors.append(f"{o['order_id']}: priorité inconnue.")
    by_order={}
    for op in ops:
        oid=op["order_id"]; stage=op["required_machine_type"]
        if oid not in order_ids: errors.append(f"{op['operation_id']}: commande {oid} inconnue.")
        if stage not in machine_types: errors.append(f"{op['operation_id']}: aucune machine pour {stage}.")
        if int(op["processing_time_minutes"])<=0: errors.append(f"{op['operation_id']}: durée non positive.")
        if tool_map.get(op["required_tool_id"])!=stage: errors.append(f"{op['operation_id']}: outillage incompatible.")
        by_order.setdefault(oid,[]).append(int(op["sequence"]))
    for oid,seqs in by_order.items():
        if sorted(seqs)!=list(range(1,len(seqs)+1)): errors.append(f"{oid}: séquences d'opérations non consécutives.")
    for stage in machine_types:
        if not any(stage in skills for skills in operator_skills.values()):
            errors.append(f"Aucun opérateur qualifié pour {stage}.")
    expected=len(machine_types)*3*3
    if len(setups)!=expected: errors.append(f"Table setup_times: {len(setups)} lignes, {expected} attendues.")
    setup_keys={(r["machine_type"],r["from_product_family"],r["to_product_family"]) for r in setups}
    if len(setup_keys)!=len(setups): errors.append("Transitions de changement de série dupliquées.")
    for m in machines:
        if m["tool_id"] not in tool_map or tool_map[m["tool_id"]]!=m["machine_type"]:
            errors.append(f"{m['machine_id']}: outillage machine incompatible.")
    machine_ids={r["machine_id"] for r in machines}
    operator_ids={r["operator_id"] for r in operators}
    for event in disruptions:
        target=event["target_id"]
        if event["event_type"]=="commande_urgente" and target not in order_ids:
            errors.append(f"{event['event_id']}: commande urgente {target} absente de orders.csv.")
        elif event["event_type"]=="panne_machine" and target not in machine_ids:
            errors.append(f"{event['event_id']}: machine cible {target} inconnue.")
        elif event["event_type"]=="absence_operateur" and target not in operator_ids:
            errors.append(f"{event['event_id']}: opérateur cible {target} inconnu.")
    urgent=[d for d in disruptions if d["event_type"]=="commande_urgente"]
    if len(urgent)!=1: warnings.append("Le scénario de commande urgente n'est pas présent exactement une fois.")
    print(f"Ordres: {len(orders)} | Machines: {len(machines)} | Opérateurs: {len(operators)} | Opérations: {len(ops)} | Événements: {len(disruptions)}")
    if warnings:
        for w in warnings: print("AVERTISSEMENT:",w)
    if errors:
        for e in errors: print("ERREUR:",e)
        print(f"ÉCHEC: {len(errors)} erreur(s)."); return 1
    print("SUCCÈS: toutes les vérifications structurelles sont passées.")
    print("Note: ce contrôle vérifie la cohérence des données, pas l'optimalité d'un planning.")
    return 0
if __name__=="__main__":
    folder=sys.argv[1] if len(sys.argv)>1 else "data/projet23"
    raise SystemExit(main(folder))
