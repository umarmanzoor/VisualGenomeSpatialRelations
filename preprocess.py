import json
import utils

with utils.rels_path.open() as f:
    image_rels = json.load(f)

with utils.flat_rels_path.open(mode='w') as f:
    first = True
    for img in image_rels:
        print("working on image %d ..." % (img['image_id']))
        for rel in img['relationships']:
            obj = rel['object']
            subj = rel['subject']
            predicate = rel['predicate']
            r_obj = utils.Rectangle(obj['x'], obj['y'], obj['w'], obj['h'])
            r_subj = utils.Rectangle(subj['x'], subj['y'], subj['w'], subj['h'])
            r = utils.SpatialRelation(r_obj, r_subj, predicate, img['image_id'])

            if first:
                f.write(r.get_header_string())
                first = False

            f.write(r.get_string())
