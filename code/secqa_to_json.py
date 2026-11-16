import csv, json, sys
src, dst = sys.argv[1], sys.argv[2]
q = [dict(question=r["Question"], answers={k: r[k] for k in "ABCD"}, solution=r["Answer"].strip()) for r in csv.DictReader(open(src, newline="", encoding="utf-8"))]
json.dump(dict(questions=q), open(dst, "w"))
print(len(q))
