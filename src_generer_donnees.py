#!/usr/bin/env python3
"""Generate the Projet 23 synthetic production-scheduling dataset reproducibly."""
import csv, random, argparse
from pathlib import Path

def generate(out_dir: Path, seed: int = 23):
    rng = random.Random(seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    families = {
        "armoire_electrique": ["decoupe", "pliage", "soudage", "peinture", "assemblage"],
        "coffret_industriel": ["decoupe", "pliage", "peinture", "assemblage"],
        "caisson_machine": ["decoupe", "pliage", "soudage", "peinture", "assemblage"],
    }
    products = list(families)
    machine_rows = [
        ["M_DEC_01","decoupe","Laser fibre 1",480,"2026-11-10","2026-11-14","T_DEC"],
        ["M_DEC_02","decoupe","Laser fibre 2",420,"2026-11-10","2026-11-14","T_DEC"],
        ["M_PLI_01","pliage","Presse plieuse 1",450,"2026-11-10","2026-11-14","T_PLI"],
        ["M_PLI_02","pliage","Presse plieuse 2",360,"2026-11-10","2026-11-14","T_PLI"],
        ["M_SOU_01","soudage","Poste soudage 1",420,"2026-11-10","2026-11-14","T_SOU"],
        ["M_PEI_01","peinture","Cabine peinture 1",420,"2026-11-10","2026-11-14","T_PEI"],
        ["M_ASS_01","assemblage","Poste assemblage 1",480,"2026-11-10","2026-11-14","T_ASS"],
        ["M_ASS_02","assemblage","Poste assemblage 2",360,"2026-11-10","2026-11-14","T_ASS"],
    ]
    operator_rows = [
        ["OP01","Amina","decoupe;pliage","2026-11-10","2026-11-14","08:00","16:00"],
        ["OP02","Youssef","decoupe","2026-11-10","2026-11-14","08:00","16:00"],
        ["OP03","Salma","pliage;soudage","2026-11-10","2026-11-14","08:00","16:00"],
        ["OP04","Mehdi","soudage","2026-11-10","2026-11-14","08:00","16:00"],
        ["OP05","Nour","peinture","2026-11-10","2026-11-14","08:00","16:00"],
        ["OP06","Omar","peinture;assemblage","2026-11-10","2026-11-14","08:00","16:00"],
        ["OP07","Lina","assemblage","2026-11-10","2026-11-14","08:00","16:00"],
        ["OP08","Karim","decoupe;pliage;assemblage","2026-11-10","2026-11-14","08:00","16:00"],
        ["OP09","Imane","soudage;assemblage","2026-11-10","2026-11-14","08:00","16:00"],
        ["OP10","Rachid","pliage;peinture","2026-11-10","2026-11-14","08:00","12:00"],
    ]
    unit = {"decoupe":2.2,"pliage":1.8,"soudage":3.0,"peinture":2.5,"assemblage":2.0}
    tool = {"decoupe":"T_DEC","pliage":"T_PLI","soudage":"T_SOU","peinture":"T_PEI","assemblage":"T_ASS"}
    orders=[]
    for i in range(1,31):
        family=rng.choice(products); qty=rng.randint(12,80)
        created=rng.randint(1,3); due=rng.randint(11,14)
        priority=rng.choices(["haute","normale","basse"],weights=[3,6,2])[0]
        orders.append([f"OF{i:03d}",family,qty,f"2026-11-{created:02d}",f"2026-11-{due:02d}",priority,
                       rng.choice(["acier_1mm","acier_2mm","inox_1mm"]),
                       "standard" if family!="caisson_machine" else "renforce"])
    # Earlier release dates represent backlog already waiting at the start of the planning horizon.
    # The urgent order is inserted as a real order so the replanning scenario is schedulable.
    orders.append(["OF_URGENT_01","coffret_industriel",20,"2026-11-12","2026-11-13","haute","acier_1mm","standard"])

    operations=[]; k=1
    for oid,family,qty,*_ in orders:
        for seq,stage in enumerate(families[family],1):
            duration=max(10,round(qty*unit[stage]*rng.uniform(.85,1.20)))
            operations.append([f"OPR{k:04d}",oid,seq,stage,duration,tool[stage],"precedente" if seq>1 else "aucune"]); k+=1
    setup=[]
    for stage in unit:
        for a in products:
            for b in products:
                minutes=0 if a==b else (15 if stage in ("decoupe","assemblage") else 25 if stage in ("pliage","soudage") else 40)
                if a!=b and "caisson_machine" in (a,b) and stage in ("soudage","peinture"): minutes+=10
                setup.append([stage,a,b,minutes])
    disruptions=[
        ["EVT001","panne_machine","2026-11-11","10:00","12:00","M_PEI_01","Cabine peinture indisponible pendant 120 minutes"],
        ["EVT002","commande_urgente","2026-11-12","09:00","","OF_URGENT_01","Commande fictive de 20 coffrets industriels, priorité haute, échéance 2026-11-13"],
        ["EVT003","absence_operateur","2026-11-13","08:00","16:00","OP05","Absence de l'opératrice qualifiée peinture"],
    ]
    tools=[
        ["T_DEC","outillage découpe","decoupe","Compatible avec les machines de découpe"],
        ["T_PLI","jeu de matrices pliage","pliage","Compatible avec les presses plieuses"],
        ["T_SOU","poste et consommables soudage","soudage","Réservé aux opérations de soudage"],
        ["T_PEI","système peinture","peinture","Réservé à la cabine de peinture"],
        ["T_ASS","outillage assemblage","assemblage","Réservé aux postes d'assemblage"],
    ]
    tables={
      "orders.csv":(["order_id","product_family","quantity","release_date","due_date","priority","material","variant"],orders),
      "machines.csv":(["machine_id","machine_type","machine_name","available_minutes_per_day","availability_start","availability_end","tool_id"],machine_rows),
      "operators.csv":(["operator_id","operator_name","skills","availability_start","availability_end","shift_start","shift_end"],operator_rows),
      "operations.csv":(["operation_id","order_id","sequence","required_machine_type","processing_time_minutes","required_tool_id","precedence"],operations),
      "setup_times.csv":(["machine_type","from_product_family","to_product_family","setup_time_minutes"],setup),
      "disruptions.csv":(["event_id","event_type","event_date","start_time","end_time","target_id","description"],disruptions),
      "tools.csv":(["tool_id","tool_name","compatible_machine_type","notes"],tools),
    }
    for filename,(headers,rows) in tables.items():
        with (out_dir/filename).open("w",newline="",encoding="utf-8-sig") as f:
            w=csv.writer(f); w.writerow(headers); w.writerows(rows)
    print(f"Dataset généré dans {out_dir.resolve()} (seed={seed}, {len(orders)} ordres, {len(operations)} opérations).")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="data/projet23")
    parser.add_argument("--seed",type=int,default=23)
    args=parser.parse_args()
    generate(Path(args.out),args.seed)
