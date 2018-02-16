import json
import utils

print(utils.rels_path)
with utils.rels_path.open() as f:
    image_rels = json.load(f)

with utils.flat_rels_path.open(mode='w') as f:
    first = True
    for img in image_rels:
        print("working on image %d ..." % (img['image_id']))
        for rel in img['relationships']:
            obj = rel['object']
            try:
                objName = obj['name']
            except KeyError:
                objName = obj['names'][0]
            subj = rel['subject']
            try:
                subjName = subj['name']
            except KeyError:
                subjName = subj['names'][0]
            predicate = rel['predicate']
            r_obj = utils.Rectangle(obj['x'], obj['y'], obj['w'], obj['h'])
            r_subj = utils.Rectangle(subj['x'], subj['y'], subj['w'], subj['h'])
            r = utils.SpatialRelation(r_obj, r_subj, objName.lower(), subjName.lower(), predicate.lower(), img['image_id'])

            if first:
                f.write(r.get_header_string())
                first = False

            f.write(r.get_string())
